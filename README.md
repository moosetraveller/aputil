# ArcPyUtil

Utility classes and functions for arcpy

## Create Distribution

```shell=
cd c:\projects\arcpy-util
python setup.py sdist bdist_wheel
```

## Install 

```shell
python -m pip install ArcPyUtil-X.X.X-py3-none-any.whl
```

Note: replace `X.X.X` with version number

## Example

### `xcursor`

```python
import arcpy
from arcpyutil import xcursor

feature_class = "points.shp"
with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:
    for row in xcursor(cursor):
        
        print(row["FieldName"])  # instead of row[0]

        # other examples
        print(row.get("FieldName", "Default Value"))
        print(row.get_by_index(0, "Default Value"))
```

### `tcursor`

```python
import arcpy
from arcpyutil import tcursor

feature_class = "points.shp"
with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:
    for row in tcursor(cursor):
        print(row.FieldName)  # instead of row[0]
```

## Run Unit Tests

```shell
cd c:\projects\arcpy-util
[conda activate arcgispro-py3]
python test.py
```
