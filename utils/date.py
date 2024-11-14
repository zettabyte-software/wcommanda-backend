from calendar import monthrange
from datetime import datetime, timedelta

from django.utils import timezone


def gerar_primeiro_e_ultimo_dia_mes(data=None):
    if data is None:
        data = timezone.now()
    primeiro_dia = data.replace(day=1)
    _, numero_ultimo_dia = monthrange(data.year, data.month)
    ultimo_dia = data.replace(day=numero_ultimo_dia)
    return primeiro_dia, ultimo_dia


def gerar_dias_entre_2_datas(data_inicial: datetime, data_final: datetime):
    datas = []
    data_atual = data_inicial
    while data_atual <= data_final:
        datas.append(data_atual)
        data_atual += timedelta(days=1)
    return datas


def gerar_semanas_entre_2_datas(data_inicial: datetime, data_final: datetime):
    datas = []
    data_atual = data_inicial
    while data_atual <= data_final:
        datas.append(data_atual)
        data_atual += timedelta(days=1 * 7)
    return datas


def gerar_semanas_entre_2_datas(data_inicial: datetime, data_final: datetime):
    datas = []
    data_atual = data_inicial
    while data_atual <= data_final:
        datas.append(data_atual)
        data_atual += timedelta(days=1 * 7)
    return datas


def gerar_meses_entre_2_datas(data_inicial: datetime, data_final: datetime):
    datas = []
    data_atual = data_inicial
    while data_atual <= data_final:
        datas.append(data_atual)
        data_atual += timedelta(days=1)
    return datas
