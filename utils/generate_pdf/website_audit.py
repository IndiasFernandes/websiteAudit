import os
import arrow

from reportlab.lib import colors
from reportlab.lib import utils
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate, FrameBreak, Table, TableStyle, PageBreak, NextPageTemplate, KeepTogether, CondPageBreak

MAIN_DIR = os.path.realpath(__file__)
BASE_DIR = '/'.join(MAIN_DIR.split('/')[0:-1])

from utils.generate_pdf.utils import cm, diff
from utils.generate_pdf.color_frame import ColorFrame

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('HelveticaNeue', 'media/Helvetica-Neue-LT-Com-35-Thin.ttf'))
pdfmetrics.registerFont(TTFont('Bahnschrift', 'media/bahnschrift.ttf'))

LOREM_IPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class WebsiteAudit(object):
    def __init__(self, doc, debug=True):
        self.doc = doc
        self.full_width = doc.width + (doc.leftMargin * 2)
        self.width = doc.width
        self.height = doc.height
        self.margins = {
            'top': doc.topMargin,
            'bottom': doc.bottomMargin,
            'left': doc.leftMargin,
            'right': doc.rightMargin
        }
        self.frames = []
        self.styles = getSampleStyleSheet()
        self.story = []
        self.debug = debug

    @property
    def template(self):
        self.build_frames()
        return PageTemplate(frames=self.frames)

    def base_frame(self):
        frames = self.build_frames(body_only=False)
        self.frames = frames
        return self.frames

    def body_frame(self):
        frames = self.build_frames(body_only=True)
        self.frames = frames
        return self.frames

    def build_frames(self, body_only=False):
        headerTopStart = diff([
            self.doc.height,
            self.doc.topMargin
        ])
        frames = []

        if not body_only:
            # Image Frame
            frames.append(
                Frame(
                    self.doc.leftMargin,
                    headerTopStart - cm(15),
                    (self.doc.width / 2) - cm(0.5),
                    cm(15),
                    id='header-left',
                    showBoundary=self.debug
                )
            )

            # Details Frame
            frames.append(
                Frame(
                    self.doc.width / 2 + cm(0.5),
                    headerTopStart - cm(15),
                    (self.doc.width / 2) - cm(0.5),
                    cm(15),
                    id='header-right',
                    showBoundary=self.debug
                )
            )

        # Body Frame
        frames.append(
            Frame(
                (self.doc.width / 6),
                headerTopStart - (cm(17) if body_only else cm(46)),
                (self.doc.width / 6) * 4,
                (cm(17) if body_only else cm(30)),
                id='body',
                showBoundary=self.debug
            )
        )

        if body_only:
            frames.append(
                Frame(
                    (self.doc.width / 6) * 0.5,
                    headerTopStart - cm(20.5),
                    cm(3),
                    cm(3),
                    id='footer-logo',
                    showBoundary=self.debug
                )
            )

            frames.append(
                Frame(
                    (self.doc.width / 6) + cm(1.5),
                    headerTopStart - cm(20.5),
                    ((self.doc.width / 6) * 5) - cm(3),
                    cm(3),
                    id='footer-text',
                    showBoundary=self.debug
                )
            )

            frames.append(
                Frame(
                    (self.doc.width / 6) * 0.5,
                    headerTopStart - cm(26),
                    ((self.doc.width / 6) * 5) + cm(0.3),
                    cm(6),
                    id='footer',
                    showBoundary=self.debug
                )
            )

        return frames

    def build_story(self, data):
        self.header(data)
        self.body(data['body_data'])
        self.footer()

    def get_image(self, filename, width):
        path = filename
        print(path)
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect), hAlign='RIGHT')

    def header(self, data):
        self.story.append(self.get_image(data['image_path'], cm(7)))
        self.story.append(FrameBreak())
        self.story.append(Paragraph('HERE IS YOUR REPORT',
            ParagraphStyle(name='PageText', fontName='Bahnschrift', fontSize=14, alignment=TA_LEFT, leading=100)
        ))

        self.story.append(Paragraph('Your Overall Score:',
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=16, alignment=TA_LEFT, leading=22)
        ))
        self.story.append(Paragraph(f"{data['overall_grade']}",
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=32, alignment=TA_LEFT, leading=150)
        ))

        self.story.append(Paragraph(f"Date: {data['date']}",
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=14)
        ))
        self.story.append(Paragraph(f"Analyzed URL: {data['url']}",
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=14)
        ))
        self.story.append(Paragraph(f"Company: {data['company']}",
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=26)
        ))

        self.story.append(Paragraph('Your details:',
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=14)
        ))
        self.story.append(Paragraph(f"{data['name']}, {data['last_name']}",
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=14)
        ))
        self.story.append(Paragraph(data['email'],
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_LEFT, leading=14)
        ))
        self.story.append(FrameBreak())

    def body(self, data):
        count = 0
        for row in data:
            count += 1
            self.story.append(Paragraph(row['title'],
                ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=18, alignment=TA_LEFT, leading=22)
            ))
            self.story.append(Spacer(cm(0), cm(0.4)))

            message = row['body'] if row['body'] != '' else LOREM_IPSUM
            self.story.append(Paragraph(message,
                ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=12, alignment=TA_LEFT, leading=12)
            ))
            self.story.append(Spacer(cm(0), cm(1.5)))

            if count == 2:
                self.story.append(CondPageBreak(cm(60)))

        self.story.append(FrameBreak())

    def footer(self):
        self.story.append(self.get_image('media/logo.png', cm(2.5)))
        self.story.append(FrameBreak())
        self.story.append(Spacer(cm(0), cm(0.25)))
        self.story.append(Paragraph('Thank You For Using Our Landing Page Optimization Audit Tool!',
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=22, alignment=TA_LEFT, leading=28)
        ))
        self.story.append(FrameBreak())
        self.story.append(Spacer(cm(0), cm(0.4)))
        self.story.append(Paragraph('Please be aware that this analysis was generated with the assistance of artificial intelligence. While it offers a comprehensive overview, it should not be considered a substitute for a website audit conducted by a professional expert.',
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_CENTER, leading=14)
        ))
        self.story.append(Spacer(cm(0), cm(0.4)))
        self.story.append(Paragraph('If you require a thorough and professional website audit, or if you need assistance with website optimization or the development of a new website, please don\'t hesitate to reach out to us. We are here to assist you.',
            ParagraphStyle(name='PageText', fontName='HelveticaNeue', fontSize=14, alignment=TA_CENTER, leading=14)
        ))

        self.story.append(Spacer(cm(0), cm(1.2)))

        self.story.append(Paragraph('GET IN TOUCH >>',
            ParagraphStyle(name='PageText', fontName='Bahnschrift', fontSize=14, alignment=TA_CENTER, leading=14)
        ))


