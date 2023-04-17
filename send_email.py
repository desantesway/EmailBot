import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import imaplib
from dotenv import load_dotenv
from datetime import datetime
import uuid

PORT = 587
EMAIL_SERVER = 'imap.gmail.com'

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables

user = os.getenv("USER")
ip = os.getenv("EC2_IP_ADDRESS")

def gen_id():
    return uuid.uuid4()

def send_email(i, ENum, templates_values, emails_values, email):

    if (emails_values[i][3] != ''):
        preset = int(emails_values[i][3]) + 2
        if preset > len(templates_values) or preset < 2:
            emails_values[i][10] += " | " + '(Preset does not exist: ' + 'E' + str(ENum) + ')'
            emails_values[i][3] = ""
            print('That preset does not exist')
            return -1

        if(templates_values[preset][1] == ''):
            emails_values[i][10] += " | " + '(No Subject: ' + 'E' + str(ENum) + ')'
            print("There's no subject")
            return -1
        if(templates_values[preset][2] == '' and templates_values[preset][3] == ''):
            emails_values[i][10] += " | " + '(No Body & Html: ' + 'E' + str(ENum) + ')'
            print("There's no body neither html")
            return -1
        
        if(ENum in [0,1,2,3]):
            weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            week_day = weekDays[datetime.now().weekday()]
            html_body = templates_values[preset][(ENum*3) + 3]
            content = templates_values[preset][(ENum*3) + 2]
            subject = templates_values[preset][(ENum*3) + 1]
            vars_dict = {}
            for j in range(19,len(emails_values[0])):
                if emails_values[13][j] != '':
                    if emails_values[i][j] != '':
                        vars_dict[str(emails_values[13][j])] = str(emails_values[i][j])
            try:
                id = "Replies"
                while(id=="Replies"):
                    temp = str(gen_id())
                    if not temp in emails_values:
                        id = temp
                html_body = html_body.format(week_day = week_day, **vars_dict)
                html_body = '<html><body>' + html_body + f'<img src="http://{ip}/images/pixel.png?id={id}/" style="display:none">' + templates_values[2][25] + '</body></html>'
                subject = subject.format(week_day = week_day, **vars_dict)
                content = content.format(week_day = week_day, **vars_dict)
            except KeyError as e:
                missing_variable = str(e).strip("'")
                emails_values[i][10] += " | " + '(Variable: "' + missing_variable + '" is missing: ' + 'E' + str(ENum) + ')'                
                print(f"The variable '{missing_variable}' is missing from your sheet")
                return -1
            emails_values[i][15+ENum] = id
            sender_email = os.getenv(f"EMAIL_{email}")
            password_email = os.getenv(f"PASSWORD_{email}")
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = formataddr((user, f"{sender_email}"))
            msg["To"] = emails_values[i][2]
            msg["BCC"] = sender_email
            msg.set_content(content)
            msg.add_alternative( html_body , subtype='html')
            
            server = imaplib.IMAP4_SSL(EMAIL_SERVER)
            with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
                server.starttls()
                server.login(sender_email, password_email)
                server.sendmail(sender_email, emails_values[i][2], msg.as_string())
        else:
            emails_values[i][10] += " | " + '(No Follow-up E-mail: ' + 'E' + str(ENum) + ')'
            print("There's no Follow-up E-mail with that number") 
            return -1   

    else:
        emails_values[i][10] += " | " + '(No Preset: ' + 'E' + str(ENum) + ')'
        print("You did not specified the Preset")
        return -1

