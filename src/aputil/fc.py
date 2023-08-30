"""
Provides some utility functions to work with feature classes and arcpy.

`use_memory()` is a function-based context manager allowing to use a memory
feature class that is automatically deleted from the memory after using
when used with the `with` statement. 

```python
import arcpy
from aputil import fc

arcpy.env.workspace = r"c:\data"

with fc.use_memory() as copied:

    print(arcpy.Exists(copied))  # false (not yet)
    arcpy.management.CopyFeatures("buildings.shp", copied)
    print(arcpy.Exists(copied))  # true

print(arcpy.Exists(copied))  # false
```

GIT Repository:
https://github.com/moosetraveller/aputil

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
import arcpy

from contextlib import contextmanager

from typing import Union

from .typings import FeatureClassType

__all__ = ["count", "use_memory"]

@contextmanager
def use_memory(name: str = None) -> str:

    # random name if no name is given
    name = name or rf"memory\fc_{uuid.uuid4().hex}"

    # if name is given, make sure that it starts with "memory\"
    name = name if name.startswith("memory\\") else rf"memory\{name}"
    
    try:
        yield name
    finally:
        arcpy.management.Delete(name)

def count(feature_class: Union[str, FeatureClassType]) -> int:
    """ Returns the numbers of features in given feature class as an int value.
        Introduced to overcome dealing with `arcpy.management.GetCount`'s
        return value of type `arcpy.arcobjects.arcobjects.Result`."""
    
    return int(arcpy.management.GetCount(feature_class)[0])