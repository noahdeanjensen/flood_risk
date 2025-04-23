import streamlit as st
from utils.db import get_assessments, get_user_projects
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_overall_score(assessment_data):
    """Calculate overall infrastructure score (0-10)"""
    try:
        # Initialize domain scores
        domain_scores = []
        domain_weights = {
            'condition': 0.30,         # 30% weight for condition
            'functionality': 0.25,     # 25% weight for functionality
            'time_effectiveness': 0.15, # 15% weight for time effectiveness
            'cost_effectiveness': 0.15, # 15% weight for cost effectiveness
            'environmental_social': 0.15 # 15% weight for environmental/social
        }
        
        # 1. Get Condition Score - from OSAC rating if available
        try:
            condition_score = assessment_data.get('condition', {}).get('OSAC', {}).get('score')
            if condition_score is None:
                # Fall back to calculating from damage levels if OSAC not available
                damage_levels = assessment_data.get('condition', {}).get('stormwaterHydraulicAssetCondition', {}).get('damageLevels', {})
                if damage_levels:
                    # Calculate based on damage levels (old method)
                    damage_score = sum(1 if (v == "low" or v.get('condition', '') == "low") 
                                    else 2 if (v == "moderate" or v.get('condition', '') == "moderate") 
                                    else 3 for v in damage_levels.values())
                    max_score = 3 * len(damage_levels) if len(damage_levels) > 0 else 1
                    condition_score = int(10 - (damage_score / max_score * 10))
                else:
                    condition_score = 5  # Default if no data
            domain_scores.append(('condition', condition_score, domain_weights['condition']))
        except Exception as e:
            logger.error(f"Error calculating condition score: {e}")
            domain_scores.append(('condition', 5, domain_weights['condition']))
        
        # 2. Get Functionality Score
        try:
            functionality_score = assessment_data.get('functionality', {}).get('overallFunctionality', {}).get('score')
            if functionality_score is None:
                # Calculate from hydraulic and hydrological performance if available
                hp_data = assessment_data.get('functionality', {}).get('hydraulicPerformance', {})
                dp_data = assessment_data.get('functionality', {}).get('hydrologicalPerformance', {})
                
                if hp_data and 'flowAttenuation' in hp_data and 'volumeReduction' in hp_data:
                    hp_score = (hp_data['flowAttenuation'] + hp_data['volumeReduction']) / 20
                    dp_score = 5  # Default hydrological score
                    
                    if dp_data and 'runoffFrequency' in dp_data and 'baseFlowPerformance' in dp_data:
                        dp_score = (dp_data['runoffFrequency'] + dp_data['baseFlowPerformance']) / 20
                        
                    functionality_score = int((hp_score + dp_score) / 2)
                else:
                    functionality_score = 5  # Default if no data
            domain_scores.append(('functionality', functionality_score, domain_weights['functionality']))
        except Exception as e:
            logger.error(f"Error calculating functionality score: {e}")
            domain_scores.append(('functionality', 5, domain_weights['functionality']))
        
        # 3. Get Time Effectiveness Score
        try:
            time_score = assessment_data.get('time_effectiveness', {}).get('overallTimeScore')
            if time_score is None:
                # Calculate from time metrics if available
                time_data = assessment_data.get('time_effectiveness', {})
                
                if 'longTermFunctionality' in time_data and 'lagTimePerformance' in time_data:
                    long_term_score = time_data['longTermFunctionality'] / 10
                    lag_time_score = time_data['lagTimePerformance'] / 10
                    
                    if 'monitoringFrequency' in time_data:
                        monitoring_scores = {
                            "Continuous (real-time)": 10,
                            "Daily": 8,
                            "Weekly": 7,
                            "Monthly": 5,
                            "Quarterly": 3,
                            "Annually": 1
                        }
                        monitoring_score = monitoring_scores.get(time_data['monitoringFrequency'], 5) / 10
                        time_score = int((long_term_score * 0.4) + (lag_time_score * 0.4) + (monitoring_score * 0.2) * 10)
                    else:
                        time_score = int((long_term_score + lag_time_score) / 2 * 10)
                else:
                    # Old calculation
                    lifespan = time_data.get('lifespan', 25)
                    maintenance_lag = time_data.get('maintenanceLagTime', 30)
                    
                    # Normalize lifespan (0-50 years scale)
                    lifespan_score = min(lifespan / 50, 1.0) 
                    
                    # Normalize maintenance lag (0-365 days scale, lower is better)
                    maintenance_score = max(0, 1 - (maintenance_lag / 365))
                    
                    time_score = int((lifespan_score * 0.7 + maintenance_score * 0.3) * 10)
            domain_scores.append(('time_effectiveness', time_score, domain_weights['time_effectiveness']))
        except Exception as e:
            logger.error(f"Error calculating time score: {e}")
            domain_scores.append(('time_effectiveness', 5, domain_weights['time_effectiveness']))
        
        # 4. Get Cost Effectiveness Score
        try:
            cost_score = assessment_data.get('cost_effectiveness', {}).get('overallCostScore')
            if cost_score is None:
                # Calculate from cost metrics if available
                cost_data = assessment_data.get('cost_effectiveness', {})
                
                if 'benefitCostRatio' in cost_data and 'roi' in cost_data:
                    bcr = cost_data['benefitCostRatio']
                    roi = cost_data['roi']
                    
                    # Normalize BCR (1.0 is break-even, 3.0 is excellent)
                    bcr_score = min(bcr / 3, 1.0)
                    
                    # Normalize ROI (-100% to 200% scale)
                    roi_score = min(max((roi + 100) / 300, 0), 1.0)
                    
                    cost_score = int((bcr_score * 0.6 + roi_score * 0.4) * 10)
                else:
                    # Old calculation
                    roi = cost_data.get('roi', 10)
                    # Normalize ROI (-100% to 100% scale)
                    cost_score = int(min((roi + 100) / 200, 1.0) * 10)
            domain_scores.append(('cost_effectiveness', cost_score, domain_weights['cost_effectiveness']))
        except Exception as e:
            logger.error(f"Error calculating cost score: {e}")
            domain_scores.append(('cost_effectiveness', 5, domain_weights['cost_effectiveness']))
        
        # 5. Get Environmental/Social Score
        try:
            env_score = assessment_data.get('environmental_social', {}).get('overallScore')
            if env_score is None:
                # Calculate from environmental metrics if available
                env_data = assessment_data.get('environmental_social', {})
                
                if 'pollutantConcentrationAttenuation' in env_data and 'eventBasedPollutantRemoval' in env_data:
                    # New format with updated field names
                    env_performance = (env_data['pollutantConcentrationAttenuation'] + 
                                     env_data.get('eventBasedPollutantRemoval', 0) + 
                                     env_data.get('pollutionRetentionPerformance', 0)) / 30
                    
                    # Social components
                    social_components = []
                    if 'customerSatisfaction' in env_data:
                        social_components.append(env_data['customerSatisfaction'] / 10)
                    
                    if 'communityEngagement' in env_data:
                        engagement_scores = {
                            "None": 0, "Minimal": 3, "Moderate": 5, 
                            "Extensive": 8, "Comprehensive": 10
                        }
                        social_components.append(engagement_scores.get(env_data['communityEngagement'], 5) / 10)
                    
                    if social_components:
                        social_score = sum(social_components) / len(social_components)
                        env_score = int((env_performance * 0.7 + social_score * 0.3) * 10)
                    else:
                        env_score = int(env_performance * 10)
                else:
                    # Old format
                    pollution_reduction = env_data.get('pollutantConcentrationReduction', 50)
                    satisfaction = env_data.get('customerSatisfaction', 5)
                    retention = env_data.get('pollutionRetention', 60)
                    
                    env_score = int((pollution_reduction + retention) / 20 + satisfaction)
            domain_scores.append(('environmental_social', env_score, domain_weights['environmental_social']))
        except Exception as e:
            logger.error(f"Error calculating environmental score: {e}")
            domain_scores.append(('environmental_social', 5, domain_weights['environmental_social']))
        
        # Calculate weighted average of domain scores
        total_weight = sum(weight for _, _, weight in domain_scores)
        if total_weight > 0:
            weighted_sum = sum(score * weight for _, score, weight in domain_scores)
            overall_score = weighted_sum / total_weight
        else:
            # Default if no weights
            overall_score = sum(score for _, score, _ in domain_scores) / len(domain_scores) if domain_scores else 5.0
            
        # Log the score calculation for debugging
        logger.debug(f"Domain scores: {domain_scores}")
        logger.debug(f"Overall score: {overall_score}")
        
        return round(overall_score, 1)
    except Exception as e:
        logger.error(f"Error calculating overall score: {e}", exc_info=True)
        return 5.0  # Default score if calculation fails

def create_condition_chart(assessment_data):
    """Create a bar chart showing infrastructure conditions"""
    try:
        condition_data = assessment_data.get('condition', {})
        damage_levels = condition_data.get('stormwaterHydraulicAssetCondition', {}).get('damageLevels', {})
        
        if not damage_levels:
            # No damage level data, try to see if we have overall score data
            if 'OSAC' in condition_data and 'score' in condition_data['OSAC']:
                # Create a simple gauge chart for the overall score
                score = condition_data['OSAC']['score']
                rating = condition_data['OSAC']['rating']
                
                # Create a gauge chart using a half donut
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': f"Overall Condition: {rating}", 'font': {'size': 24}},
                    gauge = {
                        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkgray"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 4], 'color': 'lightcoral'},
                            {'range': [4, 7], 'color': 'khaki'},
                            {'range': [7, 10], 'color': 'lightgreen'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 9
                        }
                    }
                ))
                
                fig.update_layout(
                    title="Infrastructure Condition Assessment",
                    font={'size': 12}
                )
                
                return fig
            else:
                return None

        # Process damage levels - handle both old and new format
        chart_data = []
        for asset, value in damage_levels.items():
            if isinstance(value, dict):
                # New format with condition and score
                condition = value.get('condition', 'unknown')
                score = value.get('score', 0)
                chart_data.append({
                    'Asset': asset.replace('_', ' ').title(), 
                    'Condition': condition,
                    'Score': score
                })
            else:
                # Old format with just condition string
                chart_data.append({
                    'Asset': asset.replace('_', ' ').title(), 
                    'Condition': value,
                    'Score': 5 if value == 'moderate' else (8 if value == 'low' else 2)
                })
        
        # Convert to DataFrame for plotting
        df = pd.DataFrame(chart_data)
        
        # Check if we have score data
        if 'Score' in df.columns and df['Score'].notna().all():
            # Create a horizontal bar chart with scores
            fig = px.bar(
                df,
                y='Asset',  # Switch x/y for horizontal bars
                x='Score',
                color='Condition',
                color_discrete_map={
                    'low': 'green',
                    'moderate': 'orange',
                    'high': 'red',
                    'unknown': 'gray'
                },
                labels={'Score': 'Condition Score (0-10)', 'Asset': 'Infrastructure Asset'},
                title='Infrastructure Condition Assessment',
                orientation='h',  # Horizontal bars
                text='Score'  # Show score values on bars
            )
            
            # Improve layout
            fig.update_layout(
                xaxis_range=[0, 10],
                yaxis_categoryorder='total ascending',
                height=400
            )
            
            # Add text formatting
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            
        else:
            # Fall back to simple categorical chart (old format)
            fig = px.bar(
                df,
                x='Asset',
                y='Condition',
                color='Condition',
                color_discrete_map={
                    'low': 'green',
                    'moderate': 'orange',
                    'high': 'red',
                    'unknown': 'gray'
                },
                title='Infrastructure Condition Assessment'
            )
            
        return fig
    except Exception as e:
        logger.error(f"Error creating condition chart: {e}", exc_info=True)
        return None

def create_performance_chart(assessment_data):
    """Create a radar chart for performance metrics"""
    try:
        func_data = assessment_data.get('functionality', {})
        hp_data = func_data.get('hydraulicPerformance', {})
        dp_data = func_data.get('hydrologicalPerformance', {})
        
        if not hp_data and not dp_data:
            return None
            
        # Select key performance metrics for radar chart
        # We want to display just the most important percentage-based metrics
        radar_metrics = {}
        
        # Hydraulic metrics
        if 'flowAttenuation' in hp_data:
            radar_metrics['Flow Attenuation'] = hp_data['flowAttenuation']
            
        if 'volumeReduction' in hp_data:
            radar_metrics['Volume Reduction'] = hp_data['volumeReduction']
            
        if 'overflowFrequency' in hp_data:
            radar_metrics['Overflow Control'] = hp_data['overflowFrequency']
            
        if 'dryWeatherFlow' in hp_data:
            radar_metrics['Dry Weather Flow'] = hp_data['dryWeatherFlow']
            
        if 'drainageDurationPerformance' in hp_data:
            radar_metrics['Drainage Performance'] = hp_data['drainageDurationPerformance']
            
        # Hydrological metrics
        if 'runoffFrequency' in dp_data:
            radar_metrics['Runoff Management'] = dp_data['runoffFrequency']
            
        if 'baseFlowPerformance' in dp_data:
            radar_metrics['Base Flow'] = dp_data['baseFlowPerformance']
            
        if 'inflowPerformance' in dp_data:
            radar_metrics['Inflow Performance'] = dp_data['inflowPerformance']
            
        if 'catchmentScalePerformance' in dp_data:
            radar_metrics['Catchment Scale'] = dp_data['catchmentScalePerformance']
            
        # Ensure we have enough metrics for a meaningful chart
        if len(radar_metrics) < 3:
            # Fall back to all available metrics if we don't have enough selected ones
            all_metrics = {}
            for key, value in hp_data.items():
                # Filter to include only numeric percentage metrics
                if isinstance(value, (int, float)) and key not in ['csoVolume', 'totalFlowVolume', 'timeToPeakDischarge', 'peakDischargeVolume']:
                    all_metrics[key.replace('_', ' ').title()] = value
                    
            for key, value in dp_data.items():
                # Filter to include only numeric percentage metrics
                if isinstance(value, (int, float)) and key not in ['annualRunoff', 'annualPrecipitation', 'inflowToSystem', 'inflowToWWTP', 'floodFrequency', 'floodDuration']:
                    all_metrics[key.replace('_', ' ').title()] = value
                    
            if len(all_metrics) >= 3:
                radar_metrics = all_metrics
            else:
                logger.warning("Not enough performance metrics available for radar chart")
                return None
        
        # Create the radar chart
        categories = list(radar_metrics.keys())
        values = [radar_metrics[cat] for cat in categories]
        
        # Create radar chart with Plotly
        fig = go.Figure()
        
        # Add the performance metrics
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance',
            line=dict(color='rgb(0, 100, 180)', width=2),
            fillcolor='rgba(0, 100, 180, 0.3)'
        ))
        
        # Add a reference line at 70% (good performance threshold)
        fig.add_trace(go.Scatterpolar(
            r=[70] * len(categories),
            theta=categories,
            fill=None,
            name='Target (70%)',
            line=dict(color='rgba(0, 180, 0, 0.6)', width=1, dash='dash')
        ))
        
        # Improve layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['0%', '25%', '50%', '75%', '100%']
                ),
                angularaxis=dict(
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            title={
                'text': 'System Performance Assessment',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error creating performance chart: {e}")
        return None

def create_environmental_chart(assessment_data):
    """Create a pie chart for environmental metrics"""
    try:
        env_data = assessment_data.get('environmental_social', {})
        if not env_data:
            return None

        # Try to use new field names first, fall back to old ones if needed
        metrics = {}
        
        # Environmental metrics
        if 'pollutantConcentrationAttenuation' in env_data:
            metrics['Pollutant Attenuation'] = env_data.get('pollutantConcentrationAttenuation', 0)
        else:
            metrics['Pollutant Reduction'] = env_data.get('pollutantConcentrationReduction', 0)
            
        if 'eventBasedPollutantRemoval' in env_data:
            metrics['Pollutant Removal'] = env_data.get('eventBasedPollutantRemoval', 0)
        
        if 'pollutionRetentionPerformance' in env_data:
            metrics['Pollution Retention'] = env_data.get('pollutionRetentionPerformance', 0)
        else:
            metrics['Pollution Retention'] = env_data.get('pollutionRetention', 0)
            
        # Water quality metrics
        if 'tssReduction' in env_data:
            metrics['TSS Reduction'] = env_data.get('tssReduction', 0)
            
        if 'nutrientReduction' in env_data:
            metrics['Nutrient Reduction'] = env_data.get('nutrientReduction', 0)
            
        if 'bacteriaReduction' in env_data:
            metrics['Bacteria Reduction'] = env_data.get('bacteriaReduction', 0)
            
        # Social metrics
        metrics['Customer Satisfaction'] = env_data.get('customerSatisfaction', 0)
        
        # Ensure we have at least some data
        if not metrics or sum(metrics.values()) == 0:
            # Fall back to dummy data if no real metrics found
            logger.warning("No valid environmental metrics found, using empty chart")
            return None

        # Create the pie chart
        fig = px.pie(
            values=list(metrics.values()),
            names=list(metrics.keys()),
            title='Environmental & Social Impact Metrics',
            color_discrete_sequence=px.colors.sequential.Greens,
            hole=0.3
        )
        
        # Improve layout
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        return fig
    except Exception as e:
        logger.error(f"Error creating environmental chart: {e}")
        return None

def show():
    # Enhanced dashboard header with subtitle and divider
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <h1 style="color: #2c3e50; margin-bottom: 5px;">Stormwater Infrastructure Dashboard</h1>
        <p style="color: #7f8c8d; font-size: 1.1em; margin-bottom: 10px;">Comprehensive infrastructure analysis and monitoring</p>
    </div>
    <hr style="margin-bottom: 25px; height: 1px; border: none; background: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.1), rgba(0,0,0,0));">
    """, unsafe_allow_html=True)
    
    # Add a demo badge for presentation
    st.markdown("""
    <div style="position: absolute; top: 10px; right: 20px; background-color: #3498db; color: white; padding: 4px 12px; 
                font-size: 0.8em; border-radius: 20px; font-weight: 500;">DEMO VERSION</div>
    """, unsafe_allow_html=True)

    try:
        # Project selection with enhanced styling
        projects = get_user_projects(st.session_state.user_id)
        if not projects:
            # Enhanced empty state message
            st.markdown("""
            <div style="text-align: center; padding: 50px 30px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0;">
                <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/clipboard-data.svg" width="70" style="margin-bottom: 20px;">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">No Projects Available</h3>
                <p style="color: #7f8c8d; margin-bottom: 25px;">Begin by creating your first project to start assessing stormwater infrastructure.</p>
                <div style="background-color: #3498db; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; cursor: pointer;">
                    Create New Project
                </div>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Add a container for project selection
        st.markdown("""
        <style>
        .project-selector {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #eee;
        }
        </style>
        <div class="project-selector">
            <p style="margin-bottom:10px; font-weight:500; color:#2c3e50;">Select a project to view:</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected_project = st.selectbox(
            "",  # Remove label as we added it with custom styling
            options=projects,
            format_func=lambda x: x['name']
        )

        # Get project's assessments
        assessments = get_assessments(project_id=selected_project['id'])
        if not assessments:
            # Enhanced no assessments message
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0; border: 1px dashed #ddd;">
                <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/file-earmark-bar-graph.svg" width="50" style="margin-bottom: 15px;">
                <h3 style="margin-bottom: 10px; color: #2c3e50;">No Assessments Found</h3>
                <p style="color: #7f8c8d; margin-bottom: 20px;">Project "{selected_project['name']}" does not have any infrastructure assessments yet.</p>
                <div style="background-color: #3498db; color: white; padding: 8px 16px; border-radius: 5px; display: inline-block; cursor: pointer; font-size: 0.9em;">
                    Create First Assessment
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

        latest_assessment = assessments[0]['data'] if assessments else None
        if not latest_assessment:
            st.error("Could not load assessment data")
            return

        # Project Overview Section - with enhanced styling
        st.markdown("""
        <h2 style="color: #2c3e50; margin-top: 10px; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 2px solid #3498db;">
            Project Overview
        </h2>
        """, unsafe_allow_html=True)
        
        # Calculate the overall score and get rating
        overall_score = calculate_overall_score(latest_assessment)
        
        # Enhanced score color scale
        if overall_score >= 8:
            score_color = "#27ae60"  # Green for good
            score_rating = "Good"
            gradient = "linear-gradient(135deg, #27ae60, #2ecc71)"
        elif overall_score >= 6:
            score_color = "#f39c12"  # Orange for fair
            score_rating = "Fair"
            gradient = "linear-gradient(135deg, #f39c12, #f1c40f)"
        else:
            score_color = "#e74c3c"  # Red for poor
            score_rating = "Poor"
            gradient = "linear-gradient(135deg, #e74c3c, #c0392b)"
        
        # Create row with project summary - enhanced design
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Project title and description with enhanced styling
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <h3 style="color: #2c3e50; margin-top: 0; margin-bottom: 10px;">{selected_project['name']}</h3>
                    <p style="color: #7f8c8d; margin-bottom: 0;">{selected_project.get('description', 'No description available.')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Create an enhanced score card with gradient background
                st.markdown(f"""
                <div style="background: {gradient}; padding:20px; border-radius:10px; text-align:center; color:white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <p style="margin:0 0 5px 0; font-size:0.9em; text-transform:uppercase; letter-spacing:1px; opacity:0.9;">Overall Score</p>
                    <h1 style="margin:0 0 5px 0; font-size:2.5em; font-weight:700; color:white;">{overall_score:.1f}<span style="font-size:0.5em; opacity:0.8;">/10</span></h1>
                    <p style="margin:0; font-weight:500; color:white; letter-spacing:1px;">{score_rating}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Custom styling for metrics
        st.markdown("""
        <style>
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            height: 100%;
            margin-top: 20px;
        }
        .metric-title {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .metric-value {
            color: #2c3e50;
            font-size: 2em;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .metric-detail {
            color: #95a5a6;
            font-size: 0.8em;
        }
        .metric-icon {
            color: #3498db;
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # More overview metrics with enhanced presentation
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            points_count = len(latest_assessment.get('infrastructure_points', []))
            # Use demo value if none available
            if points_count == 0:
                points_count = 12
                
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🏗️</div>
                <div class="metric-title">INFRASTRUCTURE POINTS</div>
                <div class="metric-value">{points_count}</div>
                <div class="metric-detail">Across the project</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            assessments_count = len(assessments)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-title">TOTAL ASSESSMENTS</div>
                <div class="metric-value">{assessments_count}</div>
                <div class="metric-detail">Project history</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            try:
                recent = [a for a in assessments if 
                        datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(days=30)]
                recent_count = len(recent)
            except Exception as e:
                logger.error(f"Error calculating recent assessments: {e}")
                recent_count = "N/A"
                
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🕒</div>
                <div class="metric-title">RECENT ASSESSMENTS</div>
                <div class="metric-value">{recent_count}</div>
                <div class="metric-detail">Last 30 days</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            latest_date = datetime.fromisoformat(assessments[0]['timestamp'])
            formatted_date = latest_date.strftime("%b %d")
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📆</div>
                <div class="metric-title">LATEST UPDATE</div>
                <div class="metric-value">{formatted_date}</div>
                <div class="metric-detail">{latest_date.strftime("%Y")}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add domain scores in expandable section
        with st.expander("Assessment Domain Scores"):
            # Extract domain scores
            domain_scores = {
                'Condition': latest_assessment.get('condition', {}).get('OSAC', {}).get('score', None),
                'Functionality': latest_assessment.get('functionality', {}).get('overallFunctionality', {}).get('score', None),
                'Time Effectiveness': latest_assessment.get('time_effectiveness', {}).get('overallTimeScore', None),
                'Cost Effectiveness': latest_assessment.get('cost_effectiveness', {}).get('overallCostScore', None),
                'Environmental & Social': latest_assessment.get('environmental_social', {}).get('overallScore', None)
            }
            
            # Create a progress bar for each domain score
            for domain, score in domain_scores.items():
                if score is not None:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(f"{domain}:")
                    with col2:
                        # Calculate color based on score
                        color = "red" if score < 4 else "orange" if score < 7 else "green"
                        # Create a progress bar using HTML
                        st.markdown(f"""
                        <div style="display: flex; align-items: center;">
                            <div style="background-color: #f0f0f0; width: 100%; height: 20px; border-radius: 5px; overflow: hidden;">
                                <div style="background-color: {color}; width: {score*10}%; height: 100%; border-radius: 5px;"></div>
                            </div>
                            <span style="margin-left: 10px; font-weight: bold;">{score}/10</span>
                        </div>
                        """, unsafe_allow_html=True)

        # Visualizations
        st.header("Assessment Analysis")

        # Infrastructure Condition
        condition_chart = create_condition_chart(latest_assessment)
        if condition_chart:
            st.plotly_chart(condition_chart, use_container_width=True)

        col1, col2 = st.columns(2)

        # Performance Metrics
        with col1:
            performance_chart = create_performance_chart(latest_assessment)
            if performance_chart:
                st.plotly_chart(performance_chart)

        # Environmental Impact
        with col2:
            environmental_chart = create_environmental_chart(latest_assessment)
            if environmental_chart:
                st.plotly_chart(environmental_chart)

        # Infrastructure Map
        st.header("Infrastructure Locations")
        from components.map_view import show_infrastructure_map
        if 'infrastructure_points' in latest_assessment:
            show_infrastructure_map(latest_assessment)

        # Historical Trends
        st.header("Historical Assessment Trends")
        
        # Prepare data for historical trends
        trend_data = []
        for assessment in assessments:
            date = datetime.fromisoformat(assessment['timestamp'])
            assessment_data = assessment['data']
            
            # Calculate overall score for this assessment
            overall_score = calculate_overall_score(assessment_data)
            
            # Extract domain scores
            domain_scores = {
                'condition': assessment_data.get('condition', {}).get('OSAC', {}).get('score', None),
                'functionality': assessment_data.get('functionality', {}).get('overallFunctionality', {}).get('score', None),
                'time_effectiveness': assessment_data.get('time_effectiveness', {}).get('overallTimeScore', None),
                'cost_effectiveness': assessment_data.get('cost_effectiveness', {}).get('overallCostScore', None),
                'environmental_social': assessment_data.get('environmental_social', {}).get('overallScore', None)
            }
            
            # Add record with all available scores
            trend_record = {
                'date': date,
                'overall_score': overall_score
            }
            
            # Add domain scores (if available)
            for domain, score in domain_scores.items():
                if score is not None:
                    trend_record[domain.replace('_', ' ').title()] = score
            
            trend_data.append(trend_record)
        
        if trend_data:
            # Sort by date
            trend_data.sort(key=lambda x: x['date'])
            
            # Convert to DataFrame for Plotly
            df = pd.DataFrame(trend_data)
            
            # Check if we have multiple assessments for trends
            if len(df) > 1:
                # Plot the trend chart for overall score and domain scores
                columns_to_plot = ['overall_score'] + [col for col in df.columns if col not in ['date', 'overall_score']]
                
                # Create a nice color map for the lines
                custom_colors = {
                    'overall_score': 'rgba(0, 0, 128, 1)',  # Navy blue for overall score
                    'Condition': 'rgba(220, 20, 60, 0.8)',  # Crimson
                    'Functionality': 'rgba(50, 205, 50, 0.8)',  # Lime green
                    'Time Effectiveness': 'rgba(255, 165, 0, 0.8)',  # Orange
                    'Cost Effectiveness': 'rgba(106, 90, 205, 0.8)',  # Slate blue
                    'Environmental Social': 'rgba(60, 179, 113, 0.8)'  # Medium sea green
                }
                
                fig = go.Figure()
                
                # Add traces for each score type
                for column in columns_to_plot:
                    if column in df.columns:
                        color = custom_colors.get(column, 'rgba(128, 128, 128, 0.8)')  # Default gray for others
                        fig.add_trace(go.Scatter(
                            x=df['date'],
                            y=df[column],
                            mode='lines+markers',
                            name=column,
                            line=dict(color=color, width=3 if column == 'overall_score' else 2),
                            marker=dict(size=8 if column == 'overall_score' else 6)
                        ))
                
                # Improve layout
                fig.update_layout(
                    title='Assessment Score Trends Over Time',
                    xaxis_title='Assessment Date',
                    yaxis_title='Score (0-10)',
                    yaxis=dict(range=[0, 10]),
                    hovermode='x unified',
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=-0.3,
                        xanchor='center',
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add explanatory text
                if len(df) > 2:
                    # Calculate trend
                    first_score = df['overall_score'].iloc[0]
                    last_score = df['overall_score'].iloc[-1]
                    trend_direction = "improved" if last_score > first_score else "declined" if last_score < first_score else "remained stable"
                    
                    st.info(f"The overall infrastructure condition has {trend_direction} from {first_score:.1f} to {last_score:.1f} over the assessment period.")
            else:
                # If only one assessment, show message
                st.info("More assessments are needed to show historical trends. Only one assessment is available.")
        else:
            st.warning("No assessment data available for trend analysis.")

        # Export Section
        st.header("Export Options")
        if st.button("Generate Assessment Report"):
            try:
                from utils.report import generate_report
                with st.spinner("Generating comprehensive report..."):
                    report_buffer = generate_report(latest_assessment, project_name=selected_project['name'])
                    st.success("Report generated successfully!")
                    st.download_button(
                        label="📥 Download Assessment Report",
                        data=report_buffer,
                        file_name=f"assessment_report_{selected_project['name']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                logger.error(f"Error generating report: {e}")
                st.error("Failed to generate report. Please try again.")

    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        st.error("An error occurred while loading the dashboard. Please try again.")