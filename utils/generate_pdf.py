from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf(filename):
    # Variables to be replaced with actual data
    url = "N/A"
    company = "N/A"
    name = "N/A"
    last_name = "N/A"
    email = "N/A"

    # Specify the full path for the PDF file
    pdf_path = "./media/" + filename

    # Get the current date and time
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a PDF document
    report = SimpleDocTemplate(pdf_path, pagesize=letter)
    width, height = letter

    # Custom information for the upper right cell
    upper_right_cell_content = f"""HERE IS YOUR REPORT

Your Overall Score: 10

Date: {date}
Analyzed URL: {url}
Company: {company}
Your details: {name} {last_name}, {email}
"""

    # Table 1 Data
    data1 = [['Cell (1, 1)', upper_right_cell_content]]
    table1 = Table(data1, colWidths=[width/2.0]*2)
    table1.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    # Titles and descriptions for Table 2
    sections = [
        ("DOWNLOAD REPORT >>", ""),  # Added as the first row in Table 2
        ("CTA Button Placement", "Lorem Ipsum is simply dummy text of the printing and typesetting industry..."),
        ("CTA Clarity", "Lorem Ipsum is simply dummy text of the printing and typesetting industry..."),
        ("Headline Focus", "Lorem Ipsum is simply dummy text of the printing and typesetting industry..."),
        ("Messaging Clarity", "Lorem Ipsum is simply dummy text of the printing and typesetting industry..."),
        ("Form Diagnostic", "Lorem Ipsum is simply dummy text of the printing and typesetting industry...")
    ]

    # Adding section titles and descriptions as individual full-width rows for Table 2
    data2 = [[title + "\n" + description] for title, description in sections]
    table2 = Table(data2, colWidths=[width])
    table2.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    # Build the document with both tables
    report.build([table1, table2])

    print(f"Table created and saved to {pdf_path}")

# Example usage
generate_pdf("example_report")
