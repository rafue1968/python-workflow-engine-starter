from fastapi import FastAPI

app = FastAPI(title="Workflow Engine")

@app.get("/health")
def health():
    return (
        {
            "status": "ok"
        }
    )