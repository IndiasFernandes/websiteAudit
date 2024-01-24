from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import os
from django.conf import settings

# Function to get the domain from a URL
def get_domain_from_url(url):
    # Parse the URL to extract the domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove 'www.' if it exists in the domain
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove the first 4 characters 'www.'

    return domain

# Function to take a screenshot of a web page
def take_screenshot(url):
    print('Taking screenshot of ' + url)
    # Set up headless Chrome options
    options = Options()
    options.headless = True
    options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-gpu")  # Applicable to windows os only

    # Initialize the driver
    driver = webdriver.Chrome(options=options)

    # Load the page
    driver.get(url)

    # Construct the file path using MEDIA_ROOT
    filename = get_domain_from_url(url) + '.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    print('Saving screenshot as ' + filepath + '\n')

    # Save the screenshot
    driver.save_screenshot(filepath)

    # Close the browser
    driver.quit()
