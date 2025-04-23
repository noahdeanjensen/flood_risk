# Database Access Information
## Stormwater Infrastructure Assessment Project

### Database Type
The project currently uses SQLite, a file-based database system. For future scalability, we recommend migrating to a cloud-based solution such as MongoDB Atlas or PostgreSQL.

### Database Schema

#### Users Table
- `id` (INTEGER, PRIMARY KEY): Unique user identifier
- `username` (TEXT): User's login name
- `password_hash` (TEXT): Bcrypt hashed password
- `is_admin` (BOOLEAN): Administrator status
- `created_at` (TIMESTAMP): Account creation timestamp

#### Projects Table
- `id` (INTEGER, PRIMARY KEY): Unique project identifier
- `name` (TEXT): Project name
- `description` (TEXT): Project description
- `created_by` (INTEGER, FOREIGN KEY): User ID of creator
- `created_at` (TIMESTAMP): Project creation timestamp

#### Project_Members Table
- `id` (INTEGER, PRIMARY KEY): Unique member entry identifier
- `project_id` (INTEGER, FOREIGN KEY): Project identifier
- `user_id` (INTEGER, FOREIGN KEY): User identifier
- `role` (TEXT): Role within project (admin, member, viewer)
- `joined_at` (TIMESTAMP): Timestamp of joining project

#### Assessments Table
- `id` (INTEGER, PRIMARY KEY): Unique assessment identifier
- `user_id` (INTEGER, FOREIGN KEY): Creator of assessment
- `project_id` (INTEGER, FOREIGN KEY): Associated project
- `data` (JSON): Assessment data in JSON format
- `timestamp` (TIMESTAMP): Assessment creation timestamp

### Assessment Data Structure
The assessment data is stored as a JSON object with the following structure:

```json
{
  "condition": {
    "stormwaterHydraulicAssetCondition": {
      "pipeDiameterWidth": "600mm",
      "pipeScore": 7,
      "routineInspectionFrequency": "Quarterly",
      "damageLevels": {
        "cracks": {
          "condition": "low",
          "score": 8
        },
        "sediment_build_up": {
          "condition": "moderate",
          "score": 5
        },
        "corrosion": {
          "condition": "low",
          "score": 7
        }
      }
    },
    "OSAC": {
      "score": 7,
      "rating": "Good"
    }
  },
  "functionality": {
    "hydraulicPerformance": {
      "flowAttenuation": 69,
      "volumeReduction": 73,
      "csoVolume": 250,
      "totalFlowVolume": 1000,
      "overflowPercentage": 25.0,
      "dryWeatherFlow": 82,
      "overflowFrequency": 65,
      "drainageDurationPerformance": 70
    },
    "hydrologicalPerformance": {
      "runoffFrequency": 65,
      "baseFlowPerformance": 70,
      "inflowPerformance": 80.0,
      "catchmentScalePerformance": 85
    },
    "overallFunctionality": {
      "score": 8,
      "rating": "Good"
    }
  },
  "time_effectiveness": {
    "longTermFunctionality": 60,
    "designLifespan": 50,
    "currentAge": 15,
    "agePercentage": 30.0,
    "lagTimePerformance": 80,
    "maintenanceResponseTarget": 14,
    "actualResponseTime": 18,
    "monitoringFrequency": "Weekly",
    "overallTimeScore": 7,
    "overallTimeRating": "Good"
  },
  "cost_effectiveness": {
    "preliminaryCosts": 75000,
    "constructionCosts": 1250000,
    "annualOperationalCosts": 52000,
    "lifecyclePeriod": 30,
    "discountRate": 4.5,
    "totalLifecycleCost": 1885000.0,
    "annualFloodDamagePrevention": 95000,
    "annualEnvironmentalBenefits": 45000,
    "totalBenefits": 4200000.0,
    "benefitCostRatio": 2.2,
    "roi": 122.8,
    "overallCostScore": 8,
    "overallCostRating": "Good"
  },
  "environmental_social": {
    "pollutantConcentrationAttenuation": 70,
    "eventBasedPollutantRemoval": 55,
    "pollutionRetentionPerformance": 66,
    "tssReduction": 75,
    "nutrientReduction": 60,
    "bacteriaReduction": 68,
    "customerSatisfaction": 50,
    "communityEngagement": "Moderate",
    "accidentFrequency": 2,
    "accidentSeverity": "Minor",
    "environmentalScore": 7.0,
    "socialScore": 6.0,
    "overallScore": 7,
    "overallRating": "Good"
  },
  "infrastructure_points": [
    {
      "name": "Main Outfall",
      "type": "outfalls",
      "latitude": 40.7128,
      "longitude": -74.006,
      "age": 12,
      "last_maintenance_days": 45
    },
    {
      "name": "Retention Basin North",
      "type": "bioRetentionBasins",
      "latitude": 40.7135,
      "longitude": -74.0052,
      "age": 5,
      "last_maintenance_days": 120
    }
  ],
  "timestamp": "2025-04-07T14:30:00"
}
```

### Access Instructions for Developers

#### Local Development
1. The SQLite database file is located at: `stormwater_assessment.db`
2. Use SQL queries or ORM (Object-Relational Mapping) to interact with the database
3. For Python access, use the utilities in `utils/db.py`

#### Recommended Migration Steps
1. Create a cloud database (PostgreSQL or MongoDB)
2. Execute migration scripts (provided in `utils/db_migration.py`)
3. Update connection strings in the application
4. Verify data integrity after migration

### Authentication Information
Default database access credentials:

- **Regular User Access**
  - Username: `user`
  - Password: `password123`

- **Admin Access**
  - Username: `admin`
  - Password: `admin123`

### Database Backup Information
- Current backup schedule: Daily at 2:00 AM
- Backup location: `backups/` directory
- Backup naming convention: `stormwater_assessment_YYYY-MM-DD.db`

### API Integration Information
For AI model integration, data can be accessed through the following functions in `utils/db.py`:

- `get_assessments()`: Retrieve assessment data
- `get_infrastructure_points()`: Get geospatial data
- `get_historical_metrics()`: Get time-series metrics

Sample code for AI model integration:

```python
from utils.db import get_assessments

# Get all assessments for a specific project
assessments = get_assessments(project_id=12)

# Extract features for model training
features = []
labels = []

for assessment in assessments:
    # Extract relevant features from assessment data
    data = assessment['data']
    
    # Example: Predicting condition score based on infrastructure parameters
    features.append([
        data['time_effectiveness']['currentAge'],
        data['time_effectiveness']['designLifespan'],
        data['functionality']['hydraulicPerformance']['flowAttenuation'],
        data['functionality']['hydraulicPerformance']['volumeReduction']
    ])
    
    # Target label is the condition score
    labels.append(data['condition']['OSAC']['score'])

# Train ML model with these features and labels
# model.fit(features, labels)
```

This document should be updated when migrating to a cloud-based database solution.