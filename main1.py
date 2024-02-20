from typing import List, Optional
from ciaos import get, save
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import base64

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
origins = ["*"]  # Change this to the appropriate origin(s) of your React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/uploadfiles/")
async def update_file(category: Optional[str] = Form(None), image: List[str] = Form(...)):
    try:
        save("https://storage.cialabs.tech",category,image)
        return JSONResponse(content={"message": f"Image saved locally at: {category}"}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)


    
@app.get("/get_images/{category}")
async def get_images(category: str):
  try:
      images=get("https://storage.cialabs.tech",category)
      return images
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
