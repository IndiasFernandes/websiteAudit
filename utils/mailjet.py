from dotenv import load_dotenv
from mailjet_rest import Client
import os

def create_and_update_contact(response_data, analysis_results_summary):
    load_dotenv()

    MAILJET_API = os.getenv("MAILJET_API")
    MAILJET_SECRET = os.getenv("MAILJET_SECRET")

    mailjet = Client(auth=(MAILJET_API, MAILJET_SECRET))

    # Check if the contact already exists
    check_contact = mailjet.contact.get(data={'Email': response_data['E-mail']})
    if check_contact.status_code == 200 and check_contact.json().get('Data'):
        print("Contact already exists.")
    else:
        # Attempt to create a new contact with the basic details
        data = {
            'IsExcludedFromCampaigns': "true",
            'Name': response_data['First Name'] + " " + response_data['Last Name'],
            'Email': response_data['E-mail'],
        }
        result = mailjet.contact.create(data=data)
        if result.status_code not in [200, 201]:
            print(f"Failed to create contact, status code: {result.status_code}. Attempting to add to list if exists.")

    # Proceed with adding the contact to the list and updating properties, regardless of creation status

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
            # Your properties_data content, same as in your initial code
        ]
    }
    result = mailjet.contactdata.update(id=response_data['E-mail'], data=properties_data)
    print(result.json())
    print(f"Update Contact Properties Status: {result.status_code}")

# Example usage
# Assume response_data and analysis_results_summary are defined
