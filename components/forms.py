import streamlit as st
from components.heat_map import create_risk_heat_map, calculate_risk_levels

def condition_assessment_form():
    st.header("Stormwater Condition Assessment")

    # Hydraulic Asset Condition (SHAC)
    shac = st.expander("Stormwater Hydraulic Asset Condition (SHAC)")
    with shac:
        pipe_diameter = st.text_input("Pipe diameter/width", "24 inches")
        inspection_freq = st.selectbox(
            "Routine inspection frequency",
            ["annually", "semi-annually", "quarterly", "monthly"]
        )

        # Damage levels
        damage_levels = {
            "pipes": st.select_slider("Pipes damage level", ["low", "moderate", "high"], "moderate"),
            "culverts": st.select_slider("Culverts damage level", ["low", "moderate", "high"], "low"),
            "reinforcedConcreteBoxes": st.select_slider("Reinforced concrete boxes damage level", ["low", "moderate", "high"], "high"),
            "drainageInlets": st.select_slider("Drainage inlets damage level", ["low", "moderate", "high"], "moderate"),
            "trenchDrains": st.select_slider("Trench drains damage level", ["low", "moderate", "high"], "low"),
            "manholes": st.select_slider("Manholes damage level", ["low", "moderate", "high"], "high"),
            "junctionBoxes": st.select_slider("Junction boxes damage level", ["low", "moderate", "high"], "moderate"),
            "ditches": st.select_slider("Ditches damage level", ["low", "moderate", "high"], "low"),
            "channels": st.select_slider("Channels damage level", ["low", "moderate", "high"], "moderate"),
            "swales": st.select_slider("Swales damage level", ["low", "moderate", "high"], "high"),
            "energyDissipators": st.select_slider("Energy dissipators damage level", ["low", "moderate", "high"], "low")
        }

    # Treatment Asset Condition (STAC)
    stac = st.expander("Stormwater Treatment Asset Condition (STAC)")
    with stac:
        treatment_damage_levels = {
            "outfalls": st.select_slider("Outfalls damage level", ["low", "moderate", "high"], "moderate"),
            "bioRetentionBasins": st.select_slider("Bioretention basins/filters damage level", ["low", "moderate", "high"], "low"),
            "dryDetentionBasins": st.select_slider("Dry detention basins damage level", ["low", "moderate", "high"], "high"),
            "grossSolidsRemovalDevices": st.select_slider("Gross solids removal devices damage level", ["low", "moderate", "high"], "moderate"),
            "infiltrationBasins": st.select_slider("Infiltration basins/trenches damage level", ["low", "moderate", "high"], "low"),
            "levelSpreaders": st.select_slider("Level spreaders damage level", ["low", "moderate", "high"], "high"),
            "permeablePavements": st.select_slider("Permeable pavements damage level", ["low", "moderate", "high"], "moderate"),
            "sandFilters": st.select_slider("Sand filters damage level", ["low", "moderate", "high"], "low"),
            "sedimentTraps": st.select_slider("Sediment traps damage level", ["low", "moderate", "high"], "high"),
            "wetlands": st.select_slider("Wetlands damage level", ["low", "moderate", "high"], "moderate"),
            "hydrodynamicSeparators": st.select_slider("Hydrodynamic separators damage level", ["low", "moderate", "high"], "low"),
            "treeBoxFilters": st.select_slider("Tree box filters damage level", ["low", "moderate", "high"], "high"),
            "vegetatedSwales": st.select_slider("Vegetated swales damage level", ["low", "moderate", "high"], "moderate"),
            "wetBasins": st.select_slider("Wet basins damage level", ["low", "moderate", "high"], "low")
        }

    # Structural Condition (SASC)
    sasc = st.expander("Stormwater Asset Structural Condition (SASC)")
    with sasc:
        structural_metrics = {
            "probabilityOfFailure": st.slider("Probability of failure (%)", 0, 100, 10),
            "safetyFactorInAllowableStressDesign": st.number_input("Safety factor in allowable stress design", 1.0, 5.0, 1.5),
            "reserveStrengthFactor": st.number_input("Reserve strength factor", 1.0, 5.0, 2.0),
            "robustness": st.select_slider("Robustness", ["low", "moderate", "high"], "high"),
            "resilience": st.select_slider("Resilience", ["low", "moderate", "high"], "moderate")
        }

    return {
        "assessmentType": "Stormwater Condition Assessment",
        "stormwaterHydraulicAssetCondition": {
            "pipeDiameterWidth": pipe_diameter,
            "routineInspectionFrequency": inspection_freq,
            "damageLevels": damage_levels
        },
        "stormwaterAssetCondition": {
            "damageLevels": treatment_damage_levels
        },
        "stormwaterAssetStructuralCondition": structural_metrics,
        "OSAC": "fair"  # This could be calculated based on other metrics
    }

def functionality_assessment_form():
    st.header("Functionality Assessment")

    # Hydraulic Performance
    hydraulic = st.expander("Hydraulic Performance (HP)")
    with hydraulic:
        hp_metrics = {
            "flowAttenuation": st.slider("Flow attenuation at outlet (%)", 0, 100, 50),
            "volumeReduction": st.slider("Volume reduction at outlet (%)", 0, 100, 50),
            "csoFrequency": st.number_input("Combined sewer overflows (CSO) count", 0, 100, 0),
            "pumpingStationOverflow": st.number_input("Pumping station overflow incidents", 0, 100, 0),
            "dryWeatherFlow": st.number_input("Dry weather flow (L/s)", 0.0, 1000.0, 0.0),
            "overflowFrequency": st.number_input("Overflow frequency (times/year)", 0, 100, 0),
            "drainageDurationFrequency": st.number_input("Drainage duration frequency (hours)", 0, 168, 24)
        }

    # Hydrological Performance
    hydrological = st.expander("Hydrological Performance (DP)")
    with hydrological:
        dp_metrics = {
            "runoffFrequency": st.number_input("Runoff frequency (events/year)", 0, 100, 12),
            "meanAnnualRunoffVolume": st.number_input("Mean annual runoff volume (m³)", 0, 1000000, 10000),
            "baseFlowVolume": st.number_input("Base flow volume (m³/day)", 0, 10000, 100),
            "infiltrationFlow": st.number_input("Filtered stormwater flow (L/s)", 0.0, 1000.0, 10.0),
            "catchmentFloodFrequency": st.number_input("Catchment-scale flood frequency (events/year)", 0, 50, 2)
        }

    return {
        "hydraulicPerformance": hp_metrics,
        "hydrologicalPerformance": dp_metrics
    }

def time_effectiveness_form():
    st.header("Time-Effectiveness Assessment")

    time_condition = st.expander("Time Condition (TC)")
    with time_condition:
        tc_metrics = {
            "lifespan": st.number_input("Lifespan (years)", 0, 100, 25),
            "maintenanceLagTime": st.number_input("Lag-time in maintenance actions (days)", 0, 365, 7),
            "floodDuration": st.number_input("Catchment-scale flood duration (hours)", 0, 168, 24)
        }

    return tc_metrics

def cost_effectiveness_form():
    st.header("Cost-Effectiveness Assessment")

    cost_condition = st.expander("Cost Condition (CC)")
    with cost_condition:
        cc_metrics = {
            "preliminaryCosts": st.number_input("Preliminary costs ($)", 0, 1000000, 10000),
            "constructionCosts": st.number_input("Construction costs ($)", 0, 10000000, 100000),
            "operationalCosts": st.number_input("Operational costs ($/year)", 0, 1000000, 50000),
            "roi": st.number_input("Return on investment (%)", -100, 1000, 10)
        }

    return cc_metrics

def environmental_social_form():
    st.header("Environmental and Social Impact Assessment")

    env_social = st.expander("Environmental and Social Condition (ESC)")
    with env_social:
        es_metrics = {
            "pollutantConcentrationReduction": st.slider("Pollutant concentration reduction (%)", 0, 100, 50),
            "pollutantRemovalRate": st.slider("Event-based pollutant removal rate (%)", 0, 100, 60),
            "pollutionRetention": st.slider("Pollution retention performance (%)", 0, 100, 70),
            "customerSatisfaction": st.slider("Customer satisfaction rating", 0, 10, 7),
            "safetyMetrics": {
                "accidentFrequency": st.number_input("Accident frequency (incidents/year)", 0, 100, 0),
                "accidentSeverity": st.select_slider("Accident severity level", ["low", "moderate", "high"], "low")
            }
        }

    return es_metrics

def infrastructure_location_form():
    st.header("Infrastructure Location Data")

    # Initialize infrastructure points in session state
    if 'infrastructure_points' not in st.session_state:
        st.session_state.infrastructure_points = []

    with st.expander("Add Infrastructure Point"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Location Name")
            type_options = [
                "pipes", "culverts", "drainageInlets", "manholes",
                "channels", "outfalls", "bioRetentionBasins"
            ]
            point_type = st.selectbox("Infrastructure Type", type_options)
            age = st.number_input("Age (years)", 0, 100, 0)

        with col2:
            latitude = st.number_input("Latitude", -90.0, 90.0, 40.7128)
            longitude = st.number_input("Longitude", -180.0, 180.0, -74.0060)
            last_maintenance = st.number_input("Days Since Last Maintenance", 0, 1000, 0)

        if st.button("Add Point"):
            point = {
                'name': name,
                'type': point_type,
                'latitude': latitude,
                'longitude': longitude,
                'age': age,
                'last_maintenance_days': last_maintenance
            }
            st.session_state.infrastructure_points.append(point)
            st.success(f"Added {name} to infrastructure points")

    # Display existing points
    if st.session_state.infrastructure_points:
        st.subheader("Infrastructure Points")
        for i, point in enumerate(st.session_state.infrastructure_points):
            st.text(f"{i+1}. {point['name']} ({point['type']})")

        if st.button("Clear All Points"):
            st.session_state.infrastructure_points = []
            st.rerun()

    return {'infrastructure_points': st.session_state.infrastructure_points}