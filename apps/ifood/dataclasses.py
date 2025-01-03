import dataclasses


@dataclasses.dataclass
class ProdutoIfood:
    pass


@dataclasses.dataclass
class PedidoIfood:
    pass


@dataclasses.dataclass
class EventoIfood:
    id: str
    code: str
    fullCode: str
    orderId: str
    merchantId: str
    createdAt: str
    salesChannel: str
    # metadata: dict
