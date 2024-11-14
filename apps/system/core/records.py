import json
import logging
import os

from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


class DefaultRecord:
    """Representação de um registro padrão do sistema."""

    def __init__(
        self,
        model,
        id_fields,
        active,
        raw_data,
        database_alias="default",
    ):
        if isinstance(model, str):
            model = import_string(model)

        self.active = active
        self.database_alias = database_alias
        self.id_fields = id_fields
        self.data = raw_data
        self.made_first_database_fetch = False
        self.model = model
        self._model_instance = None
        self.identifiers = {pk: raw_data[pk] for pk in id_fields}

    @property
    def model_instance(self):
        if self.made_first_database_fetch is False:
            self.made_first_database_fetch = True
            try:
                self._model_instance = self.model.objects.using(self.database_alias).get(**self.identifiers)
            except self.model.DoesNotExist:
                pass

        return self._model_instance

    @property
    def exists(self):
        return self.model_instance is not None

    @property
    def inactive(self):
        return not self.active

    def create(self, **save_kwargs):
        instance = self.model.objects.using(self.database_alias).create(**self.data)
        self._model_instance = instance
        return instance

    def delete(self):
        instance = self.model_instance
        if instance is None:
            raise self.model.DoesNotExists

        instance.delete()

    def __str__(self):
        ids = " ".join(
            [f"{chave}='{valor}'" for chave, valor in self.identifiers.items()]
        )
        return f"<DefaultRecord model={self.model.__name__} {ids}>"


class DefaultRecordsManger:
    """Objeto responsável por popular o banco de dados com os
    dados padrões do sistema.
    """

    default_records_path = "data/records/default/"

    def __init__(self, database_alias="default"):
        self.database_alias = database_alias
        self.__cached_models = {}

    def apply_updates(self):
        records = self.get_records()
        for record in records:
            print(f"[*] verificando registro:", record)
            if record.active and not record.exists:
                print(f"[*] criando registro:", record)
                record.create()

            elif not record.active and record.exists:
                print(f"[*] deletando registro:", record)
                record.delete()

    def get_records(self):
        files = self.get_files()
        records = []
        for file in files:
            records_to_insert = json.load(file)
            for dataset in records_to_insert:
                model = self.get_model(dataset["model"])
                data = dataset["data"]
                id_fields_map = dataset["id_fields_map"]
                active = dataset["active"]

                default_record = DefaultRecord(
                    model=model,
                    id_fields=id_fields_map,
                    active=active,
                    raw_data=data,
                    database_alias=self.database_alias
                )

                records.append(default_record)

        return tuple(records)

    def get_files(self):
        files = []
        for file_name in os.listdir(self.default_records_path):
            path = self.default_records_path + file_name
            file = open(path)
            files.append(file)

        return tuple(files)

    def delete_inactives(self):
        records = self.get_records()
        for record in records:
            if not record.exists or record.inactive:
                continue

            record.delete()

    def populate(self):
        records = self.get_records()
        for record in records:
            if record.exists or record.inactive:
                continue

            record.create()

    def get_model(self, path):
        if path not in self.__cached_models:
            self.__cached_models[path] = import_string(path)
        return self.__cached_models[path]
