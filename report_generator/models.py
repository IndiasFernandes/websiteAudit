from django.db import models

class WebsiteReport(models.Model):
    url = models.URLField()
    screenshot = models.ImageField(upload_to='screenshots/')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    overall_rating = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    # Diagnostics
    cta_button_placement_rating = models.FloatField()
    cta_clarity_rating = models.FloatField()
    form_simplicity_rating = models.FloatField()
    form_autofill_rating = models.FloatField()
    messaging_clarity_rating = models.FloatField()
    headline_focus_rating = models.FloatField()
    offer_transparency_rating = models.FloatField()

    # Trust Signals
    social_proof = models.TextField()  # Testimonials, reviews, etc.
    company_info_presence = models.TextField()  # Company data, policies, etc.



from report_generator.models import WebsiteReport
from django.core.files import File
from django.core.files.images import ImageFile
report1 = WebsiteReport(
    url='https://duckduckgo.com',
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    overall_rating=4.5,
    cta_button_placement_rating=4.0,
    cta_clarity_rating=4.2,
    form_simplicity_rating=3.8,
    form_autofill_rating=4.1,
    messaging_clarity_rating=4.5,
    headline_focus_rating=4.3,
    offer_transparency_rating=4.4,
    social_proof='Testimonials, reviews, etc.',
    company_info_presence='Company data, policies, etc.'
)
# Replace 'path/to/screenshot1.jpg' with the actual path to your screenshot image


with open('/exports/images/screenshots/duckduckgo.com.png', 'rb') as f:
    report1.screenshot.save('duckduckgo.com.png', ImageFile(f))
report1.save()
# Create and save the second WebsiteReport instance
report2 = WebsiteReport(
    url='https://google.com',
    first_name='Jane',
    last_name='Doe',
    email='jane@example.org',
    overall_rating=4.7,
    cta_button_placement_rating=4.5,
    cta_clarity_rating=4.6,
    form_simplicity_rating=4.0,
    form_autofill_rating=4.2,
    messaging_clarity_rating=4.6,
    headline_focus_rating=4.4,
    offer_transparency_rating=4.5,
    social_proof='More testimonials, reviews, etc.',
    company_info_presence='More company data, policies, etc.'
)
# Replace 'path/to/screenshot2.jpg' with the actual path to your screenshot image
with open('exports/images/screenshots/innerflect.com.png', 'rb') as f:
    report2.screenshot.save('innerflect.com.png', ImageFile(f))

report2.save()