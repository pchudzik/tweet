from operator import attrgetter


class FieldMatcher:
    def __init__(self, **fields):
        self.fields = dict((attrgetter(field), value) for field, value in fields.items())

    def __eq__(self, other):
        for attr, value in self.fields.items():
            assert value == attr(other)
        return True
