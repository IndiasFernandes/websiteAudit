# from rest_framework import serializers
# from .models import FormResponse
#
#
# # Serializers define the API representation, this is important to define how the data will be displayed in the API.
# # TODO: Define your serializers here
#
# class FormResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FormResponse
#         fields = '__all__'

from rest_framework import serializers
from report_generator.models import WebsiteReport

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteReport
        fields = '__all__'