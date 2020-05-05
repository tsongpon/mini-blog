from exception.mini_blog_exception import CardNotFoundException, BadRequestException


class CardService(object):
    def __init__(self, repository):
        self.repository = repository

    def get_card(self, card_id):
        book = self.repository.get_card(card_id)
        if book is None:
            raise CardNotFoundException("card not found")
        return self.repository.get_card(card_id)

    def create_card(self, card):
        return self.repository.create_card(card)

    def update_card(self, card):
        card_from_db = self.repository.get_card(card.id)
        if card_from_db is None:
            raise CardNotFoundException("card not found")
        return self.repository.update_card(card)

    def delete_card(self, card_id):
        card = self.repository.get_card(card_id)
        if card is None:
            raise CardNotFoundException("card not found")
        self.repository.delete_card(card_id)
