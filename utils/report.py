from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

def generate_report(assessment_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("Stormwater Infrastructure Assessment Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Assessment sections
    sections = [
        "Stormwater Condition",
        "Functionality Assessment",
        "Time-Effectiveness",
        "Cost-Effectiveness",
        "Environmental and Social Impact"
    ]

    for section in sections:
        story.append(Paragraph(section, styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Add section data
        if section.lower().replace(" ", "_") in assessment_data:
            data = assessment_data[section.lower().replace(" ", "_")]
            for key, value in data.items():
                text = f"{key}: {value}"
                story.append(Paragraph(text, styles['Normal']))
            
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer
