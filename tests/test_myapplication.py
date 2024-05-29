from myapplication.main import hello_world


def test_hello_world():
    if hello_world() != "Hello World":
        raise ValueError('Expected value to be "Hello World"')
