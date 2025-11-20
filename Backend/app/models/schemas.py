"""
Pydantic schemas for request and response models


"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for user queries"""
    question: str = Field(..., min_length=1, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How many IT purchases were made in 2014?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for queries"""
    answer: str
    data: List[Dict[str, Any]] = []
    query_info: Optional[Dict[str, Any]] = None
    record_count: int = 0
    agent_steps: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Found 1,234 IT purchases in 2014.",
                "data": [],
                "query_info": {"filter": {"fiscal_year": "2014-2015"}},
                "record_count": 1234,
                "agent_steps": ["Analyzed query", "Searched database"]
            }
        }


class StatsResponse(BaseModel):
    """Response model for database statistics"""
    total_records: int
    departments: int
    suppliers: int
    fiscal_years: List[str]
    total_spending: float
    date_range: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_records": 346000,
                "departments": 50,
                "suppliers": 5000,
                "fiscal_years": ["2013-2014", "2014-2015", "2015-2016"],
                "total_spending": 1500000000.00,
                "date_range": {"start": "2013", "end": "2015"}
            }
        }
