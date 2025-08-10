import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.apps.superheroes.repositories.superheroes import SuperheroesRepositoryImpl
from src.apps.superheroes.schemas.superheroes import (
    SuperheroCreateSchema,
    SuperheroQueryFilterSchema,
)
from src.apps.superheroes.exceptions import (
    DBHeroNotFoundException,
)


DATABASE_URL = "postgresql+asyncpg://test_user:test_password@postgres_test:5432/test_db"


@pytest.fixture(scope="function")
async def engine():
    return create_async_engine(DATABASE_URL)


@pytest.fixture(scope="function")
async def session(engine):
    """
    AsyncSession + transaction + rollback.
    """
    async with engine.begin() as conn:
        factory = async_sessionmaker(bind=conn, expire_on_commit=False)
        async with factory() as s:
            yield s
            await conn.rollback()


@pytest.mark.asyncio
async def test_create_and_get_by_name(session):
    repo = SuperheroesRepositoryImpl(session)
    schema = SuperheroCreateSchema(
        name="Batman",
        intelligence=100,
        strength=85,
        speed=65,
        durability=85,
        power=80,
        combat=90,
    )
    hero = await repo.create(schema)
    assert hero.name == "Batman"

    found = await repo.get_by_name("Batman")
    assert found.id == hero.id


@pytest.mark.asyncio
async def test_get_by_name_not_found(session):
    repo = SuperheroesRepositoryImpl(session)
    with pytest.raises(DBHeroNotFoundException):
        await repo.get_by_name("Missing")


@pytest.mark.asyncio
async def test_filter_eq_single(session):
    repo = SuperheroesRepositoryImpl(session)
    await repo.create(
        SuperheroCreateSchema(
            name="Flash",
            intelligence=70,
            strength=50,
            speed=100,
            durability=60,
            power=75,
            combat=85,
        )
    )
    await repo.create(
        SuperheroCreateSchema(
            name="Superman",
            intelligence=95,
            strength=100,
            speed=100,
            durability=95,
            power=100,
            combat=80,
        )
    )

    filters = SuperheroQueryFilterSchema(
        name=None,
        intelligence=70,
        intelligence_ge=None,
        intelligence_le=None,
        strength=None,
        strength_ge=None,
        strength_le=None,
        speed=None,
        speed_ge=None,
        speed_le=None,
        durability=None,
        durability_ge=None,
        durability_le=None,
        power=None,
        power_ge=None,
        power_le=None,
        combat=None,
        combat_ge=None,
        combat_le=None,
    )
    heroes = await repo.filter_all(filters)
    assert len(heroes) == 1
    assert heroes[0].name == "Flash"


@pytest.mark.asyncio
async def test_filter_ge_le_range(session):
    repo = SuperheroesRepositoryImpl(session)
    await repo.create(
        SuperheroCreateSchema(
            name="A",
            strength=90,
            speed=60,
            durability=80,
            power=90,
            combat=70,
            intelligence=85,
        )
    )
    await repo.create(
        SuperheroCreateSchema(
            name="B",
            strength=110,
            speed=70,
            durability=90,
            power=100,
            combat=80,
            intelligence=95,
        )
    )
    await repo.create(
        SuperheroCreateSchema(
            name="C",
            strength=120,
            speed=80,
            durability=95,
            power=110,
            combat=85,
            intelligence=100,
        )
    )

    filters = SuperheroQueryFilterSchema(
        name=None,
        intelligence=None,
        intelligence_ge=None,
        intelligence_le=None,
        strength=None,
        strength_ge=100,
        strength_le=110,
        speed=None,
        speed_ge=None,
        speed_le=None,
        durability=None,
        durability_ge=None,
        durability_le=None,
        power=None,
        power_ge=None,
        power_le=None,
        combat=None,
        combat_ge=None,
        combat_le=None,
    )
    heroes = await repo.filter_all(filters)
    assert {h.name for h in heroes} == {"B"}


@pytest.mark.asyncio
async def test_filter_multiple_fields(session):
    repo = SuperheroesRepositoryImpl(session)
    await repo.create(
        SuperheroCreateSchema(
            name="WonderWoman",
            intelligence=100,
            strength=85,
            speed=75,
            durability=85,
            power=90,
            combat=95,
        )
    )
    await repo.create(
        SuperheroCreateSchema(
            name="Aquaman",
            intelligence=80,
            strength=70,
            speed=60,
            durability=75,
            power=70,
            combat=85,
        )
    )

    filters = SuperheroQueryFilterSchema(
        name=None,
        intelligence=None,
        intelligence_ge=90,
        intelligence_le=None,
        strength=None,
        strength_ge=None,
        strength_le=None,
        speed=None,
        speed_ge=None,
        speed_le=80,
        durability=None,
        durability_ge=None,
        durability_le=None,
        power=None,
        power_ge=85,
        power_le=None,
        combat=None,
        combat_ge=None,
        combat_le=None,
    )
    heroes = await repo.filter_all(filters)
    assert len(heroes) == 1
    assert heroes[0].name == "WonderWoman"