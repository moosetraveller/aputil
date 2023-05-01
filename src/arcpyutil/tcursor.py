"""
`tcursor` is a generator wrapping an `arcpy.da.SearchCursor` using a namedtuple.

```python
import arcpy
from arcpyutil import tcursor

feature_class = "points.shp"
with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:
    for row in tcursor(cursor):
        print(row.FieldName)  # instead of row[0]
```

GIT Repository:
https://github.com/moosetraveller/arcpy-util

Copyright (c) 2023 Thomas Zuberbuehler

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import uuid

from typing import Generator, Tuple

from collections import namedtuple

import arcpy

__all__ = ["tcursor"]

def tcursor(cursor: arcpy.da.SearchCursor, tuple_name=None) -> Generator[Tuple, None, None]:
    """
    Generator wrapping an arcpy cursor providing namedtuple instances.
    
    ```python
    import arcpy
    from arcpyutil import tcursor

    feature_class = "points.shp"
    with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:
        for row in tcursor(cursor):
            print(row.FieldName)  # instead of row[0]
    ```
    """

    tuple_name = tuple_name if tuple_name else f"tcursor_{uuid.uuid4().hex}"
    tcursor_tuple = namedtuple(tuple_name, cursor.fields)

    for row in cursor:
        yield tcursor_tuple(*row)
