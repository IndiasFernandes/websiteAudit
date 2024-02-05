import ast

import openai
import os

API_KEY = open('config', 'r').read()
client = openai.OpenAI(api_key=API_KEY)

def generate_analysis_prompt(html_content):
    return f"""
    Based on the HTML content provided, conduct a thorough website audit focused on conversion rate optimization, considering the following aspects and criteria:

    1. **UX/UI:**
        - **Call-to-Action (CTA):**
            - Evaluate the placement of the call-to-action button. Is there a call to action, and is it placed above the fold?
            - Assess the clarity of the call to action. Is it clear what the call to action does?

        - **Forms:**
            - Are the forms simple and short?
            - Is there autofill functionality to improve user experience?

        - **Messaging and Offer:**
            - Is the text clear and easy to read?
            - Are the headlines focused on outcomes beneficial to users?
            - Is the offer transparent and clear?

    2. **Trust Signals:**
        - Evaluate the presence of social proof, such as testimonials, reviews, certifications, and partner logos.
        - Assess the presence of company information, including company data, secure payment badges, social links, and policies (return policy, privacy policy, terms of use).

    3. **Technical (Not necessary but beneficial):**
        - Comment on the page load speed.
        - Assess mobile responsiveness.

    Provide a written analysis for each point, generating a Python dictionary with the following variables and provide a concise analysis within each variable (maximum 100 characters per variable) for a website focused on conversion rate optimization:

1. 'cta_button_placement_diagnostics': ""
2. 'cta_clarity_diagnostics': ""
3. 'form_simplicity_diagnostics': ""
4. 'form_autofill_diagnostics': ""
5. 'messaging_clarity_diagnostics': ""
6. 'headline_focus_diagnostics': ""
7. 'offer_transparency_diagnostics': ""

Please ensure that each variable contains a brief analysis. Return only the dictionary in Python format, ready to use as a variable in one line (without any other text).

    HTML Content for Analysis:
    {html_content}
    """.strip()


def analyze_website(html_content):
    prompt = generate_analysis_prompt(html_content)
    print('Prompt:\n\n' + prompt)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an online inspection tool assistant, skilled in analysing websites and generating a diagnosis and a overall rating according to an effective Lead Magnet. You only return the dictionary asked, without any added text."},
            {"role": "user", "content": prompt}
        ]
    )
    parsed_dict = ast.literal_eval(completion.choices[0].message.content)
    return parsed_dict
