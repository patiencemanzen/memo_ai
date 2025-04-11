from mongoengine import Document, StringField, DateTimeField
import datetime

class UploadedImage(Document):
    image_path = StringField(required=True)
    uploaded_at = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'uploaded_images'}

    def __str__(self):
        return str(self.image)
