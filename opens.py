import paramiko
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

ip = os.getenv("EC2_IP_ADDRESS")
browser_ip = os.getenv("BROWSER_IP_ADDRESS")
username = os.getenv("EC2_USERNAME")

def opens(id):
    if id != '':    
        date = datetime.now()
        
        key = paramiko.RSAKey.from_private_key_file("SSHkey.pem")

        transport = paramiko.Transport((ip, 22))
        transport.connect(username=username, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        log_file = sftp.open('/var/log/nginx/access.log', 'r')

        log_data = str(log_file.read())

        log_file.close()
        transport.close()
        
        if str(date)[11:16] == "09:01" or str(date) == "09:00":
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,username=username, pkey=key)
            stdin, stdout, stderr = ssh.exec_command("sudo truncate -s 0 /var/log/nginx/access.log")
        if browser_ip is not None:
            if browser_ip in log_data and browser_ip != "":
                index = log_data.find(browser_ip)
                log_data = log_data[:index] + log_data[index + len(browser_ip) + 60 + len(id):]
        if id in log_data:
            return 1
    return 0