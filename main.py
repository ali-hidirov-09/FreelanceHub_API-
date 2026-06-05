from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Xabar": "Salom!"}


@app.get("/ali")
def post():
     return {"ma'lumot":"ALi 17 yoshli yosh backend dasturchi"}