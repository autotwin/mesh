from atmesh import command_line as cl


def test_say_hello():
    known = "hello world!"
    found = cl.say_hello()
    assert known == found


def test_version():
    known = "0.0.7"
    found = cl.version()
    assert known == found


def test_yml_version():
    known = 1.6
    found = cl.yml_version()
    assert known == found
