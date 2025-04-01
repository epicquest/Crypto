
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base
from schemas import CryptoCreate, CryptoResponse
from crud import create_crypto, get_crypto, get_all_cryptos, delete_crypto, update_crypto_prices

app = FastAPI(title="Crypto API")


async def async_lifespan():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

@app.post("/cryptos/", response_model=CryptoResponse)
async def add_crypto(crypto: CryptoCreate, db: AsyncSession = Depends(get_db)):
    new_crypto, exists = await create_crypto(db, crypto)
    if exists:
        raise HTTPException(status_code=409, detail="Crypto symbol already exists")

    if not new_crypto:
        raise HTTPException(status_code=400, detail="Invalid crypto symbol")

    return new_crypto

@app.get("/cryptos/{crypto_id}", response_model=CryptoResponse)
async def get_crypto_by_id(crypto_id: int, db: AsyncSession = Depends(get_db)):
    crypto = await get_crypto(db, crypto_id)
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto

@app.get("/cryptos/", response_model=list[CryptoResponse])
async def list_cryptos(db: AsyncSession = Depends(get_db)):
    return await get_all_cryptos(db)

@app.delete("/cryptos/{crypto_id}", status_code=204)
async def remove_crypto(crypto_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_crypto(db, crypto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Crypto not found")


@app.post("/cryptos/update-prices", status_code=201)
async def refresh_crypto_prices(db: AsyncSession = Depends(get_db)):
    """Endpoint to update crypto prices."""
    return await update_crypto_prices(db)

