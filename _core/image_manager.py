"""This module provides the ImageManager class, which is responsible for uploading images to cloudinary."""
import cloudinary
import cloudinary.uploader
import cloudinary.api  # this must be imported for the code to work
from cloudinary.utils import cloudinary_url
import os
from dotenv import load_dotenv
load_dotenv()



class ImageManager:
    """This class is responsible for uploading images to cloudinary."""
    __cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    __api_key = os.getenv('CLOUDINARY_API_KEY')
    __api_secret = os.getenv('CLOUDINARY_API_SECRET')
    _url = os.getenv('CLOUDINARY_URL')
    base_folder = 'wullinp/products'
    image_url = None
    image_thumb_url = None
    image_public_id = None
    thumbnail_public_id = None
    def __init__(self, image, category, product_id):
        cloudinary.config(
            cloud_name=self.__cloud_name,
            api_key=self.__api_key,
            api_secret=self.__api_secret,
            secure=True
        )
        self.image = image
        self.category = category
        self.product_id = product_id
    
    def upload_image(self):
        """Uploads an image to cloudinary."""
        # Set the asset's public ID and allow overwriting the asset with new versions
        response = cloudinary.uploader.upload(self.image, public_id=self.product_id, folder=f'{self.base_folder}/{self.category}', overwrite=True, unique_filename=False)
        self.image_url = response['secure_url']
        self.image_public_id = response['public_id']

        self.create_thumbnail()
        return
    
    def create_thumbnail(self):
        """Creates a thumbnail for the uploaded image."""
        self.image.seek(0)  # Reset file pointer to the beginning
        response = cloudinary.uploader.upload(self.image, public_id=f'thumb_{self.product_id}', folder=f'{self.base_folder}/{self.category}/thumbnails', overwrite=True, unique_filename=False, width=200, height=200, crop='fill')
        self.image_thumb_url = response['secure_url']
        self.thumbnail_public_id = response['public_id']
        return
    
    def optimize_image(self):
        """Optimizes the uploaded image."""
        optimize_url, _ = cloudinary_url(self.image_public_id, fetch_format="auto", quality="auto")
        self.image_url = optimize_url
        return
    
    def transform_image(self, width, height):
        """Transforms the uploaded image."""
        transform_url, _ = cloudinary_url(self.image_public_id, width=width, height=height, crop="fill")
        self.image_url = transform_url
        return
    