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
