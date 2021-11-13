"""
`xcursor` is a generator wrapping an `arcpy.da.SearchCursor` providing a getter
method to use field names instead of column indices.

```python
import arcpy
from arcpyutil import xcursor

feature_class = "points.shp"
with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:
    for row in xcursor(cursor):
        print(row["FieldName"]) # instead of row[0]
```

GIT Repository:
https://github.com/moosetraveller/arcpy-util

Copyright (c) 2021 Thomas Zuberbuehler

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

import arcpy


class XRow():
    """ Wraps an arcpy cursor row. """

    def __init__(self, row, fields):
        self.row = row
        self.fields = fields
        self._fields = {field_name.upper(): index for index, field_name in enumerate(fields)}

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get_by_index(index)
        return self.get(index)

    def __repr__(self):
        return "xcursor.XRow({}, {})".format(str(self.row), str(self.fields))

    def get(self, field_name, default_value=None):
        """
        Gets the field value for given field.
        In addition to just using ["FieldName"], this method can
        return a default value when the field's value is None.
        """
        if field_name is None or field_name.upper() not in self._fields:
            raise Exception("Field {} does not exist.".format(field_name))
        value = self.row[self._fields[field_name.upper()]]
        if not value:
            return default_value
        return value

    def get_by_index(self, index, default_value=None):
        """
        Gets the field value for given index.
        In addition to just using [index], this method can
        return a default value when the field's value is None.
        """
        if index >= len(self.row):
            raise Exception("Index {} is out of range.".format(index))
        value = self.row[index]
        if not value:
            return default_value
        return value

    def to_dict(self):
        """ Returns a dictionary representation. """
        return {field_name: value for field_name, value in zip(self._fields, self.row)}  # pylint: disable=unnecessary-comprehension


def xcursor(cursor):
    """ Generator wrapping an arcpy cursor providing XRow instances. """
    for row in cursor:
        yield XRow(row, cursor.fields)
