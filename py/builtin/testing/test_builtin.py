import sys
import py
from py.builtin import set, frozenset, reversed, sorted

def test_enumerate():
    l = [0,1,2]
    for i,x in enumerate(l):
        assert i == x

def test_BaseException():
    assert issubclass(IndexError, py.builtin.BaseException)
    assert issubclass(Exception, py.builtin.BaseException)
    assert issubclass(KeyboardInterrupt, py.builtin.BaseException)

    class MyRandomClass(object):
        pass
    assert not issubclass(MyRandomClass, py.builtin.BaseException)

    assert py.builtin.BaseException.__module__ in ('exceptions', 'builtins')
    assert Exception.__name__ == 'Exception'


def test_GeneratorExit():
    assert py.builtin.GeneratorExit.__module__ in ('exceptions', 'builtins')
    assert issubclass(py.builtin.GeneratorExit, py.builtin.BaseException)

def test_reversed():
    reversed = py.builtin.reversed
    r = reversed("hello")
    assert iter(r) is r
    s = "".join(list(r))
    assert s == "olleh"
    assert list(reversed(list(reversed("hello")))) == ['h','e','l','l','o']
    py.test.raises(TypeError, reversed, reversed("hello"))

def test_simple():
    s = set([1, 2, 3, 4])
    assert s == set([3, 4, 2, 1])
    s1 = s.union(set([5, 6]))
    assert 5 in s1
    assert 1 in s1

def test_frozenset():
    s = set([frozenset([0, 1]), frozenset([1, 0])])
    assert len(s) == 1

def test_sorted():
    if sys.version_info >= (2,5):
        py.test.skip("python 2.5 needs no sorted tests")
    for s in [py.builtin.sorted]:
        def test():
            assert s([3, 2, 1]) == [1, 2, 3]
            assert s([1, 2, 3], reverse=True) == [3, 2, 1]
            l = s([1, 2, 3, 4, 5, 6], key=lambda x: x % 2)
            assert l == [2, 4, 6, 1, 3, 5]
            l = s([1, 2, 3, 4], cmp=lambda x, y: -cmp(x, y))
            assert l == [4, 3, 2, 1]
            l = s([1, 2, 3, 4], cmp=lambda x, y: -cmp(x, y),
                        key=lambda x: x % 2)
            assert l == [1, 3, 2, 4]

            def compare(x, y):
                assert type(x) == str
                assert type(y) == str
                return cmp(x, y)
            data = 'The quick Brown fox Jumped over The lazy Dog'.split()
            s(data, cmp=compare, key=str.lower)
        yield test


def test_print_simple():
    from py.builtin import print_
    py.test.raises(TypeError, "print_(hello=3)")
    f = py.io.TextIO()
    print_("hello", "world", file=f)
    s = f.getvalue()
    assert s == "hello world\n"

    f = py.io.TextIO()
    print_("hello", end="", file=f)
    s = f.getvalue()
    assert s == "hello"

    f = py.io.TextIO()
    print_("xyz", "abc", sep="", end="", file=f)
    s = f.getvalue()
    assert s == "xyzabc"

    class X:
        def __repr__(self): return "rep"
    f = py.io.TextIO()
    print_(X(), file=f)
    assert f.getvalue() == "rep\n"

def test_execfile(tmpdir):
    test_file = tmpdir.join("test.py")
    test_file.write("x = y\ndef f(): pass")
    ns = {"y" : 42}
    py.builtin.execfile(str(test_file), ns)
    assert ns["x"] == 42
    assert py.builtin._getcode(ns["f"]).co_filename == str(test_file)
    class A:
        y = 3
        x = 4
        py.builtin.execfile(str(test_file))
    assert A.x == 3

def test_callable():
    class A: pass
    assert py.builtin.callable(test_callable)
    assert py.builtin.callable(A)
    assert py.builtin.callable(list)
    assert py.builtin.callable(id)
    assert not py.builtin.callable(4)
    assert not py.builtin.callable("hi")

def test_totext():
    py.builtin._totext("hello", "UTF-8")

def test_reraise():
    from py.builtin import _reraise 
    try:
        raise Exception()
    except Exception:
        cls, val, tb = sys.exc_info()
    excinfo = py.test.raises(Exception, "_reraise(cls, val, tb)")
   
def test_exec():
    l = []
    py.builtin.exec_("l.append(1)")
    assert l == [1]
    d = {}
    py.builtin.exec_("x=4", d)
    assert d['x'] == 4
