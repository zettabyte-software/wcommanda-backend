import ast

import serpy


def str_to_value(self, value):
    if value is None:
        return None
    return str(value)


def int_to_value(self, value):
    if value is None:
        return None
    return int(value)


def float_to_value(self, value):
    if value is None:
        return None
    return float(value)


# def bool_to_value(self, value):
#     if value is None:
#         return None
#     return ast.literal_eval(value)


serpy.StrField.to_value = str_to_value
serpy.IntField.to_value = int_to_value
serpy.FloatField.to_value = float_to_value
# serpy.BoolField.to_value = bool_to_value
