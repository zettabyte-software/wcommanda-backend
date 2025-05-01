import serpy


class StrField(serpy.StrField):
    @staticmethod
    def to_value(value):
        if value is None:
            return None
        return str(value)


class IntField(serpy.IntField):
    @staticmethod
    def to_value(value):
        if value is None:
            return None
        return int(value)


class FloatField(serpy.FloatField):
    @staticmethod
    def to_value(value):
        if value is None:
            return None
        return float(value)


class BoolField(serpy.BoolField):
    @staticmethod
    def to_value(value):
        if value is None:
            return None
        return bool(value)


class MethodField(serpy.MethodField):
    pass
