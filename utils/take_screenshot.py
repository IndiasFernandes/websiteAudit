from urllib.parse import urlparse
import os
import logging
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


logger = logging.getLogger(__name__)


 
# Function to get the domain from a URL
def get_domain_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

# Function to take a mobile screenshot of a webpage
def take_screenshot(url):
    logger.error('Taking mobile screenshot of ' + url)

    # Configure mobile emulation
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 612, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }
    

    


    # Specify the path to chromedriver.exe (manually download and specify the correct path)
    chrome_driver_path = os.path.join(settings.BASE_DIR, 'utils', 'chromedriver')
    service = Service(executable_path=chrome_driver_path)
    chrome_options = webdriver.ChromeOptions()
    # Chrome options including mobile emulation and headless mode
    
    #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--headless')  # Run headless Chrome


    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Construct the file path using MEDIA_ROOT
        filename = get_domain_from_url(url) + '.png'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        # Take a screenshot and save it
        driver.get_screenshot_as_file(filepath)
        logger.error(f'Saving mobile screenshot as {filepath}')
        return os.path.join(settings.MEDIA_URL, filename)
    except Exception as e:
        logger.error(f'Failed to capture mobile screenshot for {url}. Error: {e}')
        return None
    finally:
        # Clean up: close the browser
        driver.quit()

 # done
