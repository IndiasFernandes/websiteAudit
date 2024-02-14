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


def generate_pdf_view(request):
    if 'url' in request.GET:
        url = request.GET['url']
        # Assume fetch_website_html(url) fetches and returns the desired text/content
        content = fetch_website_html(url)

        # Define a suitable filename, perhaps based on the URL or a timestamp
        filename = "your_filename"  # Define how you want to name your file

        # Call your PDF generation function (this part remains largely unchanged)
        generate_pdf(filename)  # Your existing function to generate the PDF

        # Define the full path to the PDF
        pdf_path = "./media/" + filename + ".pdf"

        # Open the PDF file in binary mode and return it in the response
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.pdf"'
            return response

    # Fallback in case the URL is not provided
    return render(request, 'pdf_creator.html')