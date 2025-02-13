from django.shortcuts import render
from django.http import HttpResponse
from .models import FloodRiskAssessment
from .core.oilama_r1.llm_integration import LLMFloodPredictor
def home(request):
    return HttpResponse("Hello, World!")

def consult_Form(request):
    return render(request, 'consultForm.html')

def assess_risk(request):
    assessment = None
    
    if request.method == 'POST':
        # Process form submission
        assessment = FloodRiskAssessment(
            location=request.POST.get('location'),
            pipe_diameter=float(request.POST.get('pipe_diameter', 0)),
            damage_level=int(request.POST.get('damage_level', 5))
        )
        
        # Get prediction
        predictor = LLMFloodPredictor()
        assessment.risk_score = predictor.predict_risk({
            'damage_level': assessment.damage_level,
            'pipe_age': 2023 - assessment.last_inspection.year
        })
        
        assessment.save()

    return render(request, 'assess.html', {
        'assessment': assessment
    })