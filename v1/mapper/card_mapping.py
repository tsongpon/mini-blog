from model.card import Card
from v1.transport.card_transport import CardTransport


def to_model(transport):
    return Card(id=transport.id,
                name=transport.name,
                status=transport.status,
                content=transport.content,
                category=transport.category,
                author=transport.author,
                created_time=transport.created_time,
                modified_time=transport.modified_time)


def to_transport(model):
    transport = CardTransport(**model.__dict__)
    return transport
