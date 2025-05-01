
import serpy


class BaseSerpySerializer(serpy.Serializer):
    id = serpy.IntField()

    codigo = serpy.IntField()
    ativo = serpy.BoolField()

    data_criacao = serpy.StrField()
    hora_criacao = serpy.StrField()
    data_ultima_alteracao = serpy.StrField()
    hora_ultima_alteracao = serpy.StrField()

    filial = serpy.IntField()
    owner = serpy.IntField()
    assinatura = serpy.IntField()

    def to_value(self, instance):
        fields = self._compiled_fields
        if self.many:
            serialize = self._serialize
            return [serialize(o, fields) for o in instance]

        if instance is None:
            return None

        return self._serialize(instance, fields)
