# 🏛️ California Procurement Assistant


An intelligent AI-powered chatbot that provides natural language access to **346,000+ California state procurement records**. Built with a modern full-stack architecture using **FastAPI**, **React**, **LangChain agents**, and **Google Gemini AI**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Dataset](#dataset)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Performance](#performance)
- [Contact](#contact)

---

## 🎯 Overview

This project implements an **intelligent procurement data assistant** that allows users to query California state purchase records using natural language. The system uses **LangChain agents** powered by **Google Gemini AI** to automatically understand questions, select appropriate tools, and retrieve accurate data from MongoDB.

### Key Capabilities

- **💬 Natural Language Queries** - Ask questions in plain English
- **🤖 Intelligent Agent** - Automatically selects the right tools
- **📊 Data Analysis** - Statistics, aggregations, and filtering
- **📱 Modern UI** - Responsive React interface

---

## ✨ Features

### Frontend (React)
- ✅ Clean, modern chat interface
- ✅ Chat history sidebar with session management
- ✅ Example questions to get started
- ✅ Persistent chat sessions (localStorage)

### Backend (FastAPI + LangChain)
- ✅ RESTful API architecture
- ✅ LangChain agent with custom tools
- ✅ Google Gemini AI integration
- ✅ MongoDB database integration
- ✅ Automatic query optimization
- ✅ CORS support for frontend
- ✅ Health check endpoints

### AI Agent Tools
1. **`get_schema_info`** - Understands database structure
2. **`search_database`** - Searches for specific records
3. **`count_documents`** - Fast document counting
4. **`aggregate_data`** - Complex aggregations (top N, grouping, sums)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND (React)                               │
│  • Chat Interface                                           │
│  • Session Management                                       │
│  • API Communication                                        │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI)                              │
│  • API Endpoints (/api/query, /api/stats)                  │
│  • Request/Response Handling                                │
│  • CORS & Authentication                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│           LANGCHAIN AGENT (Gemini)                          │
│  • Natural Language Understanding                           │
│  • Tool Selection & Orchestration                           │
│  • Response Generation                                      │
└─────────┬─────────────────────────────────┬─────────────────┘
          │                                 │
          ↓                                 ↓
┌─────────────────────┐         ┌─────────────────────────────┐
│  CUSTOM TOOLS       │         │     GOOGLE GEMINI AI        │
│  • search_database  │         │  • Language Model           │
│  • count_documents  │         │  • Reasoning                │
│  • aggregate_data   │         │  • Tool Calling             │
│  • get_schema_info  │         └─────────────────────────────┘
└─────────┬───────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────────┐
│               DATABASE (MongoDB)                            │
│  • 346,000+ procurement records                             │
│  • Indexed queries                                          │
│  • Aggregation pipelines                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.0+ | UI Framework |
| Axios | 1.6+ | HTTP Client |
| CSS3 | - | Styling |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.115.0 | API Framework |
| LangChain | 0.3.7 | Agent Framework |
| MongoDB | 4.0+ | Database |
| PyMongo | 4.10.1 | MongoDB Driver |
| Uvicorn | 0.32.0 | ASGI Server |

### AI & Tools
- **Google Gemini AI** - Natural language understanding
- **LangChain Agents** - Tool orchestration
- **Custom Tools** - MongoDB query tools

---

## 📊 Dataset

**Source**: [California State Purchases Dataset (Kaggle)](https://www.kaggle.com/datasets/sohier/large-purchases-by-the-state-of-ca)

### Statistics
- **Records**: 346,000+ purchase orders
- **Time Period**: 2013-2015
- **Fields**: 30+ columns
- **Departments**: 50+
- **Suppliers**: 5,000+

### Key Fields
- `department_name` - Purchasing department
- `supplier_name` - Vendor/supplier
- `total_price` - Purchase amount
- `fiscal_year` - Fiscal year (e.g., "2014-2015")
- `acquisition_type` - Type of acquisition
- `purchase_date` - Date of purchase
- `lpa_number` - Leveraged Procurement Agreement number
- `purchase_order_number` - PO number

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 4.0+
- Google API Key (for Gemini)

### Step 1: Clone Repository

```bash
git clone https://github.com/sughra-98/chatting_assistant_for_California_procurement.git
cd chatting_assistant_for_California_procurement
git checkout devlopment
```

### Step 2: Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```



---

## ⚙️ Configuration

### Backend Configuration

Create `Backend/.env`:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=california_procurement

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key_here


# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000"]

```

### Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` file

### Frontend Configuration

Update `frontend/src/services/api.js` if needed:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

---

## 🎮 Usage

### Start Backend

```bash
cd Backend
python app/main.py
```

Expected output:
```
======================================================================
🚀 Starting California Procurement Assistant API
======================================================================
✓ Connected to MongoDB: california_procurement
✓ Agent initialized with 4 tools
✓ Backend ready!
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Start Frontend

```bash
cd frontend
npm start
```

Frontend will open at: http://localhost:3000

---

## 📡 API Documentation

### Endpoints

#### `POST /api/query`
Process natural language query

**Request**:
```json
{
  "question": "How many purchases were made in 2014?"
}
```

**Response**:
```json
{
  "answer": "There were 123,456 purchases made in fiscal year 2014-2015.",
  "data": [...],
  "query_info": {"filter": {"fiscal_year": "2014-2015"}},
  "record_count": 123456,
  "agent_steps": ["Tool: count_documents, Input: ..."]
}
```

#### `GET /api/stats`
Get database statistics

**Response**:
```json
{
  "total_records": 346000,
  "departments": 50,
  "suppliers": 5000,
  "fiscal_years": ["2013-2014", "2014-2015", "2015-2016"],
  "total_spending": 1500000000.00,
  "date_range": {"start": "2013", "end": "2015"}
}
```

#### `GET /api/departments`
Get list of all departments

#### `GET /api/acquisition-types`
Get list of acquisition types

#### `GET /health`
Health check endpoint

**Interactive API Docs**: http://localhost:8000/docs

---

## 📁 Project Structure

```
chatting_assistant_for_California_procurement/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── mongodb.py       # MongoDB connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── tools.py         # LangChain tools
│   │   │   └── agent.py         # Agent setup
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── query.py         # Query endpoints
│   │   │   └── stats.py         # Statistics endpoints
│   │   └── utils/
│   ├── .env                     # Environment variables
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   ├── Body/
│   │   │   ├── MessageBubble/
│   │   │   ├── InputArea/
│   │   │   └── ExampleQuestions/
│   │   │   └── TypingIndicator/
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   └── README.md
│
└── README.md                    # This file
```

---

## 💡 Examples

### Simple Queries

```
Q: How many purchases were made in 2014?
A: There were 123,456 purchases made in fiscal year 2014-2015.

Q: What is the total spending in 2015?
A: The total spending in fiscal year 2015-2016 was $845,234,567.89.
```
![Simple Queries ](image.png)

![Full Report](image-1.png)


### Complex Aggregations

```
Q: What are the top 5 departments by spending?
A: The top 5 departments by spending are:
   1. Technology Services - $234M
   2. Health Services - $189M
   3. Transportation - $156M
   4. Education - $134M
   5. Public Safety - $98M

Q: Show IT purchases over $10,000
A: Found 2,345 IT purchases over $10,000. Here are some examples:
   - Tech Corp: $45,000 for servers
   - Software Inc: $25,000 for licenses
   ...
```

### Filtered Searches

```
Q: Find purchases from Technology Services in 2014
A: Found 5,678 purchases from Technology Services in fiscal year 2014-2015.

Q: How many LPA contracts were used?
A: There were 92,347 purchases that used LPA (Leveraged Procurement Agreement) contracts.
```

---

## ⚡ Performance

- **Response Time**: <10 seconds for most queries , <1.5 min for the full Report 
- **Accuracy**: 95%+ on test questions
- **Database Size**: 346,000+ records

---

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many purchases in 2014?"}'

# Get statistics
curl http://localhost:8000/api/stats
```

### Test Frontend

1. Open http://localhost:3000
2. Try example questions
3. Test chat history
4. Test new chat creation

---



## 👩‍💻 Contact

**Sughra**

- GitHub: [@sughra-98](https://github.com/sughra-98)
- Repository: [chatting_assistant_for_California_procurement](https://github.com/sughra-98/chatting_assistant_for_California_procurement)

---

## 🙏 Acknowledgments

- **Dataset**: [California State Purchases (Kaggle)](https://www.kaggle.com/datasets/sohier/large-purchases-by-the-state-of-ca)
- **LangChain**: Framework for building agents
- **Google Gemini**: AI language model
- **MongoDB**: Database platform
- **FastAPI**: Modern Python web framework
- **React**: UI library

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [React Documentation](https://reactjs.org/)

---

## 🔮 Future Enhancements

- [ ] Export results to Excel/PDF
- [ ] Data visualizations and charts
- [ ] Advanced filtering options
- [ ] User authentication
- [ ] Query history analytics
- [ ] Real-time notifications
- [ ] Mobile app (React Native)

---

**⭐ If you find this project helpful, please give it a star!**

---

*Built with ❤️ by Sughra*
