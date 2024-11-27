from rest_framework.serializers import ModelSerializer, empty

from apps.users.serializers import OnwerSerializer


class BaseModelSerializer(ModelSerializer):
    owner = OnwerSerializer(read_only=True)

    def __init__(self, instance=None, data=empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        super().__init__(instance, data, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)

        if self.context["request"].method == "GET":
            self.Meta.read_only_fields = self.Meta.model.get_column_names() # type: ignore
