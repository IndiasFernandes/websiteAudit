import logging
from urllib.parse import urljoin

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from screenshot.takeScreenshot import take_screenshot
from utils.generate_pdf.generate_pdf import generate_pdf
from utils.mailjet import create_and_update_contact
from .bot_analysis import analyze_website
from .models import WebsiteReport
from .serializers import ItemSerializer

from utils.web_scrapper import fetch_website_html
logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_reports(request):
    """Fetch and return all website reports."""
    logger.info("Fetching all website reports.")
    print("Fetching all website reports.")
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    logger.info(f"Successfully fetched {len(items)} items.")
    print(f"Successfully fetched {len(items)} items.")
    return Response(serializer.data)


@api_view(['POST'])
def add_report(request):
    """Add and process a new website report based on provided analysis metrics."""

    logger.info("Adding a new website report.")
    print("Adding a new website report.")

    serializer = ItemSerializer(data=request.data)

    if serializer.is_valid():
        saved_item = serializer.save()
        logger.info("New website report saved successfully.")
        print("New website report saved successfully.")
        process_report(saved_item, request)
        return Response({"message": "Report processed successfully"}, status=status.HTTP_201_CREATED)
    else:
        log_and_return_validation_errors(serializer)

def process_report(saved_item, request):
    """Process the website report by performing analysis, taking a screenshot, and generating a PDF report."""
    analysis_results, analysis_results_summary = analyze_website_content(saved_item, request)
    screenshot_url = save_website_screenshot(saved_item, request)  # Take a screenshot and get the new URL
    response_data = generate_response_data(saved_item, analysis_results, screenshot_url, request)
    generate_pdf_report(saved_item, response_data, request)
    send_report(analysis_results_summary)
    logger.info("Report processing completed.")



def analyze_website_content(saved_item, request):
    """Analyze the website content and return analysis results."""
    # This is a placeholder for the actual analysis logic.
    logger.info(f"Analyzing website: {saved_item.url}")
    print(f"Analyzing website: {saved_item.url}")
    html_content = fetch_website_html(saved_item.url)
    analysis_results = analyze_website(html_content)
    logger.info("Website analysis completed.")
    print("Website analysis completed.")
    return analysis_results


def generate_response_data(saved_item, analysis_results, screenshot_url, request):
    """Generate the response data structure based on analysis results."""

    report_url = urljoin(request.build_absolute_uri(), saved_item.pdf.url) if saved_item.pdf else None

    # Adapt this function to construct the response data structure as needed.
    response_data = {
        'image_url': screenshot_url,  # Assuming new_url is defined elsewhere
        'Date': saved_item.date.strftime('%Y-%m-%d %H:%M:%S'),

        'First Name': saved_item.first_name,
        'Last Name': saved_item.last_name,
        'Url': saved_item.url,
        'E-mail': saved_item.email,

        'Company Name': saved_item.name_company,

        'report_url': report_url,

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
    logger.info("Response data generated.")
    print("Response data generated.")
    return response_data


def generate_pdf_report(saved_item, response_data, request):
    """Generate a PDF report for the analyzed website and associate it with the saved_item."""
    logger.info("Generating PDF report.")
    print("Generating PDF report.")
    # Assuming generate_pdf returns a path to the saved PDF

    body_data = [
        {'title': 'CTA Button Placement', 'body': response_data['cta_button_placement']},
        {'title': 'CTA Clarity', 'body': response_data['cta_clarity']},
        {'title': 'Headline Focus', 'body': response_data['headline_focus']},
        {'title': 'Messaging Clarity', 'body': response_data['messaging_clarity']},
        {'title': 'Form Diagnostics', 'body': response_data['form_diagnostics']},
    ]

    url = saved_item.url
    company_name = saved_item.name_company
    first_name = saved_item.first_name
    last_name = saved_item.last_name
    e_mail = saved_item.email
    overall_grade = response_data['overall_grade']
    image_path = response_data['report_url']

    # Ensure generate_pdf actually saves the PDF to a location that Django's FileField can access
    pdf_path = generate_pdf(body_data, url, company_name, first_name, last_name, e_mail, overall_grade, image_path)  # Adjust this call according to your PDF generation logic

    # After generating the PDF, associate it with the saved_item and save the item
    if pdf_path:
        # Assuming saved_item has a FileField named 'pdf' for storing the PDF path
        saved_item.pdf.name = pdf_path  # Assign the PDF path to the model
        saved_item.save()
        logger.info("PDF report generated and associated with the report item.")
        print("PDF report generated and associated with the report item.")
    else:
        logger.error("Failed to generate PDF report.")
        print("Failed to generate PDF report.")


def send_report(analysis_results_summary):
    """Send the report to the designated recipient."""
    # This function handles the logic to send the report, e.g., via email.
    logger.info("Sending report.")
    create_and_update_contact(analysis_results_summary)  # Placeholder function call


def log_and_return_validation_errors(serializer):
    """Log validation errors and return an appropriate response."""
    logger.error("Validation failed for the new website report.")
    print(f"Validation errors: {serializer.errors}")
    logger.debug(f"Validation errors: {serializer.errors}")
    print("Validation failed.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The views below remain unchanged
def home(request):
    return render(request, 'home.html')


def screenshot_view(request):
    url = request.GET.get('url')
    if url:
        message = take_screenshot(url)
        print(f'Screenshot taken: {message}')
        return HttpResponse(f'Screenshot taken: {message}')
    else:
        print('No URL provided')
        return HttpResponse('No URL provided', status=400)


def web_scraper_view(request):
    url = request.GET.get('url')
    if url:
        cleaned_html = fetch_website_html(url)
        return HttpResponse(cleaned_html, content_type='text/html')
    else:
        return HttpResponse('No URL provided', status=400)


def save_website_screenshot(saved_item, request):
    """Take a screenshot of the website and return the new URL for the screenshot."""
    logger.info(f"Taking screenshot for: {saved_item.url}")
    print(f"Taking screenshot for: {saved_item.url}")
    # Assume take_screenshot returns the path to the saved screenshot relative to the media root
    screenshot_path = str(take_screenshot(saved_item.url))

    # Construct the new URL for the screenshot
    new_url = request.build_absolute_uri('/media/') + screenshot_path[-6:0]
    print(request.build_absolute_uri('/media/'))
    print(screenshot_path[-6:0])

    logger.info(f"Screenshot taken and accessible at: {new_url}")
    print(f"Screenshot taken and accessible at: {new_url}")

    # Update the saved_item with the new screenshot URL
    saved_item.screenshot = screenshot_path  # Assuming the model has a field for storing the screenshot path
    saved_item.save()

    return new_url