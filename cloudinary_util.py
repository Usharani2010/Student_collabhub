import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load .env file (only required locally, not on Render)
load_dotenv()

# Read credentials from environment
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Upload function
def upload_file_to_cloudinary(file_obj):
    try:
        # Optional: print current config for debugging
        config = cloudinary.config()
        if not all([config.cloud_name, config.api_key, config.api_secret]):
            print("Cloudinary credentials are not set correctly.")
            return None

        response = cloudinary.uploader.upload(
            file_obj,
            folder="student_collabhub/posts",
            resource_type="auto"  # handles images, pdfs, etc.
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None
