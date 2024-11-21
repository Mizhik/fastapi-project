from model.models import Pet
from repository.base_repository import BaseRepository


class PetRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Pet)
