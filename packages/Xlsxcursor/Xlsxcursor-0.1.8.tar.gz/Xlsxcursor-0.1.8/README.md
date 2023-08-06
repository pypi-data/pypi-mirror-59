xslxcursor
==========

Class wrapper for xslxwriter


```
from xlsxwriter import Workbook
from xlsxcursor import XlsxCursor


workbook = Workbook(path)
worksheet = workbook.add_worksheet("list1")

cursor = XlsxCursor(workbook, worksheet)
cursor("Hello")
cursor("World!")
cursor.cr()
workbook.close()
```
