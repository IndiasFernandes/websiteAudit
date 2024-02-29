from dotenv import load_dotenv
from mailjet_rest import Client
import os

load_dotenv()

MAILJET_API = os.getenv("MAILJET_API")
MAILJET_SECRET = os.getenv("MAILJET_SECRET")

mailjet = Client(auth=(MAILJET_API, MAILJET_SECRET))

# Dummy data for demonstration
contact_info = {
    'Email': 'example2@example.com',  # This would be the unique identifier for the contact
    'CompanyName': 'Dummy Company',
    'FirstName': 'John',
    'LastName': 'Doe',
    'URL': 'https://www.example.com',
    'OverallGrade': 'A',
    'CTAButtonPlacement': 'Top',
    'CTAClarity': 'Clear',
    'HeadlineFocus': 'Focused',
    'MessagingClarity': 'Very Clear',
    'FormDiagnostics': 'No Issues'
}


data = {
  'IsExcludedFromCampaigns': "true",
  'Name': contact_info['FirstName'] + " " + contact_info['LastName'],
  'Email': contact_info['Email'],
}

# Create a new contact
result = mailjet.contact.create(data=data)
print(result.json())
print(f"Status Code: {result.status_code}")
print(f"Contact created with ID:{result.json().get('Data')[0].get('ID')}")

# Assuming result.json() contains the newly created contact details
contact_id = result.json().get('Data')[0].get('ID')

# Retrieve the List ID for "LM-website-CRO-audit"
response = mailjet.contactslist.get(filters={'Name': 'LM-website-CRO-audit'})
lists = response.json().get('Data', [])
print(f"Found {len(lists)} lists")
print(f"List ID: {lists[0].get('ID')}")

if lists:
    list_id = lists[0]['ID']
    # Prepare data to add contact to the list
    data = {
        'ContactsLists': [{
            'ListID': list_id,
            'Action': "addnoforce"  # Use "addforce" if you want to force add the contact
        }]
    }
    # Use the contact's email as an identifier to manage list membership
    result = mailjet.contact_managecontactslists.create(id=contact_info['Email'], data=data)
    print("Add to List Status:", result.status_code)
    print(result.json())
else:
    print("List not found.")

# Update contact with custom properties
if result.status_code == 201:
    contact_email = contact_info['Email']
    properties_data = {
        'Data': [
            {'Name': 'companyname', 'Value': contact_info['CompanyName']},
            {'Name': 'firstname', 'Value': contact_info['FirstName']},
            {'Name': 'lastname', 'Value': contact_info['LastName']},
            {'Name': 'url', 'Value': contact_info['URL']},
            {'Name': 'overallgrade', 'Value': contact_info['OverallGrade']},
            {'Name': 'ctabuttonplacement', 'Value': contact_info['CTAButtonPlacement']},
            {'Name': 'ctaclarity', 'Value': contact_info['CTAClarity']},
            {'Name': 'headlinefocus', 'Value': contact_info['HeadlineFocus']},
            {'Name': 'messagingclarity', 'Value': contact_info['MessagingClarity']},
            {'Name': 'formdiagnostics', 'Value': contact_info['FormDiagnostics']},
            {'Name': 'country', 'Value': contact_info.get('Country', '')},
            {'Name': 'language', 'Value': contact_info.get('Language', '')},
            {'Name': 'newsletter_sub', 'Value': contact_info.get('Newsletter_sub', 'False')},
        ]
    }
    result = mailjet.contactdata.update(id=contact_email, data=properties_data)
    print("Update Contact Properties Status:", result.status_code)
    print(result.json())
else:
    print("Failed to create contact:", result.status_code)