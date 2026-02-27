import streamlit as st
from agents.orchestrator import OrchestratorAgent

# Page config
st.set_page_config(
    page_title="OmniAgent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTextInput input { border-radius: 20px; }
    .tool-badge {
        background: #1f2937;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        color: #60a5fa;
        display: inline-block;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agent
@st.cache_resource
def get_agent():
    return OrchestratorAgent()

agent = get_agent()

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🤖 OmniAgent")
    st.caption("Autonomous AI Agent — Web Search + Code + Memory + ToolForge")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "tool_logs" not in st.session_state:
        st.session_state.tool_logs = []

    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input
    if prompt := st.chat_input("Ask me anything..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = agent.chat(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("🧠 Memory")
    memories = agent.memory.long_term
    if memories:
        for key, val in memories.items():
            st.markdown(f"""
            <div class='tool-badge'>
                <b>{key}</b>: {val['value']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No memories yet")
    
    st.divider()
    
    st.subheader("⚡ Tools Available")
    st.markdown("<div class='tool-badge'>🔍 Web Search</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-badge'>🐍 Code Executor</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-badge'>💾 Memory</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-badge'>🔨 ToolForge</div>", unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        agent.memory.clear_short_term()
        st.rerun()