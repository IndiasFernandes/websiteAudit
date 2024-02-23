from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils import web_scrapper
from .forms import ContactForm
from .models import WebsiteReport
from .bot_analysis import analyze_website
from .serializers import ItemSerializer
from rest_framework import status
import logging
from django.http import HttpResponse
from utils import take_screenshot

from utils.web_scrapper import fetch_website_html

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_reports(request):

    logger.info("Starting GET request to fetch all website reports.")
    print("Starting GET request to fetch all website reports.")
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    logger.info(f"Successfully fetched {len(items)} items from the database.")
    print(f"Successfully fetched {len(items)} items from the database.")
    return Response(serializer.data)


@api_view(['POST'])
def add_report(request):

    logger.info("Starting POST request to add a new website report.")
    print("Starting POST request to add a new website report.")
    serializer = ItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        logger.info("New website report saved successfully.")
        print("New website report saved successfully.")

        # Fetch the saved object
        saved_item = WebsiteReport.objects.get(pk=serializer.instance.pk)
        logger.debug(f"Retrieved saved website report with PK: {serializer.instance.pk}")
        print(f"Retrieved saved website report with PK: {serializer.instance.pk}")


        # Take a screenshot of the website - in Models TODO: Put it in a separate function

        # Constructing new image URL dynamically based on the request
        if saved_item.screenshot:
            parts = request.build_absolute_uri(saved_item.screenshot.url).split('/media/', 1)
            if len(parts) > 1:
                new_url = request.build_absolute_uri('/media/') + parts[1]
            else:
                new_url = request.build_absolute_uri(saved_item.screenshot.url)
        else:
            new_url = None

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

            'overall_grade': analysis_results['overall_grade'],

            'cta_button_placement': analysis_results['cta_button_placement'],
            'cta_clarity': analysis_results['cta_clarity'],
            'headline_focus': analysis_results['headline_focus'],
            'messaging_clarity': analysis_results['messaging_clarity'],
            'form_diagnostics': analysis_results['form_diagnostics'],

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


def home(request):
    logger.info("Rendering form template.")
    print("Rendering form template.")
    return render(request, 'home.html')



def screenshot_view(request):
    url = request.GET.get('url')  # Get URL from request
    if url:
        message = take_screenshot(url)
        return HttpResponse(f'Screenshot taken: {message}')
    else:
        return HttpResponse('No URL provided', status=400)

def web_scraper_view(request):
    url = request.GET.get('url')  # Get URL from request
    if url:
        cleaned_html = fetch_website_html(url)
        return HttpResponse(cleaned_html, content_type='text/html')
    else:
        return HttpResponse('No URL provided', status=400)