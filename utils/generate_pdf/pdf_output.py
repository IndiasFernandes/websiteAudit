import copy
import os
import csv
import math
import arrow

from reportlab.lib import colors
from reportlab.lib import utils
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Spacer, FrameBreak, Table, TableStyle, PageBreak
from reportlab.platypus import KeepTogether

from utils.generate_pdf.pdf_generator import PDFGenerator
from utils.generate_pdf.website_audit import WebsiteAudit
from websiteAudit.settings import MEDIA_ROOT


class PDFOutput(object):
    def __init__(self, filename=None, url='N/A', company='N/A', name='N/A', last_name='N/A', email='N/A', overall_grade=0, date='N/A', image_path='N/A', body_data=[], debug=True):
        self.filename = filename
        self.image_path = image_path
        self.url = url
        self.company = company
        self.name = name
        self.last_name = last_name
        self.email = email
        self.overall_grade = overall_grade
        self.date = date
        self.body_data = body_data
        self.debug = debug

    def get_image(self, path, width):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect), hAlign='LEFT')

    def get_data(self):
        return {
            'url': self.url,
            'company': self.company,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'overall_grade': self.overall_grade,
            'body_data': self.body_data,
            'date': self.date,
            'image_path': self.image_path
        }

    def save(self):
        pdf_generator = PDFGenerator(self.filename)
        print()
        website_audit = WebsiteAudit(pdf_generator.doc, debug=self.debug)
        pdf_generator.set_template(website_audit)
        pdf_generator.generate_pdf(self.get_data())
        return "pdf/" + self.filename