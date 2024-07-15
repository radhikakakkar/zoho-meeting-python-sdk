import os
from dotenv import load_dotenv

load_dotenv()

# MONGODB_URI = os.getenv("MONGODB_URI")
# if not MONGODB_URI:
#     raise ValueError("No MONGO_URI set")

ZOHO_CLIENT_ID = os.getenv("zoho_client_id")
ZOHO_CLIENT_SECRET = os.getenv("zoho_client_secret")
REDIRECT_URI = os.getenv("redirect_uri")
AUTH_GRANT = os.getenv("auth_grant")
