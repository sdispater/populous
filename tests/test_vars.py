from populous.vars import parse_vars


def test_parse_vars(mocker):
    class Expression(object):
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return type(self) == type(other) and self.value == other.value

        def __repr__(self):
            return "{}('{}')".format(type(self).__name__, self.value)

    class Value(Expression):
        pass

    class Template(Expression):
        pass

    assert Value('foo') != Template('foo')
    assert Value('foo') != Value('bar')

    mocker.patch('populous.vars.ValueExpression', wraps=Value)
    mocker.patch('populous.vars.TemplateExpression', wraps=Template)

    assert parse_vars(None) is None
    assert parse_vars(0) == 0
    assert parse_vars('') == ''
    assert parse_vars('foo') == 'foo'

    assert parse_vars('$foo') == Value('foo')
    assert parse_vars('$foo.bar') == Value('foo.bar')
    assert parse_vars('$foo.bar.lol') == Value('foo.bar.lol')
    assert parse_vars('$_a2.x3_') == Value('_a2.x3_')

    assert parse_vars(r'\$foo') == '$foo'
    assert parse_vars(r'\$foo.bar') == '$foo.bar'

    assert parse_vars('$foo bar') == Template('$foo bar')
    assert parse_vars('foo $bar') == Template('foo $bar')
    assert parse_vars('{foo} $bar') == Template('{foo} $bar')
    assert parse_vars('$foo$bar') == Template('$foo$bar')
    assert parse_vars('$foo.bar$lol') == Template('$foo.bar$lol')
    assert parse_vars(r'\$$foo') == Template(r'\$$foo')
    assert parse_vars('$$foo') == Template('$$foo')
