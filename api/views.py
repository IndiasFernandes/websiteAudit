from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import WebsiteReport
from .bot_analysis import analyze_website
from .serializers import ItemSerializer
from rest_framework import status
import logging

from .web_scrapper import fetch_website_html

logger = logging.getLogger(__name__)


@api_view(['GET'])
def getData(request):
    logger.info("Starting GET request to fetch all website reports.")
    print("Starting GET request to fetch all website reports.")
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    logger.info(f"Successfully fetched {len(items)} items from the database.")
    print(f"Successfully fetched {len(items)} items from the database.")
    return Response(serializer.data)


@api_view(['POST'])
def addItem(request):
    print(request.data)
    logger.info(request.data)
    logger.info("Received POST request to add a new website report.")
    print("Received POST request to add a new website report.")
    serializer = ItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        logger.info("New website report saved successfully.")
        print("New website report saved successfully.")

        # Fetch the saved object
        saved_item = WebsiteReport.objects.get(pk=serializer.instance.pk)
        logger.debug(f"Retrieved saved website report with PK: {serializer.instance.pk}")
        print(f"Retrieved saved website report with PK: {serializer.instance.pk}")

        # Constructing new image URL
        parts = request.build_absolute_uri(saved_item.screenshot.url).split('/media/', 1)
        new_url = f"http://www.innerflect.com/websiteAudit/media/{parts[1]}"
        logger.debug(f"Constructed new image URL: {new_url}")
        print(f"Constructed new image URL: {new_url}")

        # Fetch HTML content for analysis
        logger.info(f"Fetching HTML content for URL: {saved_item.url}")
        print(f"Fetching HTML content for URL: {saved_item.url}")
        html_content = fetch_website_html(saved_item.url)
        logger.debug("HTML content fetched successfully:\n\n{html_content}\n\n")
        print(f"HTML content fetched successfully:\n\n{html_content}\n\n")

        # Analyzing website
        logger.info("Analyzing website HTML content.")
        print("Analyzing website HTML content.")
        analysis_results = {}
        analysis_results = analyze_website(html_content)
        logger.info(f"Website analysis completed. Results: {analysis_results}")
        print(f"Website analysis completed. Results: {analysis_results}")

        # Constructing response data
        response_data = {
            'image_url': new_url,  # Assuming new_url is defined elsewhere
            'Date': saved_item.date.strftime('%Y-%m-%d %H:%M:%S'),

            'First Name': saved_item.first_name,
            'Last Name': saved_item.last_name,
            'Url': saved_item.url,
            'E-mail': saved_item.email,

            'Company Name': saved_item.name_company,

            'overall_rating': analysis_results['overall_rating'],

            'cta_button_placement_diagnostics': analysis_results['cta_button_placement_diagnostics'],  # Placeholder for actual diagnostics
            'cta_clarity_diagnostics': analysis_results['cta_clarity_diagnostics'],
            'form_simplicity_diagnostics': analysis_results['form_simplicity_diagnostics'],
            'messaging_clarity_diagnostics': analysis_results['messaging_clarity_diagnostics'],
            'headline_focus_diagnostics': analysis_results['headline_focus_diagnostics'],
            'offer_transparency_diagnostics': analysis_results['offer_transparency_diagnostics'],


            'Social Proof': None,
            'Company Info Presence': None,

            # Add any other fields you want to include
            'other_field': 'other_value',
        }

        logger.info(f"Constructed response data successfully: {response_data}")
        print(f"Constructed response data successfully: {response_data}")
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        logger.warning("Validation failed for website report POST request.")
        print("Validation failed for website report POST request.")
        logger.debug(f"Serializer errors: {serializer.errors}")
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def form(request):
    logger.info("Rendering form template.")
    print("Rendering form template.")
    return render(request, 'test.html')