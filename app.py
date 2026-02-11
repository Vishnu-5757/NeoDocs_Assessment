import falcon
import sqlite3
import json
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def log_event(endpoint, status, reason=None, request_id=None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "status": status,
        "reason": reason,
        "request_id": request_id
    }
    print(json.dumps(log_data))


class TestResource:
    def __init__(self):
        self.db_name = os.getenv("DATABASE_NAME")

    def validate_payload(self, data):
        """Manual Validation"""
        required_fields = ["test_id", "patient_id", "clinic_id", "test_type", "result"]
        if not data:
            return "Empty request body"
        for field in required_fields:
            if field not in data or not isinstance(data[field], str) or not data[field].strip():
                return f"Missing or invalid field: {field}"
        return None

    def on_post(self, req, resp):
        """End Point : 1 """
        request_id = str(uuid.uuid4())
        try:
            raw_data = req.get_media()
        except Exception:
            log_event("/tests", "failure", "Invalid JSON", request_id)
            raise falcon.HTTPBadRequest(description="Invalid JSON")
    
        
        error = self.validate_payload(raw_data)
        if error:
            log_event("/tests", "failure", error, request_id)
            raise falcon.HTTPUnprocessableEntity(description=error)

        
        conn = sqlite3.connect(self.db_name)
        conn.isolation_level = None 
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN") 
            
            
            cursor.execute("SELECT test_id FROM tests WHERE test_id = ?", (raw_data['test_id'],))
            if cursor.fetchone():
                cursor.execute("ROLLBACK")
                log_event("/tests", "failure", "Duplicate test_id", request_id)
                resp.status = falcon.HTTP_409
                resp.media = {"error": "test_id already exists"}
                return

            created_at = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO tests (test_id, patient_id, clinic_id, test_type, result, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (raw_data['test_id'], raw_data['patient_id'], raw_data['clinic_id'], raw_data['test_type'], raw_data['result'], created_at)
            )
            
            cursor.execute("COMMIT") 
            log_event("/tests", "success", request_id=request_id)
            resp.status = falcon.HTTP_201
            resp.media = {"status": "success", "test_id": raw_data['test_id']}

        except Exception as e:
            cursor.execute("ROLLBACK") 
            log_event("/tests", "failure", str(e), request_id)
            raise falcon.HTTPInternalServerError(description="Database operation failed")
        finally:
            conn.close()

    def on_get(self, req, resp):
        """Endpoint 2: GET /tests?clinic_id=<id>"""
        request_id = str(uuid.uuid4())
        clinic_id = req.get_param('clinic_id')

    
        if not clinic_id:
            log_event("/tests", "failure", "Missing clinic_id parameter", request_id)
            raise falcon.HTTPBadRequest(description="Query parameter 'clinic_id' is required")

        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT test_id, patient_id, clinic_id, test_type, result, created_at FROM tests WHERE clinic_id = ?", (clinic_id,))
            rows = cursor.fetchall()
            
            
            results = []
            for r in rows:
                results.append({
                    "test_id": r[0],
                    "patient_id": r[1],
                    "clinic_id": r[2],
                    "test_type": r[3],
                    "result": r[4],
                    "created_at": r[5]
                })

            log_event("/tests", "success", request_id=request_id)
            resp.status = falcon.HTTP_200
            resp.media = results  

        except Exception as e:
            log_event("/tests", "failure", str(e), request_id)
            raise falcon.HTTPInternalServerError(description="Database retrieval failed")
        finally:
            conn.close()


app = falcon.App()
tests = TestResource()
app.add_route('/tests', tests)