"""
Comprehensive tests for the ticket management system.
Run with: python -m pytest test_app.py -v
"""

import pytest
import os
import datetime
from database import TicketDatabase
from utils import (
    calculate_sla_deadline,
    get_sla_status,
    validate_ticket_input,
    get_category_icon,
    format_timedelta
)


class TestDatabase:
    """Tests for database functionality."""

    @pytest.fixture
    def test_db(self):
        """Create a test database."""
        test_db_path = "test_tickets.db"
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

        db = TicketDatabase(test_db_path)
        yield db

        # Cleanup
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def test_database_initialization(self, test_db):
        """Test that database initializes correctly."""
        stats = test_db.get_statistics()
        assert stats['total_tickets'] == 0
        assert isinstance(stats, dict)

    def test_add_ticket(self, test_db):
        """Test adding a new ticket."""
        ticket_data = {
            'ticket_id': 'TICKET-1001',
            'issue': 'Test issue',
            'status': 'Open',
            'priority': 'High',
            'category': 'Technical',
            'assigned_to': 'john_doe',
            'date_submitted': datetime.date.today(),
            'created_by': 'Test User',
            'sla_deadline': datetime.datetime.now() + datetime.timedelta(hours=24)
        }

        ticket_id = test_db.add_ticket(ticket_data)
        assert ticket_id == 'TICKET-1001'

        # Verify ticket was added
        stats = test_db.get_statistics()
        assert stats['total_tickets'] == 1

    def test_get_all_tickets(self, test_db):
        """Test retrieving all tickets."""
        # Add test tickets
        for i in range(5):
            ticket_data = {
                'ticket_id': f'TICKET-{1001 + i}',
                'issue': f'Test issue {i}',
                'status': 'Open',
                'priority': 'Medium',
                'category': 'General',
                'assigned_to': 'Unassigned',
                'date_submitted': datetime.date.today(),
                'created_by': 'Test',
                'sla_deadline': None
            }
            test_db.add_ticket(ticket_data)

        df = test_db.get_all_tickets()
        assert len(df) == 5
        assert 'ticket_id' in df.columns

    def test_update_ticket(self, test_db):
        """Test updating a ticket."""
        # Add a ticket first
        ticket_data = {
            'ticket_id': 'TICKET-1001',
            'issue': 'Test issue',
            'status': 'Open',
            'priority': 'High',
            'category': 'Technical',
            'assigned_to': 'john_doe',
            'date_submitted': datetime.date.today(),
            'created_by': 'Test',
            'sla_deadline': None
        }
        test_db.add_ticket(ticket_data)

        # Update the ticket
        updates = {'status': 'Closed', 'priority': 'Low'}
        test_db.update_ticket('TICKET-1001', updates)

        # Verify update
        ticket = test_db.get_ticket('TICKET-1001')
        assert ticket['status'] == 'Closed'
        assert ticket['priority'] == 'Low'
        assert ticket['date_updated'] is not None

    def test_search_tickets(self, test_db):
        """Test ticket search functionality."""
        # Add test tickets
        priorities = ['Critical', 'High', 'Medium', 'Low']
        for i, priority in enumerate(priorities):
            ticket_data = {
                'ticket_id': f'TICKET-{1001 + i}',
                'issue': f'Test issue {i}',
                'status': 'Open',
                'priority': priority,
                'category': 'Technical',
                'assigned_to': 'Unassigned',
                'date_submitted': datetime.date.today(),
                'created_by': 'Test',
                'sla_deadline': None
            }
            test_db.add_ticket(ticket_data)

        # Search by priority
        results = test_db.search_tickets(priority=['Critical'])
        assert len(results) == 1
        assert results.iloc[0]['priority'] == 'Critical'

        # Search by search term
        results = test_db.search_tickets(search_term='issue 2')
        assert len(results) >= 1

    def test_add_user(self, test_db):
        """Test adding users."""
        test_db.add_user('testuser', 'Test User', 'Agent')
        users = test_db.get_users()
        assert 'testuser' in users

    def test_statistics(self, test_db):
        """Test statistics calculation."""
        # Add tickets with different statuses
        statuses = ['Open', 'In Progress', 'Closed']
        for i, status in enumerate(statuses):
            ticket_data = {
                'ticket_id': f'TICKET-{1001 + i}',
                'issue': f'Test issue {i}',
                'status': status,
                'priority': 'Medium',
                'category': 'Technical',
                'assigned_to': 'Unassigned',
                'date_submitted': datetime.date.today(),
                'created_by': 'Test',
                'sla_deadline': None
            }
            test_db.add_ticket(ticket_data)

        stats = test_db.get_statistics()
        assert stats['total_tickets'] == 3
        assert stats['by_status']['Open'] == 1
        assert stats['by_status']['Closed'] == 1

    def test_next_ticket_number(self, test_db):
        """Test ticket number generation."""
        # First ticket
        next_num = test_db.get_next_ticket_number()
        assert next_num == 1001

        # Add a ticket
        ticket_data = {
            'ticket_id': 'TICKET-1001',
            'issue': 'Test',
            'status': 'Open',
            'priority': 'Medium',
            'category': 'General',
            'assigned_to': 'Unassigned',
            'date_submitted': datetime.date.today(),
            'created_by': 'Test',
            'sla_deadline': None
        }
        test_db.add_ticket(ticket_data)

        # Next ticket should be 1002
        next_num = test_db.get_next_ticket_number()
        assert next_num == 1002


class TestUtils:
    """Tests for utility functions."""

    def test_calculate_sla_deadline(self):
        """Test SLA deadline calculation."""
        base_date = datetime.datetime(2024, 1, 1, 12, 0, 0)

        # Critical: 4 hours
        deadline = calculate_sla_deadline('Critical', base_date)
        assert deadline == base_date + datetime.timedelta(hours=4)

        # High: 24 hours
        deadline = calculate_sla_deadline('High', base_date)
        assert deadline == base_date + datetime.timedelta(hours=24)

        # Medium: 72 hours
        deadline = calculate_sla_deadline('Medium', base_date)
        assert deadline == base_date + datetime.timedelta(hours=72)

        # Low: 168 hours
        deadline = calculate_sla_deadline('Low', base_date)
        assert deadline == base_date + datetime.timedelta(hours=168)

    def test_get_sla_status(self):
        """Test SLA status determination."""
        future_deadline = datetime.datetime.now() + datetime.timedelta(hours=10)
        past_deadline = datetime.datetime.now() - datetime.timedelta(hours=10)
        critical_deadline = datetime.datetime.now() + datetime.timedelta(hours=1)

        # Closed and met SLA
        status = get_sla_status(future_deadline, datetime.datetime.now(), 'Closed')
        assert '✅' in status

        # Overdue
        status = get_sla_status(past_deadline, None, 'Open')
        assert '⚠️' in status

        # On track
        status = get_sla_status(future_deadline, None, 'Open')
        assert status in ['⏳ On Track', '⚡ Critical']

        # No deadline
        status = get_sla_status(None, None, 'Open')
        assert status == 'N/A'

    def test_validate_ticket_input(self):
        """Test ticket input validation."""
        # Valid input
        is_valid, msg = validate_ticket_input("This is a valid issue description", "High")
        assert is_valid == True
        assert msg == ""

        # Too short
        is_valid, msg = validate_ticket_input("Short", "High")
        assert is_valid == False
        assert "10 characters" in msg

        # Empty
        is_valid, msg = validate_ticket_input("", "High")
        assert is_valid == False

        # Invalid priority
        is_valid, msg = validate_ticket_input("Valid description", "Invalid")
        assert is_valid == False
        assert "Invalid priority" in msg

    def test_get_category_icon(self):
        """Test category icon retrieval."""
        assert get_category_icon('Technical') == '💻'
        assert get_category_icon('Billing') == '💰'
        assert get_category_icon('General') == '📋'
        assert get_category_icon('Unknown') == '📋'  # Default

    def test_format_timedelta(self):
        """Test timedelta formatting."""
        # Days, hours, minutes
        td = datetime.timedelta(days=2, hours=3, minutes=15)
        result = format_timedelta(td)
        assert '2d' in result
        assert '3h' in result
        assert '15m' in result

        # Just hours
        td = datetime.timedelta(hours=5)
        result = format_timedelta(td)
        assert '5h' in result

        # Zero time
        td = datetime.timedelta()
        result = format_timedelta(td)
        assert result == '0m'


class TestIntegration:
    """Integration tests."""

    @pytest.fixture
    def test_db(self):
        """Create a test database."""
        test_db_path = "test_integration.db"
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

        db = TicketDatabase(test_db_path)
        yield db

        # Cleanup
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def test_complete_ticket_workflow(self, test_db):
        """Test complete ticket lifecycle."""
        # Create a ticket
        today = datetime.date.today()
        sla_deadline = calculate_sla_deadline('High', datetime.datetime.combine(today, datetime.time()))

        ticket_data = {
            'ticket_id': 'TICKET-1001',
            'issue': 'Complete workflow test ticket',
            'status': 'Open',
            'priority': 'High',
            'category': 'Technical',
            'assigned_to': 'john_doe',
            'date_submitted': today,
            'created_by': 'Test User',
            'sla_deadline': sla_deadline
        }

        # Add ticket
        ticket_id = test_db.add_ticket(ticket_data)
        assert ticket_id == 'TICKET-1001'

        # Add user
        test_db.add_user('john_doe', 'John Doe', 'Agent')

        # Get ticket
        ticket = test_db.get_ticket(ticket_id)
        assert ticket is not None
        assert ticket['status'] == 'Open'

        # Update to In Progress
        test_db.update_ticket(ticket_id, {'status': 'In Progress'})
        ticket = test_db.get_ticket(ticket_id)
        assert ticket['status'] == 'In Progress'

        # Add comment
        test_db.add_comment(ticket_id, 'Working on this issue', 'john_doe')
        comments = test_db.get_comments(ticket_id)
        assert len(comments) == 1
        assert comments.iloc[0]['comment'] == 'Working on this issue'

        # Close ticket
        test_db.update_ticket(ticket_id, {'status': 'Closed'})
        ticket = test_db.get_ticket(ticket_id)
        assert ticket['status'] == 'Closed'
        assert ticket['date_closed'] is not None

        # Check statistics
        stats = test_db.get_statistics()
        assert stats['total_tickets'] == 1
        assert stats['by_status']['Closed'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
