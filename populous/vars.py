import re
from operator import attrgetter

from populous.exceptions import GenerationError


# match a variable with attributes ($var.attr), except if it's escaped
VARS_REGEX = re.compile(r"(?<!\\)\$(?P<var>\w[\w.]*(?<!\.))+")
SUBSTITUTE = "{\g<var>}"


def parse_vars(value):
    if not isinstance(value, str):
        return value

    if "$" not in value:
        # fast path
        return value

    match = re.search(VARS_REGEX, value)

    if not match:
        return value.replace('\$', '$')

    # if the match is spanning over the entire string,
    # this is a value expression
    if match.span() == (0, len(value)):
        return ValueExpression(match.group(1))

    # otherwise we should use a template expression
    return TemplateExpression(value)


class Expression(object):

    def evaluate(self, **vars):
        raise NotImplementedError()


class ValueExpression(Expression):

    def __init__(self, var):
        self.var, _, attrs = var.partition('.')
        if attrs:
            self.attrgetter = attrgetter(attrs)
        else:
            self.attrgetter = None
        self.attrs = attrs

    def evaluate(self, **vars_):
        try:
            var = vars_[self.var]
        except KeyError:
            raise GenerationError(
                "Variable '{}' not found.".format(self.var)
            )
        if self.attrgetter:
            try:
                return self.attrgetter(var)
            except AttributeError as e:
                # this message is not very informative ('type' objects has no
                # attribute 'attr'), but we cannot do much better without
                # inspecting the calling frame
                raise GenerationError(e.message)
        else:
            return var


class TemplateExpression(Expression):

    def __init__(self, value=""):
        # escape present '{' and '}'
        value = value.replace('{', '{{').replace('}', '}}')
        template = re.sub(VARS_REGEX, SUBSTITUTE, value)
        template = template.replace('\$', '$')
        self.template = template

    def __str__(self):
        return self.evaluate()

    def evaluate(self, **vars_):
        try:
            return self.template.format(**vars_)
        except KeyError as e:
            raise GenerationError(
                "Variable '{}' not found.".format(e.args[0])
            )
        except AttributeError as e:
            # this message is not very informative ('type' objects has no
            # attribute 'attr'), but we cannot do much better without
            # inspecting the calling frame
            raise GenerationError(e.message)
