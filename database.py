"""Database module for ticket management system."""
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

        conn.commit()
        conn.close()
        return ticket_data['ticket_id']

    def update_ticket(self, ticket_id: str, updates: Dict[str, Any]):
        """Update an existing ticket."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

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

        conn.commit()
        conn.close()

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
