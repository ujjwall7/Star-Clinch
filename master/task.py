from celery import shared_task
from . models import *
from django.core.mail import EmailMessage, send_mail
import io
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

import os


@shared_task
def resize_and_convert_to_webp(image_path, recipe_id):
    try:
        from master.models import Recipe

        # Check recipe instance
        recipe = Recipe.objects.filter(id=recipe_id).last()
        if not recipe:
            print("⚠️ Recipe not found")
            return None

        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"⚠️ Image file does not exist: {image_path}")
            return None

        # Open and convert image
        img = Image.open(image_path)
        img = img.convert("RGB")  
        img = img.resize((800, 800))  

        # WebP file path
        webp_filename = os.path.splitext(os.path.basename(image_path))[0] + ".webp"
        webp_path = os.path.join(settings.MEDIA_ROOT, "recipes", webp_filename)

        # Save as WebP
        img.save(webp_path, "webp", quality=80)

        # Delete old image
        if os.path.exists(image_path):
            os.remove(image_path)

        # Update recipe image path
        recipe.image.name = f"recipes/{webp_filename}"  
        recipe.save(update_fields=["image"])

        print(f"✅ Image converted and saved: {webp_path}")
        return webp_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    




