# 📧 Python Cold Email Automation with Open & Reply Tracking

This web app automates **cold email campaigns** with **open & reply tracking**.  
It integrates with **Google Sheets** for campaign management, supports **multiple senders**, and enforces **daily sending limits** per account.

---

## 📊 Google Sheets Integration

A Google Sheets document is used to control email sending and track statistics.  
You can get a copy of the template [here](https://docs.google.com/spreadsheets/d/1IuEbKSy8YDeLrlz0ngSyRuTjIQoC_BEiEqjS7ZuCGCI/edit?usp=sharing).

- Add your email addresses in the cells `O9`, `P9`, `Q9`, etc.
- **From** → the sender’s email.  
- **Email** → the recipient’s email.  
- **Preset** → template number (from the *Templates* sheet, starting at `0`).  
  - Example: `E0` = first email, `E1` = second email, etc.  
- **E1 Date** → delay (in days) before sending the follow-up if there was no reply.  
- **Custom Variables** → placeholders for personalization (use `{var}` format).  

The sheet automatically calculates averages and performance metrics for each sender.

---

## ⚙️ Requirements

You’ll need:

- **Amazon EC2 instance** with Nginx hosting `pixel.png`  
- **SSH key** (`SSHkey.pem`)  
- **Google Sheets authentication** (`sheetAuth.json`) linked to your sheet copy  
- **[quickemailverification.com](https://quickemailverification.com/)** account (to validate emails and avoid spam flags)  

---

## 🌍 Environment Variables

Create a `.env` file with the following values:

```ini
# Email credentials (for each sender listed in row 9 of the sheet)
PASSWORD_[email] = your-email-password
EMAIL_[email] = your-email-address

# Display name for outgoing emails
USER = Your Name

# QuickEmailVerification API key
VALID_VERIFICATION_KEY = your-verification-key

# EC2 server details
EC2_IP_ADDRESS = your-ec2-ip
EC2_USERNAME = ubuntu   # usually "ubuntu"

# Browser & timezone
BROWSER_IP_ADDRESS = your-browser-ip
TIME_ZONE = Europe/Lisbon  # example, must be pytz format

# Location of your keys
SECRET_LOCATION = ''  # path where SSHkey.pem and sheetAuth.json are stored ("" = root)
```
---

## 🚀 Installation & Usage

Clone the repository
```bash
git clone https://github.com/desantesway/EmailBot.git
```
Go to the directory
```bash
cd EmailBot
```
Install the libraries
```bash
pip install -r requirements.txt
```
Then, create an .env with the values above and run your app!





