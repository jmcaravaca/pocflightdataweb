from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = FastAPI()

# Database configuration
DATABASE_URL = "mssql+pyodbc://sa:YourStrong!Passw0rd@localhost/PoC?trustServerCertificate=yes&driver=ODBC+Driver+18+for+SQL+Server"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Load Jinja2 templates
env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.get("/", response_class=HTMLResponse)
async def redirecthome(request: Request):
    return RedirectResponse("/dynamic")




@app.get("/index", response_class=HTMLResponse)
async def read_data(request: Request):
    # Render the template with the data
    data = await get_data()
    template = env.get_template("index.html")
    return template.render(request=request, data=data)

@app.get("/dynamic", response_class=HTMLResponse)
async def dynamic_site(request: Request):
    # Render the template with the data
    template = env.get_template("dynamic.html")
    return template.render(request=request)


@app.get("/flightdata", response_class=JSONResponse)
async def get_flight_data(request: Request):
    data = await get_data()
    return data


async def get_data():
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
    # Return data
    return data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5555)