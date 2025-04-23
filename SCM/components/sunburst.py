import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_sunburst_chart(assessment_data):
    """Create a sunburst chart showing project progress and component relationships"""
    try:
        logger.debug("Creating sunburst chart with assessment data")
        logger.debug(f"Assessment data keys: {assessment_data.keys() if assessment_data else 'None'}")

        if not assessment_data:
            logger.warning("No assessment data provided")
            return go.Figure()

        # Initialize data structure
        data = {
            'ids': ['root'],
            'labels': ['Project Assessment'],
            'parents': [''],
            'values': [100],
            'colors': ['#1f77b4']
        }

        # Add main categories
        categories = {
            'condition': 'Infrastructure Condition',
            'functionality': 'System Functionality',
            'time_effectiveness': 'Time Effectiveness',
            'cost_effectiveness': 'Cost Analysis',
            'environmental_social': 'Environmental Impact'
        }

        for key, label in categories.items():
            logger.debug(f"Processing category: {key}")
            data['ids'].append(key)
            data['labels'].append(label)
            data['parents'].append('root')
            data['values'].append(80)
            data['colors'].append('#2ca02c')

            try:
                # Add subcategories based on available data
                if key == 'condition' and 'condition' in assessment_data:
                    condition_data = assessment_data.get('condition', {})
                    logger.debug(f"Condition data: {condition_data}")

                    asset_condition = condition_data.get('stormwaterHydraulicAssetCondition', {})
                    damage_levels = asset_condition.get('damageLevels', {})

                    for asset, level in damage_levels.items():
                        score = 100 if level == 'low' else 50 if level == 'moderate' else 0
                        data['ids'].append(f'condition_{asset}')
                        data['labels'].append(asset.title())
                        data['parents'].append('condition')
                        data['values'].append(score)
                        color = '#2ecc71' if level == 'low' else '#f1c40f' if level == 'moderate' else '#e74c3c'
                        data['colors'].append(color)

                elif key == 'functionality' and 'functionality' in assessment_data:
                    func_data = assessment_data.get('functionality', {})
                    logger.debug(f"Functionality data: {func_data}")

                    performance = func_data.get('hydraulicPerformance', {})
                    for metric, value in performance.items():
                        try:
                            numeric_value = float(value)
                            data['ids'].append(f'functionality_{metric}')
                            data['labels'].append(metric.replace('_', ' ').title())
                            data['parents'].append('functionality')
                            data['values'].append(numeric_value)
                            data['colors'].append('#3498db')
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error converting value for metric {metric}: {e}")

                elif key == 'environmental_social' and 'environmental_social' in assessment_data:
                    env_data = assessment_data.get('environmental_social', {})
                    logger.debug(f"Environmental data: {env_data}")

                    metrics = {
                        'pollutant': env_data.get('pollutantConcentrationReduction', 0),
                        'satisfaction': env_data.get('customerSatisfaction', 0) * 10
                    }
                    for metric, value in metrics.items():
                        try:
                            numeric_value = float(value)
                            data['ids'].append(f'env_{metric}')
                            data['labels'].append(metric.title())
                            data['parents'].append('environmental_social')
                            data['values'].append(numeric_value)
                            data['colors'].append('#27ae60')
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error converting value for metric {metric}: {e}")

            except Exception as e:
                logger.error(f"Error processing category {key}: {e}")
                continue

        logger.debug("Creating Plotly figure")
        fig = go.Figure()

        # Base sunburst
        fig.add_trace(go.Sunburst(
            ids=data['ids'],
            labels=data['labels'],
            parents=data['parents'],
            values=data['values'],
            marker=dict(colors=data['colors']),
            branchvalues='total',
            maxdepth=2
        ))

        # Update layout
        fig.update_layout(
            width=800,
            height=800,
            showlegend=False,
            margin=dict(t=100, l=0, r=0, b=0)
        )

        return fig

    except Exception as e:
        logger.error(f"Failed to create sunburst chart: {str(e)}", exc_info=True)
        st.error(f"Error creating visualization: {str(e)}")
        return go.Figure()