from dotenv import load_dotenv
from mailjet_rest import Client
import os

def create_and_update_contact(response_data):
    load_dotenv()

    MAILJET_API = os.getenv("MAILJET_API")
    MAILJET_SECRET = os.getenv("MAILJET_SECRET")

    mailjet = Client(auth=(MAILJET_API, MAILJET_SECRET))

    # Create a new contact with the basic details
    data = {
        'IsExcludedFromCampaigns': "true",
        'Name': response_data['First Name'] + " " + response_data['Last Name'],
        'Email': response_data['E-mail'],
    }
    result = mailjet.contact.create(data=data)
    print(f"Contact creation status code: {result.status_code}")
    if result.status_code not in [200, 201]:
        print("Failed to create contact.")
        return

    # Retrieve the List ID for "LM-website-CRO-audit"
    response = mailjet.contactslist.get(filters={'Name': 'LM-website-CRO-audit'})
    lists = response.json().get('Data', [])
    if lists:
        list_id = lists[0]['ID']
        # Add contact to the list
        data = {
            'ContactsLists': [{
                'ListID': list_id,
                'Action': "addnoforce"
            }]
        }
        result = mailjet.contact_managecontactslists.create(id=response_data['E-mail'], data=data)
        print(f"Add to List Status: {result.status_code}")
    else:
        print("List 'LM-website-CRO-audit' not found.")

    # Update contact with custom properties
    properties_data = {
        'Data': [
            {'Name': 'companyname', 'Value': response_data.get('Company Name', '')},
            {'Name': 'firstname', 'Value': response_data.get('First Name', '')},
            {'Name': 'lastname', 'Value': response_data.get('Last Name', '')},
            {'Name': 'url', 'Value': response_data.get('Url', '')},
            {'Name': 'overallgrade', 'Value': response_data.get('overall_grade', '')},
            {'Name': 'ctabuttonplacement', 'Value': response_data.get('cta_button_placement', '')},
            {'Name': 'ctaclarity', 'Value': response_data.get('cta_clarity', '')},
            {'Name': 'headlinefocus', 'Value': response_data.get('headline_focus', '')},
            {'Name': 'messagingclarity', 'Value': response_data.get('messaging_clarity', '')},
            {'Name': 'formdiagnostics', 'Value': response_data.get('form_diagnostics', '')},
            # Include additional properties as needed
            # {'Name': 'property_name', 'Value': response_data.get('field_name', '')},
        ]
    }
    result = mailjet.contactdata.update(id=response_data['E-mail'], data=properties_data)
    print(result.json())
    print(f"Update Contact Properties Status: {result.status_code}")

# Example usage
response_data = {
    # Assuming new_url and analysis_results are defined elsewhere
    'image_url': 'http://example.com/image.jpg',
    'Date': '2020-01-01 12:00:00',

    'First Name': 'John',
    'Last Name': 'Doe',
    'Url': 'https://www.example.com',
    'E-mail': 'example@example.com',

    'Company Name': 'Dummy Company',

    'overall_grade': 'A',
    'cta_button_placement': 'Top',
    'cta_clarity': 'Clear',
    'headline_focus': 'Focused',
    'messaging_clarity': 'Very Clear',
    'form_diagnostics': 'No Issues',

    'Social Proof': None,
    'Company Info Presence': None,

    # Add any other fields you want to include
    'other_field': 'other_value',
}
