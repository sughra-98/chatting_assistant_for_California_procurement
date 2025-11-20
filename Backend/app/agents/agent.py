"""
LangChain agent for procurement data queries (new API)
Uses Gemini LLM with tools to answer questions about California procurement data.

"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from app.agents.tools import ProcurementTools
from app.config import get_settings
from pymongo.database import Database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProcurementAgent:
    """LangChain agent for procurement data queries (new API)"""

    def __init__(self, db: Database):
        """
        Initialize the Procurement Agent with Gemini LLM and tools
        in the new LangChain agent framework.
        what is purpose of the __init__ method? the __init__ method is a special method in Python classes that is 
        automatically called when an instance (object) of the class is created. 
        Its primary purpose is to initialize the attributes of the new object and set up any 
        necessary state or configuration.
        """
        self.db = db
        self.settings = get_settings()

        # Initialize LLM (Gemini)
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.MODEL_NAME,
            google_api_key=self.settings.GOOGLE_API_KEY,
            temperature=0,
            convert_system_message_to_human=True
        )

        # Load Tools
        tools_manager = ProcurementTools()
        self.tools = tools_manager.get_tools_list()

        # Create the agent with the new LangChain API
        self.agent = self._create_agent()

        logger.info(f"Gemini Procurement Agent initialized with {len(self.tools)} tools")

    def _create_agent(self):
        """Create agent using new create_agent API 
        with system prompt and tools defined.
        core function is to create and configure an agent that can 
        interact with the procurement database using the specified tools and language model.
        """
        tool_descriptions = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        tool_names = ", ".join([tool.name for tool in self.tools])

        system_prompt = system_prompt = f"""You are an AI assistant for querying California procurement data.
You have access to tools that allow you to:
  - Search procurement records
  - Count documents
  - Aggregate data
  - Retrieve schema information
  - Analyze MongoDB procurement purchase orders

==============================
IMPORTANT RULES
==============================
1. ALWAYS start by using `get_schema_info` unless the answer is purely definitional.
2. For counting questions, ALWAYS use `count_documents`.
3. For Top-N / group-by, use `aggregate_data`.
4. For specific records, use `search_database`.
5. Fiscal years follow the "2014-2015" format.
6. Always provide a numeric final answer when the user requests a numeric result.
7. Action Input MUST be valid JSON.

### FISCAL YEAR & QUARTER RULES (STRICT)
- The State of California Fiscal Year runs from July 1 to June 30.
- Fiscal quarters are defined as:
  * Q1: July 1 – September 30
  * Q2: October 1 – December 31
  * Q3: January 1 – March 31
  * Q4: April 1 – June 30

### DATA AVAILABILITY RULE
- If the dataset has transactions only up to a certain date (example: through March 31, 2015),
  then:
    * Q4 exists for years where data covers April–June.
    * If a quarter partially exists, include what exists but note missing dates.
    * Never return "$0" unless the database returns zero spend.
    * Never claim "no data" unless the database confirms no records.

### SPECIAL INSTRUCTION
- If a top-N result returns "Unknown" as the most frequent value, also report the count for "Unknown" and the second-most frequent value with its count.

### SPECIAL INSTRUCTION FOR QUARTERLY SPENDING REPORTS
- When the user asks for highest spending at each quarter:
    1. Aggregate spending for **all available fiscal years**.
    2. Use `purchase_date` to filter by quarter date ranges (Q1: Jul-Sep, Q2: Oct-Dec, Q3: Jan-Mar, Q4: Apr-Jun).
    3. For each quarter, find the fiscal year with the **highest total spending**.
    4. Include a **professional summary**:
        - Text paragraph highlighting the top spending per quarter.
        - Table: Fiscal Year | Quarter | Total Spending (USD)
    5. Include **all intermediate numbers** from aggregation if multiple fiscal years are involved.
    6. Never return “$0” unless the database confirms zero spending.

### DATE FIELD RULES
- Always use `purchase_date` for all spending, aggregation, and quarter-based calculations.
- Never use `creation_date` for spending totals or top-N analysis.
- Use ISO format (YYYY-MM-DD) when filtering by dates.

### STRATEGY FOR ANSWERING
- Definitions → Call `get_schema_info` and return a short definitional answer using the tool-provided field descriptions.
- Data / Statistics → Call `get_schema_info` first, then:
    • Small counts or existence checks → `count_documents`.
    • Top-N / groupings → `aggregate_data`.
    • Numeric aggregates (sum/avg) → `aggregate_data`.
- Complex questions (multi-step or ambiguous) → Call `get_schema_info`, then break into sub-questions and use `count_documents`, `aggregate_data`, and/or `search_database` as appropriate; include intermediate numeric outputs.
- Professional reports (summary with evidence) → Call `get_schema_info`, use `aggregate_data` for summary statistics, `search_database` for representative records, and present a concise findings section with key numbers and short supporting examples.

### IMPORTANT MONGODB TIPS
- Use double quotes in JSON: {{"field": "value"}}
- Boolean field for LPA: {{"has_lpa_number": true}}
- For Top-N, use aggregate with $group, $sort, $limit
- When returning dates, prefer ISO format (YYYY-MM-DD)

### RESPONSE STYLE
- Be clear, concise, and professional.
- Show numbers clearly when using queries (label them).
- If you use more than one tool, combine insights logically and show intermediate Observations.
- Always include a final numeric answer (if the user asked for a number).  

### REACT FORMAT (STRICT)
The agent MUST follow this format exactly for tool-using responses:

Question: {{input}}
Thought: think step-by-step
Action: the tool to use (must be one of: {{tool_names}})
Action Input: JSON input for the tool
Observation: tool result
... (repeat Thought → Action → Observation as needed)
Thought: I now know the final answer
Final Answer: <final numeric answer or explicit textual answer if numeric not requested>

==============================
AVAILABLE TOOLS
==============================
{{tool_descriptions}}

TOOL NAMES:
{{tool_names}}

BEGIN QUERY

Question: {{input}}

{{agent_scratchpad}}
"""



        # New create_agent API (returns a CompiledStateGraph)
        return create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt
        )

    def query(self, question: str):
        """ Run the agent on a question and return structured response.
        """

        try:
            logger.info(f"Processing procurement query: {question}")

            result = self.agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })

            logger.info(f"Agent result: {result}")

            answer = extract_answer_from_messages(result)
            if answer:
                return {
                    "answer": answer,
                    "data": [],  # New API does not return raw intermediate steps
                    "query_info": None,
                    "record_count": 0,
                }
            else:
            # Fallback: return string representation
                return {
                    "answer": str(result),
                    "data": [],  # New API does not return raw intermediate steps
                    "query_info": None,
                    "record_count": 0,
                }

            
            # Extract the final answer from result
            # Result is a dict with "messages" key
            
    


        except Exception as e:
            logger.error(f"Agent error: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "data": [],
                "query_info": None,
                "record_count": 0
            }

def extract_answer_from_messages(result):
    """
    Extract a clean answer from Gemini agent messages.
    - Handles text, list, dict
    - Strips model reasoning
    - Pulls only the text after 'Final Answer:' if present
    """
    try:
        # If agent already returned clean "answer" field
        # i used isinstance to check if result is dict
        # if result is a dict and has "answer" key with non-empty value, use it directly
        # this is to ensure that we get the final answer directly if it's already provided
        # result["answer"] is the final answer provided by the agent
        if isinstance(result, dict) and "answer" in result and result["answer"]: 
            text = result["answer"]
        else:
            # fallback: extract from messages
            if not isinstance(result, dict) or "messages" not in result:
                return str(result)

            messages = result["messages"]
            if not messages:
                return ""

            last_msg = messages[-1]
            # Get content from last message safely
            # used getattr to safely get the content attribute from last_msg 
            # the getattr function is used to retrieve the value of an attribute from an object.
            # If the attribute does not exist, it returns None (or a default value if provided) instead of raising an AttributeError.
            content = getattr(last_msg, "content", None)

            # Convert content → string
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                # Extract all "text" parts from list
                parts = []
                for p in content:
                    if isinstance(p, dict) and "text" in p:
                        parts.append(p["text"])
                    else:
                        parts.append(str(p))
                text = "\n".join(parts)
            else:
                text = str(content)

        lowered = text.lower()
        # Extract text after "Final Answer:"
        # used to check if the string "final answer:" exists in the lowered version of the text
        # if it does, it finds the index of that substring and extracts everything that comes after it
        # cleaned text is then stripped of leading/trailing whitespace and returned as the final answer

        if "final answer:" in lowered:
            idx = lowered.index("final answer:")
            clean = text[idx + len("Final Answer:"):].strip()
            return clean

        # If no "Final Answer", fall back to whole text
        return text.strip()

    except Exception as e:
        return f"Error extracting answer: {e}"
