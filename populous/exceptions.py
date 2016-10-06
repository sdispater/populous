class PopulousError(Exception):
    pass


class YAMLError(PopulousError):

    def __init__(self, filename, problem):
        super(YAMLError, self).__init__(
            "Error parsing '{}': {}".format(filename, problem)
        )


class ValidationError(PopulousError):

    def __init__(self, *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.filename = kwargs.pop('filename', None)

    @property
    def message(self):
        msg = super(ValidationError, self).message
        if self.filename:
            return "File '{}': {}".format(self.filename, msg)
        else:
            return msg


class GenerationError(PopulousError):
    pass


class BackendError(PopulousError):
    pass
