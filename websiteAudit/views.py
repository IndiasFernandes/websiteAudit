from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import os
from api.forms import ContactForm
from utils.generate_pdf import generate_pdf
from utils.web_scrapper import fetch_website_html
from utils.take_screenshot import take_screenshot
from websiteAudit import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib
from django.views.decorators.clickjacking import xframe_options_exempt
import logging

logging.basicConfig(level=logging.INFO)

def display_stdout(request):
    log_file_path = os.path.join(settings.LOG_DIR, 'stdout.log')
    with open(log_file_path, 'r') as log_file:
        stdout_content = log_file.read()

    return render(request, 'stdout_display.html', {'stdout_content': stdout_content})

def form_view(request):
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         # Process the data in form.cleaned_data
    #         # For example, send an email or save the data to a database
    #         return redirect('success_url')  # Redirect to a new URL
    # else:
    form = ContactForm()  # An unbound form

    return render(request, 'form.html', {'form': form})


# For the screenshot functionality
def take_screenshot_view(request):
    if 'url' in request.GET:
        url = request.GET['url']
        screenshot_url = take_screenshot(url)
        return JsonResponse({'screenshotUrl': screenshot_url})
    return render(request, 'screenshot.html')


# For the web scraping functionality
def web_scraper_view(request):
    if 'url' in request.GET:
        url = request.GET['url']
        content = fetch_website_html(url)  # Adjust to your actual function
        return HttpResponse(content, content_type='text/html')
    return render(request, 'web_scrapper.html')


def clear_stdout(request):
    log_file_path = os.path.join(settings.LOG_DIR, 'stdout.log')
    with open(log_file_path, 'w') as log_file:
        log_file.truncate()
    return HttpResponseRedirect(reverse('display_stdout'))  # Redirect back to the stdout display page


@xframe_options_exempt
def generate_pdf_view(request):

    if 'url' in request.GET:

        url = request.GET['url']

        print("Generating PDF view for URL: ", url)
        logging.info("Generating PDF view for URL: " + url)

        # Generate a hash of the URL to use as a filename
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = f"{url_hash}.pdf"
        pdf_path = os.path.join('media', filename)

        # Check if the PDF already exists
        if not os.path.exists(pdf_path):
            content = fetch_website_html(url)  # Ensure this function properly handles errors

            # Generate PDF only if it doesn't exist
            pdf_status = generate_pdf(filename)  # Ensure this function takes filename and content

            if not pdf_status:  # Handle PDF generation failure
                return JsonResponse({'error': 'Failed to generate PDF'}, status=500)

        # At this point, the PDF exists either from before or newly generated
        try:
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{filename}"'
                return response
        except IOError:
            return JsonResponse({'error': 'PDF file not found'}, status=404)

    # Fallback in case the URL is not provided
    return render(request, 'pdf_creator.html')

def homepage_view(request):
    return render(request, 'home.html')