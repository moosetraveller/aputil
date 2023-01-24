import test.xcursor_test as xcursor_test
import test.tcursor_test as tcursor_test
import test.toolbox.parameters_test as parameters_test
import test.helper_test as helper_test


if __name__ == "__main__":

    xcursor_test.run_tests()
    tcursor_test.run_tests()
    parameters_test.run_tests()
    helper_test.run_tests()
