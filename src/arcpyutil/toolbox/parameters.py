"""
`arcpy.Parameter`s wrapper allowing to retrieve values using the parameter
name. In addition, `ToolParameters` offers some helper functions. 

```python
import arcpy
from arcpyuti.toolbox.parameters import ToolParameters

params = ToolParameters(arcpy.GetParameterInfo())

feature_class = params.get_string("feature_class")  # retrieve string
count = params.get_int("count")  # retrieve integer
distance = params.get_float("distance")  # retrieve float
# and so on
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

import abc
import arcpy

from typing import Union, List, TypeVar, Dict

P = TypeVar("P")


class Parameters(abc.ABC):

    def get(self, name: str) -> Union[P, None]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_params(self) -> List[P]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_string(self, name: str, default_value: Union[str, None] = None) -> Union[str, None]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_int(self, name: str, default_value: Union[int, None] = None) -> Union[int, None]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_float(self, name: str, default_value: Union[float, None] = None) -> Union[float, None]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_bool(self, name: str, default_value: Union[bool, None] = False) -> Union[bool, None]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")
    
    def has_value(self, name: str) -> bool:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def get_multivalue(self) -> List[str]:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")

    def clear_messages(self) -> None:
        raise NotImplementedError("Please instanciate a concreate class of Parameters")


class ToolParameters(Parameters):

    def __init__(self, parameters: List[arcpy.Parameter] = None, suppress_errors = True):
        """ If `suppress_errors` is `False`, raises errors if a parameter does not
            exist or its value conversion failed. """
        self.parameters = {p.name: p for p in parameters} if parameters else {}
        self.suppress_errors = suppress_errors

    def __iter__(self):
        self.iterator = iter(self.parameters.items())
        return self

    def __next__(self):
        return next(self.iterator)

    def get(self, name: str) -> Union[arcpy.Parameter, None]:
        parameter = self.parameters.get(name)
        if not parameter and not self.suppress_errors:
            raise IndexError(f"Parameter with name {name} does not exist.")
        return parameter

    def get_params(self) -> List[arcpy.Parameter]:
        return self.parameters.values()
    
    def to_dict(self) -> Dict[str, arcpy.Parameter]:
        return {**self.parameters}

    def get_string(self, name: str, default_value: Union[str, None] = None) -> Union[str, None]:
        parameter = self.get(name)
        return parameter.valueAsText if parameter else default_value
    
    def get_int(self, name: str, default_value: Union[int, None] = None) -> Union[int, None]:
        """ Returns a int if the parameter's value can be converted
            into a int value. """

        value = self.get_string(name)
        
        if not value:
            return default_value

        try:
            return int(value)
        except ValueError as e:
            if not self.suppress_errors:
                raise e
            return default_value

    def get_float(self, name: str, default_value: Union[float, None] = None) -> Union[float, None]:
        """ Returns a float if the parameter's value can be converted
            into a float value. """

        value = self.get_string(name)
        
        if not value:
            return default_value

        try:
            return float(value)
        except ValueError as e:
            if not self.suppress_errors:
                raise e
            return default_value

    def get_bool(self, name: str, default_value: Union[bool, None] = None) -> Union[bool, None]:
        """ Returns `True` if parameter exists and the parameter's value is
            is a valid boolean value or a valid string or int representation. """

        parameter = self.get(name)
        
        if not parameter or not parameter.value:
            return default_value

        value = parameter.value

        if isinstance(value, bool):
            return value

        if isinstance(value, (str, int)):
            
            if value == 1 or value.lower() in ["true", "checked", "1"]:
                return True

            if value == 0 or value.lower() in ["false", "unchecked", "0"]:
                return False

        if not self.suppress_errors:
            raise ValueError(f"Cannot convert {value} to boolean.")
        return default_value

    def is_defined(self, name: str) -> bool:
        """ Returns `True` if parameter exists and the parameter's 
            value is not `None`, otherwise returns `False`. Does
            not raise an error if parameter does not exist. """
        
        parameter = self.parameters.get(name)
        return parameter and parameter.value is not None
    
    def get_multivalue(self) -> List[str]:
        parameter = self.get_string()
        return parameter.split(";") if parameter else None

    def clear_messages(self) -> None:
        for param in self.get_params():
            param.clearMessage()
