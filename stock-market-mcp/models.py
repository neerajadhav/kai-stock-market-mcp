from pydantic import BaseModel

class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None = None

class StockQuote(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: float | None = None

class MarketIndex(BaseModel):
    name: str
    symbol: str
    value: float
    change: float
    change_percent: float

class StockAnalysis(BaseModel):
    symbol: str
    recommendation: str
    target_price: float | None = None
    analyst_rating: str | None = None
    pe_ratio: float | None = None
    eps: float | None = None
