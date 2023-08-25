"""
Unittest for `arcpyutil.fc`.

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

import arcpy
import unittest
import tempfile

from src.arcpyutil import count, use_memory

class FcTest(unittest.TestCase):
    """ Unit test to validate functionality of `ToolParameters`. """

    FIELDS = ["Column1", "Column2", "Column3", "Column4"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.temp = None
        self.geodatabase = None
        self.feature_class = None
        
        self.count = 25

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.geodatabase = arcpy.management.CreateFileGDB(self.temp.name, "test.gdb")
        self.feature_class = arcpy.management.CreateFeatureclass(self.geodatabase, "Test")

        for field in FcTest.FIELDS:
            arcpy.management.AddField(self.feature_class, field, "TEXT")

        with arcpy.da.InsertCursor(self.feature_class, FcTest.FIELDS) as cursor:
            for index in range(0, self.count):
                cursor.insertRow((str(index), "Test", None, "Test {}".format(index)))

    def tearDown(self):

        arcpy.management.ClearWorkspaceCache(self.feature_class)
        arcpy.management.ClearWorkspaceCache(self.geodatabase)

        self.temp.cleanup()

    def test_count(self):

        self.assertEqual(count(self.feature_class), self.count)

    def test_use_memory(self):

        with use_memory() as copied:

            self.assertFalse(arcpy.Exists(copied))
            arcpy.management.CopyFeatures(self.feature_class, copied)
            self.assertTrue(arcpy.Exists(copied))

        self.assertFalse(arcpy.Exists(copied))

        name = "test"

        with use_memory(name) as test:

            self.assertEqual(fr"memory\{name}", test)


def run_tests():

    suite = unittest.TestSuite()
    suite.addTest(FcTest("test_count"))
    suite.addTest(FcTest("test_use_memory"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
