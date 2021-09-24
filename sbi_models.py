from decimal import Decimal


class GrowthRecord:
    stock_name:str
    stock_code:str
    market:str
    price:Decimal
    growth_price:Decimal
    growth_per:Decimal
    trading_unit:int

