# APUtil

Utility classes and functions for arcpy. APUtil stands for **A**rc**P**y and **UTIL**ity.

## Install 

```shell
python -m pip install aputil
```

Note: Future releases are published on PyPi.

## Example

### `aputil.xcursor`

### Using `xcursor(cursor)`

```python
import arcpy, arcpy.da

from aputil import xcursor

feature_class = "points.shp"

with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:

    for row in xcursor(cursor):
        
        print(row["FieldName"])  # instead of row[0]

        # other examples
        print(row.get("FieldName", "Default Value"))
        print(row.get_by_index(0, "Default Value"))
```

#### Using `to_row()`

See `test/xcursor_test.py` (test `test_to_row`) for an example.

### `aputil.tcursor`

### Using `tcursor(cursor)`

```python
import arcpy, arcpy.da

from aputil import tcursor

feature_class = "points.shp"

with arcpy.da.SearchCursor(feature_class, ["FieldName"]) as cursor:

    for row in tcursor(cursor):

        print(row.FieldName)  # instead of row[0]
```

### `aputil.fc`

#### Using `use_memory()`

```python
import arcpy, arcpy.management

from aputil import fc

arcpy.env.workspace = r"c:\data"

with fc.use_memory() as copied:

    print(arcpy.Exists(copied))  # false (not yet)
    arcpy.management.CopyFeatures("buildings.shp", copied)
    print(arcpy.Exists(copied))  # true

print(arcpy.Exists(copied))  # false
```

#### Using `count(fc)`

```python
import arcpy

from aputil import fc

record_count = fc.count(r"c:\data\buildings.shp")

print(record_count)
```

### `aputil.typings`

```python
import arcpy, arcpy.management

from aputil.typings import FeatureClassType

def create_feature_class() -> FeatureClassType:
    return arcpy.management.CreateFeatureclass(r"c:\temp", "test.shp")

print(create_feature_class())
```

## Run Unit Tests

```shell
cd c:\projects\aputil
[conda activate arcgispro-py3]
python test.py
```
