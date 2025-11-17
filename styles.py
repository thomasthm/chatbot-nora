"""Custom CSS styles for the ticket management system."""


def get_custom_css(dark_mode: bool = False) -> str:
    """Return custom CSS based on theme."""

    base_colors = {
        'primary': '#1f77b4' if not dark_mode else '#4dabf7',
        'secondary': '#6c757d' if not dark_mode else '#868e96',
        'success': '#28a745' if not dark_mode else '#51cf66',
        'danger': '#dc3545' if not dark_mode else '#ff6b6b',
        'warning': '#ffc107' if not dark_mode else '#ffd43b',
        'info': '#17a2b8' if not dark_mode else '#22b8cf',
        'background': '#ffffff' if not dark_mode else '#1a1a1a',
        'text': '#212529' if not dark_mode else '#e9ecef',
        'border': '#dee2e6' if not dark_mode else '#495057',
        'card_bg': '#f8f9fa' if not dark_mode else '#2d2d2d',
    }

    return f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global Styles */
        .stApp {{
            background: {base_colors['background']};
            color: {base_colors['text']};
            font-family: 'Inter', sans-serif;
        }}

        /* Header Styles */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            color: {base_colors['text']};
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, {base_colors['primary']}, {base_colors['info']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* Card Styles */
        .custom-card {{
            background: {base_colors['card_bg']};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid {base_colors['border']};
        }}

        /* Metric Card Styles */
        .metric-card {{
            background: linear-gradient(135deg, {base_colors['primary']}, {base_colors['info']});
            border-radius: 12px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}

        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }}

        .metric-label {{
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Button Styles */
        .stButton > button {{
            background: linear-gradient(135deg, {base_colors['primary']}, {base_colors['info']});
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        /* Form Styles */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            border-radius: 8px;
            border: 2px solid {base_colors['border']};
            padding: 0.75rem;
            transition: border-color 0.3s;
        }}

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {base_colors['primary']};
            box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
        }}

        /* Data Editor Styles */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        /* Badge Styles */
        .priority-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
        }}

        .badge-critical {{
            background-color: {base_colors['danger']};
            color: white;
        }}

        .badge-high {{
            background-color: #fd7e14;
            color: white;
        }}

        .badge-medium {{
            background-color: {base_colors['warning']};
            color: #000;
        }}

        .badge-low {{
            background-color: {base_colors['success']};
            color: white;
        }}

        /* Status Badge */
        .status-open {{
            background-color: {base_colors['info']};
            color: white;
        }}

        .status-progress {{
            background-color: {base_colors['warning']};
            color: #000;
        }}

        .status-closed {{
            background-color: {base_colors['success']};
            color: white;
        }}

        /* Sidebar Styles */
        .css-1d391kg {{
            background: {base_colors['card_bg']};
        }}

        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: {base_colors['card_bg']};
            border-radius: 12px;
            padding: 0.5rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {base_colors['primary']}, {base_colors['info']});
            color: white;
        }}

        /* Success/Error Messages */
        .stSuccess, .stError, .stWarning, .stInfo {{
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}

        /* Chart Styles */
        .vega-embed {{
            border-radius: 12px;
            overflow: hidden;
        }}

        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {base_colors['primary']}, {base_colors['info']});
            border-radius: 8px;
        }}

        /* Expander Styles */
        .streamlit-expanderHeader {{
            background-color: {base_colors['card_bg']};
            border-radius: 8px;
            font-weight: 600;
        }}

        /* Scrollbar Styles */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: {base_colors['background']};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {base_colors['border']};
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {base_colors['secondary']};
        }}

        /* Animation */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: {base_colors['secondary']};
            font-size: 0.9rem;
            margin-top: 3rem;
            border-top: 1px solid {base_colors['border']};
        }}

        /* Search Bar */
        .search-container {{
            background: {base_colors['card_bg']};
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
    </style>
    """


def get_priority_badge_html(priority: str) -> str:
    """Generate HTML for priority badge."""
    badge_class = f"priority-badge badge-{priority.lower()}"
    return f'<span class="{badge_class}">{priority}</span>'


def get_status_badge_html(status: str) -> str:
    """Generate HTML for status badge."""
    status_map = {
        'Open': 'open',
        'In Progress': 'progress',
        'Closed': 'closed'
    }
    badge_class = f"priority-badge status-{status_map.get(status, 'open')}"
    return f'<span class="{badge_class}">{status}</span>'
