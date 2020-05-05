import uuid
from model.card import Card
from datetime import datetime


class CardRepository(object):
    columns = """id, name, status, content, category, author, createdtime, modifiedtime"""

    def __init__(self, db_connection_pool):
        self.db_connection_pool = db_connection_pool

    def get_card(self, card_id):
        card_from_db = None
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """
                        SELECT {columns}
                        FROM card WHERE id=%s
                    """.format(columns=CardRepository.columns)
                cursor.execute(sql, (card_id,))
                result = cursor.fetchone()
                if result is not None:
                    card_from_db = Card(result[0], result[1], result[2], result[3],
                                        result[4], result[5], result[6], result[7])
        finally:
            self.db_connection_pool.putconn(conn)
        return card_from_db

    def create_card(self, card):
        new_id = str(uuid.uuid4())
        card.id = new_id
        now = datetime.now()
        card.created_time = now
        card.modified_time = now
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO card ({column})
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""".format(column=CardRepository.columns)
                cursor.execute(sql, (card.id, card.name, card.status, card.content, card.category,
                                     card.author, card.created_time, card.modified_time))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)
        return card

    def update_card(self, card):
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """UPDATE card
                            SET name=%s, 
                                status=%s ,
                                content=%s,
                                category=%s,
                                author=%s,
                                modifiedtime=%s
                            WHERE id=%s"""
                cursor.execute(sql, (card.name, card.status, card.content, card.category, card.author,
                                     datetime.now(), card.id))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)
        return self.get_card(card.id)

    def delete_card(self, card_id):
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM card WHERE id=%s"
                cursor.execute(sql, (card_id,))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)
