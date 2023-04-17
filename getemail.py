from datetime import date

def emailtemp(emails_values):
    present = date.today()
    i = 0
    for j in range(14,26):
        if emails_values[8][j] != '':
            if emails_values[9][j] != str(present):
                emails_values[9][j] = str(present)
                emails_values[10][j] = 0
            if emails_values[10][j] == '':
                emails_values[10][j] = 0
            i+= 1
        else:
            break
    if i == 0:
        return -1
    total = 0
    x = 0
    for j in range(14,14+i):
        if emails_values[11][j] != '':
            total += int(emails_values[11][j])
            x += 1
    if total != int(emails_values[2][25]):
        for j in range(14,14+i):
            if total <= int(emails_values[2][25]):
                if emails_values[11][j] == '':
                    emails_values[11][j] = (int(emails_values[2][25]) - total) / (i - x)
            else:
                emails_values[11][j] = int(emails_values[2][25])/ i
    return i

def checkemail(emails_values, i):
    i = emailtemp(emails_values)
    if i == -1:
        return -2
    for j in range(14,14+i):
        if emails_values[8][j] == emails_values[i][1]:
            if int(emails_values[10][j]) >= int(emails_values[11][j]):
                return -1
    return 1

def addemail(emailss, emails_values):
    i = emailtemp(emails_values)
    if i == -1:
        return -1
    for j in range(14,14+i):
            emails_values[10][j] = int(emails_values[10][j]) + 1
            break

def getemail(emails_values):
    email = ""
    i = emailtemp(emails_values)
    if i == -1:
        return -1
    for j in range(14,14+i):
        if int(emails_values[10][j]) < int(emails_values[11][j]) and email == "":
            email = emails_values[8][j]
    return email