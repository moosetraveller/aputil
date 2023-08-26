"""
Unittest for `arcpyutil.xcursor`.

Copyright (c) 2021-2023 Thomas Zuberbuehler

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

import arcpy, arcpy.da, arcpy.management
import unittest
import tempfile

from src.arcpyutil import xcursor

class XCursorTest(unittest.TestCase):
    """ Unit test to validate functionality of xcursor. """

    FIELDS = ["Column1", "Column2", "Column3", "Column4"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.temp = None
        self.geodatabase = None
        self.feature_class = None
        self.updated_feature_class = None

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.geodatabase = arcpy.management.CreateFileGDB(self.temp.name, "test.gdb")
        self.feature_class = arcpy.management.CreateFeatureclass(self.geodatabase, "Test")

        for field in XCursorTest.FIELDS:
            arcpy.management.AddField(self.feature_class, field, "TEXT")

        with arcpy.da.InsertCursor(self.feature_class, XCursorTest.FIELDS) as cursor:
            for index in range(0, 25):
                cursor.insertRow((str(index), "Test", None, "Test {}".format(index)))

        self.updated_feature_class = arcpy.management.CreateFeatureclass(
            self.geodatabase, 
            "Test2",
            template=self.feature_class,
            spatial_reference=arcpy.Describe(self.feature_class).spatialReference
        )

    def tearDown(self):

        arcpy.management.ClearWorkspaceCache(self.feature_class)
        arcpy.management.ClearWorkspaceCache(self.geodatabase)

        self.temp.cleanup()

    def test(self):
        """ Tests the xcursor generator. """

        with arcpy.da.SearchCursor(self.feature_class, XCursorTest.FIELDS) as cursor:
            expected_rows = [row for row in cursor].copy()

        with arcpy.da.SearchCursor(self.feature_class, XCursorTest.FIELDS) as cursor:

            for index, row in enumerate(xcursor(cursor)):

                expected_row = expected_rows[index]

                for column_index, field in enumerate(XCursorTest.FIELDS):
                    self.assertEqual(row.get(field), expected_row[column_index])
                    self.assertEqual(row[field], expected_row[column_index])
                    self.assertEqual(row.get_by_index(column_index), expected_row[column_index])
                    self.assertEqual(row[column_index], expected_row[column_index])

                self.assertIsNone(row.get("Column3"))
                self.assertEqual("1234", row.get("Column3", "1234"))
                self.assertEqual("1234", row.get_by_index(2, "1234"))

    def test_to_row(self):
        """ Tests the to_row method. """
        
        with arcpy.da.SearchCursor(self.feature_class, XCursorTest.FIELDS) as input_cursor:
            with arcpy.da.InsertCursor(self.updated_feature_class, XCursorTest.FIELDS) as output_cursor:
                for row in xcursor(input_cursor):
                    if int(row["Column1"]) % 2 == 0:
                        output_cursor.insertRow(row.to_row({
                            "Column2": "Test 2"
                        }))
                    else:
                        output_cursor.insertRow(row.to_row())
        
        with arcpy.da.SearchCursor(self.updated_feature_class, XCursorTest.FIELDS) as cursor:

            for index, row in enumerate(xcursor(cursor)):

                if index % 2 == 0:
                    self.assertEqual(row["Column2"], "Test 2")
                else:
                    self.assertEqual(row["Column2"], "Test")

def run_tests():

    suite = unittest.TestSuite()
    suite.addTest(XCursorTest("test"))
    suite.addTest(XCursorTest("test_to_row"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
