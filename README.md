# Stormwater Infrastructure Assessment Project

## **Overview**
This project provides a modular framework to evaluate and assess stormwater control infrastructure using geospatial data, Python, and QGIS. The system applies the Five-Dimensional Assessment Model (5D-SAM) to calculate scores across key dimensions:

- **Location**: Proximity to high-risk zones.
- **Quality**: Structural integrity and condition of infrastructure.
- **Time**: Maintenance schedules and asset lifecycle.
- **Cost**: Cost-effectiveness based on budgets.
- **Environmental Impact**: Pollution mitigation and community benefits.

The application is designed to support decision-making by municipalities, enabling efficient management and strategic planning for stormwater systems.

---

## **Features**
1. **GIS Integration**:
   - Supports GeoJSON for stormwater data (e.g., pipes, basins, outfalls).
   - Integrates with QGIS for map visualization and data manipulation.

2. **Assessment Modules**:
   - Individual modules for Location, Quality, Time, Cost, and Environmental Impact.
   - Modular design allows for independent evaluation of each dimension.

3. **Scoring System**:
   - Calculates individual scores for each dimension.
   - Aggregates into an overall score to prioritize actions.

4. **Data Input Options**:
   - Manual entry for testing.
   - Supports real-time data from APIs or sensors (future enhancement).

---
## **Usage**

### 1. **Setup**
- Clone the repository:
  ```bash
  git clone https://github.com/yourusername/stormwater-assessment.git
  cd stormwater-assessment
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
