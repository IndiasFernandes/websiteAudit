import os, ast
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from utils.web_scrapper import fetch_website_html

load_dotenv()

# Load the API key from a config file
API_KEY = os.getenv("OPENAI_API")
client = ChatOpenAI(api_key=API_KEY)

def generate_analysis_prompt(html_content):

    messages = [
        HumanMessage("You are a marketer specialized in landing page conversion optimization. You have been asked to analyze a website's landing page for conversion rate optimization. The website's HTML content is provided below:"),
        HumanMessage(f"This is the html content: '{html_content}'"),
        HumanMessage(
            "Compile the analysis, filling a single Python dictionary. That is the only answer you provide, without any text, only the disctionary."),
        HumanMessage("Analyze the html content and grade how well it is designed for conversion optimization. Give it a score from 1 to 10, with 1 being the lowest, and 10 being the highest grade. In your answer, fill in the 'overall_grade' field of the Python dictionary."),
        HumanMessage("Analyze the html content and detail in a complex answer up to 1000 chars how well the landing page uses CTA buttons. Focus on where the buttons are placed. At the end, fill in the 'cta_button_placement' field of the Python dictionary with your recommendations."),
        HumanMessage("Analyze the html content and detail in a complex answer up to 1000 chars if the landing page is doing well in terms of clarity of call to actions. At the end, fill in the 'cta_clarity' field of the Python dictionary with your recommendations."),
        HumanMessage("Analyze the html content and detail in a complex answer up to 1000 chars how well the landing page is doing in terms of the headlines. At the end, fill in the 'headline_focus' field of the Python dictionary with your recommendations."),
        HumanMessage("Analyze the html content and detail in a complex answer up to 1000 chars how well the landing page is doing in terms of clarity of the messaging. At the end, fill in the 'messaging_clarity' field of the Python dictionary with your recommendations."),
        HumanMessage("Analyze the html content and detail in a complex answer up to 1000 chars how well the landing page is doing in terms of clarity of forms. At the end, fill in the 'form_diagnostics' field of the Python dictionary with your recommendations."),

    ]

    return messages

def analyze_website(html_content):
    """
    Uses OpenAI's API to analyze the HTML content of a website's landing page for conversion rate optimization.
    """
    messages = generate_analysis_prompt(html_content)
    for message in messages:
        print(f"{message.content}")
    result = client.invoke(messages)
    print(result.content)
    parsed_dict = ast.literal_eval(result.content)

    return parsed_dict

def generate_analysis_promptt(html_content):
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

def analyze_websitee(html_content):
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
