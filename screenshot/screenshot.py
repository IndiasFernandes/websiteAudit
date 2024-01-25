import asyncio
from pyppeteer import launch
from urllib.parse import urlparse
import os
from django.conf import settings
import asyncio

async def take_screenshot(url):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    filename = f"{domain}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    await page.screenshot({'path': filepath})
    await browser.close()
    return filepath

def capture(url):
    return asyncio.get_event_loop().run_until_complete(take_screenshot(url))




# Define an async main function to await the coroutine
async def main():
    await take_screenshot('https://www.google.com')

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())