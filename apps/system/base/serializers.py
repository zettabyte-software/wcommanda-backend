from rest_framework import serializers

import serpy


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        if self.__class__.__name__.find("Visualizacao") != -1:
            self.Meta.read_only_fields = self.Meta.model.get_column_names()

        super().__init__(instance, data, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)

        if "assinatura" in self.fields.keys():
            del self.fields["assinatura"]

        if "owner" in self.fields.keys():
            del self.fields["owner"]

    def get_field_verbose_name(self, field_name):
        return self.Meta.model._meta.get_field(field_name).verbose_name  # type: ignore


class BaseModelSerpySerializer(serpy.Serializer):
    id = serpy.IntField()

    codigo = serpy.IntField()
    ativo = serpy.BoolField()

    data_criacao = serpy.StrField()
    hora_criacao = serpy.StrField()
    data_ultima_alteracao = serpy.StrField()
    hora_ultima_alteracao = serpy.StrField()

    def to_value(self, instance):
        fields = self._compiled_fields
        if self.many:
            serialize = self._serialize
            return [serialize(o, fields) for o in instance]

        if instance is None:
            return None

        return self._serialize(instance, fields)
