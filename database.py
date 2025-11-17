"""Extended database module with To-Do List and Activity tracking."""
import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict, Any


class TicketDatabase:
    """Handles all database operations for the ticket system."""

    def __init__(self, db_path: str = "tickets.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create all necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                issue TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                category TEXT,
                assigned_to TEXT,
                date_submitted DATE NOT NULL,
                date_updated DATE,
                date_closed DATE,
                sla_deadline DATE,
                created_by TEXT DEFAULT 'System'
            )
        """)

        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                comment TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        """)

        # Attachments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        """)

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # To-Do List table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                priority TEXT DEFAULT 'Medium',
                due_date DATE,
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                created_by TEXT,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        """)

        # Activity Log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                action TEXT NOT NULL,
                field_changed TEXT,
                old_value TEXT,
                new_value TEXT,
                user TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        """)

        # Response Templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS response_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                template_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT
            )
        """)

        conn.commit()
        conn.close()

    def add_ticket(self, ticket_data: Dict[str, Any]) -> str:
        """Add a new ticket to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tickets (
                ticket_id, issue, status, priority, category,
                assigned_to, date_submitted, created_by, sla_deadline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_data['ticket_id'],
            ticket_data['issue'],
            ticket_data['status'],
            ticket_data['priority'],
            ticket_data.get('category', 'General'),
            ticket_data.get('assigned_to', 'Unassigned'),
            ticket_data['date_submitted'],
            ticket_data.get('created_by', 'System'),
            ticket_data.get('sla_deadline')
        ))

        # Log activity
        self._log_activity(
            cursor,
            ticket_data['ticket_id'],
            'created',
            None,
            None,
            f"Ticket created with priority {ticket_data['priority']}",
            ticket_data.get('created_by', 'System')
        )

        conn.commit()
        conn.close()
        return ticket_data['ticket_id']

    def update_ticket(self, ticket_id: str, updates: Dict[str, Any], user: str = 'System'):
        """Update an existing ticket and log changes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current values for logging
        cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            old_values = dict(zip(columns, row))

        updates['date_updated'] = datetime.now().date()
        if updates.get('status') == 'Closed' and 'date_closed' not in updates:
            updates['date_closed'] = datetime.now().date()

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [ticket_id]

        cursor.execute(f"""
            UPDATE tickets
            SET {set_clause}
            WHERE ticket_id = ?
        """, values)

        # Log changes
        for field, new_value in updates.items():
            if field not in ['date_updated', 'date_closed']:
                old_value = old_values.get(field)
                if old_value != new_value:
                    self._log_activity(
                        cursor,
                        ticket_id,
                        'updated',
                        field,
                        str(old_value) if old_value else None,
                        str(new_value),
                        user
                    )

        conn.commit()
        conn.close()

    def _log_activity(self, cursor, ticket_id, action, field_changed, old_value, new_value, user):
        """Internal method to log activity."""
        cursor.execute("""
            INSERT INTO activity_log (ticket_id, action, field_changed, old_value, new_value, user)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, action, field_changed, old_value, new_value, user))

    def get_activity_log(self, ticket_id: Optional[str] = None) -> pd.DataFrame:
        """Get activity log for a ticket or all tickets."""
        conn = sqlite3.connect(self.db_path)

        if ticket_id:
            df = pd.read_sql_query(
                "SELECT * FROM activity_log WHERE ticket_id = ? ORDER BY timestamp DESC",
                conn,
                params=(ticket_id,)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 100",
                conn
            )

        conn.close()
        return df

    def get_all_tickets(self) -> pd.DataFrame:
        """Retrieve all tickets as a DataFrame."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM tickets ORDER BY id DESC", conn)
        conn.close()

        # Convert date columns
        date_columns = ['date_submitted', 'date_updated', 'date_closed', 'sla_deadline']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get a single ticket by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None

    def add_comment(self, ticket_id: str, comment: str, author: str):
        """Add a comment to a ticket."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO comments (ticket_id, comment, author)
            VALUES (?, ?, ?)
        """, (ticket_id, comment, author))

        # Log activity
        self._log_activity(
            cursor,
            ticket_id,
            'comment_added',
            None,
            None,
            f"Comment by {author}",
            author
        )

        conn.commit()
        conn.close()

    def get_comments(self, ticket_id: str) -> pd.DataFrame:
        """Get all comments for a ticket."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM comments WHERE ticket_id = ? ORDER BY created_at DESC",
            conn,
            params=(ticket_id,)
        )
        conn.close()
        return df

    # To-Do List Methods
    def add_todo(self, task: str, ticket_id: Optional[str] = None, priority: str = 'Medium',
                 due_date: Optional[datetime] = None, assigned_to: Optional[str] = None,
                 created_by: str = 'System') -> int:
        """Add a new to-do item."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO todos (ticket_id, task, priority, due_date, assigned_to, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, task, priority, due_date, assigned_to, created_by))

        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return todo_id

    def get_todos(self, ticket_id: Optional[str] = None, completed: Optional[bool] = None) -> pd.DataFrame:
        """Get to-do items, optionally filtered by ticket or completion status."""
        conn = sqlite3.connect(self.db_path)

        query = "SELECT * FROM todos WHERE 1=1"
        params = []

        if ticket_id is not None:
            query += " AND ticket_id = ?"
            params.append(ticket_id)

        if completed is not None:
            query += " AND completed = ?"
            params.append(1 if completed else 0)

        query += " ORDER BY completed ASC, due_date ASC, created_at DESC"

        df = pd.read_sql_query(query, conn, params=params if params else None)
        conn.close()

        if not df.empty:
            df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df['completed_at'] = pd.to_datetime(df['completed_at'], errors='coerce')

        return df

    def update_todo(self, todo_id: int, updates: Dict[str, Any]):
        """Update a to-do item."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if 'completed' in updates and updates['completed']:
            updates['completed_at'] = datetime.now()

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [todo_id]

        cursor.execute(f"""
            UPDATE todos
            SET {set_clause}
            WHERE id = ?
        """, values)

        conn.commit()
        conn.close()

    def delete_todo(self, todo_id: int):
        """Delete a to-do item."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

        conn.commit()
        conn.close()

    def toggle_todo(self, todo_id: int) -> bool:
        """Toggle a to-do item's completion status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()

        if row:
            new_status = not row[0]
            completed_at = datetime.now() if new_status else None

            cursor.execute("""
                UPDATE todos SET completed = ?, completed_at = ?
                WHERE id = ?
            """, (new_status, completed_at, todo_id))

            conn.commit()
            conn.close()
            return new_status

        conn.close()
        return False

    # Response Templates Methods
    def add_response_template(self, name: str, template_text: str, category: str = 'General',
                            created_by: str = 'System'):
        """Add a response template."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO response_templates (name, category, template_text, created_by)
                VALUES (?, ?, ?, ?)
            """, (name, category, template_text, created_by))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Template already exists
        finally:
            conn.close()

    def get_response_templates(self, category: Optional[str] = None) -> pd.DataFrame:
        """Get response templates."""
        conn = sqlite3.connect(self.db_path)

        if category:
            df = pd.read_sql_query(
                "SELECT * FROM response_templates WHERE category = ? ORDER BY name",
                conn,
                params=(category,)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM response_templates ORDER BY category, name",
                conn
            )

        conn.close()
        return df

    def search_tickets(self,
                      search_term: Optional[str] = None,
                      status: Optional[List[str]] = None,
                      priority: Optional[List[str]] = None,
                      category: Optional[List[str]] = None,
                      assigned_to: Optional[List[str]] = None) -> pd.DataFrame:
        """Search tickets with multiple filters."""
        conn = sqlite3.connect(self.db_path)

        query = "SELECT * FROM tickets WHERE 1=1"
        params = []

        if search_term:
            query += " AND (issue LIKE ? OR ticket_id LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])

        if status:
            placeholders = ",".join(["?" for _ in status])
            query += f" AND status IN ({placeholders})"
            params.extend(status)

        if priority:
            placeholders = ",".join(["?" for _ in priority])
            query += f" AND priority IN ({placeholders})"
            params.extend(priority)

        if category:
            placeholders = ",".join(["?" for _ in category])
            query += f" AND category IN ({placeholders})"
            params.extend(category)

        if assigned_to:
            placeholders = ",".join(["?" for _ in assigned_to])
            query += f" AND assigned_to IN ({placeholders})"
            params.extend(assigned_to)

        query += " ORDER BY id DESC"

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # Convert date columns
        date_columns = ['date_submitted', 'date_updated', 'date_closed', 'sla_deadline']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def get_next_ticket_number(self) -> int:
        """Get the next ticket number."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM tickets")
        result = cursor.fetchone()[0]
        conn.close()

        # Return ID starting at 1001 for first ticket
        if result is None:
            return 1001
        else:
            return result + 1001

    def get_statistics(self) -> Dict[str, Any]:
        """Get ticket statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total tickets
        cursor.execute("SELECT COUNT(*) FROM tickets")
        stats['total_tickets'] = cursor.fetchone()[0]

        # Tickets by status
        cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
        stats['by_status'] = dict(cursor.fetchall())

        # Tickets by priority
        cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
        stats['by_priority'] = dict(cursor.fetchall())

        # Tickets by category
        cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
        stats['by_category'] = dict(cursor.fetchall())

        # Average resolution time (in days)
        cursor.execute("""
            SELECT AVG(JULIANDAY(date_closed) - JULIANDAY(date_submitted))
            FROM tickets WHERE date_closed IS NOT NULL
        """)
        result = cursor.fetchone()[0]
        stats['avg_resolution_days'] = round(result, 2) if result else 0

        # To-Do statistics
        cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 0")
        stats['pending_todos'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
        stats['completed_todos'] = cursor.fetchone()[0]

        conn.close()
        return stats

    def add_user(self, username: str, full_name: str, role: str):
        """Add a new user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, full_name, role)
                VALUES (?, ?, ?)
            """, (username, full_name, role))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # User already exists
        finally:
            conn.close()

    def get_users(self) -> List[str]:
        """Get all users."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users ORDER BY username")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()

        return users if users else ['Unassigned']
