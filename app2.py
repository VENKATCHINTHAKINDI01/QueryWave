import streamlit as st
import streamlit.components.v1 as components
import base64

# ------------------ BACKEND IMPORTS ------------------

from app.utils.logger import get_logger
from app.orchestration.router import route_query
from app.orchestration.tool_manager import execute_tool
from app.exceptions import RoutingException
from app.memory.chat_history import ChatHistoryManager

logger = get_logger(__name__)

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------

st.set_page_config(
    page_title="QueryWave",
    page_icon="🌊",
    layout="wide"
)

# ------------------------------------------------------
# BACKGROUND IMAGE
# ------------------------------------------------------

def set_background(image_path: str):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(5,8,22,0.75);
            z-index: -1;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.jpg")

# ------------------------------------------------------
# FLOATING NEURAL PARTICLES
# ------------------------------------------------------

floating_effect = """
<canvas id="particles"></canvas>
<style>
#particles {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}
</style>
<script>
const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];
const particleCount = 60;
const maxDistance = 150;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.6;
        this.vy = (Math.random() - 0.5) * 0.6;
        this.radius = 2;
    }

    move() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(0,255,255,0.6)";
        ctx.fill();
    }
}

function connect() {
    for (let i = 0; i < particles.length; i++) {
        for (let j = i; j < particles.length; j++) {
            let dx = particles[i].x - particles[j].x;
            let dy = particles[i].y - particles[j].y;
            let dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < maxDistance) {
                ctx.strokeStyle = "rgba(0,255,255," + (1 - dist/maxDistance) * 0.3 + ")";
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    for (let p of particles) {
        p.move();
        p.draw();
    }
    connect();
    requestAnimationFrame(animate);
}

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

animate();
</script>
"""

components.html(floating_effect, height=0)

# ------------------------------------------------------
# PREMIUM CSS
# ------------------------------------------------------

st.markdown("""
<style>

.glass {
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 40px rgba(0,255,255,0.15);
}

.title {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    color: white;
    text-shadow: 0 0 30px rgba(0,255,255,0.9);
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

textarea {
    background: rgba(0,0,0,0.85) !important;
    border: 1px solid #00ffff !important;
    border-radius: 14px !important;
    color: white !important;
}

[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.9);
}
[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------

with st.sidebar:

    st.markdown("## 🌊 QueryWave")
    st.markdown("### Mode Selection")

    modes = {
        "📄 Document Q&A": "document",
        "🌐 Web Search": "web",
        "📚 Research Papers (arXiv)": "arxiv",
    }

    selected_label = st.radio("Choose mode:", list(modes.keys()))
    st.session_state.active_mode = modes[selected_label]

    st.markdown("---")

    if st.session_state.active_mode == "document":
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.session_state["uploaded_files"] = [
                {"name": f.name, "file": f} for f in uploaded_files
            ]
            st.success(f"{len(uploaded_files)} file(s) ready")

    if st.session_state.active_mode == "arxiv":
        arxiv_id = st.text_input("Enter arXiv ID")
        if arxiv_id:
            st.session_state["arxiv_id"] = arxiv_id.strip()

    st.markdown("---")
    st.caption("⚡ Powered by Llama3 + Hybrid Retrieval")

# ------------------------------------------------------
# MAIN CONTENT
# ------------------------------------------------------

st.markdown('<div class="title">QueryWave</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent Retrieval-Augmented AI Assistant</div>', unsafe_allow_html=True)

memory = ChatHistoryManager(st.session_state)

# History toggle
if "show_history" not in st.session_state:
    st.session_state.show_history = False

col1, col2 = st.columns([10,1])
with col2:
    if st.button("🕘"):
        st.session_state.show_history = not st.session_state.show_history

if st.session_state.show_history:
    with st.container():
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Conversation History")
        for msg in memory.get_history():
            role = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
            st.markdown(f"**{role}:** {msg['content']}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass">', unsafe_allow_html=True)

user_input = st.chat_input("Ask your question...")

if user_input:

    memory.add_user_message(user_input)

    try:
        routing_result = route_query(user_input, st.session_state)
        execution_result = execute_tool(routing_result)

        response_data = execution_result["data"]
        assistant_response = response_data["answer"]
        sources = response_data.get("sources", [])

    except RoutingException as e:
        assistant_response = f"⚠️ {str(e)}"
        sources = []

    memory.add_assistant_message(assistant_response)

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

        if sources:
            st.markdown("### 📚 Sources")
            for source in sources:
                st.markdown(f"- **{source['source']}** (Chunk {source['chunk_id']})")

st.markdown('</div>', unsafe_allow_html=True)
