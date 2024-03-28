import requests
from bs4 import BeautifulSoup

def clean_text_and_prepare_html(soup):
    """
    Prepares simplified HTML content with text and references to parent divs.
    """
    html_content = ['<html><head><title>Cleaned Content</title></head><body>']
    relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']

    for tag in soup.find_all(relevant_tags):
        parent_div = tag.find_parent('div')
        # Check if a parent <div> was found
        if parent_div:
            div_reference = parent_div.get('id') or ' '.join(parent_div.get('class', []))
            div_reference_str = f" <small>(in div: {div_reference})</small>" if div_reference else ""
        else:
            # Handle case where no parent <div> is found
            div_reference_str = " <small>(no parent div)</small>"
        tag_text = tag.get_text(separator=" ", strip=True)
        if tag_text:
            html_content.append(f"<div><{tag.name}>{tag_text}{div_reference_str}</{tag.name}></div>")

    html_content.append('</body></html>')
    return ''.join(html_content)


def fetch_website_html(url):
    """
    Fetches and returns HTML content of a URL, simplified and ready for display.
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup(["script", "style", "header", "footer", "nav", "a"]):
            element.decompose()

        cleaned_html = clean_text_and_prepare_html(soup)
        return cleaned_html

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
