import streamlit as st
import asyncio
import httpx
from llm_providers import fetch_openai, fetch_anthropic, fetch_gemini, fetch_perplexity, fetch_ollama, fetch_generic_openai_compatible, fetch_g4f
from offline_model import synthesize_responses
import qrcode
import socket
import io
try:
    from agents.memory import add_to_memory, retrieve_context, export_dataset
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

from agents.discovery import get_g4f_models, get_openrouter_models, verify_model

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Page Config
st.set_page_config(
    page_title="AI Nexus",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State
import json
import os

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

if "custom_providers" not in st.session_state:
    st.session_state.custom_providers = load_providers()

if "network_nodes" not in st.session_state:
    st.session_state.network_nodes = [] # List of {"name": "PC1", "url": "http://..."}

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
        
        disc_mode = st.radio("Source", ["Free Web (g4f)", "OpenRouter (API)"], horizontal=True)
        
        if disc_mode == "Free Web (g4f)":
            st.markdown("### Popular Free Models")
            if st.button("Scan for Models"):
                with st.spinner("Scanning..."):
                    models = asyncio.run(get_g4f_models())
                    for m in models:
                        col_name, col_act = st.columns([3, 1])
                        col_name.text(m["display"])
                        if col_act.button("Test & Add", key=f"add_{m['name']}"):
                            with st.status(f"Verifying {m['name']}...") as status:
                                success, msg = asyncio.run(verify_model(m['name'], "g4f"))
                                if success:
                                    status.update(label="✅ Verified!", state="complete")
                                    # Add to custom providers
                                    new_p = {
                                        "name": m["display"],
                                        "api_key": "",
                                        "base_url": "",
                                        "model": m["name"],
                                        "template": "Custom" # Handled by generic fetcher if we tweak it, or we need a specific g4f handler
                                    }
                                    # NOTE: Currently app.py generic fetcher assumes OpenAI format. 
                                    # We need to handle 'g4f' type in the main loop or wrap it.
                                    # For now, let's mark it as special type.
                                    new_p["type"] = "g4f_discovered"
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
