# Backend Engineer Assessment - Test Data API

A minimalist, high-discipline backend API for clinical test data ingestion and retrieval. Built with **Falcon** and **SQLite**, adhering to strict requirements for manual data handling and explicit transaction management.

---

## 🚀 Setup and Execution

### 1. Prerequisites
Ensure you have Python 3.8+ installed. It is recommended to use a virtual environment.

### 2. Install Dependencies

pip install -r requirements.txt



### 3. Environment Configuration
Create a .env file in the root directory (already configured in this project):

DATABASE_NAME=test_data.db


### 4. Initialize the Database
Run the setup script to create the tests table schema:

python init_db.py

### 5. Initialize the Database

Start the local server (serving on port 8000):

python run.py




### 6. END POINTS

1. POST /tests

Ingests a new clinical test record.

Request Body:

JSON

{
  "test_id": "t123",
  "patient_id": "p001",
  "clinic_id": "c001",
  "test_type": "CBC",
  "result": "Normal"
}

1. GET /tests?clinic_id=c001

Get Records for that Clinical ID
