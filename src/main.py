from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
from database import engine, sessionLocal
from sqlalchemy.orm import Session
import models
import psycopg2


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class TestDb(BaseModel):
    dataText : str


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]




conn = psycopg2.connect(
    database="dodots",
    user="postgres",
    password="qwertyuiop",
    host="127.0.0.1",
    port="5432"
)

# Create a cursor
cur = conn.cursor()



# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request":request, "name": "nur"})

@app.post("/test/")
async def home(question: TestDb, db: db_dependency):
    # return templates.TemplateResponse("index.html", {"request":request, "name": "nur"})
    # db_question = models.Data(dataText=question.dataText)
    # db.add(db_question)
    # db.commit()
    # db.refresh(db_question)

    # sql = f"INSERT INTO public.test (dataText) VALUES ({question.dataText})"

    # Execute the statement with the question text
    # cur.execute(sql, (question.dataText,))
    x = "public.test"
    y = "dataText"
    z = question.dataText
    # cur.execute('INSERT INTO public.test (%s) VALUES (%s)', (y, z))
    cur.execute("""
     INSERT INTO public.test ("dataText")
     VALUES (%s);
     """,
     (z,))


    # Commit the changes to the database
    conn.commit()

    cur.close()
    conn.close()

@app.get("/")
def query(db: db_dependency, request: Request):
    # result = db.query(models.Data.id, models.Data.dataText)
    # Execute a query
    cur.execute("SELECT generate_user_id();")

    # Fetch the results
    result = cur.fetchall()


    # Close the cursor and connection
    cur.close()
    conn.close()
    return templates.TemplateResponse("index.html", {"request":request, "name": result})




class user(BaseModel):
    fname: str
    lname: str
    dname: str
    dob: str
    nic: str
    gender: str
    pw: str



import datetime
@app.post("/createUser")
def create_user(data: user, request: Request):
    x = datetime.datetime.now()
    cur.execute("""INSERT INTO public.people_table VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", ("qwe", data.fname, data.lname, data.dname, data.dob, data.nic, data.gender, data.pw, "x"))
    conn.commit()

