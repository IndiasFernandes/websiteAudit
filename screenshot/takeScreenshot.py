from urllib.parse import urlparse
import urllib.parse

from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

# Function to get the domain from a URL
def get_domain_from_url(url):
    # Parse the URL to extract the domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove 'www.' if it exists in the domain
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove the first 4 characters 'www.'

    return domain

# Function to take a screenshot of a web page using Thumb.io
def take_screenshot(url):
    logger.error('Taking screenshot of ' + url)

    # Your Thumb.io API key
    api_key = '70136-screenshot'

    # URL-encode the website URL
    encoded_url = urllib.parse.quote_plus(url)

    # Construct the Thumb.io URL
    thumb_io_url = f'https://image.thum.io/get/auth/{api_key}/' + url;

    # Construct the file path using MEDIA_ROOT
    filename = get_domain_from_url(url) + '.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # Use Thumb.io URL to save the screenshot - here you might download the image and save it locally
    # For example, using requests (ensure you have 'requests' installed: pip install requests)
    import requests
    response = requests.get(thumb_io_url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        logger.error(f'Saving screenshot as {filepath}')
    else:
        logger.error(f'Failed to capture screenshot for {url}. Status code: {response.status_code}')

    # Note: In production, consider handling exceptions and errors more gracefully
