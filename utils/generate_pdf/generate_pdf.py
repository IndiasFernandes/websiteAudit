import secrets
import arrow

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from utils.generate_pdf.pdf_output import PDFOutput

def generate_pdf(body_data, url, company_name, first_name, last_name, e_mail, overall_grade, image_path):

    # Date of the report
    date = datetime.now().strftime('%Y-%m-%d')

    # Generate the PDF
    output = PDFOutput(
        'PDF-{}.pdf'.format(arrow.get().format('YYYYMMDDHHmmss')),
        body_data=body_data,
        url=url, company=company_name, name=first_name, last_name=last_name, email=e_mail, overall_grade=overall_grade, date=date, image_path=image_path,
        debug=False
    )

    # Save the PDF and return the path
    path = output.save()

    return path
