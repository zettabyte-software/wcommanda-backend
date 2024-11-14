from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField, empty

from apps.users.serializers import OnwerSerializer


class BaseModelSerializer(ModelSerializer):
    owner = OnwerSerializer(read_only=True)
    data_criacao = SerializerMethodField()
    hora_criacao = SerializerMethodField()
    data_ultima_alteracao = SerializerMethodField()
    hora_ultima_alteracao = SerializerMethodField()

    def get_data_criacao(self, obj):
        return obj.data_criacao

    def get_hora_criacao(self, obj):
        return obj.hora_criacao

    def get_data_ultima_alteracao(self, obj):
        return obj.data_ultima_alteracao

    def get_hora_ultima_alteracao(self, obj):
        return obj.hora_ultima_alteracao

    def __init__(self, instance=None, data=empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)
        super().__init__(instance, data, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)

        action = self.context.get("action", None)

        if action in ("list", "retrieve"):
            for field_name in self.fields:
                self.fields[field_name].read_only = True

        elif action in ("create", "update", "partial_update"):
            # del self.fields["owner"]
            del self.fields["assinatura"]

            for field_name in self.fields:
                field_cls = self.fields[field_name].__class__

                if issubclass(field_cls, ModelSerializer):
                    model = field_cls.Meta.model
                    method = getattr(self, f"get_{field_name}_queryset", None)

                    if method:
                        self.fields[field_name] = PrimaryKeyRelatedField(queryset=method(model))
                    else:
                        self.fields[field_name] = PrimaryKeyRelatedField(queryset=model.objects.all())

            self.fields["owner"].read_only = True

