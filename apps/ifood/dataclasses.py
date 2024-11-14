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
    createdAt: str
    fullCode: str
    merchantId: str
    orderId: str

