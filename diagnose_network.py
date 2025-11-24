import socket
import os
import sys
import qrcode
import time

def get_local_ip():
    try:
        # Connect to an external server to get the interface IP used for internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

def print_banner(text):
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)

def main():
    print_banner("AI Nexus Network Diagnostic Tool")
    
    local_ip = get_local_ip()
    print(f"📍 Local Network IP: {local_ip}")
    print(f"🏠 Loopback IP:      127.0.0.1")
    print("-" * 60)
    
    # Check API Port
    api_port = 8000
    api_open_local = check_port("127.0.0.1", api_port)
    api_open_lan = check_port(local_ip, api_port)
    
    print(f"🔍 Checking API Server (Port {api_port})...")
    if api_open_local:
        print(f"   ✅ Running on localhost:{api_port}")
    else:
        print(f"   ❌ NOT detected on localhost:{api_port} (Is uvicorn running?)")
        
    if api_open_lan:
        print(f"   ✅ Accessible via LAN: http://{local_ip}:{api_port}")
    else:
        print(f"   ⚠️  NOT accessible via LAN IP (Check firewall or binding)")

    print("-" * 60)

    # Check Streamlit Port
    st_port = 8501
    st_open_local = check_port("127.0.0.1", st_port)
    st_open_lan = check_port(local_ip, st_port)
    
    print(f"🔍 Checking Streamlit App (Port {st_port})...")
    if st_open_local:
        print(f"   ✅ Running on localhost:{st_port}")
    else:
        print(f"   ❌ NOT detected on localhost:{st_port} (Is streamlit running?)")
        
    if st_open_lan:
        print(f"   ✅ Accessible via LAN: http://{local_ip}:{st_port}")
    else:
        print(f"   ⚠️  NOT accessible via LAN IP (Check firewall or binding)")
        
    print("-" * 60)
    
    if api_open_lan and st_open_lan:
        url = f"http://{local_ip}:{st_port}"
        print(f"📱 MOBILE ACCESS URL: {url}")
        print("   (Scan the QR code below with your phone)")
        
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.print_ascii()
    else:
        print("❌ Cannot generate mobile link. Ensure both API and Streamlit are running.")
        print("   Run: uvicorn api:app --host 0.0.0.0 --port 8000")
        print("   Run: streamlit run app.py")

if __name__ == "__main__":
    main()
