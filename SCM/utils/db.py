import os
import sqlite3
import json
import streamlit as st
import bcrypt
from datetime import datetime, timedelta

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@st.cache_resource
def init_database():
    """Initialize SQLite database with required tables"""
    try:
        # Remove existing database to recreate schema
        if os.path.exists('stormwater_assessment.db'):
            os.remove('stormwater_assessment.db')

        conn = sqlite3.connect('stormwater_assessment.db', check_same_thread=False)
        conn.row_factory = dict_factory
        c = conn.cursor()

        # Create users table
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
        ''')

        # Create projects table
        c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_by INTEGER NOT NULL,
            created_at DATETIME NOT NULL,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')

        # Create project_members table
        c.execute('''
        CREATE TABLE IF NOT EXISTS project_members (
            project_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            joined_at DATETIME NOT NULL,
            PRIMARY KEY (project_id, user_id),
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Create activity log table
        c.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            action_details TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
        ''')

        # Create assessments table
        c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
        ''')

        # Create demo users
        demo_users = [
            ("admin", "admin123", True),
            ("john_engineer", "john123", False),
            ("sarah_manager", "sarah123", False),
            ("mike_analyst", "mike123", False),
            ("lisa_inspector", "lisa123", False),
            ("david_tech", "david123", False),
            ("emma_planner", "emma123", False),
            ("tom_supervisor", "tom123", False),
            ("kate_coordinator", "kate123", False),
            ("alex_specialist", "alex123", False)
        ]

        for username, password, is_admin in demo_users:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            c.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, hashed, is_admin)
            )

        # Create city-based projects
        city_projects = [
            ("New York City Flood Prevention", "Comprehensive stormwater management for NYC boroughs"),
            ("Miami Coastal Protection", "Climate resilience and flood control systems"),
            ("Seattle Green Infrastructure", "Sustainable urban drainage implementation"),
            ("Chicago Downtown Upgrade", "Modern stormwater infrastructure deployment"),
            ("Houston Flood Control", "Post-hurricane infrastructure enhancement"),
            ("San Francisco Bay Protection", "Bay area stormwater management"),
            ("Boston Harbor Resilience", "Coastal infrastructure modernization"),
            ("Denver Urban Drainage", "Mountain region water management"),
            ("Portland Green Solutions", "Eco-friendly stormwater systems"),
            ("Austin Water Conservation", "Integrated water management program")
        ]

        for name, description in city_projects:
            c.execute(
                "INSERT INTO projects (name, description, created_by, created_at) VALUES (?, ?, ?, ?)",
                (name, description, 1, datetime.utcnow().isoformat())
            )

        # Assign users to projects with different roles
        project_assignments = []
        for project_id in range(1, 11):  # 10 projects
            for user_id in range(1, 11):  # 10 users
                if user_id % 3 == 0:  # Make some users admins
                    project_assignments.append((user_id, project_id, "admin"))
                else:
                    project_assignments.append((user_id, project_id, "member"))

        for user_id, project_id, role in project_assignments:
            c.execute(
                "INSERT INTO project_members (project_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)",
                (project_id, user_id, role, datetime.utcnow().isoformat())
            )

        def create_city_specific_assessment(base_template, city_name):
            """Create city-specific assessment data"""
            assessment = dict(base_template)

            city_specifics = {
                "San Francisco Bay Protection": {
                    "condition": {
                        "stormwaterHydraulicAssetCondition": {
                            "damageLevels": {
                                "pipes": "moderate",
                                "culverts": "high",  # Due to seismic activity
                                "manholes": "moderate",
                                "drainageInlets": "high",  # Heavy rain seasons
                                "channels": "moderate"
                            }
                        }
                    },
                    "functionality": {
                        "hydraulicPerformance": {
                            "flowAttenuation": 85,  # Enhanced for coastal conditions
                            "volumeReduction": 75,
                            "csoFrequency": 3,
                            "drainageDurationFrequency": 18
                        }
                    },
                    "environmental_social": {
                        "pollutantConcentrationReduction": 90,  # High environmental standards
                        "customerSatisfaction": 8.5,
                        "pollutionRetention": 85
                    }
                },
                "Denver Urban Drainage": {
                    "condition": {
                        "stormwaterHydraulicAssetCondition": {
                            "damageLevels": {
                                "pipes": "low",  # Newer infrastructure
                                "culverts": "moderate",
                                "manholes": "low",
                                "drainageInlets": "moderate",  # Snow melt challenges
                                "channels": "low"
                            }
                        }
                    },
                    "functionality": {
                        "hydraulicPerformance": {
                            "flowAttenuation": 80,
                            "volumeReduction": 70,
                            "csoFrequency": 2,
                            "drainageDurationFrequency": 20
                        }
                    },
                    "environmental_social": {
                        "pollutantConcentrationReduction": 85,
                        "customerSatisfaction": 8.0,
                        "pollutionRetention": 80
                    }
                },
                "Boston Harbor Resilience": {
                    "condition": {
                        "stormwaterHydraulicAssetCondition": {
                            "damageLevels": {
                                "pipes": "high",  # Aging infrastructure
                                "culverts": "moderate",
                                "manholes": "high",
                                "drainageInlets": "moderate",
                                "channels": "high"
                            }
                        }
                    },
                    "functionality": {
                        "hydraulicPerformance": {
                            "flowAttenuation": 70,
                            "volumeReduction": 65,
                            "csoFrequency": 6,
                            "drainageDurationFrequency": 28
                        }
                    },
                    "environmental_social": {
                        "pollutantConcentrationReduction": 75,
                        "customerSatisfaction": 7.0,
                        "pollutionRetention": 70
                    }
                },
                "Portland Green Solutions": {
                    "condition": {
                        "stormwaterHydraulicAssetCondition": {
                            "damageLevels": {
                                "pipes": "low",  # Modern green infrastructure
                                "culverts": "low",
                                "manholes": "moderate",
                                "drainageInlets": "low",
                                "channels": "low"
                            }
                        }
                    },
                    "functionality": {
                        "hydraulicPerformance": {
                            "flowAttenuation": 90,  # Advanced green solutions
                            "volumeReduction": 85,
                            "csoFrequency": 1,
                            "drainageDurationFrequency": 16
                        }
                    },
                    "environmental_social": {
                        "pollutantConcentrationReduction": 95,  # Leading in environmental metrics
                        "customerSatisfaction": 9.0,
                        "pollutionRetention": 90
                    }
                }
            }

            if city_name in city_specifics:
                assessment.update(city_specifics[city_name])

            return assessment

        # Generate sample assessment data for each project
        sample_assessment_template = {
            "condition": {
                "stormwaterHydraulicAssetCondition": {
                    "damageLevels": {
                        "pipes": "moderate",
                        "culverts": "low",
                        "manholes": "high",
                        "drainageInlets": "moderate",
                        "channels": "low"
                    }
                }
            },
            "functionality": {
                "hydraulicPerformance": {
                    "flowAttenuation": 75,
                    "volumeReduction": 65,
                    "csoFrequency": 5,
                    "drainageDurationFrequency": 24
                }
            },
            "time_effectiveness": {
                "lifespan": 35,
                "maintenanceLagTime": 7,
                "floodDuration": 12
            },
            "cost_effectiveness": {
                "operationalCosts": 25000,
                "roi": 15,
                "constructionCosts": 150000,
                "preliminaryCosts": 50000
            },
            "environmental_social": {
                "pollutantConcentrationReduction": 80,
                "customerSatisfaction": 8,
                "pollutionRetention": 70
            }
        }

        # Generate 20 assessments per project with varying data
        for project_id in range(1, 11):
            # Get project name for city-specific data
            c.execute("SELECT name FROM projects WHERE id = ?", (project_id,))
            project = c.fetchone()
            project_name = project['name']

            for i in range(20):
                date = datetime.now() - timedelta(days=i*3)

                # Create variations in the assessment data
                assessment_data = create_city_specific_assessment(sample_assessment_template, project_name)

                # Add infrastructure points with city-specific locations
                city_coordinates = {
                    "San Francisco Bay Protection": (37.7749, -122.4194),
                    "Denver Urban Drainage": (39.7392, -104.9903),
                    "Boston Harbor Resilience": (42.3601, -71.0589),
                    "Portland Green Solutions": (45.5155, -122.6789)
                }

                base_lat, base_lon = city_coordinates.get(project_name, (40.7128, -74.0060))

                assessment_data["infrastructure_points"] = [
                    {
                        "name": f"Location {j+1}",
                        "type": ["pipes", "culverts", "drainageInlets", "manholes", "channels"][j % 5],
                        "latitude": base_lat + (j * 0.01),
                        "longitude": base_lon + (j * 0.01),
                        "age": 5 + j + (i % 5),  # Vary age based on assessment iteration
                        "last_maintenance_days": 30 + (j * 10) + (i % 30)  # Vary maintenance schedule
                    } for j in range(5)
                ]

                # Save assessment
                c.execute(
                    "INSERT INTO assessments (user_id, project_id, timestamp, data) VALUES (?, ?, ?, ?)",
                    (1 + (i % 10), project_id, date.isoformat(), json.dumps(assessment_data))
                )

                # Add activity log entry
                activity_types = ["assessment", "update", "maintenance", "report"]
                activity_details = [
                    "Completed infrastructure assessment",
                    "Updated risk assessment data",
                    "Performed scheduled maintenance",
                    "Generated detailed report"
                ]
                activity_index = i % 4

                c.execute(
                    "INSERT INTO activity_log (user_id, project_id, action_type, action_details, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (1 + (i % 10), project_id, activity_types[activity_index], activity_details[activity_index], date.isoformat())
                )

        conn.commit()
        return conn
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        raise e

def get_db():
    if 'db' not in st.session_state:
        st.session_state.db = init_database()
    return st.session_state.db

def create_project(name, description, created_by):
    """Create a new project"""
    try:
        db = get_db()
        c = db.cursor()
        c.execute(
            "INSERT INTO projects (name, description, created_by, created_at) VALUES (?, ?, ?, ?)",
            (name, description, created_by, datetime.utcnow().isoformat())
        )
        db.commit()
        return c.lastrowid
    except Exception as e:
        st.error(f"Failed to create project: {str(e)}")
        raise e

def add_project_member(project_id, user_id, role='member'):
    """Add a user to a project"""
    try:
        db = get_db()
        c = db.cursor()
        c.execute(
            "INSERT INTO project_members (project_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)",
            (project_id, user_id, role, datetime.utcnow().isoformat())
        )
        db.commit()
    except Exception as e:
        st.error(f"Failed to add project member: {str(e)}")
        raise e

def get_user_projects(user_id):
    """Get all projects a user is a member of"""
    try:
        db = get_db()
        c = db.cursor()
        c.execute("""
            SELECT DISTINCT p.*, pm.role
            FROM projects p
            JOIN project_members pm ON p.id = pm.project_id
            WHERE pm.user_id = ? AND p.status = 'active'
            ORDER BY p.created_at DESC
        """, (user_id,))
        return c.fetchall()
    except Exception as e:
        st.error(f"Failed to get user projects: {str(e)}")
        return []

def save_assessment(data):
    """Save assessment data"""
    try:
        db = get_db()
        c = db.cursor()

        if isinstance(data['timestamp'], datetime):
            timestamp = data['timestamp'].isoformat()
        else:
            timestamp = data['timestamp']

        c.execute(
            "INSERT INTO assessments (user_id, project_id, timestamp, data) VALUES (?, ?, ?, ?)",
            (
                int(data['user_id']),
                int(data['project_id']),
                timestamp,
                json.dumps(data, cls=DateTimeEncoder)
            )
        )
        db.commit()
        return c.lastrowid
    except Exception as e:
        st.error(f"Failed to save assessment: {str(e)}")
        raise e

def get_assessments(user_id=None, project_id=None):
    """Get assessments filtered by user and/or project"""
    try:
        db = get_db()
        c = db.cursor()

        query = "SELECT * FROM assessments WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)

        query += " ORDER BY timestamp DESC"
        c.execute(query, tuple(params))
        rows = c.fetchall()

        # Parse JSON data
        for row in rows:
            if isinstance(row['data'], str):
                row['data'] = json.loads(row['data'])

        return rows
    except Exception as e:
        st.error(f"Failed to retrieve assessments: {str(e)}")
        return []

def init_admin():
    """Initialize admin user if not exists"""
    try:
        db = get_db()
        c = db.cursor()

        c.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin = c.fetchone()

        if not admin:
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                c.execute(
                    "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                    ("admin", hashed, True)
                )
                db.commit()
                st.success("Admin user created successfully!")
                st.info("Username: admin, Password: admin123")
            except sqlite3.IntegrityError:
                pass
    except Exception as e:
        st.error(f"Failed to initialize admin user: {str(e)}")