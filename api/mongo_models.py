from mongoengine import Document, StringField, DateTimeField
import datetime

class UploadedImage(Document):
    original_image_path = StringField(required=True)
    processed_image_path = StringField(null=True)
    orchestration_plan = StringField(null=True)
    orchestration_log = StringField(null=True)
    uploaded_at = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'uploaded_images'}

    def __str__(self):
        return (f"Original: {self.original_image_path}, "
                f"Processed: {self.processed_image_path}, "
                f"Plan: {self.orchestration_plan}, "
                f"Log: {self.orchestration_log}")
