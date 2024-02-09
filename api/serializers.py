from rest_framework import serializers
from .models import WebsiteReport

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteReport
        fields = '__all__'