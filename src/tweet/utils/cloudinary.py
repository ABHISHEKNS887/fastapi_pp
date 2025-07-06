from fastapi import UploadFile, HTTPException, File, status
import cloudinary.uploader
import os


import cloudinary
import cloudinary.uploader

# Configuration       
cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"), 
    api_key = os.getenv("API_KEY"), 
    api_secret = os.getenv("API_SECRET"), 
    secure=True
)

async def upload_to_cloudinary(image_url: UploadFile = File(...)):
    try:
        # Check file size (5MB max)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        contents = await image_url.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 5MB limit"
            )
        
        # Reset file pointer after reading
        await image_url.seek(0)
        
        # Check file type (image)
        content_type = image_url.content_type
        if not content_type or not content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only image files are allowed"
            )
        
        # Upload the file to Cloudinary
        response = cloudinary.uploader.upload(image_url.file, resource_type="auto")
        return response['secure_url']  # Return the secure URL of the uploaded file
    
    except HTTPException:
        # Re-raise the HTTP exceptions we created
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file to Cloudinary: {str(e)}"
        )