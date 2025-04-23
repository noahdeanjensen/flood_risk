import streamlit as st
from components.heat_map import create_risk_heat_map, calculate_risk_levels

def condition_assessment_form():
    st.header("Stormwater Condition Assessment")

    # Stormwater Hydraulic Asset Condition (SHAC)
    shac = st.expander("Stormwater Hydraulic Asset Condition (SHAC)")
    with shac:
        # Pipe diameter selection with detailed scoring criteria
        pipe_diameter = st.selectbox(
            "Pipe diameter (S)",
            ["S ≤ 18 in", "18 in < S ≤ 48 in", "48 in < S ≤ 120 in", "S > 120 in"]
        )
        
        # Inspection frequency based on pipe diameter
        inspection_mapping = {
            "S ≤ 18 in": ["Exceeds 12 years (Poor, score: 4)", "8-12 years (Fair, score: 5)", "3-7 years (Good, score: 6)", "Less than 3 years (Excellent, score: 7)"],
            "18 in < S ≤ 48 in": ["Exceeds 7 years (Poor, score: 5)", "5-7 years (Fair, score: 6)", "3-5 years (Good, score: 7)", "Less than 3 years (Excellent, score: 8)"],
            "48 in < S ≤ 120 in": ["Exceeds 5 years (Poor, score: 6)", "3-5 years (Fair, score: 7)", "Every 3 years (Good, score: 8)", "Less than 3 years (Excellent, score: 9)"],
            "S > 120 in": ["Exceeds 3 years (Poor, score: 4)", "2-3 years (Fair, score: 5)", "1-2 years (Good, score: 6)", "Less than 1 year (Excellent, score: 7)"]
        }
        
        inspection_freq = st.selectbox(
            "Routine inspection frequency",
            inspection_mapping[pipe_diameter]
        )
        
        # Extract score from selection
        pipe_score = int(inspection_freq.split("score: ")[1].split(")")[0])
        
        st.info(f"Pipe Assessment Score: {pipe_score}/10")
        
        # Asset-specific assessment with standardized scoring
        st.subheader("Asset-Specific Assessment")
        
        # Hydraulic Asset assessment
        damage_levels = {}
        
        # Pipes, Culverts, RCBs
        conveyance_assets = {
            "pipes": "Pipes",
            "culverts": "Culverts",
            "reinforcedConcreteBoxes": "Reinforced concrete boxes (RCBs)"
        }
        
        for key, label in conveyance_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                damage_level = st.select_slider(
                    f"{label} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    "Fair (4-6)",
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in damage_level:
                    score_range = range(0, 4)
                elif "Fair" in damage_level:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                precise_score = st.selectbox(f"Score", score_range, index=len(score_range)//2, key=f"score_{key}")
                damage_levels[key] = {"condition": damage_level, "score": precise_score}
        
        # Drainage infrastructure
        st.markdown("#### Drainage Infrastructure")
        drainage_assets = {
            "drainageInlets": "Drainage inlets (Annual inspection: Good/7)",
            "trenchDrains": "Trench drains (Annual inspection: Good/7)", 
            "manholes": "Manholes (5-7 years: Fair/6)",
            "junctionBoxes": "Junction boxes (5-7 years: Fair/6)"
        }
        
        for key, label in drainage_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                default_condition = "Good (7-10)" if "Annual" in label else "Fair (4-6)"
                default_score = 7 if "Annual" in label else 6
                condition = st.select_slider(
                    f"{label.split('(')[0]} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    default_condition,
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in condition:
                    score_range = range(0, 4)
                elif "Fair" in condition:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                precise_score = st.selectbox(f"Score", score_range, 
                                            index=list(score_range).index(default_score) if default_score in score_range else len(score_range)//2, 
                                            key=f"score_{key}")
                damage_levels[key] = {"condition": condition, "score": precise_score}
        
        # Open channels 
        st.markdown("#### Open Channels and Erosion Control")
        channel_assets = {
            "ditches": "Ditches (>7 years: Poor/3)",
            "channels": "Channels (>7 years: Poor/3)",
            "swales": "Swales (>7 years: Poor/3)",
            "energyDissipators": "Energy dissipators (>7 years: Poor/3)"
        }
        
        for key, label in channel_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                condition = st.select_slider(
                    f"{label.split('(')[0]} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    "Poor (0-3)",
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in condition:
                    score_range = range(0, 4)
                elif "Fair" in condition:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                precise_score = st.selectbox(f"Score", score_range, 
                                           index=list(score_range).index(3) if 3 in score_range else 0, 
                                           key=f"score_{key}")
                damage_levels[key] = {"condition": condition, "score": precise_score}

    # Treatment Asset Condition (STAC)
    stac = st.expander("Stormwater Treatment Asset Condition (STAC)")
    with stac:
        treatment_damage_levels = {}
        
        # Outfalls
        st.markdown("#### Outfalls and Basin Systems")
        outfall_assets = {
            "outfalls": "Outfalls (1-2 years: Fair/6)"
        }
        
        for key, label in outfall_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                condition = st.select_slider(
                    f"{label.split('(')[0]} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    "Fair (4-6)",
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in condition:
                    score_range = range(0, 4)
                elif "Fair" in condition:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                precise_score = st.selectbox(f"Score", score_range, 
                                           index=list(score_range).index(6) if 6 in score_range else len(score_range)//2, 
                                           key=f"score_{key}")
                treatment_damage_levels[key] = {"condition": condition, "score": precise_score}
        
        # Basin treatment systems
        basin_assets = {
            "bioRetentionBasins": "Bioretention basins (1-2 years: Fair/6)",
            "dryDetentionBasins": "Dry detention basins (1-2 years: Fair/6)",
            "infiltrationBasins": "Infiltration basins (1-2 years: Fair/5)",
            "wetBasins": "Wet basins (1-2 years: Fair/5)"
        }
        
        for key, label in basin_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                condition = st.select_slider(
                    f"{label.split('(')[0]} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    "Fair (4-6)",
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in condition:
                    score_range = range(0, 4)
                elif "Fair" in condition:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                default_score = 5 if "5" in label else 6
                precise_score = st.selectbox(f"Score", score_range, 
                                           index=list(score_range).index(default_score) if default_score in score_range else len(score_range)//2, 
                                           key=f"score_{key}")
                treatment_damage_levels[key] = {"condition": condition, "score": precise_score}
        
        # Advanced treatment systems
        st.markdown("#### Advanced Treatment Systems")
        advanced_assets = {
            "grossSolidsRemovalDevices": "Gross solids removal devices (Annually: Good/10)",
            "permeablePavements": "Permeable pavements (Annually: Good/10)",
            "sandFilters": "Sand filters (>1 year: Poor/3)",
            "infiltrationTrenches": "Infiltration trenches (1-2 years: Fair/6)",
            "levelSpreaders": "Level spreaders (1-2 years: Fair/5)",
            "sedimentTraps": "Sediment traps (Annually: Good/7)",
            "hydrodynamicSeparators": "Hydrodynamic separators (Annually: Good/8)",
            "treeBoxFilters": "Tree box filters (Annually: Good/8)",
            "vegetatedSwales": "Vegetated swales (Annually: Good/7)"
        }
        
        for key, label in advanced_assets.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                if "Annually" in label:
                    default_condition = "Good (7-10)"
                elif ">1 year" in label:
                    default_condition = "Poor (0-3)"
                else:
                    default_condition = "Fair (4-6)"
                
                condition = st.select_slider(
                    f"{label.split('(')[0]} condition", 
                    ["Poor (0-3)", "Fair (4-6)", "Good (7-10)"], 
                    default_condition,
                    key=f"slider_{key}"
                )
            with col2:
                if "Poor" in condition:
                    score_range = range(0, 4)
                elif "Fair" in condition:
                    score_range = range(4, 7)
                else:
                    score_range = range(7, 11)
                
                # Extract default score from label
                default_score = int(label.split("/")[1].split(")")[0])
                precise_score = st.selectbox(f"Score", score_range, 
                                           index=list(score_range).index(default_score) if default_score in score_range else len(score_range)//2, 
                                           key=f"score_{key}")
                treatment_damage_levels[key] = {"condition": condition, "score": precise_score}
    
    # Structural Condition (SASC)
    sasc = st.expander("Stormwater Asset Structural Condition (SASC)")
    with sasc:
        st.markdown("#### Structural Integrity Metrics")
        st.markdown("These metrics assess the structural reliability of stormwater assets.")
        
        structural_metrics = {
            "probabilityOfFailure": st.slider("Probability of Failure (Pf) %", 0, 100, 74, 
                                            help="Indicating the instantaneous probability of failure"),
            "safetyFactorInAllowableStressDesign": st.slider("Safety Factor in Allowable Stress Design (SF) %", 0, 100, 82,
                                                           help="Providing a design margin over theoretical design capacity"),
            "reserveStrengthFactor": st.slider("Reserve Strength Factor (R1) %", 0, 100, 83,
                                             help="Ratio of the load-carrying capacity of the intact structure to the applied load"),
            "robustness": st.slider("Robustness (RO) %", 0, 100, 77,
                                   help="The ability of a structure to prevent failure progression"),
            "resilience": st.slider("Resilience (RE) %", 0, 100, 82,
                                   help="Reduce probabilities and consequences of failure and recovery time")
        }
        
        # Calculate overall score (0-10)
        weighted_scores = []
        for key, value in damage_levels.items():
            weighted_scores.append(value["score"])
        for key, value in treatment_damage_levels.items():
            weighted_scores.append(value["score"])
        
        # Average of all scores
        overall_condition_score = int(sum(weighted_scores) / len(weighted_scores)) if weighted_scores else 7
        overall_structural_health = int((structural_metrics["safetyFactorInAllowableStressDesign"] + 
                                     structural_metrics["reserveStrengthFactor"] + 
                                     (100 - structural_metrics["probabilityOfFailure"]) + 
                                     structural_metrics["robustness"] + 
                                     structural_metrics["resilience"]) / 50)
        
        # Combined final score (OSAC)
        osac_score = (overall_condition_score + overall_structural_health) // 2
        
        st.success(f"Overall Stormwater Asset Condition (OSAC) Score: {osac_score}/10")
        
        # Determine text rating
        osac_rating = "Poor" if osac_score < 4 else "Fair" if osac_score < 7 else "Good"

    return {
        "assessmentType": "Stormwater Condition Assessment",
        "stormwaterHydraulicAssetCondition": {
            "pipeDiameterWidth": pipe_diameter,
            "pipeScore": pipe_score,
            "routineInspectionFrequency": inspection_freq,
            "damageLevels": damage_levels
        },
        "stormwaterAssetCondition": {
            "damageLevels": treatment_damage_levels
        },
        "stormwaterAssetStructuralCondition": structural_metrics,
        "OSAC": {
            "score": osac_score,
            "rating": osac_rating
        }
    }

def functionality_assessment_form():
    st.header("Functionality Assessment")

    # Hydraulic Performance
    hydraulic = st.expander("Hydraulic Performance (HP)")
    with hydraulic:
        st.markdown("#### Flow and Volume Management Metrics")
        st.markdown("These metrics determine how effectively the system manages water flow and volume.")
        
        # Extract metrics from documentation with specific percentage values
        hp_metrics = {}
        
        # Flow Attenuation with reference value from document (69%)
        hp_metrics["flowAttenuation"] = st.slider(
            "Flow Attenuation at the Outlet (%)", 
            0, 100, 69,
            help="Multiplicative and Additive Models (MAM) - Deterministic assessment at Section, Component & System level"
        )
        
        # Volume Reduction with reference value from document (73%)
        hp_metrics["volumeReduction"] = st.slider(
            "Volume Reduction at the Outlet (%)", 
            0, 100, 73,
            help="Combined Sewer Overflows (CSO) - Probabilistic assessment at Section, Component & System level"
        )
        
        # CSO Metrics
        col1, col2 = st.columns(2)
        with col1:
            hp_metrics["csoVolume"] = st.number_input(
                "CSO volume (m³)", 
                0, 10000, 250,
                help="Combined Sewer Overflow volume"
            )
        
        with col2:
            hp_metrics["totalFlowVolume"] = st.number_input(
                "Total flow volume (m³)", 
                0, 50000, 1000,
                help="Total flow volume through system"
            )
        
        # Calculate overflow percentage
        overflow_percentage = (hp_metrics["csoVolume"] / hp_metrics["totalFlowVolume"] * 100) if hp_metrics["totalFlowVolume"] > 0 else 0
        hp_metrics["overflowPercentage"] = overflow_percentage
        st.info(f"Overflow Percentage: {overflow_percentage:.1f}% (Target: ≤ 35%)")
        
        # Dry Weather Flow with reference value from document (82%)
        st.markdown("#### Station Performance")
        hp_metrics["dryWeatherFlow"] = st.slider(
            "Dry Weather Flow Performance (%)", 
            0, 100, 82,
            help="Dry Weather Flow (DWF) - Deterministic assessment at Section, Component & System level"
        )
        
        # Pumping Station metrics
        col1, col2 = st.columns(2)
        with col1:
            hp_metrics["pumpingStationOverflow"] = st.number_input(
                "Pumping station overflow incidents (count/year)", 
                0, 100, 5
            )
        
        with col2:
            hp_metrics["overflowFrequency"] = st.slider(
                "Overflow Frequency Indicator (%)", 
                0, 100, 65,
                help="Determined by ratio of CSO volume to total flow volume - Component & System level"
            )
        
        # Time-based metrics
        st.markdown("#### Drainage Performance")
        col1, col2 = st.columns(2)
        
        with col1:
            hp_metrics["timeToPeakDischarge"] = st.number_input(
                "Time to peak discharge (hours)", 
                0, 72, 8
            )
        
        with col2:
            hp_metrics["peakDischargeVolume"] = st.number_input(
                "Volume of peak discharge (m³)", 
                0, 10000, 500
            )
        
        hp_metrics["drainageDurationPerformance"] = st.slider(
            "Drainage Duration Frequency Performance (%)", 
            0, 100, 70,
            help="Deterministic assessment at Component & System level"
        )

    # Hydrological Performance
    hydrological = st.expander("Hydrological Performance (DP)")
    with hydrological:
        st.markdown("#### Catchment Hydrology Metrics")
        st.markdown("These metrics determine how effectively the system manages hydrological cycles.")
        
        # Initialize metrics dictionary
        dp_metrics = {}
        
        # Runoff metrics with reference values from documentation
        dp_metrics["runoffFrequency"] = st.slider(
            "Runoff Frequency Performance (%)", 
            0, 100, 65,
            help="Simulation assessment at Component & System level"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            dp_metrics["annualRunoff"] = st.number_input(
                "Annual Runoff (m³)", 
                0, 1000000, 35000
            )
        
        with col2:
            dp_metrics["annualPrecipitation"] = st.number_input(
                "Annual Precipitation (mm)", 
                0, 3000, 1200
            )
        
        # Base flow performance with reference value from document (70%)
        dp_metrics["baseFlowPerformance"] = st.slider(
            "Base Flow and Filtered Flows Performance (%)", 
            0, 100, 70,
            help="Deterministic assessment using pipe flow ratio at Component & System level"
        )
        
        # Calculated metrics
        col1, col2 = st.columns(2)
        with col1:
            dp_metrics["inflowToSystem"] = st.number_input(
                "Inflow to sewer system (m³/day)", 
                0, 50000, 2500
            )
        
        with col2:
            dp_metrics["inflowToWWTP"] = st.number_input(
                "Inflow to WWTP (m³/day)", 
                0, 50000, 2000
            )
        
        # Calculate inflow performance
        inflow_performance = (dp_metrics["inflowToWWTP"] / dp_metrics["inflowToSystem"] * 100) if dp_metrics["inflowToSystem"] > 0 else 0
        st.info(f"Inflow Performance: {inflow_performance:.1f}% (Reference: 79%)")
        dp_metrics["inflowPerformance"] = inflow_performance
        
        # Catchment-scale outcomes with reference value from document (85%)
        st.markdown("#### Catchment-Scale Outcomes")
        dp_metrics["catchmentScalePerformance"] = st.slider(
            "Catchment-Scale Outcomes Performance (%)", 
            0, 100, 85,
            help="Deterministic assessment at Component & System level"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            dp_metrics["floodFrequency"] = st.number_input(
                "Frequency of flood (events/year)", 
                0, 50, 3
            )
        
        with col2:
            dp_metrics["floodDuration"] = st.number_input(
                "Average flood duration (hours)", 
                0, 168, 6
            )

    # Calculate overall functionality score (0-10)
    hp_avg = sum([
        hp_metrics["flowAttenuation"], 
        hp_metrics["volumeReduction"],
        hp_metrics["dryWeatherFlow"],
        hp_metrics["overflowFrequency"],
        hp_metrics["drainageDurationPerformance"]
    ]) / 5
    
    dp_avg = sum([
        dp_metrics["runoffFrequency"],
        dp_metrics["baseFlowPerformance"],
        dp_metrics["inflowPerformance"],
        dp_metrics["catchmentScalePerformance"]
    ]) / 4
    
    # Convert percentage to 0-10 scale
    functionality_score = int((hp_avg + dp_avg) / 20)
    functionality_rating = "Poor" if functionality_score < 4 else "Fair" if functionality_score < 7 else "Good"
    
    st.success(f"Overall Functionality Score: {functionality_score}/10 - {functionality_rating}")

    return {
        "hydraulicPerformance": hp_metrics,
        "hydrologicalPerformance": dp_metrics,
        "overallFunctionality": {
            "score": functionality_score,
            "rating": functionality_rating
        }
    }

def time_effectiveness_form():
    st.header("Time-Effectiveness Assessment")

    time_condition = st.expander("Time Condition (TC)")
    with time_condition:
        st.markdown("#### Long-Term Effectiveness Metrics")
        st.markdown("These metrics assess how the system performs over time.")
        
        # Initialize time condition metrics with document reference values
        tc_metrics = {}
        
        # Long-term functionality with reference value from document (60%)
        tc_metrics["longTermFunctionality"] = st.slider(
            "Long-term Functionalities Performance (%)", 
            0, 100, 60,
            help="Modeling of Simulation at Component & System level"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            tc_metrics["designLifespan"] = st.number_input(
                "Design lifespan (years)", 
                0, 100, 50,
                help="Expected service life of the system"
            )
        
        with col2:
            tc_metrics["currentAge"] = st.number_input(
                "Current age (years)", 
                0, 100, 15,
                help="Current age of the system"
            )
        
        # Calculate and display age percentage
        age_percentage = (tc_metrics["currentAge"] / tc_metrics["designLifespan"] * 100) if tc_metrics["designLifespan"] > 0 else 0
        tc_metrics["agePercentage"] = age_percentage
        remaining_life = max(0, tc_metrics["designLifespan"] - tc_metrics["currentAge"])
        
        st.info(f"Age Percentage: {age_percentage:.1f}% (Remaining Life: {remaining_life} years)")
        
        # Lag-time metrics with reference value from document (80%)
        st.markdown("#### Maintenance Responsiveness")
        tc_metrics["lagTimePerformance"] = st.slider(
            "Lag-Time Performance (%)", 
            0, 100, 80,
            help="Probabilistic assessment at Component & System level"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            tc_metrics["maintenanceResponseTarget"] = st.number_input(
                "Maintenance response target (days)", 
                0, 365, 14,
                help="Target response time for maintenance actions"
            )
        
        with col2:
            tc_metrics["actualResponseTime"] = st.number_input(
                "Actual maintenance response time (days)", 
                0, 365, 18,
                help="Actual average response time for maintenance actions"
            )
        
        # Monitoring frequency metrics
        st.markdown("#### Monitoring Effectiveness")
        tc_metrics["monitoringFrequency"] = st.selectbox(
            "Infrastructure monitoring frequency",
            ["Continuous (real-time)", "Daily", "Weekly", "Monthly", "Quarterly", "Annually"],
            index=2
        )
        
        # Calculate time effectiveness score (0-10)
        long_term_score = tc_metrics["longTermFunctionality"] / 10
        
        # Response time ratio (lower is better)
        response_ratio = tc_metrics["maintenanceResponseTarget"] / tc_metrics["actualResponseTime"] if tc_metrics["actualResponseTime"] > 0 else 1
        
        # Monitoring frequency score
        monitoring_scores = {
            "Continuous (real-time)": 10,
            "Daily": 8,
            "Weekly": 7,
            "Monthly": 5,
            "Quarterly": 3,
            "Annually": 1
        }
        monitoring_score = monitoring_scores[tc_metrics["monitoringFrequency"]]
        
        # Weighted average for time effectiveness
        time_score = int((long_term_score * 0.4) + (tc_metrics["lagTimePerformance"] / 10 * 0.4) + (monitoring_score / 10 * 0.2))
        time_rating = "Poor" if time_score < 4 else "Fair" if time_score < 7 else "Good"
        
        st.success(f"Time Effectiveness Score: {time_score}/10 - {time_rating}")
        
        tc_metrics["overallTimeScore"] = time_score
        tc_metrics["overallTimeRating"] = time_rating

    return tc_metrics

def cost_effectiveness_form():
    st.header("Cost-Effectiveness Assessment")

    cost_condition = st.expander("Cost Condition (CC)")
    with cost_condition:
        st.markdown("#### Life-Cycle Cost Analysis")
        st.markdown("These metrics assess the economic efficiency of the stormwater infrastructure.")
        
        # Initialize cost metrics
        cc_metrics = {}
        
        # Project costs
        project_cols = st.columns(3)
        with project_cols[0]:
            cc_metrics["preliminaryCosts"] = st.number_input(
                "Preliminary costs ($)", 
                0, 1000000, 75000,
                help="Initial planning and design costs"
            )
        
        with project_cols[1]:
            cc_metrics["constructionCosts"] = st.number_input(
                "Construction costs ($)", 
                0, 10000000, 1250000,
                help="Capital costs for infrastructure construction"
            )
        
        with project_cols[2]:
            cc_metrics["annualOperationalCosts"] = st.number_input(
                "Annual O&M costs ($/year)", 
                0, 1000000, 52000,
                help="Annual operation and maintenance costs"
            )
        
        # Lifecycle period
        st.markdown("#### Lifecycle Parameters")
        col1, col2 = st.columns(2)
        
        with col1:
            cc_metrics["lifecyclePeriod"] = st.number_input(
                "Lifecycle period (years)", 
                5, 100, 30,
                help="Period over which to evaluate economic performance"
            )
        
        with col2:
            cc_metrics["discountRate"] = st.number_input(
                "Discount rate (%)", 
                0.0, 20.0, 4.5,
                help="Annual rate used to discount future costs and benefits"
            )
        
        # Calculate lifecycle costs (simple calculation without NPV)
        total_operation_cost = cc_metrics["annualOperationalCosts"] * cc_metrics["lifecyclePeriod"]
        total_lifecycle_cost = cc_metrics["preliminaryCosts"] + cc_metrics["constructionCosts"] + total_operation_cost
        cc_metrics["totalLifecycleCost"] = total_lifecycle_cost
        
        st.info(f"Total Lifecycle Cost: ${total_lifecycle_cost:,.2f}")
        
        # Economic benefits
        st.markdown("#### Economic Benefits")
        col1, col2 = st.columns(2)
        
        with col1:
            cc_metrics["annualFloodDamagePrevention"] = st.number_input(
                "Annual flood damage prevention ($)", 
                0, 1000000, 95000,
                help="Estimated annual cost savings from preventing flood damage"
            )
        
        with col2:
            cc_metrics["annualEnvironmentalBenefits"] = st.number_input(
                "Annual environmental benefits ($)", 
                0, 1000000, 45000,
                help="Monetized environmental benefits (water quality, habitat, etc.)"
            )
        
        # Calculate total benefits
        annual_benefits = cc_metrics["annualFloodDamagePrevention"] + cc_metrics["annualEnvironmentalBenefits"]
        total_benefits = annual_benefits * cc_metrics["lifecyclePeriod"]
        cc_metrics["totalBenefits"] = total_benefits
        
        # Calculate benefit-cost ratio and ROI
        benefit_cost_ratio = total_benefits / total_lifecycle_cost if total_lifecycle_cost > 0 else 0
        cc_metrics["benefitCostRatio"] = benefit_cost_ratio
        
        roi_percentage = ((total_benefits - total_lifecycle_cost) / total_lifecycle_cost * 100) if total_lifecycle_cost > 0 else 0
        cc_metrics["roi"] = roi_percentage
        
        st.success(f"Benefit-Cost Ratio: {benefit_cost_ratio:.2f}")
        st.success(f"Return on Investment: {roi_percentage:.1f}%")
        
        # Calculate cost-effectiveness score (0-10)
        # Combination of BCR and ROI
        cost_score = min(10, int(benefit_cost_ratio * 3 + roi_percentage/20))
        cost_rating = "Poor" if cost_score < 4 else "Fair" if cost_score < 7 else "Good"
        
        st.success(f"Cost Effectiveness Score: {cost_score}/10 - {cost_rating}")
        
        cc_metrics["overallCostScore"] = cost_score
        cc_metrics["overallCostRating"] = cost_rating

    return cc_metrics

def environmental_social_form():
    st.header("Environmental and Social Impact Assessment")

    env_social = st.expander("Environmental and Social Condition (ESC)")
    with env_social:
        st.markdown("#### Environmental Performance Metrics")
        st.markdown("These metrics assess how effectively the system protects the environment.")
        
        # Initialize metrics with document reference values
        es_metrics = {}
        
        # Pollution reduction metrics with reference values from the document
        col1, col2 = st.columns(2)
        
        with col1:
            # Pollutant Concentration with reference value from document (70%)
            es_metrics["pollutantConcentrationAttenuation"] = st.slider(
                "Pollutant Concentration Attenuation (%)", 
                0, 100, 70,
                help="Event Mean Concentration (EMC) for predicting water quality - Deterministic assessment at Component & System level"
            )
        
        with col2:
            # Pollutant Removal with reference value from document (55%)
            es_metrics["eventBasedPollutantRemoval"] = st.slider(
                "Event-Based Pollutant Removal (%)", 
                0, 100, 55,
                help="Deterministic assessment at Component & System level"
            )
        
        # Pollution Retention with reference value from document (66%)
        es_metrics["pollutionRetentionPerformance"] = st.slider(
            "Pollution Retention Performance (%)", 
            0, 100, 66,
            help="Semi-Deterministic assessment at Component & System level"
        )
        
        # Water quality metrics
        st.markdown("#### Water Quality Parameters")
        quality_cols = st.columns(3)
        
        with quality_cols[0]:
            es_metrics["tssReduction"] = st.slider(
                "Total Suspended Solids Reduction (%)", 
                0, 100, 75,
                help="Percentage reduction in TSS compared to untreated runoff"
            )
        
        with quality_cols[1]:
            es_metrics["nutrientReduction"] = st.slider(
                "Nutrient Reduction (%)", 
                0, 100, 60,
                help="Percentage reduction in nitrogen and phosphorus"
            )
            
        with quality_cols[2]:
            es_metrics["bacteriaReduction"] = st.slider(
                "Bacteria Reduction (%)", 
                0, 100, 68,
                help="Percentage reduction in bacteria (E. coli, etc.)"
            )
        
        # Calculate water quality score
        water_quality_score = (es_metrics["tssReduction"] + es_metrics["nutrientReduction"] + es_metrics["bacteriaReduction"]) / 30
        
        # Social impact metrics
        st.markdown("#### Social Impact Metrics")
        
        # Customer Satisfaction with reference value from document (50%)
        es_metrics["customerSatisfaction"] = st.slider(
            "Customer Satisfaction (%)", 
            0, 100, 50,
            help="Semi-Deterministic assessment at Component & System level"
        )
        
        # Community engagement
        col1, col2 = st.columns(2)
        with col1:
            es_metrics["communityEngagement"] = st.select_slider(
                "Community Engagement Level", 
                ["None", "Minimal", "Moderate", "Extensive", "Comprehensive"],
                "Moderate"
            )
        
        with col2:
            # Convert engagement to score
            engagement_scores = {
                "None": 0,
                "Minimal": 3,
                "Moderate": 5,
                "Extensive": 8,
                "Comprehensive": 10
            }
            engagement_score = engagement_scores[es_metrics["communityEngagement"]]
            st.info(f"Engagement Score: {engagement_score}/10")
        
        # Safety metrics with reference value from document
        st.markdown("#### Safety Metrics")
        st.markdown("These metrics assess safety for staff and the public.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            es_metrics["accidentFrequency"] = st.number_input(
                "Accident frequency rate (incidents/year)", 
                0, 100, 2,
                help="Number of accidents per year"
            )
            
        with col2:
            es_metrics["accidentSeverity"] = st.select_slider(
                "Accident severity level", 
                ["Minor", "Moderate", "Serious", "Critical", "Fatal"],
                "Minor"
            )
                
        # Calculate safety score (lower is better)
        severity_scores = {
            "Minor": 1,
            "Moderate": 2,
            "Serious": 4,
            "Critical": 7,
            "Fatal": 10
        }
        severity_score = severity_scores[es_metrics["accidentSeverity"]]
        safety_score = 10 - min(10, (es_metrics["accidentFrequency"] * severity_score) / 2)
        st.info(f"Safety Score: {safety_score:.1f}/10 (higher is better)")
        
        # Calculate overall environmental-social score (0-10)
        environmental_avg = (es_metrics["pollutantConcentrationAttenuation"] + 
                           es_metrics["eventBasedPollutantRemoval"] + 
                           es_metrics["pollutionRetentionPerformance"]) / 30
        
        social_avg = (es_metrics["customerSatisfaction"]/10 + engagement_score + safety_score) / 3
        
        # Combined score with 70% environmental, 30% social weighting
        overall_score = int((environmental_avg * 7 + social_avg * 3) / 10)
        overall_rating = "Poor" if overall_score < 4 else "Fair" if overall_score < 7 else "Good"
        
        st.success(f"Overall Environmental & Social Score: {overall_score}/10 - {overall_rating}")
        
        # Add scores to metrics dictionary
        es_metrics["environmentalScore"] = environmental_avg
        es_metrics["socialScore"] = social_avg
        es_metrics["overallScore"] = overall_score
        es_metrics["overallRating"] = overall_rating

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