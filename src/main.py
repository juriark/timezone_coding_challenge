from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    This is awesome
    """
    return {"Hello": "World"}
