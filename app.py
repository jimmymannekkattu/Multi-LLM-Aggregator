import streamlit as st
import asyncio
import httpx
from llm_providers import fetch_openai, fetch_anthropic, fetch_gemini, fetch_perplexity, fetch_ollama, fetch_generic_openai_compatible, fetch_g4f
from offline_model import synthesize_responses
import qrcode
import socket
import io
import json
import os
import streamlit.components.v1 as components

# --- Configuration & State ---
st.set_page_config(
    page_title="AI Nexus",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "custom_providers" not in st.session_state:
    st.session_state.custom_providers = []

if "network_nodes" not in st.session_state:
    st.session_state.network_nodes = []

PROVIDERS_FILE = "custom_providers.json"

def load_providers():
    if os.path.exists(PROVIDERS_FILE):
        try:
            with open(PROVIDERS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_providers(providers):
    with open(PROVIDERS_FILE, "w") as f:
        json.dump(providers, f)

if not st.session_state.custom_providers:
    st.session_state.custom_providers = load_providers()

try:
    from agents.memory import add_to_memory, retrieve_context, export_dataset
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

from agents.discovery import get_g4f_models, get_openrouter_models, verify_model, search_models

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# --- Navigation Functions ---
def go_to_landing():
    st.session_state.page = "landing"
    st.rerun()

def go_to_app():
    st.session_state.page = "app"
    st.rerun()

def go_to_chat():
    st.session_state.page = "chat"
    st.rerun()

# --- Page Renderers ---

def render_landing_page():
    # Custom CSS for Landing Page
    st.markdown("""
    <style>
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 50px 20px;
            text-align: center;
        }
        .landing-header h1 {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .landing-header p {
            font-size: 1.2rem;
            color: #a0aec0;
            margin-bottom: 50px;
        }
        .cards-container {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .card {
            background: #1a202c;
            border: 1px solid #2d3748;
            border-radius: 20px;
            padding: 40px;
            width: 320px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
            border-color: #667eea;
        }
        .card-icon {
            font-size: 4rem;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
        }
        .card-desc {
            color: #a0aec0;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        .card-btn {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-secondary {
            background: #2d3748;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="landing-container"><div class="landing-header"><h1>🤖 AI Nexus Portal</h1><p>Choose your preferred interface to get started</p></div></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("""
            <div class="card">
                <div class="card-icon">🖥️</div>
                <div class="card-title">Desktop App</div>
                <div class="card-desc">Full-featured control panel with advanced settings, discovery, and memory management.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch Desktop App", use_container_width=True, type="primary"):
                go_to_app()

        with c2:
            st.markdown("""
            <div class="card">
                <div class="card-icon">💬</div>
                <div class="card-title">Web Chat</div>
                <div class="card-desc">Modern, beautiful chat interface with persistent settings and model selection.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch Web Chat", use_container_width=True, type="primary"):
                go_to_chat()

def render_web_chat():
    # Sidebar navigation
    with st.sidebar:
        if st.button("⬅️ Back to Portal"):
            go_to_landing()
        if st.button("🖥️ Switch to Desktop App"):
            go_to_app()
    
    # Read chat-full.html content
    try:
        chat_path = os.path.join(os.getcwd(), "examples", "chat-full.html")
        with open(chat_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Embed using iframe for isolation or direct html
        # Using components.html with height to fill screen
        components.html(html_content, height=900, scrolling=True)
        
    except Exception as e:
        st.error(f"Failed to load Web Chat: {e}")

def render_desktop_app():
    # Sidebar navigation
    with st.sidebar:
        if st.button("⬅️ Back to Portal"):
            go_to_landing()
        st.divider()

    # --- Original App Logic ---
    
    # Custom CSS for "Premium" feel
    st.markdown("""
    <style>
        /* Main App Background */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Text Area Styling */
        .stTextArea textarea {
            background-color: #262730;
            color: #ffffff;
            border-radius: 12px;
            border: 1px solid #444;
            padding: 15px;
            font-size: 16px;
        }
        .stTextArea textarea:focus {
            border-color: #ff4b4b;
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.2);
        }

        /* Button Styling */
        .stButton button {
            background: linear-gradient(90deg, #ff4b4b 0%, #ff6b6b 100%);
            color: white;
            border-radius: 25px;
            padding: 12px 28px;
            font-weight: 600;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        }

        /* Provider Card Styling */
        .provider-card {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #333;
            margin-bottom: 20px;
            height: 400px;
            overflow-y: auto;
            transition: border-color 0.3s ease;
        }
        .provider-card:hover {
            border-color: #555;
        }

        /* Final Answer Card Styling */
        .final-answer {
            background: linear-gradient(145deg, #1a1c24, #2d2d2d);
            padding: 35px;
            border-radius: 20px;
            border: 1px solid #444;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        .final-answer::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
        }

        /* Sidebar Headers */
        .css-10trblm {
            color: #ff4b4b;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # --- Tabbed Interface for Cleaner UI ---
        tab_online, tab_offline, tab_knowledge, tab_mobile, tab_discovery = st.tabs(["🌐 Online", "💻 Offline", "🧠 Brain", "📱 Mobile", "🔍 Discovery"])
        
        # --- TAB 1: ONLINE MODELS ---
        with tab_online:
            st.subheader("Online Providers")
            
            # Provider Manager (Expander)
            with st.expander("➕ Add Custom Provider", expanded=False):
                st.markdown("Add OpenAI-compatible APIs")
                
                provider_template = st.selectbox(
                    "Template", 
                    ["Custom", "Groq", "OpenRouter", "DeepSeek", "Together AI", "Mistral API"]
                )
                
                base_url_default = ""
                if provider_template == "Groq": base_url_default = "https://api.groq.com/openai/v1"
                elif provider_template == "OpenRouter": base_url_default = "https://openrouter.ai/api/v1"
                elif provider_template == "DeepSeek": base_url_default = "https://api.deepseek.com/v1"
                elif provider_template == "Together AI": base_url_default = "https://api.together.xyz/v1"
                elif provider_template == "Mistral API": base_url_default = "https://api.mistral.ai/v1"
                
                new_provider_name = st.text_input("Name", value=provider_template if provider_template != "Custom" else "")
                new_base_url = st.text_input("Base URL", value=base_url_default)
                new_api_key = st.text_input("API Key", type="password")
                new_model_name = st.text_input("Model ID", placeholder="e.g. llama3-70b")
                
                if st.button("Add Provider"):
                    if new_provider_name and new_base_url and new_api_key and new_model_name:
                        st.session_state.custom_providers.append({
                            "name": new_provider_name,
                            "base_url": new_base_url,
                            "api_key": new_api_key,
                            "model": new_model_name
                        })
                        save_providers(st.session_state.custom_providers)
                        st.success(f"Added {new_provider_name}!")
                        st.rerun()
                    else:
                        st.error("Missing fields")

                # Manage existing
                if st.session_state.custom_providers:
                    st.divider()
                    for i, p in enumerate(st.session_state.custom_providers):
                        col_p, col_del = st.columns([4, 1])
                        col_p.text(f"{p['name']}")
                        if col_del.button("❌", key=f"del_{i}"):
                            st.session_state.custom_providers.pop(i)
                            save_providers(st.session_state.custom_providers)
                            st.rerun()

            # Selection
            standard_options = ["ChatGPT (OpenAI)", "Claude (Anthropic)", "Gemini (Google)", "Perplexity"]
            custom_options = [p["name"] for p in st.session_state.custom_providers]
            all_online_options = standard_options + custom_options
            
            selected_online_models = st.multiselect(
                "Select Active Models",
                all_online_options,
                default=standard_options
            )

        # --- TAB 2: OFFLINE & NETWORK ---
        with tab_offline:
            st.subheader("Local & Network Fleet")
            use_ollama = st.toggle("Enable Offline Fleet", value=False)
            
            selected_ollama_models = []
            synthesizer_model_option = None
            
            if use_ollama:
                # Network Nodes Manager
                with st.expander("🌐 Manage Network Nodes", expanded=False):
                    node_name = st.text_input("Node Name", placeholder="Living Room PC")
                    node_url = st.text_input("Node URL", placeholder="http://192.168.1.X:11434")
                    
                    if st.button("Add Node"):
                        if node_name and node_url:
                            st.session_state.network_nodes.append({"name": node_name, "url": node_url})
                            st.success(f"Added {node_name}!")
                            st.rerun()
                    
                    if st.session_state.network_nodes:
                        st.markdown("**Active Nodes:**")
                        for i, node in enumerate(st.session_state.network_nodes):
                            col_n, col_d = st.columns([4, 1])
                            col_n.text(f"🟢 {node['name']}")
                            if col_d.button("❌", key=f"del_node_{i}"):
                                st.session_state.network_nodes.pop(i)
                                st.rerun()

                col_refresh, _ = st.columns([1, 2])
                with col_refresh:
                    if st.button("🔄 Refresh Fleet"):
                        st.rerun()

                # Distributed Model Discovery
                all_discovered_models = [] 
                
                # 1. Localhost
                try:
                    tags = httpx.get("http://localhost:11434/api/tags", timeout=1.0).json()["models"]
                    for m in tags:
                        all_discovered_models.append({
                            "display": f"🏠 [Local] {m['name']}",
                            "model": m["name"],
                            "url": "http://localhost:11434/api/generate",
                            "node": "Local"
                        })
                except:
                    pass

                # 2. Network Nodes
                for node in st.session_state.network_nodes:
                    try:
                        base_url = node["url"].rstrip("/")
                        tags = httpx.get(f"{base_url}/api/tags", timeout=2.0).json()["models"]
                        for m in tags:
                            all_discovered_models.append({
                                "display": f"🌐 [{node['name']}] {m['name']}",
                                "model": m["name"],
                                "url": f"{base_url}/api/generate",
                                "node": node["name"]
                            })
                    except:
                        st.error(f"❌ Unreachable: {node['name']}")

                if all_discovered_models:
                    model_options = [m["display"] for m in all_discovered_models]
                    
                    selected_displays = st.multiselect(
                        "Select Fleet Models", 
                        model_options,
                        default=[model_options[0]] if model_options else []
                    )
                    
                    for display in selected_displays:
                        for m in all_discovered_models:
                            if m["display"] == display:
                                selected_ollama_models.append(m)
                                break
                    
                    st.divider()
                    st.markdown("**🧠 The Brain (Synthesizer)**")
                    synthesizer_display = st.selectbox(
                        "Select Synthesizer Node",
                        model_options,
                        index=0
                    )
                    
                    for m in all_discovered_models:
                        if m["display"] == synthesizer_display:
                            synthesizer_model_option = m
                            break
                else:
                    st.warning("No offline models found.")
                    st.info("Ensure Ollama is running (`ollama serve`).")

        # --- TAB 3: KNOWLEDGE BASE ---
        with tab_knowledge:
            st.subheader("Knowledge Distillation")
            if MEMORY_AVAILABLE:
                st.info("Train your offline models with online wisdom.")
                enable_learning = st.toggle("Enable Learning (Save)", value=True)
                enable_context = st.toggle("Enable Context (Recall)", value=True)
                
                st.divider()
                if st.button("📂 Export Dataset (JSONL)"):
                    msg = export_dataset()
                    st.success(msg)
            else:
                st.error("Dependencies missing.")
                enable_learning = False
                enable_context = False

        # --- TAB 4: MOBILE CONNECT ---
        with tab_mobile:
            st.subheader("📱 Connect Mobile App")
            st.info("Scan this QR code with the AI Nexus Mobile App to connect.")
            
            local_ip = get_local_ip()
            api_url = f"http://{local_ip}:8000"
            
            # Generate QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(api_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes for streamlit
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            st.image(img_byte_arr, caption=f"API URL: {api_url}", width=200)
            st.markdown(f"**Manual Entry:** `{api_url}`")

        # --- TAB 5: DISCOVERY ---
        with tab_discovery:
            st.subheader("🔍 Model Discovery")
            st.info("Find and add new models to your fleet.")
            
            disc_mode = st.radio("Source", ["Global Search", "Free Web (g4f)", "OpenRouter (API)", "Local/Network (Ollama)"], horizontal=True)
            
            if disc_mode == "Free Web (g4f)":
                st.markdown("### Popular Free Models")
                
                if "discovered_g4f_models" not in st.session_state:
                    st.session_state.discovered_g4f_models = []

                if st.button("Scan for Models"):
                    with st.spinner("Scanning..."):
                        st.session_state.discovered_g4f_models = asyncio.run(get_g4f_models())
                
                if st.session_state.discovered_g4f_models:
                    for m in st.session_state.discovered_g4f_models:
                        col_name, col_act = st.columns([3, 1])
                        col_name.text(m["display"])
                        
                        # Check if already added
                        is_added = any(p["name"] == m["display"] for p in st.session_state.custom_providers)
                        
                        if is_added:
                            col_act.success("Added")
                        else:
                            if col_act.button("Test & Add", key=f"add_{m['name']}"):
                                with st.status(f"Verifying {m['name']}...") as status:
                                    success, msg = asyncio.run(verify_model(m['name'], "g4f"))
                                    if success:
                                        status.update(label="✅ Verified!", state="complete")
                                        new_p = {
                                            "name": m["display"],
                                            "api_key": "",
                                            "base_url": "",
                                            "model": m["name"],
                                            "template": "Custom",
                                            "type": "g4f_discovered"
                                        }
                                        st.session_state.custom_providers.append(new_p)
                                        save_providers(st.session_state.custom_providers)
                                        st.success(f"Added {m['name']}!")
                                        st.rerun()
                                    else:
                                        status.update(label="❌ Failed", state="error")
                                        st.error(msg)
                                        
            elif disc_mode == "OpenRouter (API)":
                st.markdown("### OpenRouter Discovery")
                or_key = st.text_input("OpenRouter API Key", type="password")
                if st.button("Fetch Models") and or_key:
                    with st.spinner("Fetching catalog..."):
                        models = asyncio.run(get_openrouter_models(or_key))
                        if isinstance(models, list):
                            st.success(f"Found {len(models)} models!")
                            # Search
                            search_term = st.text_input("Search Models", placeholder="llama, mistral, etc.")
                            filtered = [m for m in models if search_term.lower() in m["name"].lower()] if search_term else models[:20]
                            
                            for m in filtered:
                                with st.expander(f"{m['display']}"):
                                    st.write(f"**ID:** `{m['name']}`")
                                    st.write(f"**Context:** {m['context']}")
                                    st.write(f"**Cost:** ${m['cost_prompt']}/1M prompt")
                                    if st.button("Add to Fleet", key=f"add_or_{m['name']}"):
                                        new_p = {
                                            "name": m["display"],
                                            "api_key": or_key,
                                            "base_url": "https://openrouter.ai/api/v1",
                                            "model": m["name"],
                                            "template": "OpenRouter"
                                        }

                                        st.session_state.custom_providers.append(new_p)
                                        save_providers(st.session_state.custom_providers)
                                        st.success(f"Added {m['name']}!")
                                        st.rerun()
                        else:
                            st.error(models["error"])

            elif disc_mode == "Local/Network (Ollama)":
                st.markdown("### Offline Model Discovery")
                st.info("Scanning Localhost and configured Network Nodes...")
                
                if "discovered_ollama_models" not in st.session_state:
                    st.session_state.discovered_ollama_models = []

                if st.button("Scan Network"):
                    with st.spinner("Scanning fleet..."):
                        found_models = []
                        # 1. Localhost
                        try:
                            tags = httpx.get("http://localhost:11434/api/tags", timeout=1.0).json()["models"]
                            for m in tags:
                                found_models.append({
                                    "display": f"🏠 [Local] {m['name']}",
                                    "model": m["name"],
                                    "base_url": "http://localhost:11434",
                                    "node": "Local"
                                })
                        except:
                            pass

                        # 2. Network Nodes
                        for node in st.session_state.network_nodes:
                            try:
                                base_url = node["url"].rstrip("/")
                                tags = httpx.get(f"{base_url}/api/tags", timeout=2.0).json()["models"]
                                for m in tags:
                                    found_models.append({
                                        "display": f"🌐 [{node['name']}] {m['name']}",
                                        "model": m["name"],
                                        "base_url": base_url,
                                        "node": node["name"]
                                    })
                            except:
                                pass
                        
                        st.session_state.discovered_ollama_models = found_models
                
                if st.session_state.discovered_ollama_models:
                    for m in st.session_state.discovered_ollama_models:
                        col_name, col_act = st.columns([3, 1])
                        col_name.text(m["display"])
                        
                        # Check if already added
                        is_added = any(p["name"] == m["display"] for p in st.session_state.custom_providers)
                        
                        if is_added:
                            col_act.success("Added")
                        else:
                            if col_act.button("Test & Add", key=f"add_ollama_{m['display']}"):
                                with st.status(f"Verifying {m['model']} on {m['node']}...") as status:
                                    success, msg = asyncio.run(verify_model(m['model'], "Ollama", base_url=m["base_url"]))
                                    if success:
                                        status.update(label="✅ Verified!", state="complete")
                                        new_p = {
                                            "name": m["display"],
                                            "api_key": "",
                                            "base_url": m["base_url"],
                                            "model": m["model"],
                                            "template": "Custom",
                                            "type": "ollama_discovered"
                                        }
                                        st.session_state.custom_providers.append(new_p)
                                        save_providers(st.session_state.custom_providers)
                                        st.success(f"Added {m['display']}!")
                                        st.rerun()
                                    else:
                                        status.update(label="❌ Failed", state="error")
                                        st.error(msg)
            elif disc_mode == "Global Search":
                st.markdown("### 🌍 Global Model Search")
                st.info("Search across Free Web (g4f) and OpenRouter.")
                
                search_query = st.text_input("Search for a model (e.g., 'llama', 'gpt', 'mistral')")
                or_key_search = st.text_input("OpenRouter API Key (Optional)", type="password", help="Required for OpenRouter results")
                
                if "search_results" not in st.session_state:
                    st.session_state.search_results = []

                if st.button("Search") and search_query:
                    with st.spinner(f"Searching for '{search_query}'..."):
                        st.session_state.search_results = asyncio.run(search_models(search_query, or_key_search))
                
                if st.session_state.search_results:
                    st.success(f"Found {len(st.session_state.search_results)} models.")
                    for m in st.session_state.search_results:
                        with st.expander(f"{m['display']} ({m['source']})"):
                            st.write(f"**Provider:** {m['provider']}")
                            if m.get("context") != "Unknown":
                                st.write(f"**Context:** {m.get('context')}")
                                st.write(f"**Cost:** ${m.get('cost_prompt')}/1M prompt")
                            
                            # Check if already added
                            is_added = any(p["name"] == m["display"] for p in st.session_state.custom_providers)
                            
                            if is_added:
                                st.success("✅ Added")
                            else:
                                if st.button("Test & Add", key=f"add_search_{m['name']}_{m['source']}"):
                                    with st.status(f"Verifying {m['name']}...") as status:
                                        # Verify based on source
                                        if m["source"] == "g4f":
                                            success, msg = asyncio.run(verify_model(m['name'], "g4f"))
                                            ptype = "g4f_discovered"
                                            base_url = ""
                                            api_key = ""
                                            template = "Custom"
                                        elif m["source"] == "OpenRouter":
                                            success, msg = asyncio.run(verify_model(m['name'], "OpenRouter", api_key=or_key_search))
                                            ptype = "OpenRouter" # Or custom type if needed
                                            base_url = "https://openrouter.ai/api/v1"
                                            api_key = or_key_search
                                            template = "OpenRouter"
                                        else:
                                            success, msg = False, "Unknown source"

                                        if success:
                                            status.update(label="✅ Verified!", state="complete")
                                            new_p = {
                                                "name": m["display"],
                                                "api_key": api_key,
                                                "base_url": base_url,
                                                "model": m["name"],
                                                "template": template,
                                                "type": ptype
                                            }
                                            st.session_state.custom_providers.append(new_p)
                                            save_providers(st.session_state.custom_providers)
                                            st.success(f"Added {m['display']}!")
                                            st.rerun()
                                        else:
                                            status.update(label="❌ Failed", state="error")
                                            st.error(msg)
                elif search_query and not st.session_state.search_results:
                    st.warning("No models found.")
                
                elif st.session_state.get("discovered_ollama_models") == []:
                     st.warning("No models found. Ensure Ollama is running.")

    st.title("🤖 AI Nexus")
    st.markdown("Ask one question. Get the combined wisdom of selected AI models, synthesized by your local AI.")

    # Input Section
    with st.container():
        query = st.text_area("Enter your question here...", height=100)
        ask_button = st.button("🚀 Ask the Swarm")

    if ask_button and query:
        # Build active providers list
        active_providers = []
        
        # Map friendly names to internal functions
        if "ChatGPT (OpenAI)" in selected_online_models:
            active_providers.append({"name": "ChatGPT", "type": "online", "func": fetch_openai})
        if "Claude (Anthropic)" in selected_online_models:
            active_providers.append({"name": "Claude", "type": "online", "func": fetch_anthropic})
        if "Gemini (Google)" in selected_online_models:
            active_providers.append({"name": "Gemini", "type": "online", "func": fetch_gemini})
        if "Perplexity" in selected_online_models:
            active_providers.append({"name": "Perplexity", "type": "online", "func": fetch_perplexity})
        
        # Add Custom Providers
        for custom_provider in st.session_state.custom_providers:
            if custom_provider["name"] in selected_online_models:
                # Create a partial function or wrapper for the custom provider
                # We need to capture the specific config for this provider
                # Check type
                if custom_provider.get("type") == "g4f_discovered":
                    def make_g4f_fetcher(cp):
                        async def fetcher(q, c):
                            # fetch_g4f doesn't use client, it uses g4f internal
                            return await fetch_g4f(q, cp["model"], cp["name"])
                        return fetcher
                    
                    active_providers.append({
                        "name": custom_provider["name"],
                        "type": "g4f_discovered",
                        "func": make_g4f_fetcher(custom_provider)
                    })
                elif custom_provider.get("type") == "ollama_discovered":
                    def make_ollama_disc_fetcher(cp):
                        async def fetcher(q, c):
                            try:
                                # Use the stored base_url
                                url = f"{cp['base_url']}/api/generate"
                                resp = await c.post(
                                    url,
                                    json={"model": cp["model"], "prompt": q, "stream": False},
                                    timeout=60.0
                                )
                                resp.raise_for_status()
                                return resp.json()["response"]
                            except Exception as e:
                                return f"Error ({cp['name']}): {str(e)}"
                        return fetcher

                    active_providers.append({
                        "name": custom_provider["name"],
                        "type": "ollama_discovered",
                        "func": make_ollama_disc_fetcher(custom_provider)
                    })
                else:
                    # Generic OpenAI Compatible
                    def make_custom_fetcher(cp):
                        async def fetcher(q, c):
                            return await fetch_generic_openai_compatible(
                                q, cp["api_key"], cp["base_url"], cp["model"], cp["name"], c
                            )
                        return fetcher
                    
                    active_providers.append({
                        "name": custom_provider["name"],
                        "type": "custom",
                        "func": make_custom_fetcher(custom_provider)
                    })
        
        # Add Distributed Ollama Models
        for m in selected_ollama_models:
            # We need a custom fetcher for remote nodes too, or update fetch_ollama
            # Let's update fetch_ollama to take a URL, or create a wrapper here.
            # Since fetch_ollama is in llm_providers.py and hardcoded to localhost, 
            # we should probably create a dynamic fetcher here similar to custom providers.
            
            def make_ollama_fetcher(model_obj):
                async def fetcher(q, c):
                    try:
                        resp = await c.post(
                            model_obj["url"],
                            json={"model": model_obj["model"], "prompt": q, "stream": False},
                            timeout=60.0
                        )
                        resp.raise_for_status()
                        return resp.json()["response"]
                    except Exception as e:
                        return f"Error ({model_obj['display']}): {str(e)}"
                return fetcher

            active_providers.append({
                "name": m["display"],
                "type": "ollama_distributed",
                "func": make_ollama_fetcher(m)
            })

        if not active_providers:
            st.warning("Please select at least one model in the sidebar.")
        else:
            # Status Container for Detailed Progress
            status_box = st.status("Processing...", expanded=True)
            
            # Run async loop
            async def run_process():
                responses = {}
                
                async with httpx.AsyncClient() as client:
                    tasks = []
                    
                    # 1. Retrieve Context (Memory)
                    retrieved_context = ""
                    if MEMORY_AVAILABLE and enable_context:
                        status_box.write("🧠 Retrieving relevant memory...")
                        try:
                            retrieved_context = retrieve_context(query)
                            if retrieved_context:
                                status_box.write("✅ Memory retrieved")
                        except Exception as e:
                            status_box.write(f"⚠️ Memory retrieval failed: {e}")

                    # Create tasks
                    for provider in active_providers:
                        status_box.write(f"⏳ Querying {provider['name']}...")
                        # All providers now have a 'func' wrapper
                        coro = provider["func"](query, client)
                        
                        # Wrap coroutine to return name + result
                        async def task_wrapper(name, c):
                            try:
                                res = await c
                                return name, res
                            except Exception as e:
                                return name, f"Error: {str(e)}"
                                
                        tasks.append(task_wrapper(provider["name"], coro))
                    
                    # Execute tasks as they complete
                    for future in asyncio.as_completed(tasks):
                        name, result = await future
                        responses[name] = result
                        status_box.write(f"✅ {name} finished")
                
                status_box.update(label="All queries complete! Synthesizing...", state="running")
                
                # 2. Synthesize with offline model (passing context and target)
                # Determine target synthesizer
                target_url = "http://localhost:11434/api/generate"
                target_model = "llama3"
                
                if synthesizer_model_option:
                    target_url = synthesizer_model_option["url"]
                    target_model = synthesizer_model_option["model"]
                    status_box.write(f"🧠 Synthesizing with {synthesizer_model_option['display']}...")
                
                final_answer = await synthesize_responses(
                    query, 
                    responses, 
                    context=retrieved_context,
                    target_url=target_url,
                    target_model=target_model
                )
                
                # 3. Save to Memory (Learning)
                if MEMORY_AVAILABLE and enable_learning:
                    status_box.write("💾 Saving knowledge to memory...")
                    try:
                        # We save the synthesized answer as the "expert" answer
                        add_to_memory(query, final_answer, "Synthesized")
                        status_box.write("✅ Knowledge saved")
                    except Exception as e:
                        status_box.write(f"⚠️ Failed to save memory: {e}")
                
                status_box.update(label="Processing Complete!", state="complete", expanded=False)
                return responses, final_answer

            # Streamlit runs sync by default, so we use asyncio.run
            try:
                responses, final_answer = asyncio.run(run_process())
                
                # Display Final Answer
                st.markdown("### ✨ Synthesized Answer")
                st.markdown(f'<div class="final-answer">{final_answer}</div>', unsafe_allow_html=True)
                
                st.divider()
                
                # Display Individual Responses (Collapsible)
                with st.expander("Show/Hide Individual Model Perspectives", expanded=False):
                    st.markdown("### 🧠 Individual Model Perspectives")
                    
                    # Dynamic Grid Layout
                    cols = st.columns(2) # 2 columns grid
                    
                    for i, (provider, response) in enumerate(responses.items()):
                        col = cols[i % 2]
                        with col:
                            st.markdown(f"#### {provider}")
                            st.markdown(f'<div class="provider-card">{response}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:
        if ask_button:
            st.warning("Please enter a question first.")

# --- Main Router ---
if st.session_state.page == "landing":
    render_landing_page()
elif st.session_state.page == "app":
    render_desktop_app()
elif st.session_state.page == "chat":
    render_web_chat()
