
"""
LangChain tools for querying procurement data
Defines tools for searching, counting, aggregating procurement records in MongoDB.
These tools are used by the procurement agent to answer user queries.
"""

from langchain.tools import tool
from typing import Dict, Any, List, Optional
from pymongo.database import Database
import logging
import json
# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from app.database.mongodb import get_database
from fastapi import APIRouter, HTTPException, Depends


logger = logging.getLogger(__name__)


class SearchDatabaseInput(BaseModel):
    """
    Input for search_database tool
    this class defines the schema for the input parameters of the search_database tool.
    its used to validate and structure the input data when the tool is called.
    and its contains:
    - query: A dictionary representing the MongoDB query filter.
    - limit: An integer specifying the maximum number of results to return (default is 100).
    - sort_field: An optional string indicating the field to sort the results by.
    - sort_order: An integer indicating the sort order (1 for ascending, -1 for descending; default is -1).

    The purpose of this class is to ensure that the input data for the search_database tool
    is well-defined and adheres to the expected format.
    and why i put both query and limit?
    1. query: This parameter allows users to specify the criteria for searching the procurement database.
       It defines what records to retrieve based on various fields and conditions.
    2. limit: This parameter controls the number of results returned by the search.
    By including both parameters, the tool can perform targeted searches while also managing
    the volume of data returned, ensuring efficient and relevant responses.
    and why i put sort_field and sort_order?
    3. sort_field: This parameter allows users to specify which field the search results should be sorted by.
       Sorting can help organize the results in a meaningful way, such as by date, price, or department name.
    4. sort_order: This parameter defines the order of sorting (ascending or descending).
    Including both sorting parameters enables users to customize the presentation of search results,
    making it easier to analyze and interpret the data retrieved from the database.

    
    """
    query: Dict[str, Any] = Field(description="MongoDB query filter as a dictionary")
    limit: int = Field(default=100, description="Maximum number of results to return")
    sort_field: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: int = Field(default=-1, description="Sort order: 1 for ascending, -1 for descending")


class CountDocumentsInput(BaseModel):
    """Input for count_documents tool
    this class defines the schema for the input parameters of the count_documents tool.
    its used to validate and structure the input data when the tool is called.
    and its contains:
    - query: A dictionary representing the MongoDB query filter.
    The purpose of this class is to ensure that the input data for the count_documents tool
    is well-defined and adheres to the expected format.
    """
    query: Dict[str, Any] = Field(description="MongoDB query filter as a dictionary")


class AggregateDataInput(BaseModel):
    """Input for aggregate_data tool
    this class defines the schema for the input parameters of the aggregate_data tool.
    its used to validate and structure the input data when the tool is called.
    and its contains:
    - pipeline: A list of dictionaries representing the MongoDB aggregation pipeline.
    The purpose of this class is to ensure that the input data for the aggregate_data tool
    
    """
    pipeline: List[Dict[str, Any]] = Field(description="MongoDB aggregation pipeline")


class ProcurementTools:
    """LangChain tools for querying procurement data"""
    

    
    @tool("search_database", args_schema=SearchDatabaseInput)
    def search_database(query: Dict[str, Any], limit: int = 100, 
                       sort_field: Optional[str] = None, sort_order: int = -1) -> str:
        """
        Search the procurement database with a MongoDB query.
        
        Use this tool to find procurement records matching specific criteria.
        
        Examples:
        - Find records by year: {"fiscal_year": "2014-2015"}
        - Find by department: {"department_name": "Technology Services"}
        - Find by price range: {"total_price": {"$gt": 10000}}
        - Find IT purchases: {"department_name": {"$regex": "Technology", "$options": "i"}}
        
        Returns JSON string with results.
        """
        try:
            # Get database from global instance
            db= get_database()

            collection = db["purchases"]
            
            cursor = collection.find(query)
            
            if sort_field:
                cursor = cursor.sort(sort_field, sort_order)
            
            cursor = cursor.limit(limit)
            
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            logger.info(f"Search found {len(results)} results")
            
            return json.dumps({
                "success": True,
                "count": len(results),
                "results": results[:10],  # Return max 10 for context
                "total_found": len(results)
            })
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return json.dumps({"success": False, "error": str(e)})
    
    @tool("count_documents", args_schema=CountDocumentsInput)
    def count_documents(query: Dict[str, Any] ) -> str:
        """
        Count documents matching a query without retrieving them.
        
        Use this when you need to know HOW MANY records match criteria.
        
        Examples:
        - Count 2014 purchases: {"fiscal_year": "2014-2015"}
        - Count expensive purchases: {"total_price": {"$gt": 100000}}
        
        Returns JSON string with count.
        """
        try:
            logger.info(f"its count query: {query}")
            db= get_database()

            collection = db["purchases"]
            
            count = collection.count_documents(query)
            
            logger.info(f"Count query returned {count}")
            
            return json.dumps({
                "success": True,
                "count": count
            })
            
        except Exception as e:
            logger.error(f"Count error: {e}")
            return json.dumps({"success": False, "error": str(e)})
    
    @tool("aggregate_data", args_schema=AggregateDataInput)
    def aggregate_data(pipeline: List[Dict[str, Any]]) -> str:
        """
        Perform MongoDB aggregation for complex queries like grouping, summing, and calculations.
        
        Use this for:
        - Top N queries (e.g., "top 5 departments by spending")
        - Sum/average calculations
        - Grouping data
        
        Examples:
        - Top departments: [
            {"$group": {"_id": "$department_name", "total": {"$sum": "$total_price"}}},
            {"$sort": {"total": -1}},
            {"$limit": 5}
          ]
        
        Returns JSON string with aggregation results.
        """
        try:
            db= get_database()

            collection = db["purchases"]
            
            results = list(collection.aggregate(pipeline))
            
            # Convert ObjectId to string
            for doc in results:
                if '_id' in doc and hasattr(doc['_id'], '__str__'):
                    doc['_id'] = str(doc['_id'])
            
            logger.info(f"Aggregation returned {len(results)} results")
            
            return json.dumps({
                "success": True,
                "results": results
            })
            
        except Exception as e:
            logger.error(f"Aggregation error: {e}")
            return json.dumps({"success": False, "error": str(e)})
    
    @tool("get_schema_info")
    def get_schema_info() -> str:
        """
        Get information about the database schema and available fields.
        
        Use this tool FIRST to understand what fields are available before querying.
        
        Returns JSON string with schema information.
        """
        try:
            db= get_database()

            collection = db["purchases"]
            
            # Get sample document
            sample = collection.find_one()
            fields = list(sample.keys()) if sample else []
            
            # Get distinct values for key fields
            departments = collection.distinct("department_name")[:20]
            fiscal_years = sorted(collection.distinct("fiscal_year"))
            acquisition_types = collection.distinct("acquisition_type")
            data_dictionary = {
            "Creation Date": "Date of purchase order entered by the user. Can be back-dated; creation date is used.",
            "Fiscal Year": "Derived from creation date. CA fiscal year: July 1 – June 30.",
            "LPA Number": "Leveraged Procurement Agreement (contract) number.",
            "Purchase Order Number": "Not unique across departments.",
            "Requisition Number": "Not unique across departments.",
            "Acquisition Type": "Non-IT Goods, Non-IT Services, IT Goods, IT Services.",
            "Sub-Acquisition Type": "Depends on acquisition type.",
            "Acquisition Method": "Type of acquisition used. See supplemental dictionary.",
            "Sub-Acquisition Method": "Depends on acquisition method.",
            "Department Name": "Name of purchasing department (normalized).",
            "Supplier Code": "Normalized supplier code.",
            "Supplier Name": "Supplier name at time of registration.",
            "Supplier Qualifications": "SB, SBE, DVBE, NP, MB (can be combined).",
            "Supplier Zip Code": "Zip code of supplier.",
            "CalCard": "Whether CalCard used (Yes/No).",
            "Item Name": "Name of purchased item.",
            "Item Description": "Description of purchased item.",
            "Quantity": "Quantity purchased.",
            "Unit Price": "Price per unit.",
            "Total Price": "Total price excluding tax/shipping.",
            "Classification Codes": "UNSPSC v14. May have multiple codes.",
            "Normalized UNSPSC": "First 8 digits of UNSPSC for the full PO.",
            "Commodity Title": "Based on normalized UNSPSC.",
            "Class": "Class number based on normalized UNSPSC.",
            "Class Title": "Class title based on normalized UNSPSC.",
            "Family": "Family number based on normalized UNSPSC.",
            "Family Title": "Family title based on normalized UNSPSC.",
            "Segment": "Segment number based on normalized UNSPSC."
        }


            
            schema_info = {
                "collection": "purchases",
                "available_fields": fields,
                "sample_departments": departments,
                "fiscal_years": fiscal_years,
                "acquisition_types": acquisition_types,
                "important_fields": {
                    "department_name": "Name of the purchasing department",
                    "supplier_name": "Vendor/supplier name",
                    "total_price": "Purchase amount (numeric)",
                    "fiscal_year": "Fiscal year (e.g., '2014-2015')",
                    "acquisition_type": "Type of acquisition (e.g., 'IT', 'LPA')",
                    "purchase_date": "Date of purchase",
                    "creation_date": "Record creation date"
                },
                "data_dictionary": data_dictionary

            }
            
            return json.dumps(schema_info)
            
        except Exception as e:
            logger.error(f"Schema info error: {e}")
            return json.dumps({"success": False, "error": str(e)})
    
    def get_tools_list(self):
        """Get list of all tools for the agent"""
        return [
            self.get_schema_info,
            self.search_database,
            self.count_documents,
            self.aggregate_data
        ]
