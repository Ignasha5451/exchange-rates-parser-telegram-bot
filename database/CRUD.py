from datetime import datetime

from sqlalchemy import select
from sqlalchemy import func

from database.models import async_session
from database.models import ExchangeRate


async def create_instance(date_time: datetime, exchange_rate: float) -> None:
    async with async_session() as session:
        instance = await session.execute(select(ExchangeRate).where(
            func.strftime('%Y-%m-%d %H', ExchangeRate.datetime) == date_time.strftime('%Y-%m-%d %H')))
        if not instance.fetchall():
            session.add(ExchangeRate(datetime=date_time, exchange_rate=exchange_rate))
            await session.commit()


async def read_instances() -> list:
    async with async_session() as session:
        today = datetime.today().date()
        query = await session.execute(select(ExchangeRate).where(func.date(ExchangeRate.datetime) == today))
        return query.fetchall()
