import os
from fastapi import FastAPI, Header
from v1.transport.card_transport import CardTransport as CardTransportV1
from service.card_service import CardService
from repository.card_reporitory import CardRepository
from v1.mapper import card_mapping
from starlette.status import *
from yoyo import read_migrations
from yoyo import get_backend
from exception.mini_blog_exception import *
import psycopg2
from psycopg2 import pool
from starlette.responses import JSONResponse
from starlette.responses import Response
import hashlib

db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'postgres')
db_port = os.getenv('DB_PORT', 5432)
db_pass = os.getenv('DB_PASSWORD', 'pingu123')

backend_url = 'postgresql://{user}:{password}@{host}:{port}/miniblog'.format(user=db_user,
                                                                              password=db_pass,
                                                                              host=db_host,
                                                                              port=db_port)
backend = get_backend(backend_url)
migrations = read_migrations('./migrations')

with backend.lock():
    backend.apply_migrations(backend.to_apply(migrations))

api = FastAPI()
api.title = "Card API"

connection_pool = psycopg2.pool.SimpleConnectionPool(2, 20,
                                                     user=db_user, password=db_pass,
                                                     host=db_host, port=int(db_port),
                                                     database="miniblog")

cardRepository = CardRepository(connection_pool)
cardService = CardService(cardRepository)


def generate_etag(card_model):
    return hashlib.md5(str(card_model.modified_time).encode('utf-8')).hexdigest()


@api.get("/ping")
def ping():
    return {"ping": "ok"}


@api.post("/v1/cards", status_code=HTTP_201_CREATED)
def create_card(card_transport: CardTransportV1):
    card_model = card_mapping.to_model(card_transport)
    created = cardService.create_card(card_model)
    return card_mapping.to_transport(created)


@api.get("/v1/cards/{card_id}")
def get_card(card_id: str, response: Response):
    card_model = cardService.get_card(card_id)
    response.headers["etag"] = generate_etag(card_model)
    return card_mapping.to_transport(card_model)


@api.put("/v1/cards/{card_id}")
def update_card(card_transport: CardTransportV1, card_id: str, if_match: str = Header(None)):
    card_from_db = cardService.get_card(card_id)
    etag_from_card_from_db = generate_etag(card_from_db)
    if if_match != etag_from_card_from_db:
        raise PreconditionFailException("Conflict")
    card_model = card_mapping.to_model(card_transport)
    updated = cardService.update_card(card_model)
    return card_mapping.to_transport(updated)


@api.delete("/v1/cards/{card_id}")
def delete_card(card_id: str):
    cardService.delete_card(card_id)
    return {"status": "OK"}


@api.exception_handler(CardNotFoundException)
def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"message": str(exc)})


@api.exception_handler(PreconditionFailException)
def conflict_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_412_PRECONDITION_FAILED, content={"message": str(exc)})


@api.exception_handler(BadRequestException)
def bad_request_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": str(exc)})
