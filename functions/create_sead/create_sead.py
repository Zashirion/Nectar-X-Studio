import os, json
from appwrite.client import Client
from dotenv import load_dotenv
from appwrite.services.databases import Databases

load_dotenv()
client = Client()
client.set_endpoint(os.getenv('APPWRITE_ENDPOINT')) \
      .set_project(os.getenv('APPWRITE_PROJECT_ID')) \
      .set_key(os.getenv('APPWRITE_API_KEY'))

db = Databases(client)

def main(req):
    data = json.loads(req['payload'])
    # data must contain: sead, name, surname, email, unique_user_code, expiry_date
    doc = db.create_document(
        database_id=os.getenv("APPWRITE_DATABASE_ID"),
        collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
        document_id=data['unique_user_code'],
        data=data
    )
    return {"status": "created", "doc": doc}
