from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import StatsResponse
from app.database.mongodb import get_database
from pymongo.database import Database

router = APIRouter(prefix="/api", tags=["statistics"])


@router.get("/stats", response_model=StatsResponse)
async def get_statistics(db: Database = Depends(get_database)):
    """Get database statistics"""
    try:
        collection = db["purchases"]
        
        # Basic counts
        total_records = collection.count_documents({})
        departments = len(collection.distinct("department_name"))
        suppliers = len(collection.distinct("supplier_name"))
        fiscal_years = sorted(collection.distinct("fiscal_year"))
        
        # Date range
        earliest = collection.find_one(
            {"creation_date": {"$exists": True}},
            sort=[("creation_date", 1)]
        )
        latest = collection.find_one(
            {"creation_date": {"$exists": True}},
            sort=[("creation_date", -1)]
        )
        # Total spending
        pipeline = [
            {"$match": {"total_price": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_price"}}}
        ]
        spending_result = list(collection.aggregate(pipeline))
        total_spending = spending_result[0]["total"] if spending_result else 0.0
        
        return StatsResponse(
            total_records=total_records,
            departments=departments,
            suppliers=suppliers,
            fiscal_years=fiscal_years,
            total_spending=total_spending,
            date_range={
                "start": earliest["creation_date"].isoformat() if earliest else "N/A",
                "end": latest["creation_date"].isoformat() if latest else "N/A"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

