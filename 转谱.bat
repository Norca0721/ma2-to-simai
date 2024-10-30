@echo off
cd .\
python .\library\fix_version.py
.\library\MaichartConverter\MaichartConverter.exe CompileDatabase -p .\ChartData -o .\ChartData -g 6
pause