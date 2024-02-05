import requests

def fetch_website_html(url):
    """
    Fetches and returns the HTML content of the specified URL.

    Parameters:
    - url (str): The URL of the website to fetch.

    Returns:
    - str: The HTML content of the website.
    """
    try:
        # Specify headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Make the request and directly return the HTML content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure the request was successful

        return response.text
    except requests.exceptions.RequestException as e:
        # Return an error message if the request encounters an issue
        return f"Error: {e}"
