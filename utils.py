"""Utility functions for the ticket management system."""
import io
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def calculate_sla_deadline(priority: str, submitted_date: datetime) -> datetime:
    """Calculate SLA deadline based on priority."""
    sla_hours = {
        'Critical': 4,
        'High': 24,
        'Medium': 72,
        'Low': 168
    }
    hours = sla_hours.get(priority, 72)
    return submitted_date + timedelta(hours=hours)


def get_sla_status(deadline: Optional[datetime], closed_date: Optional[datetime], status: str) -> str:
    """Determine SLA status."""
    if not deadline:
        return "N/A"

    if status == "Closed":
        if closed_date and closed_date <= deadline:
            return "✅ Met"
        else:
            return "❌ Missed"
    else:
        if datetime.now() > deadline:
            return "⚠️ Overdue"
        elif datetime.now() > deadline - timedelta(hours=2):
            return "⚡ Critical"
        else:
            return "⏳ On Track"


def export_to_csv(df: pd.DataFrame) -> bytes:
    """Export DataFrame to CSV bytes."""
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue().encode('utf-8')


def format_timedelta(td: timedelta) -> str:
    """Format timedelta to human-readable string."""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "0m"


def get_priority_color(priority: str) -> str:
    """Get color for priority badge."""
    colors = {
        'Critical': '#dc3545',
        'High': '#fd7e14',
        'Medium': '#ffc107',
        'Low': '#28a745'
    }
    return colors.get(priority, '#6c757d')


def get_status_color(status: str) -> str:
    """Get color for status badge."""
    colors = {
        'Open': '#007bff',
        'In Progress': '#ffc107',
        'Closed': '#28a745',
        'On Hold': '#6c757d'
    }
    return colors.get(status, '#6c757d')


def validate_ticket_input(issue: str, priority: str) -> tuple[bool, str]:
    """Validate ticket input."""
    if not issue or len(issue.strip()) < 10:
        return False, "Issue description must be at least 10 characters long."

    if priority not in ['Critical', 'High', 'Medium', 'Low']:
        return False, "Invalid priority selected."

    return True, ""


def get_category_icon(category: str) -> str:
    """Get emoji icon for category."""
    icons = {
        'Technical': '💻',
        'Billing': '💰',
        'General': '📋',
        'Feature Request': '✨',
        'Bug Report': '🐛',
        'Security': '🔒',
        'Performance': '⚡',
        'Documentation': '📚'
    }
    return icons.get(category, '📋')
