from rest_framework import serializers

from apps.users.serializers import OnwerSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    owner = OnwerSerializer(read_only=True)

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        if self.__class__.__name__.find("Visualizacao") != -1:
            self.Meta.read_only_fields = self.Meta.model.get_column_names()

        super().__init__(instance, data, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)

    def get_field_verbose_name(self, field_name):
        return self.Meta.model._meta.get_field(field_name).verbose_name  # type: ignore

    # def run_validation(self, data=serializers.empty):
    #     try:
    #         return super().run_validation(data)
    #     except serializers.ValidationError as e:
    #         errors = e.detail
    #         new_errors = {}
    #         for field_name, field_errors in errors.items():
    #             verbose_name = self.get_field_verbose_name(field_name)
    #             new_errors[verbose_name] = field_errors

    #         raise serializers.ValidationError(new_errors)
