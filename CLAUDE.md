# CLAUDE.md - AI Assistant Guide for chatbot-nora

## Project Overview

**chatbot-nora** is a Streamlit-based therapeutic chatbot that helps users navigate life's challenges using evidence-based psychological techniques. Nora combines Rogerian therapy's empathetic approach with Cognitive Behavioral Therapy (CBT) methods to provide compassionate, practical support. The application features a beautiful, intuitive chat interface designed for an exceptional user experience.

### Quick Facts
- **Primary Language**: Python 3.11
- **Framework**: Streamlit
- **License**: Apache 2.0
- **Application Type**: Therapeutic life-helper chatbot
- **Deployment**: Streamlit Cloud-ready
- **Character**: Nora - empathetic, supportive life companion
- **Therapeutic Approach**: Rogerian therapy + CBT techniques
- **Natural Language**: API-powered (OpenAI/Anthropic/similar)

## Project Vision

Nora is designed to help people with everyday life challenges by providing:

### Therapeutic Approach
- **Rogerian Therapy**: Active listening, unconditional positive regard, empathetic understanding
- **CBT Techniques**: Identifying thought patterns, cognitive restructuring, behavioral activation
- **Person-Centered**: Non-judgmental, supportive, empowering conversations
- **Practical Support**: Actionable insights and coping strategies

### User Experience Goals
- **Beautiful Interface**: Modern, calming chat UI with thoughtful design
- **Intuitive Flow**: Natural conversation without friction
- **Responsive**: Fast, smooth interactions
- **Accessible**: Clear typography, good contrast, mobile-friendly
- **Safe Space**: Private, judgment-free environment

### Nora's Personality
- **Empathetic**: Deeply understanding and validating
- **Warm**: Friendly, approachable, genuine
- **Non-Judgmental**: Accepts users without criticism
- **Encouraging**: Supportive and hopeful
- **Professional**: Maintains therapeutic boundaries

## Repository Structure

```
chatbot-nora/
├── streamlit_app.py          # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # User-facing documentation
├── CLAUDE.md                  # This file - AI assistant guide
├── LICENSE                    # Apache 2.0 license
├── .gitignore                # Git ignore patterns
├── .devcontainer/            # VS Code devcontainer config
│   └── devcontainer.json
└── .github/                  # GitHub configuration
    └── CODEOWNERS            # Code ownership
```

## Core Technologies

### Primary Stack
- **Streamlit**: Web application framework for interactive apps
- **Python Standard Library**: Core functionality
- **Potential additions**:
  - LangChain for LLM integration
  - OpenAI API or Anthropic API for AI responses
  - Vector databases for memory/context

### Python Version
- Python 3.11 (as specified in devcontainer.json)

## Application Architecture

### Chat Interface Design

The application should follow a conversational UI pattern:

1. **Initialization & Configuration**
   - Page configuration with appropriate title and icon
   - Session state setup for conversation history
   - Optional: API key configuration for LLM integration

2. **Conversation State Management**
   - Store messages in session state as list of dicts
   - Each message: `{"role": "user"/"assistant", "content": "text"}`
   - Maintain conversation context across reruns

3. **Chat Interface Components**
   - Message display area (chat history)
   - User input field (text input or chat input widget)
   - Submit/send functionality
   - Clear chat option

4. **Response Generation**
   - Process user input
   - Generate Nora's response (hardcoded, rule-based, or LLM-powered)
   - Update conversation history
   - Display new message

### Key Design Patterns for Chatbots

#### Session State for Conversation History
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Optional: Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm Nora, your friendly assistant. How can I help you today?"
    })
```

#### Message Display Pattern
```python
# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
```

#### Chat Input Pattern
```python
# Get user input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    response = generate_response(user_input)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Rerun to display new messages
    st.rerun()
```

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
- Session state for conversation persistence (within session)
- Single requirements.txt file
- Optional: API keys via Streamlit secrets

## Code Conventions

### Python Style
- **Imports**: Grouped logically (standard library, third-party, local)
- **Comments**: Used to explain Nora's personality and response logic
- **Naming**:
  - Snake_case for variables and functions
  - Descriptive names (e.g., `user_input`, `conversation_history`, `generate_nora_response`)

### Streamlit Conventions
1. **Page Config First**: Always call `st.set_page_config()` as first Streamlit command
2. **Session State**: Check existence before initializing (`if "messages" not in st.session_state`)
3. **Chat Components**: Use `st.chat_message()` and `st.chat_input()` for modern chat UI
4. **Rerun After Updates**: Use `st.rerun()` after adding messages to refresh display
5. **Container Width**: Use containers and columns for layout control

### Nora's Therapeutic Communication Guidelines

**Rogerian Principles (Person-Centered Therapy):**
1. **Active Listening**: Reflect back what the user says to show understanding
2. **Empathy**: Demonstrate understanding of user's feelings and experiences
3. **Unconditional Positive Regard**: Accept the user without judgment
4. **Genuineness**: Be authentic and sincere in responses
5. **Reflection**: Mirror emotions and content to validate experiences

**CBT Techniques:**
1. **Identify Thoughts**: Help users recognize automatic thoughts
2. **Challenge Beliefs**: Gently question unhelpful thought patterns
3. **Behavioral Activation**: Encourage small, actionable steps
4. **Cognitive Restructuring**: Reframe negative thoughts constructively
5. **Problem-Solving**: Break down challenges into manageable parts

**Communication Style:**
- Warm, compassionate, and validating
- Clear and accessible language
- Patient and non-rushed
- Asks open-ended questions
- Avoids clinical jargon unless helpful
- Never dismissive or minimizing

**Example Therapeutic Responses:**

```python
# Good: Rogerian reflection + validation
"It sounds like you've been feeling overwhelmed with work lately, and that's really weighing on you. That must be exhausting."

# Good: CBT cognitive reframing
"I hear you saying 'I always fail at everything.' I'm wondering - can we look at some times when things did work out for you?"

# Good: Empathy + action-oriented
"That's a really difficult situation you're facing. What would feel like a small, manageable first step we could explore together?"

# Avoid: Dismissive
"Everyone feels that way sometimes. You'll be fine."

# Avoid: Prescriptive without empathy
"You need to just stop thinking that way."

# Avoid: Clinical without warmth
"This appears to be a cognitive distortion requiring restructuring."
```

**User Experience & Interface Guidelines:**

**Visual Design:**
- Calming color palette (soft blues, greens, neutrals)
- Generous whitespace for breathing room
- Smooth animations and transitions
- Clear visual hierarchy
- Thoughtful use of icons and emojis

**Interaction Design:**
- Immediate feedback on user actions
- Typing indicators during response generation
- Smooth message appearance animations
- Easy-to-find clear chat option
- Accessible on all device sizes

**Conversational Flow:**
- Natural pacing (not too fast or slow)
- Appropriate message length (digestible chunks)
- Strategic use of follow-up questions
- Summarize long conversations periodically
- Offer breaks in intense discussions

### Data Conventions

**Message Structure:**
```python
{
    "role": "user" | "assistant",
    "content": "message text",
    "timestamp": "optional timestamp"
}
```

**Session State Keys:**
- `messages`: List of message dictionaries (conversation history)
- `user_name`: Optional - store user's name if provided
- `conversation_id`: Optional - unique ID for analytics
- `context`: Optional - additional context or metadata

## AI Assistant Guidelines

### When Making Changes

#### 1. Understand Conversation Flow
- **Source of Truth**: `st.session_state.messages`
- **Display**: Iterate through messages and render with `st.chat_message()`
- **Updates**: Append new messages and call `st.rerun()` to refresh

#### 2. Maintain Nora's Personality
- Keep responses friendly and helpful
- Ensure consistent tone across all interactions
- Review responses for appropriateness
- Test conversation flows for natural feel

#### 3. Adding New Features

**For Enhanced Responses:**
1. Consider context from previous messages
2. Implement response generation logic
3. Add error handling for edge cases
4. Test with various user inputs
5. Consider rate limiting and API costs

**For LLM Integration:**
1. Add appropriate dependencies (openai, anthropic, langchain)
2. Update requirements.txt
3. Implement API key management via secrets
4. Add system prompts to guide Nora's personality
5. Handle API errors gracefully
6. Consider token limits and costs

**For Memory/Context:**
1. Implement conversation summarization
2. Store important context separately
3. Consider vector database for retrieval
4. Limit context window to prevent token overflow

**For Additional UI Features:**
1. Add clear chat button
2. Implement conversation export
3. Add typing indicators
4. Include helpful suggestions/prompts
5. Add conversation history sidebar

#### 4. Common Pitfalls to Avoid

- **Don't** lose conversation history on page refresh (use session state)
- **Don't** make Nora sound robotic or overly formal
- **Don't** expose API keys in code
- **Don't** forget error handling for external API calls
- **Don't** let conversation history grow unbounded (implement cleanup)
- **Don't** forget to handle edge cases (empty input, very long input)

#### 5. Testing Checklist

- [ ] Run `streamlit run streamlit_app.py` successfully
- [ ] Start a conversation and verify messages display correctly
- [ ] Test multiple back-and-forth exchanges
- [ ] Verify conversation history persists during session
- [ ] Test edge cases (empty input, very long messages)
- [ ] Verify Nora's personality is consistent
- [ ] Check for any API errors or timeouts
- [ ] Test on mobile layout (responsive design)
- [ ] Verify no sensitive data is logged

#### 6. Code Quality Standards

**Readability:**
- Keep response generation logic modular
- Use clear function names
- Comment on personality decisions
- Document any prompt engineering choices

**Performance:**
- Cache API responses when appropriate
- Implement streaming for long responses
- Limit conversation history length
- Optimize message rendering

**Security:**
- Never commit API keys
- Sanitize user input
- Implement rate limiting
- Validate all inputs
- Use secrets management for sensitive data

#### 7. Debugging Tips

**For Conversation Issues:**
- Check `st.session_state.messages` with `st.write(st.session_state.messages)`
- Verify message structure is correct
- Use `st.write()` to inspect state during development

**For UI Issues:**
- Test with different message lengths
- Verify chat container scrolling works
- Check responsive design on mobile
- Ensure emojis and special characters display correctly

**For API Issues:**
- Log API calls and responses
- Implement retry logic
- Check API quotas and limits
- Verify API key configuration

### Common Modification Scenarios

#### Adding LLM Integration with Therapeutic Prompt

```python
import openai

# In secrets.toml
# openai_api_key = "sk-..."

# Initialize
openai.api_key = st.secrets["openai_api_key"]

# System prompt defining Nora's therapeutic approach
NORA_SYSTEM_PROMPT = """You are Nora, a compassionate and supportive AI companion trained in Rogerian
person-centered therapy and Cognitive Behavioral Therapy (CBT) techniques. Your purpose is to help
people navigate everyday life challenges.

Core Principles:
- Practice active listening and reflect back what users share
- Show unconditional positive regard - accept without judgment
- Be genuinely empathetic and warm in your responses
- Use CBT techniques to help identify and reframe unhelpful thoughts
- Encourage small, actionable behavioral steps
- Ask thoughtful, open-ended questions
- Validate feelings while offering new perspectives

Communication Style:
- Warm, genuine, and accessible
- Avoid clinical jargon
- Use "I" statements to show understanding ("I hear that...", "It sounds like...")
- Break down complex emotional situations into manageable parts
- Never be dismissive or prescriptive

Boundaries:
- You are a supportive companion, not a replacement for professional therapy
- Encourage seeking professional help for serious mental health concerns
- Maintain appropriate therapeutic boundaries
- Be transparent about your limitations as an AI

Remember: Every person's experience is valid. Meet them where they are with compassion and support."""

def generate_nora_response(conversation_history):
    """Generate therapeutic response using LLM API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": NORA_SYSTEM_PROMPT},
                *conversation_history
            ],
            temperature=0.7,  # Balanced creativity and consistency
            max_tokens=500,   # Keep responses digestible
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error("I'm having trouble connecting right now. Could you try again?")
        return None
```

**Alternative: Using Anthropic Claude API**

```python
import anthropic

# Initialize
client = anthropic.Anthropic(api_key=st.secrets["anthropic_api_key"])

def generate_nora_response(conversation_history):
    """Generate therapeutic response using Claude API"""
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=NORA_SYSTEM_PROMPT,
            messages=conversation_history
        )
        return response.content[0].text
    except Exception as e:
        st.error("I'm having trouble connecting right now. Could you try again?")
        return None
```

#### Adding Conversation Export

```python
import json
from datetime import datetime

def export_conversation():
    """Export conversation as JSON"""
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": st.session_state.messages
    }
    return json.dumps(export_data, indent=2)

# In UI
if st.button("Export Conversation"):
    export_json = export_conversation()
    st.download_button(
        "Download Chat History",
        export_json,
        file_name=f"nora_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
```

#### Adding Clear Chat Functionality

```python
# In sidebar or main area
if st.button("Clear Chat"):
    st.session_state.messages = []
    # Re-add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm Nora. How can I help you today?"
    })
    st.rerun()
```

### Repository-Specific Commands

```bash
# Run application
streamlit run streamlit_app.py

# Run with auto-reload (helpful during development)
streamlit run streamlit_app.py --server.runOnSave true

# Run on specific port
streamlit run streamlit_app.py --server.port 8502

# Clear cache
streamlit cache clear
```

### Environment Variables & Secrets

**For Streamlit Cloud:**
Create `.streamlit/secrets.toml` (gitignored):
```toml
# API Keys
openai_api_key = "sk-..."
anthropic_api_key = "sk-ant-..."

# Optional configurations
max_conversation_length = 50
```

**Access in Code:**
```python
api_key = st.secrets["openai_api_key"]
max_length = st.secrets.get("max_conversation_length", 50)
```

## Nora's Implementation Roadmap

### Phase 1: Beautiful Chat Interface (MVP)
- [ ] Design calming color scheme and UI layout
- [ ] Implement Streamlit chat UI with `st.chat_message()` and `st.chat_input()`
- [ ] Add custom CSS for enhanced visual design
- [ ] Implement session state for conversation history
- [ ] Create warm welcome message
- [ ] Add clear chat functionality
- [ ] Test responsive design on mobile
- [ ] Ensure smooth animations and transitions

### Phase 2: Therapeutic AI Integration
- [ ] Choose and integrate LLM API (OpenAI/Anthropic)
- [ ] Write comprehensive therapeutic system prompt
- [ ] Implement Rogerian reflection patterns
- [ ] Add CBT technique guidance in prompts
- [ ] Implement error handling with empathetic fallbacks
- [ ] Add typing indicators during response generation
- [ ] Test therapeutic consistency across conversations
- [ ] Validate responses maintain appropriate boundaries

### Phase 3: Enhanced User Experience
- [ ] Add conversation pacing (prevent overwhelming users)
- [ ] Implement periodic conversation summaries
- [ ] Add "take a break" suggestions for intense discussions
- [ ] Create helpful starter prompts/suggestions
- [ ] Add conversation export feature (JSON/PDF)
- [ ] Implement sentiment tracking (optional, private)
- [ ] Add accessibility features (keyboard navigation, screen reader support)
- [ ] Optimize loading times and response speed

### Phase 4: Memory & Personalization
- [ ] Implement conversation summarization
- [ ] Add context retention across sessions (optional)
- [ ] Store user preferences (if user opts in)
- [ ] Implement topic continuity ("Last time we talked about...")
- [ ] Add progress tracking for recurring issues
- [ ] Optimize token usage with smart context windows

### Phase 5: Advanced Therapeutic Features
- [ ] Add CBT thought record templates
- [ ] Implement mood tracking visualization
- [ ] Create guided exercises (breathing, grounding)
- [ ] Add journaling prompts
- [ ] Implement crisis resource recommendations
- [ ] Add professional therapist finder integration
- [ ] Create feedback and improvement mechanisms

### Phase 6: Polish & Production
- [ ] Comprehensive testing with real users
- [ ] Performance optimization
- [ ] Security audit (especially for user data)
- [ ] Privacy policy and terms of service
- [ ] Analytics for improvement (anonymized)
- [ ] Error monitoring and logging
- [ ] Deployment to Streamlit Cloud
- [ ] User onboarding flow

## UI/UX Best Practices for Nora

### Custom Styling with Streamlit

```python
# Add custom CSS for beautiful interface
def apply_custom_css():
    st.markdown("""
        <style>
        /* Calming color scheme */
        :root {
            --primary-color: #4A90E2;
            --background-color: #F5F7FA;
            --text-color: #2C3E50;
            --accent-color: #7CB9E8;
        }

        /* Chat message styling */
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Input styling */
        .stChatInput {
            border-radius: 1rem;
            border: 2px solid var(--accent-color);
        }

        /* Smooth transitions */
        * {
            transition: all 0.2s ease;
        }
        </style>
    """, unsafe_allow_html=True)
```

### Typing Indicator

```python
import time

def show_typing_indicator():
    """Show typing indicator while generating response"""
    with st.chat_message("assistant"):
        with st.spinner("Nora is typing..."):
            time.sleep(0.5)  # Brief pause for natural feel
```

### Message Pacing

```python
def should_suggest_break(message_count):
    """Suggest break after extended conversation"""
    if message_count > 20 and message_count % 10 == 0:
        return True
    return False

# In main chat loop
if should_suggest_break(len(st.session_state.messages)):
    st.info("💙 We've been chatting for a while. Would you like to take a break and come back later?")
```

## Ethical Considerations & Safety

### Important Disclaimers

**Must Include:**
- Nora is an AI companion, not a licensed therapist
- Not a substitute for professional mental health care
- Clear guidance on when to seek professional help
- Crisis resources readily available

### Crisis Detection & Resources

```python
CRISIS_KEYWORDS = ['suicide', 'kill myself', 'end it all', 'not worth living', 'self-harm']

def check_for_crisis(user_message):
    """Detect potential crisis situations"""
    message_lower = user_message.lower()
    if any(keyword in message_lower for keyword in CRISIS_KEYWORDS):
        return True
    return False

def show_crisis_resources():
    """Display crisis resources immediately"""
    st.error("""
    🚨 **If you're in crisis, please reach out for immediate help:**

    - **National Suicide Prevention Lifeline**: 988 (US)
    - **Crisis Text Line**: Text HOME to 741741
    - **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

    These services provide immediate, confidential support from trained professionals.
    """)

# In message processing
if check_for_crisis(user_input):
    show_crisis_resources()
```

### Privacy & Data Protection

**Key Principles:**
- Never store sensitive conversations without explicit consent
- Be transparent about data usage
- Provide easy way to delete conversation history
- Don't log personally identifiable information
- Use secure API connections (HTTPS)

```python
# Privacy-conscious implementation
if "user_consented_storage" not in st.session_state:
    st.session_state.user_consented_storage = False

# Show privacy notice on first use
if not st.session_state.get("privacy_shown", False):
    st.info("""
    🔒 **Your Privacy Matters**

    Conversations with Nora are:
    - Only stored in your browser session
    - Never saved to our servers without your consent
    - Not used to train AI models
    - Automatically cleared when you close your browser

    You can clear your chat history anytime using the "Clear Chat" button.
    """)
    st.session_state.privacy_shown = True
```

### Therapeutic Boundaries

**Nora Should:**
- ✅ Provide support and coping strategies
- ✅ Help identify thought patterns
- ✅ Encourage positive behavioral changes
- ✅ Validate feelings and experiences
- ✅ Suggest professional help when appropriate

**Nora Should NOT:**
- ❌ Diagnose mental health conditions
- ❌ Prescribe treatment or medication
- ❌ Replace professional therapy
- ❌ Make medical recommendations
- ❌ Handle severe psychiatric emergencies

## Additional Resources

### Streamlit & Development
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Chat Elements](https://docs.streamlit.io/library/api-reference/chat)
- [Streamlit Custom Components](https://docs.streamlit.io/library/components)

### AI & NLP APIs
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [LangChain Documentation](https://python.langchain.com/)

### Therapeutic Approaches
- [Person-Centered Therapy (Rogerian)](https://www.apa.org/topics/psychotherapy/person-centered)
- [Cognitive Behavioral Therapy](https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral)
- [Active Listening Techniques](https://www.ccl.org/articles/leading-effectively-articles/coaching-others-use-active-listening-skills/)

### Mental Health Resources
- [National Alliance on Mental Illness (NAMI)](https://www.nami.org/)
- [Mental Health America](https://www.mhanational.org/)
- [Crisis Text Line](https://www.crisistextline.org/)

## Maintainer Notes

- **Project Purpose**: Therapeutic life-helper chatbot using evidence-based techniques
- **Character**: Nora - empathetic, supportive AI companion
- **Therapeutic Approach**: Rogerian person-centered therapy + CBT
- **Focus**: Beautiful UX, natural conversation, genuine support
- **Priority**: User safety, privacy, and well-being
- **Not**: A replacement for professional mental health care

---

**Last Updated**: 2025-11-17
**Claude Version**: This guide is optimized for Claude Code and AI assistants working with this repository.
**Important**: This is a supportive tool, not a substitute for professional mental health services.
