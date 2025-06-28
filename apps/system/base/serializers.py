from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        # if self.__class__.__name__.find("Visualizacao") != -1:
        #     self.Meta.read_only_fields = self.Meta.model.get_column_names()

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
