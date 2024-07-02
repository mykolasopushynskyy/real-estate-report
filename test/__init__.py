def read_file_data(filename: str, encoding="cp1251"):
    """Reads test data file as string and return its value

    :param filename: absolute path to test data file
    :param encoding: test file data encoding
    :return: test datafile content
    """
    with(open(filename, mode="rb") as test_file):
        testdata = test_file.read()
        test_file.close()

    return testdata.decode(encoding)
