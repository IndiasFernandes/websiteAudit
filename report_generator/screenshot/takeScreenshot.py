from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

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

    path = '../../media/' + get_domain_from_url(url) + '.png'

    # Save the screenshot
    driver.save_screenshot(path)

    # Close the browser
    driver.quit()

take_screenshot('https://duckduckgo.com')



