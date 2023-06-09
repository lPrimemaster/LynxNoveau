import sys
import json
from datetime import datetime
import traceback

from PyQt5.QtCore import QTimer, QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication
from PyQt5 import uic

import numpy as np
import pyqtgraph as pg

# import the Lynx device proxy and other resources
from Lynx.DeviceFactory import *
from Lynx.ParameterCodes import *
from Lynx.CommandCodes import *
from Lynx.ParameterTypes import *
from Lynx.DlfcData import *
from Lynx.PhaData import *

class Config:
    FILENAME = 'lynxnoveau_cfg.json'
    def __init__(self) -> None:
        # Read the config file / not using QT for this ... (simpler)
        self.config = self._read_cfg()

    def _read_cfg(self):
        try:
            with open(Config.FILENAME, 'r') as cfg:
                return json.load(cfg)
        except FileNotFoundError:
            print('Config file not found...')
        except Exception as e:
            print(f'File unhandled exception: {e}')
        return None
    
    def _create_cfg(self, **kwargs):
        try:
            with open(Config.FILENAME, 'w') as cfg:
                return json.dump(kwargs, cfg)
        except Exception as e:
            print(f'Could not create config file. Exception: {e}')
        return None

    def set_config(self, connection_ip, username, password, input_mode, preset_mode, acq_group, acq_time, num_channels, poll_rate):
        self.config = self._create_cfg(
            connection_ip=connection_ip,
            username=username,
            password=password,
            input_mode=input_mode,
            preset_mode=preset_mode,
            acq_group=acq_group,
            acq_time=acq_time,
            num_channels=num_channels,
            poll_rate=poll_rate
        )

    def get_dict(self):
        return self.config
    
    def empty(self):
        return self.config == None

class ConfigWindow(QDialog):
    def __init__(self, parent) -> None:
        super(ConfigWindow, self).__init__(parent)
        self.ui = uic.loadUi('ui/ConfigWindow.ui', self)

        self.setWindowIcon(QIcon('res/icon.png'))

        self.config = Config()
        self._change_fields()

        self.ui.buttonBox.accepted.connect(self.change_config)
        self.ui.buttonBox.accepted.connect(parent.acq_set_ready)

    def _change_fields(self):
        if not self.config.empty():
            config_dict = self.config.get_dict()

            self.ui.ip_addr.setText(config_dict['connection_ip'])
            self.ui.username.setText(config_dict['username'])
            self.ui.password.setText(config_dict['password'])

            if config_dict['input_mode'] == 1:
                self.ui.input_mode_1.setChecked(True)
            else:
                self.ui.input_mode_2.setChecked(True)

            if config_dict['preset_mode'] == 1:
                self.ui.preset_mode_1.setChecked(True)
            else:
                self.ui.preset_mode_2.setChecked(True)
            
            self.ui.memory_group.setCurrentIndex(config_dict['acq_group'])
            self.ui.acq_time.setValue(config_dict['acq_time'])
            self.ui.num_channels.setValue(config_dict['num_channels'])

    def change_config(self):
        self.config.set_config(
            connection_ip=self.ui.ip_addr.text(),
            username=self.ui.username.text(),
            password=self.ui.password.text(),
            input_mode  = 1 if self.ui.input_mode_1.isChecked() else 2,
            preset_mode = 1 if self.ui.preset_mode_1.isChecked() else 2,
            acq_group=self.ui.memory_group.currentIndex(),
            acq_time=self.ui.acq_time.value(),
            num_channels=self.ui.num_channels.value(),
            poll_rate=2.0 # Default to 2 Hz screen refresh rate
        )
    
    def get_config(self):
        return self.config

class DataHistogram(pg.PlotWidget):
    def __init__(self, parent, num_channels=2048, poll_rate=5, background='default', plotItem=None, **kargs):
        super(DataHistogram, self).__init__(parent, background, plotItem, **kargs)
        parent.setCentralWidget(self)

        self._x = np.arange(0, num_channels)
        self._y = np.zeros(num_channels)
        self.bars = pg.BarGraphItem(x=self._x, y1=self._y, width=0.5)
        self.addItem(self.bars)

        timer = QTimer(self)
        timer.timeout.connect(self._update_data)
        timer.start(1000 // poll_rate)

    def change_y(self):
        self._y = self.parent().get_live_y()

    def _update_data(self):
        self.bars.setOpts(y=self._y)

# This is like a friend class for the main window ... (just quick and dirty)
class AsyncConnect(QObject):
    exception = pyqtSignal()

    def run(self, lynx_window):
        try:
            lynx_window._acq_running = True
            lynx_window.acq_set_running()

            if not lynx_window._lynx:
                lynx_window._lynx = DeviceFactory.createInstance(DeviceFactory.DeviceInterface.IDevice)
            config_options = lynx_window.configWindow.get_config().get_dict()

            ip_addr = config_options['connection_ip']
            lynx_window._lynx.open('', ip_addr)

            lynx_window._lynx.lock(config_options['username'], config_options['password'], config_options['input_mode'])
            
            try:
                lynx_window._lynx.control(CommandCodes.Stop, config_options['input_mode'])
            except:
                pass
            # Abort acquisition (only needed for MSS or MCS collections)
            try:
                lynx_window._lynx.control(CommandCodes.Abort, config_options['input_mode'])
            except:
                pass
            # Stop SCA collection
            try:
                lynx_window._lynx.setParameter(ParameterCodes.Input_SCAstatus, 0, config_options['input_mode'])
            except:
                pass
            # Stop Aux counter collection
            try:
                lynx_window._lynx.setParameter(ParameterCodes.Counter_Status, 0, config_options['input_mode'])
            except:
                pass
            
            lynx_window._lynx.setParameter(ParameterCodes.Input_Mode, 0, config_options['input_mode'])

            if (PresetModes.PresetLiveTime == config_options['preset_mode']):
                lynx_window._lynx.setParameter(ParameterCodes.Preset_Live, float(config_options['acq_time']), config_options['input_mode'])
            elif(PresetModes.PresetRealTime == config_options['preset_mode']):
                lynx_window._lynx.setParameter(ParameterCodes.Preset_Real, float(config_options['acq_time']), config_options['input_mode'])
            
            lynx_window._lynx.control(CommandCodes.Clear, config_options['input_mode'])

            # TODO: Add HV control stuff

            lynx_window._lynx.control(CommandCodes.Start, config_options['input_mode'])

            lynx_window._acq_timer.start(100)

        except Exception as e:
            print(f'Exception caught. Details: {e}.')
            print(traceback.format_exc())

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Exception caught. Details:")
            msg.setInformativeText(f'{e}\n\nTraceback:\n{traceback.format_exc()}')
            msg.setWindowTitle("Error")
            msg.exec_()

            self.exception.emit() # Just reset the buttons on the menu


class LynxNoveauMainWindow(QMainWindow):
    def __init__(self) -> None:
        super(LynxNoveauMainWindow, self).__init__()
        self.ui = uic.loadUi('ui/LynxNoveauMainWindow.ui', self)

        self.setWindowIcon(QIcon('res/icon.png'))

        # Setup other windows
        self.configWindow = ConfigWindow(self)
        
        # Setup graph
        self.graph = DataHistogram(self, num_channels=2048, poll_rate=5)

        # Some internal variables
        self._acq_running = False
        self._lynx = None
        self._acq_timer = QTimer()
        self._acq_timer.timeout.connect(self._handle_acq)
        self._acq_timer.timeout.connect(self.graph.change_y)
        self._acq_time = (0.0, 0.0)
        self._live_y = np.zeros(2048)

        # Disable stuff at the start
        if self.configWindow.get_config().empty():
            self.ui.actionStart.setEnabled(False)
        self.ui.actionStop.setEnabled(False)
        self.ui.actionPause.setEnabled(False)

        self.ui.actionStart.triggered.connect(self._start_acq)
        self.ui.actionStop.triggered.connect(self._stop_acq)

        # Setup signals
        self.ui.actionConfigure.triggered.connect(self.configWindow.show)

        # Finally draw the window
        self.show()

    def get_live_y(self):
        return self._live_y

    def acq_set_ready(self):
        self.ui.actionStart.setEnabled(True)
        self.ui.actionStop.setEnabled(False)
        self.ui.actionPause.setEnabled(False)
    
    def acq_set_running(self):
        self.ui.actionStart.setEnabled(False)
        self.ui.actionStop.setEnabled(True)
        self.ui.actionPause.setEnabled(True)

    def _start_acq(self):
        if not self._acq_running:
            # Try a synchronous task to see if the error persists
            async_worker = AsyncConnect()
            async_worker.exception.connect(self._stop_acq)

            curr_screen = QGuiApplication.screenAt(self.pos())
            splash_screen = QSplashScreen(curr_screen, QPixmap('res/splash.png'))
            splash_screen.show()
            splash_screen.showMessage('Attempting connection with hardware\nPlease wait...', Qt.AlignHCenter | Qt.AlignBottom)
            async_worker.run(self)
            splash_screen.close()
            
    def _stop_acq(self):
        if self._acq_running:
            self._display_msg('Acquisition stopping ...')
            self._acq_timer.stop()
            self._acq_running = False
            self.acq_set_ready()
            self._display_msg('Ready.')

    def _save_spectrum(self):
        now = datetime.now()
        with open(f'{now}.csv', 'w') as file:
            file.writelines([','.join([n, y])+',' for n, y in enumerate(self._live_y)])

    def _handle_acq(self):
        config_options = self.configWindow.get_config().get_dict()
        spectral_data = self._lynx.getSpectralData(config_options['input_mode'], config_options['acq_group'])
        self._acq_time = (spectral_data.getLiveTime(), spectral_data.getRealTime())
        self._live_y = spectral_data.getSpectrum().getCounts()

        if ((0 == (StatusBits.Busy & spectral_data.getStatus())) and (0 == (StatusBits.Waiting & spectral_data.getStatus()))):
            self._stop_acq()
            self._save_spectrum()

    def _display_msg(self, msg):
        self.statusBar().showMessage(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LynxNoveauMainWindow()
    app.exec_()
