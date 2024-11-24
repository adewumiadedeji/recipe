Setting Up Your Environment

First, create a virtual environment and install FastAPI and Uvicorn:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt


To further secure your API, use HTTPS for all communications and configure CORS (Cross-Origin Resource Sharing) properly.
Enabling HTTPS

To enable HTTPS, you need a certificate. You can generate a self-signed certificate for testing purposes or use a service like Let’s Encrypt for a free, trusted certificate.

Use Uvicorn with SSL
uvicorn services.users.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile=path/to/key.pem --ssl-certfile=path/to/cert.pem