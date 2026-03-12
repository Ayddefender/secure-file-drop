import streamlit as st
import uuid
import hashlib
from base64 import urlsafe_b64encode
from crypto_utils import encrypt_file, decrypt_file
import time

# ---------- PASSWORD → KEY FUNCTION ----------
def password_to_key(password: str):
    """Convert a password into a Fernet-compatible key using SHA-256."""
    hashed = hashlib.sha256(password.encode()).digest()
    return urlsafe_b64encode(hashed)

# ---------- GLOBAL STORAGE ----------
@st.cache_resource
def get_storage():
    return {}

storage = get_storage()

# ---------- SESSION STATE SETUP ----------
if "activity_log" not in st.session_state:
    st.session_state["activity_log"] = []

if "stats" not in st.session_state:
    st.session_state["stats"] = {
        "uploads": 0,
        "downloads": 0,
        "failed_attempts": 0,
        "total_data_mb": 0.0,
    }

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = set()

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="🔒 Secure File Drop", layout="centered")

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align:center;color:#1E90FF;'>🔒 Secure File Drop</h1>
    <p style='text-align:center;color:gray;'>Encrypt, share, and download files securely with password protection and one-time links.</p>
    <hr style='border:1px solid #1E90FF;'>
    """,
    unsafe_allow_html=True,
)

# Keep last link in session
if "last_link" not in st.session_state:
    st.session_state["last_link"] = ""

# ---------- LOG FUNCTION ----------
def log_event(message):
    """Add timestamped message to activity log."""
    timestamp = time.strftime("%H:%M:%S")
    st.session_state["activity_log"].insert(0, f"🕒 [{timestamp}] {message}")

# ===============================================================
# 📤 STEP 1 – UPLOAD & ENCRYPT
# ===============================================================
st.subheader("📤 Step 1 – Upload and Generate Secure Link")
st.write("Upload your file, set a password, and generate a one-time download link.")

uploaded_file = st.file_uploader("Choose a file", type=None)
password = st.text_input("Set a password for this file (share it securely):", type="password")

if uploaded_file is not None and password:
    try:
        # Check if this exact file has already been uploaded this session
        if uploaded_file.name not in st.session_state["uploaded_files"]:
            key = password_to_key(password)
            encrypted_data = encrypt_file(uploaded_file.read(), key)
            link_id = str(uuid.uuid4())

            storage[link_id] = {
                "data": encrypted_data,
                "filename": uploaded_file.name,
                "used": False,
            }

            # Update stats only once per new upload
            st.session_state["uploaded_files"].add(uploaded_file.name)
            st.session_state["stats"]["uploads"] += 1
            st.session_state["stats"]["total_data_mb"] += len(encrypted_data) / (1024 * 1024)
            log_event(f"File '{uploaded_file.name}' encrypted successfully and link generated.")

            st.session_state["last_link"] = link_id
            st.success("✅ File encrypted successfully!")
            st.info("Share the following Link ID with your recipient (works only once):")
            st.code(link_id, language="text")
            st.caption("⚠️ The recipient will also need the password you set above.")
        else:
            st.warning(f"File '{uploaded_file.name}' has already been uploaded this session.")
    except Exception as e:
        st.error(f"Encryption failed: {e}")
        log_event(f"⚠️ Encryption failed for file '{uploaded_file.name}': {e}")

# ===============================================================
# 📥 STEP 2 – DOWNLOAD & DECRYPT
# ===============================================================
st.write("---")
st.subheader("📥 Step 2 – Retrieve and Download File")
st.write("Paste the Link ID and enter the password to decrypt and download the file (works only once).")

link_input = st.text_input("🔑 Enter Link ID")
download_password = st.text_input("Enter password to unlock file:", type="password")

if st.button("Retrieve File"):
    if not link_input or not download_password:
        st.warning("Please provide both the Link ID and password.")
    elif link_input not in storage:
        st.error("❌ Invalid Link ID.")
        st.session_state["stats"]["failed_attempts"] += 1
        log_event(f"Invalid or unknown Link ID '{link_input}' entered.")
    else:
        file_info = storage[link_input]
        if file_info["used"]:
            st.error("⚠️ This link has already been used and has expired.")
            log_event(f"Attempted reuse of expired link '{link_input}'.")
        else:
            try:
                key = password_to_key(download_password)
                decrypted_data = decrypt_file(file_info["data"], key)
                st.download_button(
                    label=f"⬇️ Download {file_info['filename']}",
                    data=decrypted_data,
                    file_name=file_info["filename"],
                    mime="application/octet-stream",
                )
                file_info["used"] = True
                st.success("✅ File ready for download. This link will now expire.")
                st.session_state["stats"]["downloads"] += 1
                log_event(f"File '{file_info['filename']}' downloaded and link expired.")
            except Exception:
                st.error("❌ Incorrect password or file could not be decrypted.")
                st.session_state["stats"]["failed_attempts"] += 1
                log_event(f"Failed decryption attempt for link '{link_input}' (wrong password).")

# ===============================================================
# 📊 SESSION SUMMARY & ACTIVITY LOG
# ===============================================================
st.write("---")
st.subheader("📊 Session Summary")
stats = st.session_state["stats"]
st.write(
    f"""
    - Files uploaded: {stats['uploads']}
    - Files downloaded: {stats['downloads']}
    - Failed attempts: {stats['failed_attempts']}
    - Total data processed: {stats['total_data_mb']:.2f} MB
    """
)

st.write("---")
st.subheader("📝 Live Activity Log")
if st.session_state["activity_log"]:
    for event in st.session_state["activity_log"]:
        st.write(event)
else:
    st.info("No activity yet. Actions will appear here as you use the app.")
