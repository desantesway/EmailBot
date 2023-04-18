<h1>Python Cold Email Automation with Open & Reply tracking.</h1>

<h2>What you need:</h2>
Amazon EC2 with nginx with a .pem ssh named SSHkey.pem on your root,
sheetAuth.json (sheet authentication, the information will be stored there) to a copy of this https://docs.google.com/spreadsheets/d/1IuEbKSy8YDeLrlz0ngSyRuTjIQoC_BEiEqjS7ZuCGCI/edit?usp=sharing,
quickemailverification.com account (if you send e-mails to a non existent account you can be flagged as spam).
<h3>Environment</h3>
<li>PASSWORD_[email in sheets] (your email password)</li>
<li>EMAIL_[email in sheets] (your email)</li>
<li>USER (what you want to show on your email name to the receiver)</li>
<li>VALID_VERIFICATION_KEY (key for quickemailverification api)</li>
<li>EC2_IP_ADDRESS (ec2 ip address)</li>
<li>EC2_USERNAME (ec username, normaly is "ubuntu")</li>
<li>BROWSER_IP_ADDRESS (the ip address the email gives to you so you can exclude the emails views by you)</li>
<li>TIME_ZONE (your time zone in pytz format)</li>
<li>SECRET_LOCATION = '' (location where your SSHkey.pem and sheetAuth.json are, " " means root)</li>

<h2>How to use it</h2>    
soon
