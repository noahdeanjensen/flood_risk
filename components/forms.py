import streamlit as st

def condition_assessment_form():
    st.header("Stormwater Condition Assessment")
    
    shac = st.expander("Stormwater Hydraulic Asset Condition (SHAC)")
    with shac:
        pipe_diameter = st.number_input("Pipe diameter/width", min_value=0.0)
        inspection_freq = st.selectbox(
            "Routine inspection frequency",
            ["Monthly", "Quarterly", "Semi-annually", "Annually"]
        )
        
        damage_levels = {
            "Pipes": st.slider("Damage level - Pipes", 0, 10, 5),
            "Drainage inlets": st.slider("Damage level - Drainage inlets", 0, 10, 5),
            "Manholes": st.slider("Damage level - Manholes", 0, 10, 5),
            "Ditches": st.slider("Damage level - Ditches", 0, 10, 5)
        }
    
    return {
        "pipe_diameter": pipe_diameter,
        "inspection_freq": inspection_freq,
        "damage_levels": damage_levels
    }

def functionality_assessment_form():
    st.header("Functionality Assessment")
    
    hydraulic = st.expander("Hydraulic Performance")
    with hydraulic:
        flow_attenuation = st.slider("Flow attenuation at outlet", 0, 100, 50)
        volume_reduction = st.slider("Volume reduction at outlet", 0, 100, 50)
        cso = st.number_input("Combined sewer overflows (CSO)", min_value=0)
    
    return {
        "flow_attenuation": flow_attenuation,
        "volume_reduction": volume_reduction,
        "cso": cso
    }

def time_effectiveness_form():
    st.header("Time-Effectiveness Assessment")
    
    lifespan = st.number_input("Lifespan (years)", min_value=0)
    maintenance_lag = st.number_input("Maintenance lag time (days)", min_value=0)
    
    return {
        "lifespan": lifespan,
        "maintenance_lag": maintenance_lag
    }

def cost_effectiveness_form():
    st.header("Cost-Effectiveness Assessment")
    
    costs = {
        "preliminary": st.number_input("Preliminary costs ($)", min_value=0),
        "construction": st.number_input("Construction costs ($)", min_value=0),
        "operational": st.number_input("Operational costs ($)", min_value=0)
    }
    
    return costs

def environmental_social_form():
    st.header("Environmental and Social Impact Assessment")
    
    pollutant_reduction = st.slider("Pollutant concentration reduction (%)", 0, 100, 50)
    satisfaction = st.slider("Customer satisfaction", 0, 10, 7)
    
    return {
        "pollutant_reduction": pollutant_reduction,
        "satisfaction": satisfaction
    }
