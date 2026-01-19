import subprocess
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURATION (FILL THESE IN) ---
BLACKLIST = ['tor', 'virtualbox', 'nmap']
LOG_FILE = "installed_software.txt"

# Email Settings
SENDER_EMAIL = "sender-email@gmail.com"        # Your Gmail
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"      # Your 16-char App Password
RECEIVER_EMAIL = "reciever-email@gmail.com"  # Who receives the alert
# -------------------------------------

def get_software_via_powershell():
    # ... (Same PowerShell logic as before) ...
    ps_command = r"""
    Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*, 
                     HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*, 
                     HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Select-Object DisplayName | 
    Format-Table -HideTableHeaders
    """
    try:
        result = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        software_list = []
        for line in result.stdout.splitlines():
            cleaned_line = line.strip()
            if cleaned_line and not cleaned_line.isspace():
                software_list.append(cleaned_line)
        return sorted(list(set(software_list)))
    except FileNotFoundError:
        return []

def send_email_alert(detected_app):
    """
    Sends an email listing ALL detected threats and attaches the log file.
    """
    print("📧 Preparing to send email alert...")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"🚨 SECURITY ALERT: {len(detected_app)} Blacklisted Apps Detected"
    
    # Create a bulleted list of the bad apps for the email body
    formatted_list = "\n".join([f"- {app}" for app in detected_app])
    
    body = f"""
    SECURITY MONITOR ALERT
    
    The following blacklisted applications were detected on the system:
    
    {formatted_list}
    
    --------------------------------------
    Please check the attached log file for the full list of installed software.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # 2. Attach the File
    try:
        with open(LOG_FILE, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        
        # Add header
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {LOG_FILE}",
        )
        msg.attach(part)
        
    except FileNotFoundError:
        print("Could not find the log file to attach.")
        return

    # 3. Login and Send
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("--- MONITORING STARTED ---")
    
    # We use this to prevent spamming emails every 60 seconds if the app stays installed
    alert_sent = False 

    while True:
        # 1. Scan
        apps = get_software_via_powershell()
        
        # 2. Save Log
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"--- SCAN TIME: {time.ctime()} ---\n")
            for app in apps:
                f.write(app + "\n")
        
        # 3. Check Blacklist
        found_threat = False
        detected_name = ""
        found_bad_apps = []

        for bad_app in BLACKLIST:
            for installed_app in apps:
                if bad_app.lower() in installed_app.lower():
                    if installed_app not in found_bad_apps:
                        found_bad_apps.append(installed_app)
                        print(f"🚨 FOUND THREAT: {installed_app}")
                
        # 4. ALERT LOGIC
        if found_bad_apps:
            # If we found threats and haven't emailed about them yet...
            if not alert_sent:
                send_email_alert(found_bad_apps)
                alert_sent = True  # Block further emails until system is clean
        else:
            # If system is clean, reset the status so we are ready for new threats later
            if alert_sent:
                print("✅ System clean. Resetting alert status.")
            alert_sent = False
            
        print(f"Scan complete. Found {len(found_bad_apps)} threats. Sleeping 60s...")
        time.sleep(60)
