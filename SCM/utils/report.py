from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import io
import datetime
import json

class ScoreIndicator(Flowable):
    """A custom flowable that shows a score as a colored box with text"""
    def __init__(self, score, width=1*inch, height=0.3*inch):
        Flowable.__init__(self)
        self.score = score
        self.width = width
        self.height = height
        
    def draw(self):
        """Draw the score indicator"""
        # Determine color based on score
        if self.score < 4:
            color = colors.red
        elif self.score < 7:
            color = colors.orange
        else:
            color = colors.green
            
        # Draw rectangle
        self.canv.setFillColor(color)
        self.canv.rect(0, 0, self.width, self.height, fill=1)
        
        # Draw score text
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 14)
        self.canv.drawCentredString(self.width/2, self.height/4, f"{self.score}/10")

def create_score_chart(scores, title):
    """Create a simple bar chart for multiple scores"""
    drawing = Drawing(400, 200)
    
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 350
    chart.data = [scores]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 10
    chart.valueAxis.valueStep = 1
    
    # Set colors based on scores
    colors_list = []
    for score in scores:
        if score < 4:
            colors_list.append(colors.red)
        elif score < 7:
            colors_list.append(colors.orange)
        else:
            colors_list.append(colors.green)
    
    chart.bars[0].fillColor = colors_list[0]  # Use the first color for all bars
    
    chart.categoryAxis.labels.boxAnchor = 'ne'
    chart.categoryAxis.labels.dx = -8
    chart.categoryAxis.labels.dy = -2
    chart.categoryAxis.labels.angle = 30
    
    # Add title
    from reportlab.graphics.shapes import String
    title_element = String(200, 180, title, fontSize=12, textAnchor='middle')
    drawing.add(title_element)
    
    drawing.add(chart)
    return drawing

def generate_report(assessment_data, project_name=""):
    """Generate a simplified PDF report that works reliably"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Ensure assessment_data is a dict
    if not isinstance(assessment_data, dict):
        assessment_data = {}

    # Simple title styling
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    section_style = styles['Heading3']
    normal_style = styles['Normal']
    
    # Title and Date
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    title = Paragraph("Stormwater Infrastructure Assessment Report", title_style)
    story.append(title)
    project_heading = Paragraph(project_name, subtitle_style)
    story.append(project_heading)
    story.append(Paragraph("Generated: " + current_date, normal_style))
    story.append(Spacer(1, 20))

    # Executive Summary
    story.append(Paragraph("Executive Summary", subtitle_style))
    
    # Simplified score collection
    condition_score = 5
    if 'condition' in assessment_data and 'OSAC' in assessment_data['condition']:
        condition_score = assessment_data['condition']['OSAC'].get('score', 5)
    
    functionality_score = 5
    if 'functionality' in assessment_data and 'overallFunctionality' in assessment_data['functionality']:
        functionality_score = assessment_data['functionality']['overallFunctionality'].get('score', 5)
    
    time_score = 5
    if 'time_effectiveness' in assessment_data:
        time_score = assessment_data['time_effectiveness'].get('overallTimeScore', 5)
    
    cost_score = 5
    if 'cost_effectiveness' in assessment_data:
        cost_score = assessment_data['cost_effectiveness'].get('overallCostScore', 5)
    
    env_score = 5
    if 'environmental_social' in assessment_data:
        env_score = assessment_data['environmental_social'].get('overallScore', 5)
    
    # Calculate final score
    scores = [condition_score, functionality_score, time_score, cost_score, env_score]
    final_score = sum(scores) // len(scores)
    
    # Rating text based on score
    rating = "Good" if final_score >= 7 else "Fair" if final_score >= 4 else "Poor"
    
    # Add overall assessment info
    summary_text = "This report provides a comprehensive assessment of stormwater infrastructure"
    if project_name:
        summary_text += " for " + project_name
    summary_text += "."
    
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Overall Rating: " + rating, subtitle_style))
    story.append(Paragraph("Overall Score: " + str(final_score) + "/10", normal_style))
    story.append(Spacer(1, 15))
    
    # Domain Scores Table
    story.append(Paragraph("Domain Score Breakdown", section_style))
    domain_data = [
        ['Domain', 'Score', 'Rating'],
        ['Condition', str(condition_score), "Good" if condition_score >= 7 else "Fair" if condition_score >= 4 else "Poor"],
        ['Functionality', str(functionality_score), "Good" if functionality_score >= 7 else "Fair" if functionality_score >= 4 else "Poor"],
        ['Time Effectiveness', str(time_score), "Good" if time_score >= 7 else "Fair" if time_score >= 4 else "Poor"],
        ['Cost Effectiveness', str(cost_score), "Good" if cost_score >= 7 else "Fair" if cost_score >= 4 else "Poor"],
        ['Environmental & Social', str(env_score), "Good" if env_score >= 7 else "Fair" if env_score >= 4 else "Poor"]
    ]
    
    # Create domain score table
    domain_table = Table(domain_data, colWidths=[2*inch, 1*inch, 1*inch])
    domain_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(domain_table)
    story.append(Spacer(1, 20))
    
    # Infrastructure Points Analysis 
    story.append(Paragraph("Infrastructure Analysis", subtitle_style))
    if 'infrastructure_points' in assessment_data and assessment_data['infrastructure_points']:
        # Simple table of infrastructure points
        data = [['Location', 'Type', 'Age', 'Last Maintenance']]
        
        for point in assessment_data['infrastructure_points']:
            data.append([
                str(point.get('name', 'N/A')),
                str(point.get('type', 'N/A')).replace('_', ' ').title(),
                str(point.get('age', 'N/A')),
                str(point.get('last_maintenance_days', 'N/A')) + " days ago"
            ])
            
        # Create a simple table
        infra_table = Table(data)
        infra_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(infra_table)
    else:
        story.append(Paragraph("No infrastructure points available.", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Recommendations section
    story.append(Paragraph("Recommendations", subtitle_style))
    
    # Generic recommendations
    recommendations = """
    • Implement regular inspection and maintenance schedules
    • Consider climate change impacts in future designs
    • Engage community stakeholders in planning processes
    • Update emergency response protocols for extreme weather events
    • Evaluate opportunities for green infrastructure integration
    """
    story.append(Paragraph(recommendations, normal_style))
    
    # Footer with page numbers
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        page_num = canvas.getPageNumber()
        text = "Page " + str(page_num)
        canvas.drawRightString(doc.width + doc.rightMargin - 10, doc.bottomMargin - 20, text)
        
        footer_text = "Stormwater Infrastructure Assessment"
        if project_name:
            footer_text += " - " + project_name
        canvas.drawString(doc.leftMargin, doc.bottomMargin - 20, footer_text)
        
        canvas.restoreState()
    
    # Build the document with page numbers
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    return buffer