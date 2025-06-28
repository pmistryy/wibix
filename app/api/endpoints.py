from fastapi import APIRouter, UploadFile, File, Depends, Query
import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.services.vectorizer import vectorize_id_name, vectorize_id_only, vectorize_name_only, vectorize_query
from app.services.search import semantic_search, get_best_match, smart_search
from app.schemas.data import DataEntrySchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    updated_count = 0
    new_count = 0
    
    for _, row in df.iterrows():
        combined_vec = vectorize_id_name(str(row['id']), str(row['name']))
        id_vec = vectorize_id_only(str(row['id']))
        name_vec = vectorize_name_only(str(row['name']))
        
        description = row.get('description', '') if 'description' in row else ''
        
        # Check if entry already exists
        existing_entry = db.query(models.DataEntry).filter(models.DataEntry.id == int(row['id'])).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.name = str(row['name'])
            existing_entry.meta = description
            existing_entry.vector = combined_vec
            existing_entry.id_vector = id_vec
            existing_entry.name_vector = name_vec
            updated_count += 1
        else:
            # Create new entry
            entry = models.DataEntry(
                id=int(row['id']),
                name=str(row['name']),
                meta=description,
                vector=combined_vec,
                id_vector=id_vec,
                name_vector=name_vec
            )
            db.add(entry)
            new_count += 1
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Processed {len(df)} entries",
        "updated": updated_count,
        "new": new_count,
        "total_processed": len(df)
    }

@router.get("/search/", response_model=DataEntrySchema)
def search_best(
    query: str = Query(..., description="Search query (ID, name, or both)"),
    db: Session = Depends(get_db)
):
    """
    Get only the best (first) semantic match using smart search.
    
    - query: Your search term (ID, name, or both)
    """
    entries = db.query(models.DataEntry).all()
    result = get_best_match(query, entries)
    
    if result:
        score, entry = result
        return DataEntrySchema(id=entry.id, name=entry.name, meta=entry.meta, score=float(score))
    else:
        return {"message": "No matches found", "id": None, "name": None, "meta": None, "score": 0.0}