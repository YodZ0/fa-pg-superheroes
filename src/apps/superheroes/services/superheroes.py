from typing import Protocol

from ..repositories.superheroes import SuperheroesRepositoryProtocol


class SuperheroesServiceProtocol(Protocol):
    pass


class SuperheroesServiceImpl:
    def __init__(self, repository: SuperheroesRepositoryProtocol) -> None:
        self.repository = repository
