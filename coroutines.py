import aiohttp
from sqlalchemy import select
from consts import async_session, engine, Base, BASE_URL
import datetime

from models import Currency


async def update_currency_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as resp:
            data = await resp.json()
            timestamp_str = data['meta']["last_updated_at"]
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')

            async with async_session as async_sec:
                for currency, rate_data in data["data"].items():
                    rate = rate_data['value']
                    existing_currency = await async_sec.execute(
                        select(Currency).where(Currency.currency_code == currency))
                    existing_currency = existing_currency.scalar_one_or_none()

                    if existing_currency:
                        existing_currency.rate = rate
                        existing_currency.timestamp = timestamp
                    else:
                        new_currency = Currency(currency_code=currency, rate=rate, timestamp=timestamp)
                        async_sec.add(new_currency)
                await async_sec.commit()


async def get_last_update() -> str:
    async with async_session as session:
        result = await session.execute(
            select(Currency).order_by(Currency.timestamp.desc())
        )
        last_updated_currency = result.scalars().first()
        if last_updated_currency:
            return str(last_updated_currency.timestamp)
        else:
            return "Currency rates have not been updated yet."


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
