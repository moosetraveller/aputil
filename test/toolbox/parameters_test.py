"""
Unittest for `arcpyutil.toolbox.parameters`.

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

import os
import arcpy
import unittest
import tempfile

from arcpy.arcobjects.arcobjects import Value

from src.arcpyutil.toolbox import ToolParameters

class ToolParametersTest(unittest.TestCase):
    """ Unit test to validate functionality of `ToolParameters`. """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.temp = None
        self.geodatabase = None
        self.feature_class = None

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.geodatabase = arcpy.management.CreateFileGDB(self.temp.name, "test.gdb")
        self.feature_class = arcpy.management.CreateFeatureclass(self.geodatabase, "Test")

        p1 = arcpy.Parameter(
            name="feature_class",
            datatype="DEFeatureClass",
        )
        p1.value = self.feature_class

        p2 = arcpy.Parameter(
            name="count",
            datatype="GPLong",
        )
        p2.value = 42
        
        p3 = arcpy.Parameter(
            name="checkbox_true",
            datatype="GPBoolean",
        )
        p3.value = True
        
        p4 = arcpy.Parameter(
            name="checkbox_false",
            datatype="GPBoolean",
        )
        p4.value = False
        
        p5 = arcpy.Parameter(
            name="checkbox_undefined",
            datatype="GPBoolean",
        )
        p5.value = None

        # simulating arcpy.GetParameterInfo()
        self.parameter_info = [p1, p2, p3, p4, p5]

    def tearDown(self):

        arcpy.management.ClearWorkspaceCache(self.feature_class)
        arcpy.management.ClearWorkspaceCache(self.geodatabase)

        self.temp.cleanup()

    def test(self):
        
        params = ToolParameters(self.parameter_info)
        
        self.assertEqual(params.get_int("count"), 42)
        self.assertEqual(params.get_string("count"), "42")
        self.assertEqual(params.get_float("count"), 42.0)

        self.assertTrue(arcpy.Exists(params.get_string("feature_class")))
        
        self.assertIsNone(params.get_bool("feature_class"))
        self.assertIsNone(params.get_int("feature_class"))
        self.assertIsNone(params.get_float("feature_class"))
        self.assertFalse(params.get_bool("feature_class", False))
        self.assertEqual(params.get_int("feature_class", 42), 42)

        self.assertTrue(params.get_bool("checkbox_true"))
        self.assertFalse(params.get_bool("checkbox_false"))
        self.assertFalse(params.get_bool("checkbox_undefined"))

        self.assertTrue(params.is_defined("checkbox_true"))
        self.assertFalse(params.is_defined("checkbox_undefined"))

    def test_iterator(self):
        
        params = ToolParameters(self.parameter_info)
        actual_parameters = [p.name for p in self.parameter_info]
        for name, _ in params:
            self.assertTrue(name in actual_parameters)

    def test_errors(self):
        
        params = ToolParameters(self.parameter_info, False)
        self.assertRaises(IndexError, params.get, "foo")
        self.assertIsNotNone(params.get("count"))
        self.assertRaises(ValueError, params.get_bool, "feature_class")
        self.assertRaises(ValueError, params.get_int, "feature_class")
        self.assertRaises(ValueError, params.get_float, "feature_class")

        self.assertRaises(ValueError, params.get_int, "checkbox_true")
        self.assertRaises(ValueError, params.get_float, "checkbox_false")

        self.assertIsNone(params.get_float("checkbox_undefined"))
        
    def test_multivalue(self):
        
        param = ToolParameters(self.parameter_info)
        # TODO

def run_tests():

    suite = unittest.TestSuite()
    suite.addTest(ToolParametersTest("test"))
    suite.addTest(ToolParametersTest("test_iterator"))
    suite.addTest(ToolParametersTest("test_errors"))
    suite.addTest(ToolParametersTest("test_multivalue"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
