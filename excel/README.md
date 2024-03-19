# read Excel files from Python 

## openpyxl
```sh
pip install openpyxl
python3
```
```python
file_path='database-tables.xlsm'
sheet_name='Transaction Tables'

import openpyxl
xls=openpyxl.open(file_path)
# xls=openpyxl.load_workbook(file_path)
xls.worksheets
sheet=xls.get_sheet_by_name(sheet_name)
sheet.max_row
sheet.max_column

for row in sheet.iter_rows(min_row=1,
                           max_row=sheet.max_row,
                           min_col=1,
                           max_col=sheet.max_column):
    for cell in row:
        print(cell.value)
```


## xlrd
```sh
pip install xlrd
python3
```
```python
import xlrd
file_path='database-tables.xlsm'
# only for xls-files
xls=xlrd.open_workbook(file_path)
```


## xlwings
```sh
pip install xlwings
python3
```
```python
import xlwings
file_path='database-tables.xlsm'
dir(xlwings)
xls=xlwings.load(file_path)
dir(xls)
```
