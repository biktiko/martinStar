import io
import uuid
from PIL import Image
from django.core.files.base import ContentFile

def optimize_image(image_file, max_size=(1920, 1920), quality=85):
    """
    Optimizes an image by resizing and converting to WebP format.
    """
    img = Image.open(image_file)
    
    # Convert to RGB if necessary (e.g. RGBA to RGB for WebP, though WebP supports alpha)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGBA')

    # Resize while maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=quality)
    output.seek(0)
    
    # Generate new safe filename using UUID to avoid Cyrillic/Unicode issues with S3
    new_name = f"{uuid.uuid4().hex}.webp"
    
    return ContentFile(output.read(), name=new_name)
