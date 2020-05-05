from pydantic import BaseModel
from datetime import datetime


class CardTransport(BaseModel):
    id: str = None
    name: str
    status: str
    content: str = None
    category: str = None
    author: str
    created_time: datetime = None
    modified_time: datetime = None
