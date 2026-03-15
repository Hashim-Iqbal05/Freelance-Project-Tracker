import sqlite3

DB_NAME = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS freelancers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill TEXT,
            email TEXT
        )
    """)
    # Safely migrate existing database
    try: cursor.execute("ALTER TABLE freelancers ADD COLUMN years_experience INTEGER DEFAULT 0")
    except Exception: pass
    try: cursor.execute("ALTER TABLE freelancers ADD COLUMN portfolio_link TEXT DEFAULT ''")
    except Exception: pass
    try: cursor.execute("ALTER TABLE freelancers ADD COLUMN projects_completed INTEGER DEFAULT 0")
    except Exception: pass
    try: cursor.execute("ALTER TABLE freelancers ADD COLUMN specialization TEXT DEFAULT 'React'")
    except Exception: pass
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            client_name TEXT,
            freelancer TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'Pending',
            payment_status TEXT DEFAULT 'Unpaid'
        )
    """)
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
#  FREELANCER CRUD OPERATIONS
# ─────────────────────────────────────────────

def add_freelancer(name, skill, email, years_experience=0, portfolio_link='', projects_completed=0, specialization='React'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO freelancers (name, skill, email, years_experience, portfolio_link, projects_completed, specialization) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        (name, skill, email, years_experience, portfolio_link, projects_completed, specialization)
    )
    conn.commit()
    conn.close()

def get_all_freelancers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM freelancers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_freelancer(freelancer_id, name, skill, email, years_experience=0, portfolio_link='', projects_completed=0, specialization='React'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE freelancers SET name=?, skill=?, email=?, years_experience=?, portfolio_link=?, projects_completed=?, specialization=? WHERE id=?", 
        (name, skill, email, years_experience, portfolio_link, projects_completed, specialization, freelancer_id)
    )
    conn.commit()
    conn.close()

def delete_freelancer(freelancer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM freelancers WHERE id=?", (freelancer_id,))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
#  PROJECT CRUD OPERATIONS
# ─────────────────────────────────────────────

def check_and_auto_add_freelancer(freelancer_name):
    """Checks if a freelancer exists by NOCASE. If not, adds them instantly."""
    if freelancer_name and freelancer_name.strip():
        name = freelancer_name.strip()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM freelancers WHERE name=? COLLATE NOCASE", (name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO freelancers (name, skill, email) VALUES (?, ?, ?)", (name, "Auto-Added", "None"))
            conn.commit()
        conn.close()

def add_project(project_name, client_name, freelancer, deadline, status, payment_status):
    check_and_auto_add_freelancer(freelancer)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO projects 
           (project_name, client_name, freelancer, deadline, status, payment_status) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (project_name, client_name, freelancer, deadline, status, payment_status)
    )
    conn.commit()
    conn.close()

def get_all_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_project(project_id, project_name, client_name, freelancer, deadline, status, payment_status):
    check_and_auto_add_freelancer(freelancer)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE projects 
           SET project_name=?, client_name=?, freelancer=?, 
               deadline=?, status=?, payment_status=? 
           WHERE id=?""",
        (project_name, client_name, freelancer, deadline, status, payment_status, project_id)
    )
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM projects")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='In Progress'")
    in_progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE payment_status='Unpaid'")
    unpaid = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM freelancers")
    total_freelancers = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "unpaid": unpaid,
        "total_freelancers": total_freelancers
    }

def get_upcoming_deadlines(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_name, deadline, status FROM projects WHERE status != 'Completed' ORDER BY deadline ASC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_recent_projects(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_name, client_name, status FROM projects ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows