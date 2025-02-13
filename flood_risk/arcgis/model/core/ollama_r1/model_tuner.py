# core/ml_models/model_tuner.py
from ollama import Client
import pandas as pd
from sklearn.model_selection import train_test_split

class ModelTuner:
    def __init__(self, base_model='r1'):
        self.client = Client()
        self.base_model = base_model
        self.tuned_model_name = f"{base_model}-stormwater"

    def prepare_training_data(self):
        # Convert your stormwater data to text prompts
        df = pd.read_csv('data/stormwater_metrics.csv')
        
        training_data = []
        for _, row in df.iterrows():
            prompt = f"""
            Assess stormwater infrastructure condition based on:
            - Pipe diameter: {row['pipe_diameter']}
            - Failure probability: {row['failure_probability']}
            - Structural condition: {row['structural_condition']}
            - Flow attenuation: {row['flow_attenuation']}
            Output score between 0-100.
            """
            
            training_data.append({
                "prompt": prompt,
                "completion": str(row['condition_score'])
            })
        
        return training_data

    def tune_model(self):
        training_data = self.prepare_training_data()
        response = self.client.create(
            model=self.tuned_model_name,
            base_model=self.base_model,
            examples=training_data,
            parameters={
                "num_epochs": 10,
                "learning_rate": 0.0001,
                "batch_size": 4
            }
        )
        return response