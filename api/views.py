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
            'Date': saved_item.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as needed

            'First Name': saved_item.first_name,
            'Last Name': saved_item.last_name,
            'Url': saved_item.url,
            'E-mail': saved_item.email,

            'Company Name': saved_item.name_company,
            'Industry': saved_item.industry,
            'Product/Service': saved_item.service,

            'Overall Rating': saved_item.overall_rating,
            'CTA Button Placement Rating': saved_item.cta_button_placement_rating,
            'CTA Clarity Rating': saved_item.cta_clarity_rating,
            'Form Simplicity Rating': saved_item.form_simplicity_rating,
            'Form Autofill Rating': saved_item.form_autofill_rating,
            'Messaging Clarity Rating': saved_item.messaging_clarity_rating,
            'Headline Focus Rating': saved_item.headline_focus_rating,

            'CTA Button Placement Diagnostics': saved_item.cta_button_placement_diagnostics,
            'CTA Clarity Diagnostics': saved_item.cta_clarity_diagnostics,
            'Form Simplicity Diagnostics': saved_item.form_simplicity_diagnostics,
            'Form Autofill Diagnostics': saved_item.form_autofill_diagnostics,
            'Messaging Clarity Diagnostics': saved_item.messaging_clarity_diagnostics,
            'Headline Focus Diagnostics': saved_item.headline_focus_diagnostics,

            'Social Proof': saved_item.social_proof,
            'Company Info Presence': saved_item.company_info_presence,

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
