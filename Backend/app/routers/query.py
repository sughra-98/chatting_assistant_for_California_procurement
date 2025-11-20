from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse
from app.agents.agent import ProcurementAgent
from app.database.mongodb import get_database
from pymongo.database import Database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["queries"])

# Cache agent instance
_agent_instance = None


def get_agent(db: Database = Depends(get_database)) -> ProcurementAgent:
    """Get or create agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ProcurementAgent(db)
    return _agent_instance


@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    agent: ProcurementAgent = Depends(get_agent)
):
    """
    Process natural language query using LangChain agent
    """
    try:
        logger.info(f"📝 Query: {request.question}")
        
        # Use agent to process query
        result = agent.query(request.question)
        
        
        logger.info(f"✓ Response: {result['answer'][:100]}...")
        logger.info(f"✓ Response: {result['answer']}...")
        
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"✗ Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/departments")
async def get_departments(db: Database = Depends(get_database)):
    """Get list of all departments"""
    try:
        collection = db["purchases"]
        departments = collection.distinct("department_name")
        return {"departments": sorted(departments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/acquisition-types")
async def get_acquisition_types(db: Database = Depends(get_database)):
    """Get list of all acquisition types"""
    try:
        collection = db["purchases"]
        types = collection.distinct("acquisition_type")
        return {"acquisition_types": sorted(types)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
