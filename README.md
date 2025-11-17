# 🎫 Professional Support Ticket Management System

A production-ready, feature-rich support ticket management application built with Streamlit, featuring advanced analytics, SLA tracking, To-Do Lists, Activity Tracking, Response Templates, and a beautiful modern UI.

[![Built with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

## ✨ Features

### Core Functionality
- **📋 Comprehensive Dashboard** - Real-time overview of all tickets, to-dos, and recent activity
- **➕ Smart Ticket Creation** - Create tickets with validation, categories, and automatic SLA assignment
- **🎫 Advanced Ticket Management** - Edit, filter, search, and manage all tickets with persistence
- **✅ To-Do List Management** - Create, track, and manage tasks linked to tickets or standalone
- **📝 Response Templates** - Pre-built templates for common responses
- **📊 Analytics & Reporting** - Detailed analytics with trends, performance metrics, and insights

### Advanced Features
- **💾 SQLite Database** - Persistent data storage with full CRUD operations
- **🔍 Search & Filtering** - Multi-criteria search by status, priority, category, assignee, and keywords
- **📥 Data Export** - Export tickets to CSV format
- **🌙 Dark Mode** - Toggle between light and dark themes
- **⏱️ SLA Tracking** - Automatic SLA deadline calculation and compliance monitoring
- **👥 User Management** - Assign tickets to agents and track performance
- **🏷️ Categories & Tags** - Organize tickets with customizable categories
- **💬 Comments System** - Add comments and notes to tickets
- **📜 Activity Log** - Complete audit trail of all ticket changes
- **📈 Time Series Analysis** - Track ticket trends over time
- **🎯 Priority Management** - 4-tier priority system (Critical, High, Medium, Low)
- **✅ Input Validation** - Comprehensive validation for all user inputs
- **💾 Persistent Editing** - Save ticket changes directly to database
- **🔗 Ticket Linking** - Associate to-dos with specific tickets
- **🎨 Beautiful UI** - Modern, gradient-based design with custom CSS

### SLA Timeframes
- **Critical**: 4 hours
- **High**: 24 hours
- **Medium**: 72 hours (3 days)
- **Low**: 168 hours (7 days)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot-nora
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 📖 Usage Guide

### Creating a Ticket

1. Navigate to the **"➕ New Ticket"** tab
2. Fill in the required fields:
   - **Issue Description**: Detailed description (minimum 10 characters)
   - **Priority**: Select from Critical, High, Medium, or Low
   - **Category**: Choose the appropriate category
   - **Assign To**: Select an agent or leave as Unassigned
   - **Create related To-Do**: Optionally create a linked to-do item
3. Click **"🚀 Submit Ticket"**
4. The system will automatically calculate the SLA deadline based on priority

### Managing Tickets

1. Go to the **"🎫 Tickets"** tab
2. Use the sidebar filters to narrow down tickets:
   - Filter by Status, Priority, Category, or Assignee
   - Use the search box to find specific tickets
3. Edit tickets directly in the table by double-clicking cells
4. Click **"💾 Save Changes"** to persist edits to the database
5. Select a ticket to view full details, comments, and activity
6. Add comments to tickets for collaboration

### Using the To-Do List

1. Navigate to the **"✅ To-Do List"** tab
2. Create new to-dos:
   - Enter task description
   - Set priority and due date
   - Assign to a team member
   - Optionally link to a ticket
3. Manage existing to-dos:
   - Check boxes to mark as complete
   - View overdue tasks (highlighted in red)
   - Delete completed or obsolete tasks
4. Track completion metrics and productivity

### Working with Response Templates

1. Go to the **"📝 Templates"** tab
2. Browse existing templates by category
3. Create new templates:
   - Give it a descriptive name
   - Select a category (Technical, Billing, General, Follow-up)
   - Write template text with [PLACEHOLDERS]
4. Use templates to speed up common responses

### Viewing Analytics

1. Navigate to the **"📊 Analytics"** tab
2. Explore various metrics:
   - **Ticket Trends**: Time series analysis of ticket volume
   - **Resolution Time**: Average and median resolution times
   - **Agent Performance**: See which agents are most effective
   - **SLA Compliance**: Monitor SLA adherence rates

### Exporting Data

1. In the sidebar, find the **"📥 Export Data"** section
2. Click **"Download CSV"**
3. Click the **"💾 Download"** button to save the CSV file

### Using Dark Mode

1. In the sidebar, find the **"⚙️ Settings"** section
2. Toggle the **"🌙 Dark Mode"** checkbox
3. The entire interface will switch themes

## 🏗️ Architecture

### Project Structure
```
chatbot-nora/
├── streamlit_app.py      # Main application file
├── database.py           # Database operations and models
├── utils.py              # Utility functions
├── styles.py             # Custom CSS styling
├── test_app.py           # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── tickets.db           # SQLite database (auto-generated)
```

### Database Schema

**Tickets Table**
- `id`: Primary key (auto-increment)
- `ticket_id`: Unique ticket identifier (e.g., TICKET-1001)
- `issue`: Issue description
- `status`: Open, In Progress, Closed, On Hold
- `priority`: Critical, High, Medium, Low
- `category`: Technical, Billing, General, etc.
- `assigned_to`: Assigned agent username
- `date_submitted`: Creation date
- `date_updated`: Last update date
- `date_closed`: Closure date
- `sla_deadline`: SLA deadline timestamp
- `created_by`: Creator name

**To-Dos Table** (NEW!)
- `id`: Primary key
- `ticket_id`: Optional link to ticket
- `task`: Task description
- `completed`: Boolean completion status
- `priority`: Critical, High, Medium, Low
- `due_date`: Due date
- `assigned_to`: Assigned user
- `created_at`: Creation timestamp
- `completed_at`: Completion timestamp
- `created_by`: Creator name

**Comments Table**
- `id`: Primary key
- `ticket_id`: Foreign key to tickets
- `comment`: Comment text
- `author`: Comment author
- `created_at`: Timestamp

**Activity Log Table** (NEW!)
- `id`: Primary key
- `ticket_id`: Related ticket
- `action`: Type of action (created, updated, etc.)
- `field_changed`: Which field was modified
- `old_value`: Previous value
- `new_value`: New value
- `user`: User who made the change
- `timestamp`: When the change occurred

**Response Templates Table** (NEW!)
- `id`: Primary key
- `name`: Unique template name
- `category`: Template category
- `template_text`: Template content
- `created_at`: Creation timestamp
- `created_by`: Creator name

**Users Table**
- `id`: Primary key
- `username`: Unique username
- `full_name`: Full name
- `role`: Agent, Admin, etc.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
python -m pytest test_app.py -v

# Run specific test class
python -m pytest test_app.py::TestDatabase -v

# Run with coverage
pip install pytest-cov
pytest test_app.py --cov=. --cov-report=html
```

### Test Coverage
- Database operations (CRUD)
- Search and filtering
- SLA calculations
- Input validation
- Statistics generation
- Complete ticket lifecycle

## 🎨 Customization

### Adding New Categories

Edit `streamlit_app.py` and update the category options:

```python
categories = ["Technical", "Billing", "General", "YourNewCategory"]
```

Also update the icon mapping in `utils.py`:

```python
def get_category_icon(category: str) -> str:
    icons = {
        'YourNewCategory': '🆕',
        # ... other categories
    }
```

### Modifying SLA Timeframes

Edit `utils.py`:

```python
def calculate_sla_deadline(priority: str, submitted_date: datetime) -> datetime:
    sla_hours = {
        'Critical': 4,      # Change these values
        'High': 24,
        'Medium': 72,
        'Low': 168
    }
```

### Customizing Colors

Edit `styles.py` to change the color scheme:

```python
base_colors = {
    'primary': '#1f77b4',    # Change these colors
    'success': '#28a745',
    'danger': '#dc3545',
    # ... other colors
}
```

## 📊 Sample Data

The application automatically generates 100 sample tickets on first run for demonstration purposes. This helps you:
- Explore all features immediately
- See analytics with realistic data
- Test search and filtering capabilities

To start fresh, simply delete `tickets.db` and restart the application.

## 🔧 Configuration

### Default Users
The system creates three default users:
- `admin` - System Administrator
- `john_doe` - Agent
- `jane_smith` - Agent

You can add more users through the database interface.

### Database Location
By default, the database is stored as `tickets.db` in the project root. To change this, modify `database.py`:

```python
db = TicketDatabase(db_path="your_custom_path.db")
```

## 🚀 Deployment

### Deploy to Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Deploy to Other Platforms

The application can be deployed to:
- **Heroku**: Use the included `requirements.txt`
- **AWS EC2**: Run with Streamlit server
- **Docker**: Create a Dockerfile based on the Python Streamlit image
- **Google Cloud Run**: Deploy as a containerized application

### Environment Variables

For production deployment, consider adding:
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Database Locked Error
If you get a "database is locked" error:
- Close other instances of the application
- Delete `tickets.db` and restart

### Import Errors
If modules are not found:
```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use
If port 8501 is busy:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the test suite for usage examples

## 🎯 Roadmap

Completed Features:
- [x] To-Do List Management with ticket linking
- [x] Activity Logging and Audit Trail
- [x] Response Templates System
- [x] Persistent Ticket Editing
- [x] Comments and Collaboration
- [x] Advanced Filtering and Search
- [x] Dark Mode Support
- [x] SLA Tracking and Compliance
- [x] Comprehensive Analytics

Future enhancements planned:
- [ ] Email notifications for ticket updates
- [ ] File attachments support
- [ ] Advanced user authentication (OAuth, SSO)
- [ ] Mobile-responsive design improvements
- [ ] REST API for external integrations
- [ ] Ticket templates
- [ ] Custom fields
- [ ] Multi-language support
- [ ] Bulk ticket operations
- [ ] Automated escalation rules

## ⭐ Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Charts powered by [Altair](https://altair-viz.github.io)
- Data handling with [Pandas](https://pandas.pydata.org)
- Database: SQLite3

---

**Version**: 2.5 - Enhanced Edition
**Last Updated**: November 2024
**Status**: Production Ready ✅ | Market Ready ✅ | Fully Tested ✅
