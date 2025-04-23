import os
import uuid
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .serializers import UploadImageSerializer
from .mongo_models import UploadedImage

from orchestrator.agent import OrchestrationAgent
from orchestrator.controller import run_pipeline
from orchestrator.utils import generate_image_id, generate_metadata_from_image

logger = logging.getLogger(__name__)

class UploadMultipleImagesView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        images = request.FILES.getlist('images')

        if not images:
            return Response({"error": "No images uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded = []

        try: 
            for image in images:
                serializer = UploadImageSerializer(data={'image': image})

                if serializer.is_valid():
                    # --- Step 1: Save original image ---
                    ext = os.path.splitext(image.name)[1]
                    filename = f"{uuid.uuid4().hex}{ext}"
                    save_path = os.path.join(settings.MEDIA_ROOT, 'originals', filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    with open(save_path, 'wb+') as f:
                        for chunk in image.chunks():
                            f.write(chunk)

                    relative_path = f'originals/{filename}'

                    try:
                        # --- Step 2: Generate metadata ---
                        metadata = generate_metadata_from_image(save_path)

                        # --- Step 3: Orchestrator Agent generates plan ---
                        agent = OrchestrationAgent(image_preview_path=save_path, metadata=metadata)
                        plan = agent.analyze()

                        logger.info(f"Generated orchestration plan: {plan}")
                    except Exception as e:
                        return Response({"error": f"Failed to generate orchestration plan: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # --- Step 4: Run image pipeline based on plan ---
                    processed_path, log = run_pipeline(save_path, plan, generate_image_id())

                    # --- Step 5: Save results to MongoDB ---
                    UploadedImage(
                        original_image_path=relative_path,
                        processed_image_path=processed_path.replace(settings.MEDIA_ROOT, '').lstrip("/\\"),
                        orchestration_plan=str(plan),
                        orchestration_log=str(log),
                    ).save()

                    # --- Step 6: Prepare response ---
                    uploaded.append({
                        'original_image_path': filename,
                        'processed_image_path': processed_path.replace(settings.MEDIA_ROOT, '').lstrip("/\\"),
                        'orchestration_plan': plan,
                        'orchestration_log': log,
                    })
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Images processed successfully.",
                "uploaded": uploaded
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error processing images: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
