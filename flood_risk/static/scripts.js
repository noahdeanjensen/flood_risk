
// Wait until the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  const simulateButton = document.getElementById('simulateButton');

  // Make sure the button exists
  if (simulateButton) {
      simulateButton.addEventListener('click', intakeData);
  } else {
      console.error('Button not found!');
  }
});

// Function to intake and display the input data
function intakeData() {
  // Get input values for TC
  const vegetationEstablishment = document.getElementById('vegetationEstablishment').value;
  const startingEfficiency = document.getElementById('startingEfficiency').value;
  const stormEventEfficiency = document.getElementById('stormEventEfficiency').value;
  const maintenanceEfficiency = document.getElementById('maintenanceEfficiency').value;
  const lifecycleEfficiency = document.getElementById('lifecycleEfficiency').value;
  const longTermEfficiency = document.getElementById('longTermEfficiency').value;
  const monitoringChecklists = document.getElementById('monitoringChecklists').value;

  // Get input values for ESC
  const totalRunoffVolume = document.getElementById('totalRunoffVolume').value;
  const pollutantConcentration = document.getElementById('pollutantConcentration').value;
  const flowRate = document.getElementById('flowRate').value;
  const samples = document.getElementById('samples').value;
  const inletLoading = document.getElementById('inletLoading').value;
  const outletLoading = document.getElementById('outletLoading').value;
  const rvr = document.getElementById('rvr').value;
  const prret = document.getElementById('prret').value;
  const prover = document.getElementById('prover').value;
  const satisfaction = document.getElementById('satisfaction').value;
  const frequencyRate = document.getElementById('frequencyRate').value;
  const severityRate = document.getElementById('severityRate').value;
  const manHoursWorked = document.getElementById('manHoursWorked').value;

  // Display the input values without calculations
  const resultDiv = document.getElementById('resultmod5');
  resultDiv.innerHTML = `
    <h3>Time Condition (TC) - Lifespan and Long-Term Effectiveness</h3>
    <p><strong>Vegetation Establishment Efficiency:</strong> ${vegetationEstablishment}</p>
    <p><strong>Starting Efficiency:</strong> ${startingEfficiency}</p>
    <p><strong>Storm Event Efficiency:</strong> ${stormEventEfficiency}</p>
    <p><strong>Efficiency Between Maintenance:</strong> ${maintenanceEfficiency}</p>
    <p><strong>Efficiency Over Life Cycle:</strong> ${lifecycleEfficiency}</p>
    <p><strong>Long-Term Efficiency:</strong> ${longTermEfficiency}</p>
    <p><strong>Monitoring and Maintenance Checklist:</strong> ${monitoringChecklists}</p>

    <h3>Environmental and Social Condition (ESC)</h3>
    <p><strong>Total Runoff Volume per Event:</strong> ${totalRunoffVolume} L</p>
    <p><strong>Pollutant Concentration:</strong> ${pollutantConcentration} mg/L</p>
    <p><strong>Flow Rate:</strong> ${flowRate} L/s</p>
    <p><strong>Number of Samples:</strong> ${samples}</p>
    <p><strong>Inlet Loading:</strong> ${inletLoading}%</p>
    <p><strong>Outlet Loading:</strong> ${outletLoading}%</p>
    <p><strong>Percent Annual Runoff Volume Retained (RVR):</strong> ${rvr}%</p>
    <p><strong>Percent Annual Pollutant Removal Rate (PRret):</strong> ${prret}%</p>
    <p><strong>Percent Annual Pollutant Removal Rate for Overflow (PRover):</strong> ${prover}%</p>
    <p><strong>Customer Satisfaction Level:</strong> ${satisfaction}/10</p>
    <p><strong>Accident Frequency Rate:</strong> ${frequencyRate}</p>
    <p><strong>Injury Severity Rate:</strong> ${severityRate}</p>
    <p><strong>Total Man-Hours Worked:</strong> ${manHoursWorked}</p>
  `;
}

function calculateRunoff(precipitation, evapotranspiration) {
  return precipitation - evapotranspiration;
}

function calculatePipeFlowRatio(flowPipe1, flowPipe2) {
  return flowPipe1 / flowPipe2;
}

function calculateFloodFrequency(floodEvents, totalTime) {
  return floodEvents / totalTime;
}

function calculateInflowOutflow(instantaneousFlow) {
  return instantaneousFlow; // Simplified model
}

function simulateHydrologicalPerformance() {
  // Get input values
  const precipitation = parseFloat(document.getElementById('precipitation').value);
  const evapotranspiration = parseFloat(document.getElementById('evapotranspiration').value);
  const flowPipe1 = parseFloat(document.getElementById('flowPipe1').value);
  const flowPipe2 = parseFloat(document.getElementById('flowPipe2').value);
  const floodEvents = parseFloat(document.getElementById('floodEvents').value);
  const totalTime = parseFloat(document.getElementById('totalTime').value);
  const instantaneousFlow = parseFloat(document.getElementById('instantaneousFlow').value);

  // Perform calculations
  const runoff = calculateRunoff(precipitation, evapotranspiration);
  const pipeFlowRatio = calculatePipeFlowRatio(flowPipe1, flowPipe2);
  const floodFrequency = calculateFloodFrequency(floodEvents, totalTime);
  const inflowOutflow = calculateInflowOutflow(instantaneousFlow);

  // Display results
  const resultDiv = document.getElementById('resultmod4');
  resultDiv.innerHTML = `
      <p><strong>Runoff Volume: </strong>${runoff} m³</p>
      <p><strong>Pipe Flow Ratio: </strong>${pipeFlowRatio}</p>
      <p><strong>Flood Frequency: </strong>${floodFrequency} events/day</p>
      <p><strong>Inflow/Outflow: </strong>${inflowOutflow} m³/s</p>
  `;
}

  let savedResults = [];

  // Handle feature selection and display input fields accordingly
  document.getElementById("feature-select").addEventListener("change", function() {
    const feature = this.value;
    const inputContainer = document.getElementById("input-fields-container");
    const saveButton = document.getElementById("save-feature");

    // Clear existing fields
    inputContainer.innerHTML = '';
    saveButton.style.display = "none"; // Hide save button by default

    switch (feature) {
      case 'flow_attenuation':
        inputContainer.innerHTML = `
          <label for="x_in">X-in (Flow Input) (m3/s):</label>
          <input type="number" id="x_in" placeholder="Enter flow input value" step="0.01" min="0"><br>
          <label for="x_out">X-out (Flow Output) (m3/s):</label>
          <input type="number" id="x_out" placeholder="Enter flow output value" step="0.01" min="0"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
      case 'volume_reduction':
        inputContainer.innerHTML = `
          <label for="volume_in">Volume In (m³):</label>
          <input type="number" id="volume_in" placeholder="Enter volume in value" step="0.1" min="0"><br>
          <label for="volume_out">Volume Out (m³):</label>
          <input type="number" id="volume_out" placeholder="Enter volume out value" step="0.1" min="0"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
      case 'dwf':
        inputContainer.innerHTML = `
          <label for="population">Population in Catchment:</label>
          <input type="number" id="population" placeholder="Enter population value" min="0"><br>
          <label for="domestic_consumption">Domestic Consumption (m³/hd/day):</label>
          <input type="number" id="domestic_consumption" placeholder="Enter domestic consumption" min="0" step="0.1"><br>
          <label for="industrial_flows">Industrial Flows (m³/day):</label>
          <input type="number" id="industrial_flows" placeholder="Enter industrial flows" min="0" step="0.1"><br>
          <label for="infiltration">Infiltration (m³/day):</label>
          <input type="number" id="infiltration" placeholder="Enter infiltration value" min="0" step="0.1"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
      case 'overflow_freq':
        inputContainer.innerHTML = `
          <label for="total_flow_volume">Total Flow Volume (m³):</label>
          <input type="number" id="total_flow_volume" placeholder="Enter total flow volume" step="0.1" min="0"><br>
          <label for="cso_volume">CSO Volume (m³):</label>
          <input type="number" id="cso_volume" placeholder="Enter CSO volume" step="0.1" min="0"><br>
          <label for="overflow_return_period">Overflow Return Period (years):</label>
          <input type="number" id="overflow_return_period" placeholder="Enter overflow return period" min="1"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
      case 'drainage_duration':
        inputContainer.innerHTML = `
          <label for="time_to_peak">Time to Peak Discharge (hrs):</label>
          <input type="number" id="time_to_peak" placeholder="Enter time to peak discharge" step="0.1" min="0"><br>
          <label for="peak_discharge_volume">Peak Discharge Volume (m³):</label>
          <input type="number" id="peak_discharge_volume" placeholder="Enter peak discharge volume" step="0.1" min="0"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
      case 'pumping_overflow':
        inputContainer.innerHTML = `
          <label for="dwf_volume">Dry Weather Flow Volume (m³/day):</label>
          <input type="number" id="dwf_volume" placeholder="Enter DWF volume" step="0.1" min="0"><br>
          <label for="pumping_station_capacity">Pumping Station Capacity (m³/s):</label>
          <input type="number" id="pumping_station_capacity" placeholder="Enter pumping station capacity" step="0.1" min="0"><br>
          <label for="overflow_volume">Pumping Station Overflow Volume (m³):</label>
          <input type="number" id="overflow_volume" placeholder="Enter overflow volume" step="0.1" min="0"><br>
        `;
        saveButton.style.display = "block"; // Show save button
        break;
    }
  });

  // Handle the save button click to save the input values
  document.getElementById("save-feature").addEventListener("click", function() {
    const feature = document.getElementById("feature-select").value;
    let inputs = {};

    // Collect the input values based on the selected feature
    switch (feature) {
      case 'flow_attenuation':
        inputs = {
          "X-in (Flow Input)": document.getElementById("x_in").value,
          "X-out (Flow Output)": document.getElementById("x_out").value
        };
        break;
      case 'volume_reduction':
        inputs = {
          "Volume In": document.getElementById("volume_in").value,
          "Volume Out": document.getElementById("volume_out").value
        };
        break;
      case 'dwf':
        inputs = {
          "Population": document.getElementById("population").value,
          "Domestic Consumption": document.getElementById("domestic_consumption").value,
          "Industrial Flows": document.getElementById("industrial_flows").value,
          "Infiltration": document.getElementById("infiltration").value
        };
        break;
      case 'overflow_freq':
        inputs = {
          "Total Flow Volume": document.getElementById("total_flow_volume").value,
          "CSO Volume": document.getElementById("cso_volume").value,
          "Overflow Return Period": document.getElementById("overflow_return_period").value
        };
        break;
      case 'drainage_duration':
        inputs = {
          "Time to Peak Discharge": document.getElementById("time_to_peak").value,
          "Peak Discharge Volume": document.getElementById("peak_discharge_volume").value
        };
        break;
      case 'pumping_overflow':
        inputs = {
          "Dry Weather Flow Volume": document.getElementById("dwf_volume").value,
          "Pumping Station Capacity": document.getElementById("pumping_station_capacity").value,
          "Overflow Volume": document.getElementById("overflow_volume").value
        };
        break;
    }

    // Save the input values
    savedResults.push({ feature, inputs });

    // Display a confirmation message (optional)
    alert('Feature saved successfully');

    // Clear input fields after saving
    document.getElementById("input-fields-container").innerHTML = '';
    document.getElementById("feature-select").value = '';

    // Update the saved results table
    updateSavedResults();
  });

  // Function to update the saved results table
  function updateSavedResults() {
    const savedResultsTable = document.getElementById("saved-results").getElementsByTagName('tbody')[0];
    savedResultsTable.innerHTML = ''; // Clear current saved results

    savedResults.forEach((result, index) => {
      const row = savedResultsTable.insertRow();
      const cell1 = row.insertCell(0);
      const cell2 = row.insertCell(1);
      const cell3 = row.insertCell(2);
      cell1.textContent = result.feature;

      // Format the input values as a string
      const inputsString = Object.entries(result.inputs)
        .map(([key, value]) => `${key}: ${value}`)
        .join(', ');

      cell2.textContent = inputsString;

      // Add delete button for each saved feature
      const deleteButton = document.createElement('button');
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", function() {
        // Remove this entry from savedResults
        savedResults.splice(index, 1);
        updateSavedResults(); // Update the table after deletion
      });
      cell3.appendChild(deleteButton);
    });
  }

// Automatically calculate Probability of Failure (Pf)
document.getElementById('resistance-input').addEventListener('input', function() {
    const resistance = parseFloat(document.getElementById('resistance-input').value);
    const load = parseFloat(document.getElementById('load-input').value);

    if (!isNaN(resistance) && !isNaN(load)) {
        const pf = load / resistance; // Simplified calculation for probability of failure
        document.getElementById('pf-value').textContent = `${(pf * 100).toFixed(2)}%`;
    } else {
        document.getElementById('pf-value').textContent = 'Not Calculated';
    }
});

document.getElementById('load-input').addEventListener('input', function() {
    const resistance = parseFloat(document.getElementById('resistance-input').value);
    const load = parseFloat(document.getElementById('load-input').value);

    if (!isNaN(resistance) && !isNaN(load)) {
        const pf = load / resistance; // Simplified calculation for probability of failure
        document.getElementById('pf-value').textContent = `${(pf * 100).toFixed(2)}%`;
    } else {
        document.getElementById('pf-value').textContent = 'Not Calculated';
    }
});

// Automatically calculate Safety Factor (SF)
document.getElementById('sigma-u-input').addEventListener('input', function() {
    const sigmaU = parseFloat(document.getElementById('sigma-u-input').value);
    const sigmaAll = parseFloat(document.getElementById('sigma-all-input').value);

    if (!isNaN(sigmaU) && !isNaN(sigmaAll)) {
        const sf = sigmaU / sigmaAll;
        document.getElementById('sf-value').textContent = sf.toFixed(2);
    } else {
        document.getElementById('sf-value').textContent = 'Not Calculated';
    }
});

document.getElementById('sigma-all-input').addEventListener('input', function() {
    const sigmaU = parseFloat(document.getElementById('sigma-u-input').value);
    const sigmaAll = parseFloat(document.getElementById('sigma-all-input').value);

    if (!isNaN(sigmaU) && !isNaN(sigmaAll)) {
        const sf = sigmaU / sigmaAll;
        document.getElementById('sf-value').textContent = sf.toFixed(2);
    } else {
        document.getElementById('sf-value').textContent = 'Not Calculated';
    }
});

// Automatically calculate Reserve Strength Factor (R1)
document.getElementById('load-carrying-capacity').addEventListener('input', function() {
    const loadCarryingCapacity = parseFloat(document.getElementById('load-carrying-capacity').value);
    const appliedLoad = parseFloat(document.getElementById('applied-load').value);

    if (!isNaN(loadCarryingCapacity) && !isNaN(appliedLoad)) {
        const r1 = loadCarryingCapacity / appliedLoad;
        document.getElementById('r1-value').textContent = r1.toFixed(2);
    } else {
        document.getElementById('r1-value').textContent = 'Not Calculated';
    }
});

document.getElementById('applied-load').addEventListener('input', function() {
    const loadCarryingCapacity = parseFloat(document.getElementById('load-carrying-capacity').value);
    const appliedLoad = parseFloat(document.getElementById('applied-load').value);

    if (!isNaN(loadCarryingCapacity) && !isNaN(appliedLoad)) {
        const r1 = loadCarryingCapacity / appliedLoad;
        document.getElementById('r1-value').textContent = r1.toFixed(2);
    } else {
        document.getElementById('r1-value').textContent = 'Not Calculated';
    }
});

// Automatically calculate Robustness (RO)
document.getElementById('robustness-input').addEventListener('input', function() {
    const robustness = parseFloat(document.getElementById('robustness-input').value);

    if (!isNaN(robustness) && robustness >= 0 && robustness <= 1) {
        document.getElementById('ro-value').textContent = robustness.toFixed(2);
    } else {
        document.getElementById('ro-value').textContent = 'Not Calculated';
    }
});

// Automatically calculate Resilience (RE)
document.getElementById('resilience-input').addEventListener('input', function() {
    const resilience = parseFloat(document.getElementById('resilience-input').value);

    if (!isNaN(resilience) && resilience >= 0 && resilience <= 1) {
        document.getElementById('re-value').textContent = resilience.toFixed(2);
    } else {
        document.getElementById('re-value').textContent = 'Not Calculated';
    }
});




      document.addEventListener("DOMContentLoaded", function () {
        // Event delegation for slider updates
        document.querySelectorAll("input[type='range']").forEach(slider => {
          slider.addEventListener("input", function () {
            this.nextElementSibling.textContent = this.value + (this.max == 100 ? "%" : "");
          });
        });
      });


      function showModule(moduleId) {
        document.querySelectorAll('.module-content').forEach(module => module.classList.remove('active'));
        document.getElementById(moduleId).classList.add('active');
      }

      // Generate report with form data
      function generateReport() {
        // Collect the form data
        const gcrValue = document.getElementById('gcr-slider').value;
        const assetClassification = document.getElementById('asset-classification').textContent;
        const selectedStrategies = Array.from(document.getElementById('rehabilitation-strategy').selectedOptions)
          .map(option => option.text).join(', ');
        const preservationValue = document.getElementById('cost-slider').value;

        // Format the report
        const reportContent = `
        Stormwater Asset Management Report:
        -----------------------------
        General Condition Rating (GCR): ${gcrValue}
        Asset Classification: ${assetClassification}
        Rehabilitation Strategies: ${selectedStrategies || 'None selected'}
        Preservation vs Replacement: ${preservationValue}%
      `;

        // Create a downloadable file (text format)
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'stormwater_report.txt';

        // Trigger the download
        link.click();
      }

      // Save data (currently just an alert)
      function saveData() {
        alert('Data saved!');
      }

  
      document.getElementById("add-condition").addEventListener("click", function () {
        const conditionSelect = document.getElementById("condition-select");
        const selectedValue = conditionSelect.value;
        const selectedText = conditionSelect.options[conditionSelect.selectedIndex].text;
        const container = document.getElementById("conditions-container");

        // Prevent duplicate conditions
        if (document.getElementById(`condition-${selectedValue}`)) {
          alert("This condition has already been added!");
          return;
        }

        // Create a new condition rating section Module 2
        const conditionDiv = document.createElement("div");
        conditionDiv.classList.add("condition-item");
        conditionDiv.id = `condition-${selectedValue}`;
        conditionDiv.innerHTML = `
      <label>${selectedText}:</label>
      <input type="range" min="0" max="10" step="1" value="5" class="condition-slider">
      <span class="condition-value">5</span>
      <button class="remove-condition">Remove</button>
    `;

        // Update slider value display
        conditionDiv.querySelector(".condition-slider").addEventListener("input", function () {
          conditionDiv.querySelector(".condition-value").textContent = this.value;
        });

        // Remove condition feature
        conditionDiv.querySelector(".remove-condition").addEventListener("click", function () {
          conditionDiv.remove();
        });

        // Append to container
        container.appendChild(conditionDiv);
      });



      // Get the slider and value display elements
      const osacSlider = document.getElementById("osac-slider");
      const osacValue = document.getElementById("osac-value");
    
      // Update the displayed value when the slider changes
      osacSlider.addEventListener("input", function() {
        osacValue.textContent = osacSlider.value;
      });
