
from rest_framework import serializers
from .models import Registration, AdoptionApplication
from rest_framework import serializers
from .models import Child

class RegisterSerializer(serializers.ModelSerializer):
    father_name = serializers.CharField(required=False, allow_blank=True)
    mother_name = serializers.CharField(required=False, allow_blank=True)
    father_email = serializers.EmailField(required=False, allow_blank=True)
    mother_email = serializers.EmailField(required=False, allow_blank=True)
    father_phone = serializers.CharField(required=False, allow_blank=True)
    mother_phone = serializers.CharField(required=False, allow_blank=True)
    father_age = serializers.IntegerField(required=False, allow_null=True)
    mother_age = serializers.IntegerField(required=False, allow_null=True)
    father_aadhar = serializers.CharField(required=False, allow_blank=True)
    mother_aadhar = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Registration
        fields = [
            'father_name', 'mother_name',
            'father_email', 'mother_email',
            'father_phone', 'mother_phone',
            'father_age', 'mother_age',
            'father_aadhar', 'mother_aadhar',
            'address', 'reason', 'document'
        ]
        
        read_only_fields = ("is_approved", "user_id", "password")

    def validate(self, data):
        father_name = data.get('father_name', '').strip()
        father_email = data.get('father_email', '').strip()
        father_phone = data.get('father_phone', '').strip()
        father_age = data.get('father_age')
        father_aadhar = data.get('father_aadhar', '').strip()
        mother_name = data.get('mother_name', '').strip()
        mother_email = data.get('mother_email', '').strip()
        mother_age = data.get('mother_age')
        mother_aadhar = data.get('mother_aadhar', '').strip()
        mother_phone = data.get('mother_phone', '').strip()

        father_details = [father_name, father_email, father_phone, father_age, father_aadhar]
        mother_details = [mother_name, mother_email, mother_phone, mother_age, mother_aadhar]

        if not all(father_details) and not all(mother_details):
            raise serializers.ValidationError("At least one parent's full details must be provided.")

        # Validate individual fields if one parent's details are partially filled
        if any(father_details) and not all(father_details):
            if not father_name or not father_email or not father_phone or not isinstance(father_age, int) or not father_aadhar:
                raise serializers.ValidationError("Please enter complete details")
            
        if any(mother_details) and not all(mother_details):
            if not mother_name or not mother_email or not mother_phone or not isinstance(mother_age, int) or not mother_aadhar:
                raise serializers.ValidationError("Please enter complete details")
        
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    """Used in Admin and APIs for listing/viewing registrations."""
    class Meta:
        model = Registration
        fields = "__all__"


class ChildSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url") and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class AdoptionApplicationSerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(source="child.name", read_only=True)

    class Meta:
        model = AdoptionApplication
        fields = "__all__"

    def validate(self, data):
        if not data.get("full_name") and not data.get("email"):
            raise serializers.ValidationError("Applicant must have at least a name or email.")
        return data