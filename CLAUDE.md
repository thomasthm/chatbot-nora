# CLAUDE.md - AI Assistant Guide for chatbot-nora

## Project Overview

**chatbot-nora** is a Streamlit-based support ticket management application that demonstrates how to build internal tools for creating, managing, and visualizing support tickets. The application uses session state for data persistence and provides an interactive interface for ticket management.

### Quick Facts
- **Primary Language**: Python 3.11
- **Framework**: Streamlit
- **License**: Apache 2.0
- **Application Type**: Single-page web application
- **Deployment**: Streamlit Cloud-ready

## Repository Structure

```
chatbot-nora/
├── streamlit_app.py          # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # User-facing documentation
├── LICENSE                    # Apache 2.0 license
├── .gitignore                # Git ignore patterns
├── .devcontainer/            # VS Code devcontainer config
│   └── devcontainer.json
└── .github/                  # GitHub configuration
    └── CODEOWNERS            # Code ownership (@streamlit/community-cloud)
```

## Core Technologies

### Primary Stack
- **Streamlit**: Web application framework for data apps
- **Pandas**: Data manipulation and DataFrame operations
- **NumPy**: Numerical operations and random data generation
- **Altair**: Declarative statistical visualization library

### Python Version
- Python 3.11 (as specified in devcontainer.json)

## Application Architecture

### Single-File Architecture
The entire application is contained in `streamlit_app.py` (~173 lines), structured as follows:

1. **Imports & Configuration** (lines 1-18)
   - Library imports
   - Page configuration with `st.set_page_config()`
   - App title and description

2. **Data Initialization** (lines 20-65)
   - Session state initialization
   - Mock data generation (100 tickets)
   - Reproducible seeding (np.random.seed(42))

3. **Ticket Creation UI** (lines 68-98)
   - Form-based input (`st.form`)
   - Ticket submission and ID generation
   - DataFrame concatenation for new tickets

4. **Ticket Management UI** (lines 100-132)
   - Interactive data editor (`st.data_editor`)
   - Column configuration for dropdowns
   - Disabled columns for ID and Date

5. **Statistics & Visualization** (lines 134-172)
   - Metrics display using `st.columns` and `st.metric`
   - Monthly ticket status chart (Altair bar chart)
   - Priority distribution chart (Altair pie chart)

### Key Design Patterns

#### Session State Pattern
```python
if "df" not in st.session_state:
    # Initialize data
    st.session_state.df = df
```
- Used for persisting ticket data across reruns
- Prevents data loss on user interaction

#### Form Pattern
```python
with st.form("add_ticket_form"):
    # Input widgets
    submitted = st.form_submit_button("Submit")
```
- Batches widget inputs to prevent multiple reruns
- Improves performance for multi-field forms

#### Data Editor Pattern
```python
edited_df = st.data_editor(
    st.session_state.df,
    column_config={...},
    disabled=["ID", "Date Submitted"]
)
```
- Allows inline editing of ticket data
- Returns modified DataFrame
- Configured columns for specific input types

## Development Workflow

### Local Development

#### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

#### Dev Container Setup
The project includes a devcontainer configuration for consistent development environments:
- **Base Image**: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- **Extensions**: Python, Pylance
- **Auto-commands**:
  - `updateContentCommand`: Installs packages and requirements
  - `postAttachCommand`: Runs Streamlit server on port 8501
- **Port Forwarding**: Port 8501 (Application)
- **CORS Settings**: Disabled for development

#### Running in Codespaces/Devcontainer
The devcontainer automatically:
1. Opens README.md and streamlit_app.py
2. Installs dependencies
3. Starts Streamlit server with CORS disabled
4. Forwards port 8501 with auto-preview

### Deployment
The app is designed for Streamlit Cloud deployment:
- No database dependencies
- In-memory session state
- Single requirements.txt file
- Public deployment badge in README

## Code Conventions

### Python Style
- **Imports**: Grouped logically (standard library, third-party, local)
- **Comments**: Used sparingly, code is self-documenting
- **Naming**:
  - Snake_case for variables and functions
  - Descriptive names (e.g., `issue_descriptions`, `recent_ticket_number`)

### Streamlit Conventions
1. **Page Config First**: Always call `st.set_page_config()` as first Streamlit command
2. **Session State**: Check existence before initializing (`if "key" not in st.session_state`)
3. **Widget Keys**: Use descriptive form names (e.g., `"add_ticket_form"`)
4. **Layout**: Use columns for side-by-side elements (`st.columns()`)
5. **Container Width**: Prefer `use_container_width=True` for responsive design
6. **Index Display**: Use `hide_index=True` for cleaner data tables

### Data Conventions
- **Ticket IDs**: Format `TICKET-{number}` (sequential, descending in display)
- **Status Values**: `["Open", "In Progress", "Closed"]`
- **Priority Values**: `["High", "Medium", "Low"]`
- **Date Format**:
  - Storage: `datetime.date` objects
  - Display: Default pandas formatting
  - New tickets: `datetime.datetime.now().strftime("%m-%d-%Y")`

### Mock Data
- **Seed**: Fixed at 42 for reproducibility
- **Dataset Size**: 100 initial tickets (TICKET-1100 to TICKET-1001)
- **Issue Pool**: 20 predefined issue descriptions
- **Date Range**: 183 days from June 1, 2023

## Key Files Deep Dive

### streamlit_app.py

#### Critical Sections

**Session State Initialization** (lines 21-65)
- Initialize only once per session
- Create reproducible mock data
- Store in `st.session_state.df`

**Ticket Addition Logic** (lines 78-98)
- Extract latest ticket number from existing data
- Increment for new ticket ID
- Concatenate new ticket to top of DataFrame
- Always set status to "Open" for new tickets

**Data Editor Configuration** (lines 112-132)
- `SelectboxColumn` for Status and Priority
- Disabled editing for ID and Date Submitted
- Returns edited DataFrame (updates not auto-saved to session state)

**Visualization Setup** (lines 147-172)
- Altair charts use `edited_df` (live updates)
- Bottom-oriented legends for consistency
- Streamlit theme for consistent styling
- Fixed height for pie chart (300px)

### requirements.txt
```
streamlit
```
- Minimal dependencies
- Streamlit includes pandas, numpy, altair as dependencies
- No version pinning (uses latest)

### .gitignore
- Standard Python gitignore
- **Important**: Excludes `.streamlit/secrets.toml` (first line)
- Covers virtual environments, bytecode, caches

## AI Assistant Guidelines

### When Making Changes

#### 1. Understand Data Flow
- **Source of Truth**: `st.session_state.df`
- **Display/Edit**: `edited_df` from `st.data_editor()`
- **Note**: Charts use `edited_df` for live updates, but changes aren't persisted until user action

#### 2. Maintain Backwards Compatibility
- Keep ticket ID format consistent
- Preserve Status and Priority value sets
- Don't break existing session state structure

#### 3. Adding New Features

**For New Ticket Fields:**
1. Add to mock data generation
2. Update form inputs
3. Update new ticket creation logic
4. Add to column_config if special input needed
5. Consider if field should be disabled in editor

**For New Visualizations:**
1. Use `edited_df` for live data
2. Use Altair for consistency
3. Apply Streamlit theme: `theme="streamlit"`
4. Use `use_container_width=True` for responsiveness
5. Configure legend orientation

**For New Status/Priority Values:**
1. Update SelectboxColumn options
2. Update mock data generation
3. Update any hardcoded filtering logic

#### 4. Common Pitfalls to Avoid

- **Don't** modify session state directly in multiple places
- **Don't** forget to update both display and edit logic
- **Don't** break ticket ID sequencing
- **Don't** add dependencies without updating requirements.txt
- **Don't** use stateful operations outside session state
- **Don't** forget CORS settings differ in dev vs production

#### 5. Testing Checklist

- [ ] Run `streamlit run streamlit_app.py` successfully
- [ ] Add a new ticket and verify ID increments
- [ ] Edit existing ticket and verify changes appear
- [ ] Check that charts update when data is edited
- [ ] Verify metrics reflect current data
- [ ] Test form validation (if applicable)
- [ ] Ensure no errors in browser console

#### 6. Code Quality Standards

**Readability:**
- Keep functions small and focused
- Use descriptive variable names
- Add comments for complex logic only
- Maintain consistent indentation (4 spaces)

**Performance:**
- Minimize reruns with `st.form` for multi-input
- Use `@st.cache_data` if adding expensive operations
- Avoid large computations outside session state check

**Security:**
- Never commit `.streamlit/secrets.toml`
- Sanitize user input if adding database features
- Follow Streamlit security best practices

#### 7. Debugging Tips

**For Data Issues:**
- Check `st.session_state.df` with `st.write(st.session_state.df)`
- Verify DataFrame schema with `.dtypes`
- Use `st.write()` liberally during development

**For UI Issues:**
- Check browser developer console
- Verify Streamlit version compatibility
- Test with `--server.runOnSave true` for rapid iteration

**For Deployment Issues:**
- Ensure all imports are in requirements.txt
- Check Streamlit Cloud logs
- Verify Python version compatibility

### Common Modification Scenarios

#### Adding a New Field (e.g., "Assignee")

```python
# 1. Update mock data
data = {
    # ... existing fields ...
    "Assignee": np.random.choice(["Alice", "Bob", "Charlie"], size=100),
}

# 2. Update form
with st.form("add_ticket_form"):
    # ... existing inputs ...
    assignee = st.selectbox("Assignee", ["Alice", "Bob", "Charlie"])

# 3. Update new ticket creation
df_new = pd.DataFrame([{
    # ... existing fields ...
    "Assignee": assignee,
}])

# 4. Update column config (if needed)
column_config={
    # ... existing config ...
    "Assignee": st.column_config.SelectboxColumn(
        "Assignee",
        options=["Alice", "Bob", "Charlie"],
        required=True,
    ),
}
```

#### Adding Database Persistence

**Important**: Current app uses session state (no persistence between sessions)

To add database:
1. Add database dependency to requirements.txt
2. Replace session state initialization with DB query
3. Add save operations after form submit and data edit
4. Handle database connection errors gracefully
5. Update .gitignore if using local DB files

#### Modifying Charts

All charts use Altair. Key methods:
- `.mark_bar()` - Bar chart
- `.mark_arc()` - Pie/donut chart
- `.mark_line()` - Line chart
- `.encode()` - Define x, y, color, etc.
- `.properties()` - Set height, width
- `.configure_legend()` - Style legend

### Repository-Specific Commands

```bash
# Run application
streamlit run streamlit_app.py

# Run with auto-reload
streamlit run streamlit_app.py --server.runOnSave true

# Run on specific port
streamlit run streamlit_app.py --server.port 8502

# Clear cache
streamlit cache clear
```

### Environment Variables

**For Streamlit Cloud:**
- Secrets: Use `.streamlit/secrets.toml` (gitignored)
- Access: `st.secrets["key"]`

**For Local Development:**
- Create `.streamlit/secrets.toml` if needed
- Format: TOML key-value pairs

## File References

When discussing code, reference specific locations:
- Session state init: `streamlit_app.py:21-65`
- Form handling: `streamlit_app.py:73-98`
- Data editor: `streamlit_app.py:112-132`
- Charts: `streamlit_app.py:147-172`

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Altair Documentation](https://altair-viz.github.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## Maintainer Notes

- **Code Owner**: @streamlit/community-cloud
- **Template Purpose**: Demonstrates internal tool patterns
- **Educational Focus**: Session state, forms, data editing, visualizations
- **Production Use**: Would require database backend for real deployment

---

**Last Updated**: 2025-11-17
**Claude Version**: This guide is optimized for Claude Code and AI assistants working with this repository.
