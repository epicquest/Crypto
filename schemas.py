from pydantic import BaseModel
from typing import Optional, Dict, Any

class CryptoCreate(BaseModel):
    symbol: str

class CryptoResponse(BaseModel):
    id: int
    name: str
    symbol: str
    extra_data: Optional[Dict[str, Any]]
