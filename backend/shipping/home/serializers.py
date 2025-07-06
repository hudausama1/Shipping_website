from rest_framework import serializers
from .models import Plan, Testimonial, CompanyInfo, ContactMessage


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'feedback', 'company', 'rating', 'created_at']
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True},
            'user': {'write_only': True},
            'created_at': {'read_only': True},
        }

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']