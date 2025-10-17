import os, json
from appwrite.client import Client
from dotenv import load_dotenv
from appwrite.services.databases import Databases
from cryptography.fernet import Fernet

load_dotenv()
FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY)

client = Client()
client.set_endpoint(os.getenv('APPWRITE_ENDPOINT')) \
      .set_project(os.getenv('APPWRITE_PROJECT_ID')) \
      .set_key(os.getenv('APPWRITE_API_KEY'))

db = Databases(client)

def main(req):
    data = json.loads(req['payload'])
    try:
        if 'unique_user_code' in data:
            doc = db.get_document(
                database_id=os.getenv("APPWRITE_DATABASE_ID"),
                collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
                document_id=data['unique_user_code']
            )
            sead_encrypted = doc['sead']
        elif 'sead' in data:
            # if validating by SEAD, you may need to scan documents to match SEAD
            # For simplicity, assume client sends unique_user_code
            return {"status": "error", "reason": "Please provide unique_user_code"}
        decrypted = json.loads(fernet.decrypt(sead_encrypted.encode()).decode())
        # Check expiry
        from datetime import datetime
        if datetime.strptime(decrypted['expiry_date'], "%Y-%m-%d") < datetime.now():
            return {"status": "expired", "payload": decrypted}
        return {"status": "valid", "payload": decrypted}
    except Exception as e:
        return {"status": "invalid", "reason": str(e)}
