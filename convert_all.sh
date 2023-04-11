for file in Lynx/*.py
do
    name=${file##*/}
    2to3 -w "$file"
done

2to3 -w lynx.py
2to3 -w Utilities.py
