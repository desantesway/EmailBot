from datetime import date, datetime, timedelta
from fastapi import FastAPI
from send_email import send_email
from num_replies import replies
import gspread
import imaplib
from pathlib import Path
from dotenv import load_dotenv
import os
from getemail import getemail
from getemail import addemail
from getemail import checkemail
from opens import opens
from opens import clean
import quickemailverification
import pytz

emailvalidkey = os.getenv("VALID_VERIFICATION_KEY")
client = quickemailverification.Client(emailvalidkey)

sheet = os.getenv("SECRET_LOCATION") + "sheetAuth.json"

app = FastAPI()

PORT = 587
EMAIL_SERVER = 'imap.gmail.com'

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

@app.get("/")
def run_myapp():
    return "[QUYKKDEV - SMTP] " + read_root()

def statsupdate(result,emails_values,rep):
    month = str(date.today())[5] + str(date.today())[6]
    if rep != 0:
        replies = rep
        sent = 0
    else:
        replies = result[0]
        j = 0
        if result[1] != " ":
            replies += result[1]
            j +=1
        sent = result[18+j]
        if result[19+j] != " ":
            sent += result[19+j]
        pos = 0
    for k in range(14,26):
        if month == emails_values[3][k]:
            pos = k
            break
    if emails_values[4][pos] == '':
        emails_values[4][pos] = 0
    if emails_values[5][pos] == '':
        emails_values[5][pos] = 0
    emails_values[4][pos] = int(emails_values[4][pos]) + int(sent)
    emails_values[5][pos] = int(emails_values[5][pos]) + int(replies)

def logout(imap):
    imap.close()
    imap.logout()

def login(email,password):
    imap = imaplib.IMAP4_SSL(EMAIL_SERVER)
    imap.login(email, password)
    return imap

def update(emails, emails_values):
    num = len(emails_values[0])-1
    def num_to_alpha(num):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num < 26:
            return alphabet[num]
        else:
            q, r = divmod(num, 26)
            return num_to_alpha(q-1) + alphabet[r]
    emails.batch_update([{
    'range': f'A1:{num_to_alpha(num)}{len(emails_values)}',
    'values': emails_values,
    }])  


def update_stats():

    print("Updating stats...")

    gc = gspread.service_account(filename=sheet)
    emails = gc.open("Emails").sheet1
    emails_values = emails.get_all_values()
    templates = gc.open("Emails").get_worksheet(1)
    templates_values = templates.get_all_values()

    i = 14
    ret = 0
    openz = 0
    while(i < len(emails_values)):
        if emails_values[i][2] == '':
            i+=1
            continue
        rep = 0
        open = 0
        if emails_values[i][1] != '' and emails_values[i][4] != 'REPLIED':
            if emails_values[i][4] != '' and emails_values[i][0] != "no":
                for enum in range(0,4):
                    if (emails_values[i][11+enum] == "" or emails_values[i][11+enum] == "no"):
                        if opens(emails_values[i][15+enum]) == 1: 
                            now_utc = datetime.now(pytz.utc)
                            tz = pytz.timezone(os.getenv("TIME_ZONE"))
                            now_eastern = now_utc.astimezone(tz)
                            emails_values[i][11+enum] = str(now_eastern)
                            month = int(str(date.today())[5:7]) + 13
                            if emails_values[6][month] == '':
                                emails_values[6][month] = 0
                            emails_values[6][month] = int(emails_values[6][month]) + 1
                            open += 1
                            openz += open
                    if emails_values[i][11+enum] == "":
                        emails_values[i][11+enum] = "no"
                email = os.getenv(f"EMAIL_{str(emails_values[i][1])}")
                password = os.getenv(f"PASSWORD_{str(emails_values[i][1])}")
                log = login(email,password)
                rep += replies(i, log, templates_values, emails_values)
                ret += rep
                logout(log)
            if(rep != 0):
                emails_values[i][4] = 'REPLIED'

        i+=1
    clean()
    statsupdate(f'''0 New replies and 0 Emails Sent.''',emails_values,ret)
    update(emails, emails_values)
    return f"{ret}#{openz}"

def is_valid_email(email):

    quickemailverification = client.quickemailverification()
    response = quickemailverification.verify(email)
    return response.body

def query_data_and_send_emails(templates_values, emails_values,rep):
    print("Starting E-mail Automation...")
    present = date.today()
    email_sent = 0
    errors = 0
    i = 14
    if(emails_values[2][23] != str(present) or emails_values[2][24] == ''):
        emails_values[2][24] = '0'
    while(i < len(emails_values) and int(emails_values[2][25]) > email_sent + int(emails_values[2][24])):
        if emails_values[i][2] == '':
            i+=1
            continue
        print('===========================')
        print(emails_values[i][2])

        if emails_values[i][0] == '':
            dict = is_valid_email(emails_values[i][2])
            if dict['safe_to_send'] == 'false':
                print('E-mail does not exist')
                emails_values[i][10] += " | " + '(E-mail does not exist' + ')'
                emails_values[i][0] = "no"
                i+=1
                errors += 1
                continue
            else:
                emails_values[i][0] = "yes"
        elif emails_values[i][0] == "no":
            print('E-mail does not exist')
            emails_values[i][10] += " | " + '(E-mail does not exist' + ')'
            emails_values[i][0] = "no"
            i+=1
            errors += 1            
            continue
        ret = 0
        if emails_values[i][4] == 'REPLIED':
            i += 1
            continue
        days = [-1,-1,-1]
        if not(emails_values[i][9] == ''):
            day = str(emails_values[i][9])
            datetype = datetime.strptime(day, "%Y-%m-%d").date()
            days[0] = str(datetype + timedelta(days=int(emails_values[2][19])))
            days[1] = str(datetype + timedelta(days=int(emails_values[2][19]) + int(emails_values[2][20])))
            days[2] = str(datetype + timedelta(days=int(emails_values[2][19]) + int(emails_values[2][20])+ int(emails_values[2][21])))
        if (emails_values[i][4] == '2' and str(present) >= days[2]):
            print('Sending E3 to', emails_values[i][3], "with email", emails_values[i][2])
            check = checkemail(emails_values, i)
            if check == -1:
                errors += 1
                emails_values[i][10] += " | " + '(Sender E-mail is on Daily Limit: ' + 'E3' + ')'
                i += 1
                continue  
            elif check == -2:
                errors += 1
                emails_values[i][10] += " | " + "(You don't have emails to send!" + ')'
                i += 1
                continue  
            ret = send_email(i, 3, templates_values, emails_values,emails_values[i][1])
            emails_values[i][4] = '3'
            email_sent += 1
            addemail(emails_values[i][1], emails_values)
        if (emails_values[i][4] == '1' and str(present) >= days[1]):
            print('Sending E2 to', emails_values[i][3], "with email", emails_values[i][2])
            check = checkemail(emails_values, i)
            if check == -1:
                errors += 1
                emails_values[i][10] += " | " + '(Sender E-mail is on Daily Limit: ' + 'E2' + ')'
                i += 1
                continue  
            elif check == -2:
                errors += 1
                emails_values[i][10] += " | " + "(You don't have emails to send!" + ')'
                i += 1
                continue       
            ret = send_email(i, 2, templates_values, emails_values,emails_values[i][1])              
            emails_values[i][4] = '2'
            email_sent += 1
            addemail(emails_values[i][1], emails_values)
        if (emails_values[i][4] == '0' and str(present) >= days[0]):
            print('Sending E1 to', emails_values[i][3], "with email", emails_values[i][2])
            check = checkemail(emails_values, i)
            if check == -1:
                errors += 1
                emails_values[i][10] += " | " + '(Sender E-mail is on Daily Limit: ' + 'E1' + ')'
                i += 1
                continue  
            elif check == -2:
                errors += 1
                emails_values[i][10] += " | " + "(You don't have emails to send!" + ')'
                i += 1
                continue                                   
            ret = send_email(i, 1, templates_values, emails_values,emails_values[i][1])              
            emails_values[i][4] = '1'
            email_sent += 1
            addemail(emails_values[i][1], emails_values)
        if (emails_values[i][4] == ''):
            print('Sending E0 to', emails_values[i][3], "with email", emails_values[i][2])
            if emails_values[i][1] == '':
                email = getemail(emails_values)
                if email == -1:
                    errors += 1
                    emails_values[i][10] += " | " + "(You don't have emails to send!" + ')'
                    i += 1
                    continue  
                else:
                    emails_values[i][1] = email
            check = checkemail(emails_values, i)
            if check == -1:
                errors += 1
                emails_values[i][10] += " | " + '(Sender E-mail is on Daily Limit: ' + 'E0' + ')'
                i += 1
                continue  
            elif check == -2:
                errors += 1
                emails_values[i][10] += " | " + "(You don't have emails to send!" + ')'
                i += 1
                continue       
            ret = send_email(i, 0, templates_values, emails_values, emails_values[i][1])              
            emails_values[i][9] = str(present)
            emails_values[i][4] = '0'
            emails_values[i][5] = "no"
            email_sent += 1
            addemail(emails_values[i][1], emails_values)
        if(ret == -1):
            email_sent -= 1
            errors += 1
            print(f"Error sending E{emails_values[i][4]} to {emails_values[i][2]}: {ret}")
            if(emails_values[i][4] == '0'):
                emails_values[i][4] = ''
            else:
                emails_values[i][4] = str(int(emails_values[i][4])-1)
        i+=1
    emails_values[2][24] = int(emails_values[2][24]) + email_sent
    emails_values[2][23] = str(present)
    if (int(emails_values[2][24]) == int(emails_values[2][25])):
        return f'''{rep} New replies and {email_sent} Emails Sent. {errors} Errors -- REACHED MAX DAILY E-MAILS -- '''
    return f'''{rep} New replies and {email_sent} Emails Sent. {errors} Errors'''

def read_root():
    time = str(datetime.now())
    if time[11:13] == "13" or "14":
        print("Welcome to Cold E-mail Automation!")
        ret = update_stats()
        ret = ret.split("#")

        gc = gspread.service_account(filename=sheet)
        emails = gc.open("Emails").sheet1
        emails_values = emails.get_all_values()
        templates = gc.open("Emails").get_worksheet(1)
        templates_values = templates.get_all_values()

        result = query_data_and_send_emails(templates_values, emails_values,int(ret[0]))
        statsupdate(result, emails_values,0)
        update(emails, emails_values)
        return ret[1] + " New opens, " + result