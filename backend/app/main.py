from fastapi import FastAPI


app=FastAPI(title="rental management",description="api for rental",version="1.0.0")

@app.get("/")
def health_check():
    return {"message":"ok"}
