from PIL import Image
from django.core.files.base import ContentFile
import io
import os

class RescaleImageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_field_name = kwargs.get('image_field_name', 'image')
        self.max_width = kwargs.get('max_width', 1680)
        self.max_size = kwargs.get('max_size', 500000)

    def save(self, *args, **kwargs):
        image_field = getattr(self, self.image_field_name)

        if image_field:
            img = Image.open(image_field)
            if img.mode != 'RGB' :
                img = img.convert('RGB')
            output = io.BytesIO()
            # Resize the image to a maximum width of max_width pixels
            if img.width > self.max_width:
                ratio = self.max_width / float(img.width)
                height = round(ratio * float(img.height))
                img = img.resize((self.max_width, height), Image.ANTIALIAS)
                img.save(output, format='JPEG', quality=75)

            # Check if image size is more than max_size
            elif image_field.size > self.max_size:
                quality_ratio = round(self.max_size / image_field.size * 100)
                img.save(output, format='JPEG', quality=quality_ratio)
            else:
                img.save(output , format('JPEG') , quality = 95)

            output.seek(0)
            image_name , ext = os.path.splitext(image_field.name)
            setattr(
                self,
                self.image_field_name,
                ContentFile(output.read(), name=image_name+'.jpg')
            )
        super().save(*args, **kwargs)