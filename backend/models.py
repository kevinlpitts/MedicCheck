from pydantic import BaseModel, Field


class MedQuery(BaseModel):
    med_name: str = Field(..., example="Paracetamol")
    # Keeping country in reserve for later logic
    country: str | None = Field(None, example="USA")


class MedResult(BaseModel):
    original: str
    equivalents: dict[str, str]
