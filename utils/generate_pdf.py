from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(filename):
    # Specify the full path for the PDF file
    pdf_path = "./media/" + filename + ".pdf"

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Hello, ReportLab!")
    c.save()
