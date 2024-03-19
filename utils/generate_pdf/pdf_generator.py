import os

from reportlab.lib import colors
from reportlab.lib import utils
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate, FrameBreak, Table, TableStyle, PageBreak
from reportlab.platypus import KeepTogether
from reportlab.rl_config import defaultPageSize

from utils.generate_pdf.utils import cm
from websiteAudit.settings import BASE_DIR

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

from reportlab.platypus import BaseDocTemplate

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self.__pageNum = 1

    def afterPage(self):
        """Called after all flowables have been drawn on a page"""

        # Increment pageNum since the page has been completed
        self.__pageNum += 1

        # If the page number is even, force "left-side" template
        if self.__pageNum >= 2:
            self._handle_nextPageTemplate('succeeding-pages')
        else:
            self._handle_nextPageTemplate('first-page')

class PDFGenerator(object):
    def __init__(self, filename, destination_folder=os.path.join(BASE_DIR, 'media/pdf'), debug=False):
        self.debug = debug
        self.filename = filename
        self.destination_folder = destination_folder
        self.path = os.path.join(self.destination_folder, self.filename)

        self.doc = MyDocTemplate(self.path,
            pageSize='letter',
            rightMargin=cm(0.1),
            leftMargin=cm(0.1),
            topMargin=cm(0.2),
            bottomMargin=cm(1)
        )

        self.styles = getSampleStyleSheet()
        self.template = None

        os.makedirs(self.destination_folder, exist_ok=True)

    def set_template(self, template):
        self.template = template

    def generate_pdf(self, data):
        print(data)
        base_frames = self.template.base_frame()
        body_frames = self.template.body_frame()
        self.template.build_story(data)

        self.doc.addPageTemplates([
            PageTemplate(id='first-page', frames=base_frames),
            PageTemplate(id='succeeding-pages', frames=body_frames)
        ])
        self.doc.build(self.template.story)
