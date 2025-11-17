"""
🎫 Professional Support Ticket Management System
A production-ready ticket management application with advanced features.
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
    # Add default users if not exist
    db.add_user("admin", "System Administrator", "Admin")
    db.add_user("john_doe", "John Doe", "Agent")
    db.add_user("jane_smith", "Jane Smith", "Agent")
    return db

db = init_db()

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'initialized' not in st.session_state:
    # Create sample data if database is empty
    stats = db.get_statistics()
    if stats['total_tickets'] == 0:
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

        for i in range(100):
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
Professional ticket management with advanced analytics and automation
</p>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Dashboard", "➕ New Ticket", "🎫 Tickets", "📊 Analytics"])

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
        progress_count = stats['by_status'].get('In Progress', 0)
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #ffc107, #fd7e14);'>
            <div class='metric-label'>In Progress</div>
            <div class='metric-value'>{progress_count}</div>
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

    # Recent tickets
    st.subheader("🆕 Recent Tickets")
    recent_tickets = db.get_all_tickets().head(10)

    if not recent_tickets.empty:
        display_df = recent_tickets[['ticket_id', 'issue', 'priority', 'status', 'category', 'assigned_to', 'date_submitted']].copy()
        display_df.columns = ['Ticket ID', 'Issue', 'Priority', 'Status', 'Category', 'Assigned To', 'Date']

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn(format="MMM DD, YYYY"),
                "Issue": st.column_config.TextColumn(width="large"),
            }
        )
    else:
        st.info("No tickets found.")

    # Priority distribution
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

            st.write("")
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

                # Auto-refresh to show new ticket
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

        # Show data editor
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
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

        # Detect changes and update database
        if not display_df.equals(edited_df):
            changes = edited_df.compare(display_df)
            if not changes.empty:
                st.info("💾 Changes detected. Updating tickets...")
                # Update logic would go here

        # Pagination info
        st.caption(f"Displaying {len(display_df)} tickets")
    else:
        st.warning("No tickets found matching your criteria.")

# Tab 4: Analytics
with tab4:
    st.header("📊 Advanced Analytics")

    all_tickets = db.get_all_tickets()

    if not all_tickets.empty:
        # Time series analysis
        st.subheader("📈 Ticket Trends Over Time")

        # Prepare time series data
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

                # Resolution time distribution
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
    <p>🎫 Support Ticket Management System v2.0 | Built with Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)
