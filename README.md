<h1>Python Cold Email Automation with Open & Reply tracking.</h1>

<h2>What you need:</h2>
Amazon EC2 with nginx with a .pem ssh named SSHkey.pem on your root,
sheetAuth.json (sheet authentication, the information will be stored there) to a copy of this https://docs.google.com/spreadsheets/d/1IuEbKSy8YDeLrlz0ngSyRuTjIQoC_BEiEqjS7ZuCGCI/edit?usp=sharing,
<h3>environment</h3><li>
PASSWORD_[email in sheets] (your email password)
EMAIL_[email in sheets] (your email)
USER (what you want to show on your email name to the receiver)
VALID_VERIFICATION_KEY (key for quickemailverification api)
EC2_IP_ADDRESS (ec2 ip address)
EC2_USERNAME (ec username, normaly is "ubuntu")
BROWSER_IP_ADDRESS (the ip address the email gives to you so you can exclude the emails views by you)
TIME_ZONE (your time zone in pytz format)
SECRET_LOCATION = '' (location where your SSHkey.pem and sheetAuth.json are, " " means root)</li>

<h2>How to use it</h2>    
soon
