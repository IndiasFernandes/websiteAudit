from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from report_generator.models import WebsiteReport
from screenshot.takeScreenshot import take_screenshot, get_domain_from_url
from .serializers import ItemSerializer
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

# View para obter dados usando o Django Rest Framework
@api_view(['GET'])
def getData(request):
    print('olala')
    logger.error('olala')
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)





@api_view(['POST'])
def addItem(request):
    print(request.data)
    logger.error(request.data)
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()





        # Fetch the saved object
        saved_item = WebsiteReport.objects.get(pk=serializer.instance.pk)

        # Serialize the saved object to include the image URL
        saved_item_serializer = ItemSerializer(saved_item)

        # Add the image URL to the serialized data
        saved_item_data = saved_item_serializer.data

        saved_item_data['image_url'] = request.build_absolute_uri(saved_item.screenshot.url)
        parts = saved_item_data['image_url'].split('/media/', 1)
        new_url = f"http://www.innerflect.com/websiteAudit/media/{parts[1]}"

        # Construct the JSON response
        response_data = {
            'image_url': new_url,
            'url': saved_item.url,
            'first_name': saved_item.first_name,
            'last_name': saved_item.last_name,
            'email': saved_item.email,
            'date': saved_item.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as needed
            'overall_rating': saved_item.overall_rating,
            'cta_button_placement_rating': saved_item.cta_button_placement_rating,
            'cta_clarity_rating': saved_item.cta_clarity_rating,
            'form_simplicity_rating': saved_item.form_simplicity_rating,
            'form_autofill_rating': saved_item.form_autofill_rating,
            'messaging_clarity_rating': saved_item.messaging_clarity_rating,
            'headline_focus_rating': saved_item.headline_focus_rating,
            'offer_transparency_rating': saved_item.offer_transparency_rating,
            'social_proof': saved_item.social_proof,
            'company_info_presence': saved_item.company_info_presence,
            'other_field': 'other_value',  # Add any other fields you want to include
        }

        print(response_data)
        logger.error(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        logger.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View baseada em função para renderizar um formulário
def form(request):
    return render(request, 'test.html')
