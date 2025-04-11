from rest_framework import serializers

class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        max_size = 2 * 1024 * 1024  # 2MB

        if value.size > max_size:
            raise serializers.ValidationError("Image must be less than 2MB.")
        
        return value
