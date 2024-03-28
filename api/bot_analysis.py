import os, ast
from dotenv import load_dotenv
# Assuming ChatOpenAI and HumanMessage are part of a custom implementation you've access to.
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

# Load the API key from a config file
API_KEY = os.getenv("OPENAI_API")
client = ChatOpenAI(api_key=API_KEY)

def generate_analysis_prompt(html_content):
    # Your existing prompts remain unchanged
    # This function now returns a list of prompt strings instead of HumanMessage objects
    prompts = [
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html and grade how well it is designed for conversion optimization. Give it a score from 1 to 10, with 1 being the lowest, and 10 being the highest grade. In your answer provide only a numeric score, without any text.",
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html including spaces and detail how well the landing page uses CTA buttons. Focus on where the buttons are placed: is there a call-to-action button in the header and is there a main call to action above the fold. Furthermore, check if the landing page repeats call to action throughout the page, and if there are any secondary call to actions. At the end provide further recommendations about placement of call-to-action buttons.",
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html including spaces and detail if the landing page is doing well in terms of clarity of call to actions. Focus on how instructive the call to actions are; can call to actions be interpreted only in one way or are they confusing; are call to actions using simple language that the user can easily understand? At the end provide further recommendations about clarity of call-to-actions buttons.",
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html including spaces and detail how well the landing page is doing in terms of the headlines. Focus on how clear the headlines are, are they clearly communicating the purpose of the landing page, or are they confusing, to abstract or too difficult to understand. At the end provide further recommendations about focus of the headlines.",
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html, including spaces and detail how well the landing page is doing in terms of clarity of the messaging. Focus on: How well focused is the message of the page: is there a clear goal to the page and is the user guided to that goal in a simple and clear way? If there is an offer on the page, how well is it presented - is the messaging appealing, are the benefits clear and well presented, are the terms transparent? Is the message of the page cohesive, or are there any contradictory or opposing messages? Are there any signals of trust, such as customer reviews, testimonials, or clients lists? How is the readability of the text? At the end provide further recommendations about clarity of the messaging.",
        "You are a marketer specialized in landing page conversion optimization. Analyze landing page in html, including spaces and detail how well the landing page is doing in terms of clarity of forms. Is there a form on the website; how well is it placed on the landing page; does the landing page provide alternative way of contact, for those who fail to fill the form; is the form short enough; if the form is divided into steps, does it use the progress bar, to signal the length of the form. At the end, provide further recommendations regarding the form."
    ]
    return prompts

def analyze_website(html_content):
    """
    Uses OpenAI's API to analyze the HTML content of a website's landing page for conversion optimization.
    Each prompt is processed individually and the results are aggregated into a dictionary.
    """
    prompts = generate_analysis_prompt(html_content)
    analysis_results = {}

    for i, prompt in enumerate(prompts, start=1):
        # Assuming `client.invoke` can process a string directly. If not, adjust accordingly.
        result = client.invoke(prompt)
        # Assuming result.content is the response string that needs to be parsed into a dictionary value.
        # You might need to adjust this part based on how your OpenAI client returns the result.
        if i == 1:
            key = 'overall_grade'
        elif i == 2:
            key = 'cta_button_placement'
        elif i == 3:
            key = 'cta_clarity'
        elif i == 4:
            key = 'headline_focus'
        elif i == 5:
            key = 'messaging_clarity'
        elif i == 6:
            key = 'form_diagnostics'


        analysis_results[key] = result.content  # Or parse as needed

    results = client.invoke(f"Create a Python dictionary with summarized content from the following dictionary: {analysis_results}. Return only the python dictionary, ready to be used without any extra text. The dictionary should contain keys for 'overall_grade', 'cta_button_placement', 'cta_clarity', 'headline_focus', 'messaging_clarity' and 'form_diagnostics'. Each key will have a value consisting of 2 to 3 sentences summarizing the detailed content provided previously, without including any ' symbol in the answer, avoiding any errors in python code. tThe 'overall_grade' variable has to be an integer only, no text")

    print(results.content)
    analysis_results_summary = ast.literal_eval(results.content)  # Or parse as needed

    # create dummy data for analysis_results_summary and analysis_results
    analysis_results = {
        'overall_grade': 8,
        'cta_button_placement': 'The CTA buttons are well-placed with a clear main call to action above the fold. There are secondary CTAs throughout the page, providing a good user experience.',
        'cta_clarity': 'The CTAs are clear and instructive, using simple language that is easy to understand. The messaging is concise and guides the user effectively.',
        'headline_focus': 'The headlines are clear and effectively communicate the purpose of the landing page. They are engaging and draw the user in.',
        'messaging_clarity': 'The messaging is focused and cohesive, guiding the user towards the goal of the page. The benefits are well-presented, and the text is readable.',
        'form_diagnostics': 'The form is well-placed on the landing page, providing alternative contact methods. It is short and user-friendly, enhancing the overall conversion experience.'
    }

    analysis_results_summary = {
        'overall_grade': 'The landing page received a grade of 8 for conversion optimization. The CTA buttons are well-placed and clear, with concise messaging. The headlines effectively communicate the page\'s purpose, and the messaging is focused and cohesive. The form is user-friendly and enhances the overall conversion experience.',
        'cta_button_placement': 'The CTA buttons are well-placed with a clear main call to action above the fold. There are secondary CTAs throughout the page, providing a good user experience.',
        'cta_clarity': 'The CTAs are clear and instructive, using simple language that is easy to understand. The messaging is concise and guides the user effectively.',
        'headline_focus': 'The headlines are clear and effectively communicate the purpose of the landing page. They are engaging and draw the user in.',
        'messaging_clarity': 'The messaging is focused and cohesive, guiding the user towards the goal of the page. The benefits are well-presented, and the text is readable.',
        'form_diagnostics': 'The form is well-placed on the landing page, providing alternative contact methods. It is short and user-friendly, enhancing the overall conversion experience.'
    }

    print(type(analysis_results_summary))
    return analysis_results, analysis_results_summary


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
