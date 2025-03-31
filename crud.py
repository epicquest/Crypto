from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Crypto
from schemas import CryptoCreate
from coingecko import fetch_crypto_info, fetch_crypto_prices


async def create_crypto(db: AsyncSession, crypto: CryptoCreate) -> tuple[Crypto | None, bool]:
    existing_crypto = await db.execute(select(Crypto).where(Crypto.symbol == crypto.symbol))
    existing_crypto = existing_crypto.scalar()

    if existing_crypto:
        return None, True


    crypto_info = fetch_crypto_info(crypto.symbol)
    if not crypto_info:
        return None, False

    new_crypto = Crypto(symbol=crypto.symbol, name=crypto_info["name"], extra_data=crypto_info)
    db.add(new_crypto)
    await db.commit()
    return new_crypto, False

async def get_crypto(db: AsyncSession, crypto_id: int):
    return await db.get(Crypto, crypto_id)

async def get_all_cryptos(db: AsyncSession):
    result = await db.execute(select(Crypto))
    return result.scalars().all()

async def delete_crypto(db: AsyncSession, crypto_id: int):
    crypto = await db.get(Crypto, crypto_id)
    if crypto:
        await db.delete(crypto)
        await db.commit()
        return True
    return False


async def update_crypto_prices(db: AsyncSession) -> dict[str, str]:
    """Updates crypto data in the database based on CoinGecko response."""
    result = await db.execute(select(Crypto))
    cryptos = result.scalars().all()
    if not cryptos:
        return {"message": "No cryptos found in the database"}

    symbols = [crypto.symbol.lower() for crypto in cryptos]
    prices = fetch_crypto_prices(symbols)

    for crypto in cryptos:
        if crypto.symbol.lower() in prices:
            crypto.price = prices[crypto.symbol.lower()]

    await db.commit()
    return {"message": "Crypto prices updated successfully"}