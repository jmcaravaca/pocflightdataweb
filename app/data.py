from sqlalchemy import create_engine, MetaData, Table, select, insert, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from schemas import FlightDataRow
from fastapi.encoders import jsonable_encoder


class Base(DeclarativeBase):
    ...
    
class FlightDataModel(Base):
    __tablename__ = "flightdatamodel"
    id = mapped_column(Integer, primary_key=True)
    RANK  = mapped_column(Integer)
    FLIGHTRADARINDEX = mapped_column(Float)
    CANCELEDFLIGHTS = mapped_column(Integer)
    DELAYEDFLIGHTS = mapped_column(Integer)
    AVERAGEDELAY= mapped_column(Float)
    NAME = mapped_column(String)
    NAMEURL = mapped_column(String)
    COUNTRY = mapped_column(String)
    TIMESTAMP = mapped_column(DateTime)
    
    

# Database configuration
DATABASE_URL = "sqlite:///data.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
FlightDataModel.metadata.create_all(bind=engine)


async def get_data():
    session = SessionLocal()
    try:
        # Reflect the table
        # Query the table
        stmt = select(FlightDataModel)
        results = session.execute(stmt).fetchall()
        # Convert results to a list of dicts
        data = [jsonable_encoder(row[0]) for row in results]
    finally:
        session.close()
    # Return data
    return data


async def post_data(data: list[FlightDataRow]):
    session = SessionLocal()
    for row in data:
        try:
            stmt = insert(FlightDataModel).values(dict(row))
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            ...

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_data())