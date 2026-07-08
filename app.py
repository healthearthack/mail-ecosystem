from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Mail Ecosystem Core API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MailboxSchema(BaseModel):
    address: str
    routing_type: str
    status: str = "Active"

class EmailMessageSchema(BaseModel):
    id: Optional[int] = None
    sender: str
    recipient: str
    subject: str
    body: str

SYSTEM_DIRECTORY = [
    {"name": "andy", "domain": "adp", "privacy": "kieckhefer"},
    {"name": "alex", "domain": " x", "privacy": "schwab"},
    {"name": "ericka", "domain": "nm", "privacy": "turner"},
    {"name": "michelle", "domain": "amazon", "privacy": "brenmark"},
    {"name": "matt", "domain": "aws", "privacy": "jensen"},
    {"name": "robert", "domain": "ibm", "privacy": "d'arienzo"},
    {"name": "sarah", "domain": "lyft", "privacy": "farkas"},
    {"name": "sevi", "domain": "bofa", "privacy": "vaz"},
    {"name": "jordan", "domain": "epic", "privacy": "pruitt"},
    {"name": "marian-eugene", "domain": "froedtert", "privacy": "pruitt"}
]

MESSAGES_DATA_STORE: List[EmailMessageSchema] = []
SYSTEM_TRACKING_ID = 1

def verify_system_address(address: str) -> bool:
    try:
        if "@" not in address:
            return False
        parts = address.split("@")
        domain_part = parts[1].split("/")[0]
        return any(user["domain"] == domain_part for user in SYSTEM_DIRECTORY)
    except Exception:
        return False

@app.get("/api/mailboxes", response_model=List[MailboxSchema])
def fetch_active_mailboxes():
    compiled_catalog = []
    for user in SYSTEM_DIRECTORY:
        external_uri = f"{user['name']}@{user['domain']}"
        internal_uri = f"{user['name']}@{user['domain']}/#'privacy'"
        
        compiled_catalog.append(MailboxSchema(address=external_uri, routing_type="external")),
        compiled_catalog.append(MailboxSchema(address=internal_uri, routing_type="internal"))
    return compiled_catalog

# Using a query parameter format (?address=...) avoids 404 route errors caused by special characters like '#'
@app.get("/api/messages/inbox")
def read_inbox_data(address: str):
    return [msg for msg in MESSAGES_DATA_STORE if msg.recipient.strip().lower() == address.strip().lower()]

@app.post("/api/messages/compose", response_model=EmailMessageSchema, status_code=status.HTTP_201_CREATED)
def transmit_message(payload: EmailMessageSchema):
    global SYSTEM_TRACKING_ID
    
    if not verify_system_address(payload.sender) or not verify_system_address(payload.recipient):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Routing not convinced: Unrecognized ecosystem domain identity."
        )

    payload.id = SYSTEM_TRACKING_ID
    MESSAGES_DATA_STORE.append(payload)
    SYSTEM_TRACKING_ID += 1
    return payload

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7999)