from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import MedQuery, MedResult
from med_data import get_equivalents

app = FastAPI(title="MedicCheck API")

# Allow requests from any origin (fine for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root() -> dict:
    return {"status": "ok", "message": "MedicCheck API running 🚀"}


@app.post("/medications", response_model=MedResult, tags=["medications"])
def find_equivalents(query: MedQuery) -> MedResult:
    """
    Return a mapping of country → brand name for the requested active ingredient.
    """
    equivalents = get_equivalents(query.med_name)
    return MedResult(original=query.med_name, equivalents=equivalents)
