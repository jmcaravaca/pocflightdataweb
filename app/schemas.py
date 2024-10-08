from datetime import datetime
from pydantic import BaseModel
class FlightDataRow(BaseModel):
    RANK : int
    FLIGHTRADARINDEX : float
    CANCELEDFLIGHTS : int
    DELAYEDFLIGHTS : int
    AVERAGEDELAY : float
    NAME: str
    NAMEURL : str
    COUNTRY : str
    TIMESTAMP : datetime
    
    class Config:
        orm_mode = True
        from_attributes = True