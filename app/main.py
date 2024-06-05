from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = FastAPI()

# Database configuration
DATABASE_URL = "mssql+pyodbc://pocuser:pocuser@11LAP5CD2472NZS/SQLEXPRESS/PoC?driver=ODBC+Driver+17+for+SQL+Server"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
schema = "dbo"
metadata = MetaData(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Load Jinja2 templates
env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.get("/index", response_class=HTMLResponse)
async def read_data(request: Request):
    session = SessionLocal()
    try:
        # Reflect the table
        poc_flight_data_processed = Table("PoCFlightDataProcessed", metadata, autoload_with=engine)
        
        # Query the table
        stmt = select(poc_flight_data_processed)
        results = session.execute(stmt).fetchall()
        
        # Convert results to a list of dicts
        data = [dict(row) for row in results]
        
    finally:
        session.close()

    # Render the template with the data
    template = env.get_template("index.html")
    return template.render(request=request, data=data)

