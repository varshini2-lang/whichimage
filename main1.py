from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import os
import base64
from typing import List

app1 = FastAPI()

# Set up CORS
app1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    category: str
    images: List[UploadFile]

    @validator("images")
    def validate_images(cls, value):
        allowed_formats = ['jpeg', 'png', 'gif']
        allowed_size_mb = 5  # Adjust as needed

        for image in value:
            if image.content_type.lower() not in ['image/jpeg', 'image/png', 'image/gif']:
                raise ValueError(f"Unsupported image format. Supported formats: JPEG, PNG, GIF")

            if image.file:
                file_size_mb = len(image.file.read()) / (1024 * 1024)
                image.file.seek(0)  # Reset file pointer

                if file_size_mb > allowed_size_mb:
                    raise ValueError(f"Image size exceeds the allowed limit of {allowed_size_mb} MB")

        return value

def save_uploaded_images(category: str, images: List[UploadFile]):
    upload_directory = f"uploaded_images/{category}"
    os.makedirs(upload_directory, exist_ok=True)

    saved_image_paths = []

    for image in images:
        file_path = os.path.join(upload_directory, image.filename)
        with open(file_path, "wb") as file:
            file.write(image.file.read())
            saved_image_paths.append(file_path)

    return saved_image_paths

def get_images_by_category(category: str):
    image_directory = f"uploaded_images/{category}"

    images = []

    for file_name in os.listdir(image_directory):
        file_path = os.path.join(image_directory, file_name)
        with open(file_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("utf-8")
            images.append({"name": file_name, "data": image_data})

    return images

@app1.post("/uploadfiles/")
async def create_upload_files(item: Item = Depends()):
    category = item.category

    try:
        saved_image_paths = save_uploaded_images(category, item.images)
        confirmation_messages = [f"Image '{os.path.basename(path)}' uploaded to '{category}' category." for path in saved_image_paths]

        return JSONResponse(content={"confirmation_messages": confirmation_messages}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app1.get("/get_images/{category}")
async def get_images(category: str):
    try:
        images = get_images_by_category(category)
        return {"category": category, "images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
