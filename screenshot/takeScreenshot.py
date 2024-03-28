from urllib.parse import urlparse
import os
import logging
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Configure logging
logger = logging.getLogger(__name__)

def get_domain_from_url(url):
    """
    Extracts the domain from a given URL.

    Args:
        url (str): The URL from which to extract the domain.

    Returns:
        str: The extracted domain.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove 'www.' if present to get a clean domain
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def take_screenshot(url):
    """
    Takes a mobile screenshot of a webpage.

    Args:
        url (str): The URL of the webpage to capture.

    Returns:
        str: The path to the saved screenshot relative to MEDIA_URL, or None if an error occurs.
    """
    print('Taking mobile screenshot of ' + url)
    logger.info('Taking mobile screenshot of ' + url)

    # Configuration for mobile emulation to mimic an iPhone X
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 712, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    # Path to chromedriver (ensure you've downloaded chromedriver and it matches your Chrome version)
    chrome_driver_path = os.path.join(settings.BASE_DIR, 'utils', 'chromedriver')
    service = Service(executable_path=chrome_driver_path)
    chrome_options = webdriver.ChromeOptions()

    # Enable mobile emulation and headless mode for Chrome
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Open the URL

        # Construct the file path for saving the screenshot
        filename = get_domain_from_url(url) + '.png'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        driver.get_screenshot_as_file(filepath)  # Save the screenshot
        logger.info(f'Saving mobile screenshot as {filepath}')
        print(f'Saving mobile screenshot as {filepath}')

        # Return the relative path to the screenshot
        return os.path.join(settings.MEDIA_URL, filename)
    except Exception as e:
        logger.error(f'Failed to capture mobile screenshot for {url}. Error: {e}')
        print(f'Failed to capture mobile screenshot for {url}. Error: {e}')
        return None
    finally:
        driver.quit()  # Clean up by closing the browser

