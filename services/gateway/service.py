
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Header
import requests

async def get_authorization_header(authorization: str = Header(...)):
    print("Authorization: ", authorization)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    return token

async def processRequest(
    url: str, 
    method: str, 
    token:  Optional[str]=None, 
    data: Optional[Dict[str, Any]] = None
) -> Any:
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Determine the request method dynamically
        response = requests.request(method=method.upper(), url=url, headers=headers, json=data)
        
        # Check the response status
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except requests.exceptions.ConnectionError as e:
        print("Exception: ", e)
        raise HTTPException(status_code=503, detail="Service is unavailable")