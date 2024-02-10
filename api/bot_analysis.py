import openai
import os
import ast

# Load the API key from a config file
API_KEY = open('config', 'r').read().strip()
client = openai.OpenAI(api_key=API_KEY)

def generate_analysis_prompt(html_content):
    """
    Generates a prompt for analyzing a website's landing page based on HTML content, focusing on conversion rate optimization.
    """
    prompt_text = f"""
    Given the HTML content of a landing page, provide a detailed analysis focusing on elements crucial for conversion rate optimization. Consider the user experience (UX/UI), the effectiveness of call-to-action (CTA) buttons, form simplicity, clarity of messaging and offers, trust signals, and technical aspects like page load speed and mobile responsiveness.

    Evaluate the landing page on the following points:

    1. UX/UI Design:
       - Placement and clarity of CTA buttons.
       - Simplicity and brevity of forms.

    2. Content and Messaging:
       - Readability and focus of text and headlines.
       - Transparency and appeal of offers.

    3. Trust Signals:
       - Presence of testimonials, certifications, and secure payment badges.
       - Availability of company information and policies.

    4. Technical Performance:
       - Page load speed.
       - Mobile responsiveness.

    Your analysis should fill in the following Python dictionary with concise feedback (up to 1000 characters) for each listed aspect and provide an overall rating for the landing page's optimization level from 0 (poorly optimized) to 100 (highly optimized):

    {{
    'cta_button_placement_diagnostics': "",
    'cta_clarity_diagnostics': "",
    'form_simplicity_diagnostics': "",
    'messaging_clarity_diagnostics': "",
    'headline_focus_diagnostics': "",
    'offer_transparency_diagnostics': "",
    'overall_rating': 0  # Provide an overall optimization rating between 0 and 100.
    }}

    HTML Content for Analysis:
    {html_content}
    """.strip()

    return prompt_text


def analyze_website(html_content):
    """
    Uses OpenAI's API to analyze the HTML content of a website's landing page for conversion rate optimization.
    """
    prompt = generate_analysis_prompt(html_content)
    print('Prompt for Analysis:\n\n' + prompt)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an AI designed to assist in analyzing landing pages for optimization. Your analysis should help in identifying areas for improvement to enhance conversion rates, and you should provide an overall optimization rating."},
            {"role": "user", "content": prompt}
        ]
    )

    # Parsing the response to a Python dictionary
    parsed_dict = ast.literal_eval(completion.choices[0].message.content)
    return parsed_dict
