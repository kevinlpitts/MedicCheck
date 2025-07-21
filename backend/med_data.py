"""
MVP in‑memory lookup table.

Phase 2 → replace with calls to RxNorm, OpenFDA, DrugBank, etc.
"""

med_db = {
    "paracetamol": {  # acetaminophen
        "USA": "Tylenol",
        "UK": "Panadol",
        "India": "Calpol",
        "France": "Doliprane",
    },
    "ibuprofen": {
        "USA": "Advil",
        "UK": "Nurofen",
        "India": "Brufen",
        "France": "Nurofen",
    },
}


def get_equivalents(med_name: str) -> dict[str, str]:
    """
    Normalizes name and returns country → equivalent mapping.
    Unknown meds return an empty dict.
    """
    key = med_name.strip().lower()
    return med_db.get(key, {})
