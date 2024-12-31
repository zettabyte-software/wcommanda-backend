from django.core.cache import cache
from django.utils import timezone

from apps.system.tenants.models import Ambiente

RATING_CACHE_KEY = "ifood-requests-rate-%s-%s"


class IfoodRequestsLimit:
    def __init__(self, tenant: Ambiente, limite: int, modulo: str):
        self.tenant = tenant
        self.modulo = modulo
        self.limite_requests = limite

    def atingiu_limite(self):
        cache_key = RATING_CACHE_KEY % (self.modulo, self.tenant.pk)
        quantidade_atual_requests = cache.get(cache_key, 0)
        return quantidade_atual_requests >= self.limite_requests

    def calcular_segundos_ate_virada_mes(self):
        now = timezone.now()

        if now.month == 12:
            primeiro_dia_mes_seguinte = timezone.datetime(now.year + 1, 1, 1)
        else:
            primeiro_dia_mes_seguinte = timezone.datetime(now.year, now.month + 1, 1)

        delta = primeiro_dia_mes_seguinte - now
        return int(delta.total_seconds())

    def resetar_limite(self):
        cache_key = RATING_CACHE_KEY % (self.modulo, self.tenant.pk)
        cache.set(cache_key, 0, timeout=self.calcular_segundos_ate_virada_mes())

    def incrementar_integracao(self):
        cache_key = RATING_CACHE_KEY % (self.modulo, self.tenant.pk)
        quantidade_atual_requests = cache.get(cache_key, 0)
        cache.set(
            cache_key,
            quantidade_atual_requests + 1,
            timeout=self.calcular_segundos_ate_virada_mes(),
        )
