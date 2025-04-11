import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import UploadImageSerializer
from .mongo_models import UploadedImage

class UploadMultipleImagesView(APIView):
    def post(self, request):
        images = request.FILES.getlist('images')

        if not images:
            return Response({"error": "No images uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded = []

        for image in images:
            serializer = UploadImageSerializer(data={'image': image})
            
            if serializer.is_valid():
                # Generate a unique filename
                ext = os.path.splitext(image.name)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                save_path = os.path.join(settings.MEDIA_ROOT, 'originals', filename)

                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # Save the file
                with open(save_path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

                # Save path to MongoDB
                UploadedImage(image_path=f'originals/{filename}').save()

                uploaded.append({'filename': filename})
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Images uploaded successfully.",
            "uploaded": uploaded
        }, status=status.HTTP_201_CREATED)
