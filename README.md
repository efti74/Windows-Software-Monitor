# Windows Software Monitor Script (`3_monitor.py`)

This Python script continuously monitors the installed software on a Windows computer. If it detects an application from a predefined "blacklist," it automatically sends an email alert.

## Features

-   Scans all user- and system-level installed programs.
-   Compares installed programs against a customizable blacklist.
-   Sends an immediate email notification if a blacklisted application is found.
-   Creates a log file (`installed_software.txt`) with a list of all detected software during each scan.
-   Prevents spamming by only sending one alert until the detected software is removed.

## Requirements

-   Windows Operating System
-   Python 3.x
-   A Gmail Account to be used for sending alerts.

---

## Step-by-Step Guide to Run the Script

### Step 1: Get a Gmail App Password

To send emails securely without exposing your main Google password, you need to generate a special 16-digit "App Password".

1.  Go to your Google Account: [myaccount.google.com](https://myaccount.google.com/).
2.  Navigate to the **Security** tab on the left.
3.  Scroll down to the "How you sign in to Google" section and click on **2-Step Verification**. You must have this enabled to create app passwords.
4.  At the very bottom, click on **App passwords**.
5.  Under "Select app," choose **Mail**.
6.  Under "Select device," choose **Windows Computer**.
7.  Click **Generate**.
8.  Google will display a 16-digit password. **Copy this password now.** You will not be able to see it again.

![Google App Password](https://i.imgur.com/gFG0Aan.png)

### Step 2: Configure the Script

Open the `3_monitor.py` file in a text editor and modify the `--- CONFIGURATION ---` section at the top.

```python
# --- CONFIGURATION (FILL THESE IN) ---
BLACKLIST = ['tor', 'virtualbox', 'nmap'] # Add or remove programs to monitor

# Email Settings
SENDER_EMAIL = "your-email@gmail.com"        # Your Gmail address
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"      # The 16-digit App Password from Step 1
RECEIVER_EMAIL = "destination-email@example.com"  # Where the alerts should be sent
# -------------------------------------
```

-   **`BLACKLIST`**: Customize this list with the names of applications you want to detect. The script will flag any installed program whose name contains one of these keywords (case-insensitive).
-   **`SENDER_EMAIL`**: Enter the Gmail address you generated the App Password for.
-   **`SENDER_PASSWORD`**: Paste the 16-digit App Password you copied in Step 1.
-   **`RECEIVER_EMAIL`**: Enter the email address where you want to receive the security alerts. This can be the same as the sender or a different one.

### Step 3: Run the Script

Once configured, you can run the script from your terminal or command prompt.

1.  Open a Command Prompt or PowerShell.
2.  Navigate to the directory where `3_monitor.py` is saved.
    ```sh
    cd "C:\Path\To\Your\Script"
    ```
3.  Run the script using Python.
    ```sh
    python 3_monitor.py
    ```

The script will start running and print its status to the console.

```
--- MONITORING STARTED ---
Scan complete. Found 0 threats. Sleeping 60s...
Scan complete. Found 0 threats. Sleeping 60s...
```

Leave the terminal window open. The script will run indefinitely, scanning your system every 60 seconds. If it finds a blacklisted application, it will print a threat alert to the console and send an email.

---

## Security Notice

This script stores your email credentials directly in the code. For personal use, this is a common convenience, but for more advanced or security-critical applications, it is highly recommended to use a more secure method for handling secrets, such as environment variables or a dedicated secrets management tool.
