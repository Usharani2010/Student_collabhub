import cloudinary, os
import cloudinary.uploader 



# Configure credentials directly here (not recommended for production)
cloudinary.config(
    cloud_name="digbw7wxi",
    api_key="732136532161337",
    api_secret="pcj-E3zXggc9bgnAReMRYVlQLxA"
)


# function to upload file to cloudinary
def upload_file_to_cloudinary(file_obj):
    try:
        # Check credentials before upload
        if not all([
            cloudinary.config().cloud_name,
            cloudinary.config().api_key,
            cloudinary.config().api_secret
        ]):
            print("Cloudinary credentials are not set correctly.")
            return None
        response = cloudinary.uploader.upload(file_obj, folder="student_collabhub/posts")
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None