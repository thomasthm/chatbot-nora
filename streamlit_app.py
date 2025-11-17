"""
🎫 Professional Support Ticket Management System - ENHANCED VERSION
Production-ready with To-Do Lists, Activity Tracking, Templates, and more
"""

import datetime
import io
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from database import TicketDatabase
from utils import (
    calculate_sla_deadline,
    get_sla_status,
    export_to_csv,
    validate_ticket_input,
    get_category_icon
)
from styles import get_custom_css

# Page configuration
st.set_page_config(
    page_title="Support Ticket Management System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_db():
    """Initialize database connection."""
    db = TicketDatabase()
    # Add default users
    db.add_user("admin", "System Administrator", "Admin")
    db.add_user("john_doe", "John Doe", "Agent")
    db.add_user("jane_smith", "Jane Smith", "Agent")

    # Add sample response templates
    templates = [
        ("Ticket Received", "Technical", "Thank you for contacting support. We have received your ticket and will respond within the SLA timeframe."),
        ("Request More Info", "General", "Thank you for reaching out. To better assist you, could you please provide more details about: [SPECIFY DETAILS NEEDED]"),
        ("Issue Resolved", "General", "We're happy to inform you that your issue has been resolved. Please let us know if you need any further assistance."),
        ("Escalation Notice", "Technical", "Your ticket has been escalated to our senior technical team for further investigation. We appreciate your patience."),
    ]

    for name, category, text in templates:
        db.add_response_template(name, text, category, "System")

    return db

db = init_db()

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'selected_ticket' not in st.session_state:
    st.session_state.selected_ticket = None

if 'initialized' not in st.session_state:
    stats = db.get_statistics()
    if stats['total_tickets'] == 0:
        # Create sample data
        np.random.seed(42)
        issue_descriptions = [
            "Network connectivity issues in the office",
            "Software application crashing on startup",
            "Printer not responding to print commands",
            "Email server downtime",
            "Data backup failure",
            "Login authentication problems",
            "Website performance degradation",
            "Security vulnerability identified",
            "Hardware malfunction in the server room",
            "Employee unable to access shared files",
            "Database connection failure",
            "Mobile application not syncing data",
            "VoIP phone system issues",
            "VPN connection problems for remote employees",
            "System updates causing compatibility issues",
            "File server running out of storage space",
            "Intrusion detection system alerts",
            "Inventory management system errors",
            "Customer data not loading in CRM",
            "Collaboration tool not sending notifications",
        ]

        categories = ["Technical", "Billing", "General", "Feature Request", "Bug Report", "Security"]
        users = ["john_doe", "jane_smith", "Unassigned"]
        priorities = ["Critical", "High", "Medium", "Low"]
        statuses = ["Open", "In Progress", "Closed"]

        for i in range(50):
            ticket_date = datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            priority = np.random.choice(priorities)
            status = np.random.choice(statuses)

            ticket_data = {
                'ticket_id': f"TICKET-{1001 + i}",
                'issue': np.random.choice(issue_descriptions),
                'status': status,
                'priority': priority,
                'category': np.random.choice(categories),
                'assigned_to': np.random.choice(users),
                'date_submitted': ticket_date,
                'created_by': 'System',
                'sla_deadline': calculate_sla_deadline(priority, datetime.datetime.combine(ticket_date, datetime.time()))
            }
            db.add_ticket(ticket_data)

        # Add sample To-Dos
        todo_tasks = [
            "Review server logs for errors",
            "Update documentation for new feature",
            "Schedule team meeting",
            "Test backup restoration process",
            "Update firewall rules",
            "Review pending tickets",
            "Prepare weekly report",
            "Contact vendor about licensing",
        ]

        for i, task in enumerate(todo_tasks):
            db.add_todo(
                task=task,
                priority=random.choice(["Critical", "High", "Medium", "Low"]),
                assigned_to=random.choice(users),
                due_date=datetime.date.today() + datetime.timedelta(days=random.randint(1, 14)),
                created_by="System"
            )

    st.session_state.initialized = True

# Apply custom CSS
st.markdown(get_custom_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    st.divider()

    # Quick stats
    st.subheader("📊 Quick Stats")
    stats = db.get_statistics()
    st.metric("Total Tickets", stats['total_tickets'])
    st.metric("Open Tickets", stats['by_status'].get('Open', 0))
    st.metric("Pending To-Dos", stats['pending_todos'])
    st.metric("Avg Resolution (days)", stats['avg_resolution_days'])

    st.divider()

    # Filter section
    st.subheader("🔍 Filters")
    filter_status = st.multiselect(
        "Status",
        options=["Open", "In Progress", "Closed", "On Hold"],
        default=None
    )

    filter_priority = st.multiselect(
        "Priority",
        options=["Critical", "High", "Medium", "Low"],
        default=None
    )

    filter_category = st.multiselect(
        "Category",
        options=["Technical", "Billing", "General", "Feature Request", "Bug Report", "Security", "Performance", "Documentation"],
        default=None
    )

    users = db.get_users()
    filter_assigned = st.multiselect(
        "Assigned To",
        options=users,
        default=None
    )

    search_term = st.text_input("🔎 Search", placeholder="Search tickets...")

    if st.button("Clear Filters", use_container_width=True):
        st.rerun()

    st.divider()

    # Export options
    st.subheader("📥 Export Data")
    if st.button("Download CSV", use_container_width=True):
        df = db.get_all_tickets()
        csv_data = export_to_csv(df)
        st.download_button(
            label="💾 Download",
            data=csv_data,
            file_name=f"tickets_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Main content
st.title("🎫 Support Ticket Management System")
st.markdown("""
<p style='font-size: 1.1rem; color: #666; margin-bottom: 2rem;'>
Professional ticket management with To-Do Lists, Activity Tracking & Templates
</p>
""", unsafe_allow_html=True)

# Create tabs - NOW WITH TO-DO LIST!
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Dashboard",
    "➕ New Ticket",
    "🎫 Tickets",
    "✅ To-Do List",
    "📝 Templates",
    "📊 Analytics"
])

# Tab 1: Dashboard
with tab1:
    st.header("Dashboard Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Tickets</div>
            <div class='metric-value'>{stats['total_tickets']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        open_count = stats['by_status'].get('Open', 0)
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #17a2b8, #20c997);'>
            <div class='metric-label'>Open Tickets</div>
            <div class='metric-value'>{open_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #ffc107, #fd7e14);'>
            <div class='metric-label'>Pending To-Dos</div>
            <div class='metric-value'>{stats['pending_todos']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        closed_count = stats['by_status'].get('Closed', 0)
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #28a745, #20c997);'>
            <div class='metric-label'>Closed</div>
            <div class='metric-value'>{closed_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Recent tickets
        st.subheader("🆕 Recent Tickets")
        recent_tickets = db.get_all_tickets().head(10)

        if not recent_tickets.empty:
            display_df = recent_tickets[['ticket_id', 'issue', 'priority', 'status', 'assigned_to', 'date_submitted']].copy()
            display_df.columns = ['Ticket ID', 'Issue', 'Priority', 'Status', 'Assigned To', 'Date']

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.DateColumn(format="MMM DD, YYYY"),
                    "Issue": st.column_config.TextColumn(width="large"),
                }
            )

    with col2:
        # Recent Activity
        st.subheader("📜 Recent Activity")
        activity = db.get_activity_log()

        if not activity.empty:
            for idx, row in activity.head(5).iterrows():
                action_emoji = "➕" if row['action'] == 'created' else "✏️" if row['action'] == 'updated' else "💬"
                st.markdown(f"""
                <div style='padding: 0.5rem; margin: 0.5rem 0; border-left: 3px solid #1f77b4;'>
                    <small>{action_emoji} <b>{row['user']}</b> {row['action']} {row['ticket_id'] if row['ticket_id'] else 'item'}</small><br>
                    <small style='color: #666;'>{pd.to_datetime(row['timestamp']).strftime('%m/%d %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity")

    # Priority and Category distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Priority Distribution")
        priority_data = pd.DataFrame(list(stats['by_priority'].items()), columns=['Priority', 'Count'])

        if not priority_data.empty:
            priority_chart = alt.Chart(priority_data).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(
                    field="Priority",
                    type="nominal",
                    scale=alt.Scale(
                        domain=["Critical", "High", "Medium", "Low"],
                        range=["#dc3545", "#fd7e14", "#ffc107", "#28a745"]
                    )
                ),
                tooltip=['Priority', 'Count']
            ).properties(height=300)
            st.altair_chart(priority_chart, use_container_width=True)

    with col2:
        st.subheader("📂 Category Distribution")
        category_data = pd.DataFrame(list(stats['by_category'].items()), columns=['Category', 'Count'])

        if not category_data.empty:
            category_chart = alt.Chart(category_data).mark_bar().encode(
                x=alt.X('Count:Q', title='Number of Tickets'),
                y=alt.Y('Category:N', sort='-x', title='Category'),
                color=alt.Color('Count:Q', scale=alt.Scale(scheme='blues')),
                tooltip=['Category', 'Count']
            ).properties(height=300)
            st.altair_chart(category_chart, use_container_width=True)

# Tab 2: New Ticket
with tab2:
    st.header("➕ Create New Ticket")

    with st.form("new_ticket_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            issue = st.text_area(
                "Issue Description *",
                placeholder="Describe the issue in detail...",
                height=150,
                help="Please provide a detailed description (minimum 10 characters)"
            )

            priority = st.selectbox(
                "Priority *",
                options=["Critical", "High", "Medium", "Low"],
                index=2,
                help="Critical: 4h SLA | High: 24h SLA | Medium: 72h SLA | Low: 168h SLA"
            )

            category = st.selectbox(
                "Category",
                options=["Technical", "Billing", "General", "Feature Request", "Bug Report", "Security", "Performance", "Documentation"],
                index=2
            )

        with col2:
            users = db.get_users()
            assigned_to = st.selectbox(
                "Assign To",
                options=users,
                index=0 if "Unassigned" in users else 0
            )

            created_by = st.text_input(
                "Your Name",
                value="System",
                help="Who is creating this ticket?"
            )

            add_todo = st.checkbox("Create related To-Do item")

            st.write("")
            submitted = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)

    if submitted:
        is_valid, error_message = validate_ticket_input(issue, priority)

        if not is_valid:
            st.error(f"❌ {error_message}")
        else:
            ticket_number = db.get_next_ticket_number()
            ticket_id = f"TICKET-{ticket_number}"
            today = datetime.date.today()
            sla_deadline = calculate_sla_deadline(priority, datetime.datetime.combine(today, datetime.time()))

            ticket_data = {
                'ticket_id': ticket_id,
                'issue': issue,
                'status': 'Open',
                'priority': priority,
                'category': category,
                'assigned_to': assigned_to,
                'date_submitted': today,
                'created_by': created_by,
                'sla_deadline': sla_deadline
            }

            try:
                db.add_ticket(ticket_data)
                st.success(f"✅ Ticket {ticket_id} created successfully!")

                if add_todo:
                    db.add_todo(
                        task=f"Resolve: {issue[:50]}...",
                        ticket_id=ticket_id,
                        priority=priority,
                        assigned_to=assigned_to,
                        due_date=sla_deadline.date(),
                        created_by=created_by
                    )
                    st.success("✅ Related To-Do item created!")

                # Show ticket details
                st.markdown("### Ticket Details")
                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.write(f"**Ticket ID:** {ticket_id}")
                    st.write(f"**Priority:** {priority}")
                    st.write(f"**Category:** {get_category_icon(category)} {category}")
                with detail_col2:
                    st.write(f"**Assigned To:** {assigned_to}")
                    st.write(f"**SLA Deadline:** {sla_deadline.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Status:** Open")

                st.balloons()
            except Exception as e:
                st.error(f"❌ Error creating ticket: {str(e)}")

# Tab 3: Tickets
with tab3:
    st.header("🎫 All Tickets")

    # Apply filters
    if search_term or filter_status or filter_priority or filter_category or filter_assigned:
        filtered_df = db.search_tickets(
            search_term=search_term if search_term else None,
            status=filter_status if filter_status else None,
            priority=filter_priority if filter_priority else None,
            category=filter_category if filter_category else None,
            assigned_to=filter_assigned if filter_assigned else None
        )
        st.info(f"Showing {len(filtered_df)} filtered tickets")
    else:
        filtered_df = db.get_all_tickets()

    if not filtered_df.empty:
        # Prepare display dataframe
        display_columns = ['ticket_id', 'issue', 'priority', 'status', 'category', 'assigned_to', 'date_submitted', 'sla_deadline']
        display_df = filtered_df[display_columns].copy()

        # Add SLA status
        display_df['sla_status'] = display_df.apply(
            lambda row: get_sla_status(row['sla_deadline'], None, row['status']),
            axis=1
        )

        # Show data editor with ON_CHANGE handler
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            key="ticket_editor",
            column_config={
                "ticket_id": st.column_config.TextColumn("Ticket ID", disabled=True),
                "issue": st.column_config.TextColumn("Issue", width="large"),
                "priority": st.column_config.SelectboxColumn(
                    "Priority",
                    options=["Critical", "High", "Medium", "Low"],
                    required=True
                ),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Open", "In Progress", "Closed", "On Hold"],
                    required=True
                ),
                "category": st.column_config.SelectboxColumn(
                    "Category",
                    options=["Technical", "Billing", "General", "Feature Request", "Bug Report", "Security", "Performance", "Documentation"],
                    required=True
                ),
                "assigned_to": st.column_config.SelectboxColumn(
                    "Assigned To",
                    options=db.get_users()
                ),
                "date_submitted": st.column_config.DateColumn(
                    "Submitted",
                    format="MMM DD, YYYY",
                    disabled=True
                ),
                "sla_deadline": st.column_config.DatetimeColumn(
                    "SLA Deadline",
                    format="MMM DD, YYYY HH:mm",
                    disabled=True
                ),
                "sla_status": st.column_config.TextColumn("SLA Status", disabled=True)
            },
            disabled=["ticket_id", "date_submitted", "sla_deadline", "sla_status"],
            num_rows="fixed"
        )

        # Detect and save changes
        if st.button("💾 Save Changes", type="primary"):
            changes_made = False
            for idx in range(len(display_df)):
                ticket_id = display_df.iloc[idx]['ticket_id']
                updates = {}

                # Check each editable field
                for col in ['priority', 'status', 'category', 'assigned_to', 'issue']:
                    if display_df.iloc[idx][col] != edited_df.iloc[idx][col]:
                        updates[col] = edited_df.iloc[idx][col]
                        changes_made = True

                if updates:
                    db.update_ticket(ticket_id, updates, user="System")

            if changes_made:
                st.success("✅ Changes saved successfully!")
                st.rerun()
            else:
                st.info("No changes detected")

        # Ticket detail expanders
        st.markdown("---")
        st.subheader("📝 Ticket Details")

        selected_ticket = st.selectbox(
            "Select a ticket to view details:",
            options=display_df['ticket_id'].tolist(),
            key="ticket_selector"
        )

        if selected_ticket:
            ticket_details = db.get_ticket(selected_ticket)

            if ticket_details:
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown(f"**Ticket ID:** {ticket_details['ticket_id']}")
                    st.markdown(f"**Status:** {ticket_details['status']}")
                    st.markdown(f"**Priority:** {ticket_details['priority']}")
                    st.markdown(f"**Category:** {get_category_icon(ticket_details['category'])} {ticket_details['category']}")

                with detail_col2:
                    st.markdown(f"**Assigned To:** {ticket_details['assigned_to']}")
                    st.markdown(f"**Created By:** {ticket_details['created_by']}")
                    st.markdown(f"**Created:** {ticket_details['date_submitted']}")
                    if ticket_details['date_closed']:
                        st.markdown(f"**Closed:** {ticket_details['date_closed']}")

                st.markdown(f"**Issue:**\n\n{ticket_details['issue']}")

                # Comments section
                st.markdown("---")
                st.subheader("💬 Comments")

                comments_df = db.get_comments(selected_ticket)

                if not comments_df.empty:
                    for idx, comment in comments_df.iterrows():
                        st.markdown(f"""
                        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
                            <b>{comment['author']}</b> <small style='color: #666;'>• {pd.to_datetime(comment['created_at']).strftime('%Y-%m-%d %H:%M')}</small><br>
                            {comment['comment']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No comments yet")

                # Add new comment
                with st.form(f"comment_form_{selected_ticket}"):
                    new_comment = st.text_area("Add a comment", key=f"comment_{selected_ticket}")
                    comment_author = st.text_input("Your name", value="System", key=f"author_{selected_ticket}")

                    if st.form_submit_button("💬 Add Comment"):
                        if new_comment.strip():
                            db.add_comment(selected_ticket, new_comment, comment_author)
                            st.success("Comment added!")
                            st.rerun()
                        else:
                            st.error("Comment cannot be empty")

        st.caption(f"Displaying {len(display_df)} tickets")
    else:
        st.warning("No tickets found matching your criteria.")

# Tab 4: TO-DO LIST - NEW FEATURE!
with tab4:
    st.header("✅ To-Do List Management")

    col1, col2 = st.columns([2, 1])

    with col2:
        st.subheader("➕ Add New To-Do")

        with st.form("new_todo_form"):
            todo_task = st.text_area("Task Description", height=100, placeholder="What needs to be done?")

            todo_col1, todo_col2 = st.columns(2)
            with todo_col1:
                todo_priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"], index=2)
                todo_assigned = st.selectbox("Assign To", db.get_users())

            with todo_col2:
                todo_due = st.date_input("Due Date", value=datetime.date.today() + datetime.timedelta(days=7))
                todo_created_by = st.text_input("Created By", value="System")

            # Optional ticket association
            all_tickets = db.get_all_tickets()
            ticket_options = ["None"] + all_tickets['ticket_id'].tolist() if not all_tickets.empty else ["None"]
            todo_ticket = st.selectbox("Link to Ticket (Optional)", ticket_options)

            if st.form_submit_button("✅ Create To-Do", use_container_width=True):
                if todo_task.strip():
                    db.add_todo(
                        task=todo_task,
                        ticket_id=None if todo_ticket == "None" else todo_ticket,
                        priority=todo_priority,
                        due_date=todo_due,
                        assigned_to=todo_assigned,
                        created_by=todo_created_by
                    )
                    st.success("✅ To-Do created!")
                    st.rerun()
                else:
                    st.error("Task description cannot be empty")

    with col1:
        st.subheader("📝 Active To-Dos")

        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            show_completed = st.checkbox("Show Completed", value=False)
        with filter_col2:
            sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Created Date"])

        # Get todos
        if show_completed:
            todos_df = db.get_todos()
        else:
            todos_df = db.get_todos(completed=False)

        if not todos_df.empty:
            # Display todos as interactive cards
            for idx, todo in todos_df.iterrows():
                # Determine color based on priority
                priority_colors = {
                    'Critical': '#dc3545',
                    'High': '#fd7e14',
                    'Medium': '#ffc107',
                    'Low': '#28a745'
                }
                color = priority_colors.get(todo['priority'], '#6c757d')

                # Check if overdue
                is_overdue = False
                if todo['due_date'] and pd.notna(todo['due_date']):
                    is_overdue = pd.to_datetime(todo['due_date']).date() < datetime.date.today() and not todo['completed']

                # Create card
                checkbox_col, content_col, action_col = st.columns([0.5, 4, 1])

                with checkbox_col:
                    if st.checkbox("", value=bool(todo['completed']), key=f"todo_check_{todo['id']}"):
                        if not todo['completed']:
                            db.toggle_todo(todo['id'])
                            st.rerun()
                    elif todo['completed']:
                        db.toggle_todo(todo['id'])
                        st.rerun()

                with content_col:
                    task_style = "text-decoration: line-through; color: #999;" if todo['completed'] else ""
                    overdue_badge = "🔴 OVERDUE" if is_overdue else ""

                    st.markdown(f"""
                    <div style='border-left: 4px solid {color}; padding-left: 1rem; margin-bottom: 1rem;'>
                        <span style='{task_style}'><b>{todo['task']}</b></span> {overdue_badge}<br>
                        <small>
                            <span style='background: {color}; color: white; padding: 2px 8px; border-radius: 4px;'>{todo['priority']}</span>
                            👤 {todo['assigned_to']} |
                            📅 Due: {pd.to_datetime(todo['due_date']).strftime('%Y-%m-%d') if pd.notna(todo['due_date']) else 'No due date'}
                            {f" | 🎫 {todo['ticket_id']}" if todo['ticket_id'] else ""}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)

                with action_col:
                    if st.button("🗑️", key=f"del_todo_{todo['id']}"):
                        db.delete_todo(todo['id'])
                        st.rerun()

            # Summary stats
            st.markdown("---")
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            with summary_col1:
                st.metric("Total Tasks", len(todos_df))
            with summary_col2:
                completed_count = len(todos_df[todos_df['completed'] == 1])
                st.metric("Completed", completed_count)
            with summary_col3:
                completion_rate = (completed_count / len(todos_df) * 100) if len(todos_df) > 0 else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%")

        else:
            st.info("No to-do items found. Create one to get started!")

# Tab 5: Response Templates
with tab5:
    st.header("📝 Response Templates")

    col1, col2 = st.columns([2, 1])

    with col2:
        st.subheader("➕ Add Template")

        with st.form("new_template_form"):
            template_name = st.text_input("Template Name")
            template_category = st.selectbox("Category", ["Technical", "Billing", "General", "Follow-up"])
            template_text = st.text_area("Template Text", height=200,
                placeholder="Enter your template text here. Use [PLACEHOLDERS] for dynamic content.")
            template_creator = st.text_input("Created By", value="System")

            if st.form_submit_button("💾 Save Template", use_container_width=True):
                if template_name and template_text:
                    db.add_response_template(template_name, template_text, template_category, template_creator)
                    st.success("✅ Template saved!")
                    st.rerun()
                else:
                    st.error("Name and text are required")

    with col1:
        st.subheader("📚 Available Templates")

        templates_df = db.get_response_templates()

        if not templates_df.empty:
            for idx, template in templates_df.iterrows():
                with st.expander(f"📄 {template['name']} ({template['category']})"):
                    st.markdown(f"**Category:** {template['category']}")
                    st.markdown(f"**Created By:** {template['created_by']}")
                    st.markdown("**Template:**")
                    st.text_area("", value=template['template_text'], height=150, key=f"template_{template['id']}", disabled=True)

                    if st.button("📋 Copy to Clipboard", key=f"copy_{template['id']}"):
                        st.code(template['template_text'])
                        st.success("Template displayed above - copy manually")
        else:
            st.info("No templates found. Create one to get started!")

# Tab 6: Analytics
with tab6:
    st.header("📊 Advanced Analytics")

    all_tickets = db.get_all_tickets()

    if not all_tickets.empty:
        # Time series analysis
        st.subheader("📈 Ticket Trends Over Time")

        time_series_df = all_tickets.copy()
        time_series_df['month'] = pd.to_datetime(time_series_df['date_submitted']).dt.to_period('M').astype(str)

        monthly_counts = time_series_df.groupby(['month', 'status']).size().reset_index(name='count')

        trend_chart = alt.Chart(monthly_counts).mark_line(point=True).encode(
            x=alt.X('month:N', title='Month'),
            y=alt.Y('count:Q', title='Number of Tickets'),
            color=alt.Color('status:N', title='Status'),
            tooltip=['month', 'status', 'count']
        ).properties(height=400)

        st.altair_chart(trend_chart, use_container_width=True)

        # Performance metrics
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⏱️ Resolution Time Analysis")
            closed_tickets = all_tickets[all_tickets['status'] == 'Closed'].copy()

            if not closed_tickets.empty and 'date_closed' in closed_tickets.columns:
                closed_tickets['resolution_days'] = (
                    pd.to_datetime(closed_tickets['date_closed']) -
                    pd.to_datetime(closed_tickets['date_submitted'])
                ).dt.days

                avg_resolution = closed_tickets['resolution_days'].mean()
                median_resolution = closed_tickets['resolution_days'].median()

                st.metric("Average Resolution Time", f"{avg_resolution:.1f} days")
                st.metric("Median Resolution Time", f"{median_resolution:.1f} days")

                hist_chart = alt.Chart(closed_tickets).mark_bar().encode(
                    x=alt.X('resolution_days:Q', bin=alt.Bin(maxbins=20), title='Days to Resolution'),
                    y=alt.Y('count():Q', title='Number of Tickets'),
                    tooltip=['count()']
                ).properties(height=300)

                st.altair_chart(hist_chart, use_container_width=True)
            else:
                st.info("No closed tickets with resolution data available.")

        with col2:
            st.subheader("👥 Agent Performance")
            agent_stats = all_tickets.groupby('assigned_to').agg({
                'ticket_id': 'count',
                'status': lambda x: (x == 'Closed').sum()
            }).reset_index()
            agent_stats.columns = ['Agent', 'Total Tickets', 'Closed Tickets']
            agent_stats['Closure Rate %'] = (agent_stats['Closed Tickets'] / agent_stats['Total Tickets'] * 100).round(1)

            st.dataframe(
                agent_stats,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Closure Rate %": st.column_config.ProgressColumn(
                        "Closure Rate",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%"
                    )
                }
            )

        # SLA compliance
        st.subheader("✅ SLA Compliance")
        sla_col1, sla_col2, sla_col3 = st.columns(3)

        with sla_col1:
            total_with_sla = len(all_tickets[all_tickets['sla_deadline'].notna()])
            st.metric("Tickets with SLA", total_with_sla)

        with sla_col2:
            overdue = len(all_tickets[
                (all_tickets['status'] != 'Closed') &
                (pd.to_datetime(all_tickets['sla_deadline']) < datetime.datetime.now())
            ])
            st.metric("Overdue Tickets", overdue, delta=f"-{overdue}", delta_color="inverse")

        with sla_col3:
            if total_with_sla > 0:
                compliance_rate = ((total_with_sla - overdue) / total_with_sla * 100)
                st.metric("SLA Compliance", f"{compliance_rate:.1f}%")
            else:
                st.metric("SLA Compliance", "N/A")
    else:
        st.info("No data available for analytics. Create some tickets first!")

# Footer
st.markdown("""
<div class='footer'>
    <p>🎫 Support Ticket Management System v2.5 | Built with Streamlit | © 2024</p>
    <p><small>Features: Tickets • To-Do Lists • Templates • Activity Log • Analytics • Dark Mode</small></p>
</div>
""", unsafe_allow_html=True)
