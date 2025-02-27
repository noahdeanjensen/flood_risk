from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from views.dashboard import calculate_overall_score

def generate_report(assessment_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("Stormwater Infrastructure Assessment Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Overall Score
    overall_score = calculate_overall_score(assessment_data)
    score_text = f"Overall Infrastructure Score: {overall_score}/10"
    score_para = Paragraph(score_text, styles['Heading2'])
    story.append(score_para)
    story.append(Spacer(1, 12))

    # Score interpretation
    if overall_score >= 8:
        interpretation = "Excellent condition - Minor maintenance required"
    elif overall_score >= 6:
        interpretation = "Good condition - Regular maintenance recommended"
    elif overall_score >= 4:
        interpretation = "Fair condition - Some repairs needed"
    else:
        interpretation = "Poor condition - Major repairs/replacement recommended"

    story.append(Paragraph(f"Assessment: {interpretation}", styles['Normal']))
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