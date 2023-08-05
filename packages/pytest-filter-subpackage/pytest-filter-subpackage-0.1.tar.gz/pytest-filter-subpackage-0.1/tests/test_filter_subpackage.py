pytest_plugins = ['pytester']


def test_default(testdir, testpackage):
    # Make sure all code tests are picked up by default
    reprec = testdir.inline_run()
    reprec.assertoutcome(passed=4, failed=2)


def test_with_rst(testdir, testpackage):
    # Make sure all rst tests are also picked up when using pytest-doctestplus
    testdir.makeini("""
    [pytest]
    doctest_plus = enabled
    """)
    reprec = testdir.inline_run('--doctest-rst')
    reprec.assertoutcome(passed=6, failed=2)


def test_flag_single_subpackage(testdir, testpackage):
    # Test -P with a single sub-package
    reprec = testdir.inline_run('-P a')
    reprec.assertoutcome(passed=2, failed=0)


def test_flag_single_subpackage_with_rst(testdir, testpackage):
    # Test -P with a single sub-package including rst files
    testdir.makeini("""
    [pytest]
    doctest_plus = enabled
    """)
    reprec = testdir.inline_run('-P a', '--doctest-rst')
    reprec.assertoutcome(passed=3, failed=0)


def test_flag_multiple_subpackage(testdir, testpackage):
    # Test -P with several sub-packages
    reprec = testdir.inline_run('-P a,b')
    reprec.assertoutcome(passed=3, failed=1)


def test_flag_multiple_subpackage_with_rst(testdir, testpackage):
    # Test -P with several sub-packages including rst files
    testdir.makeini("""
    [pytest]
    doctest_plus = enabled
    """)
    reprec = testdir.inline_run('-P a,b', '--doctest-rst')
    reprec.assertoutcome(passed=4, failed=1)
