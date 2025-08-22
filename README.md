<h1>Python Cold Email Automation with Open & Reply tracking.</h1>

This web app reads and registers info in a google sheets, it supports multiple email senders and how much each can send per day.

## Google Sheets

In the sheets with the link bellow, you will get all the averages of every email calculated for you. 

To use it, you can put your email adresses in the cells O9, P9, Q9, etc.

From it's the email you want to send from, email is the one that receives the email, preset is the number of the email preset in the Templates page starting from 0, E0 mean first email sent, E1 means the second, etc.

On the right side E1 Date, means how long in days to send E1 after E0 if the email got no response back, then the same for others but the email is sent after the days provided the previous email.

Under custom variables that's where you can fill the custom variables you want to put in your email presets - all variables should be in this format {var}

<h2>What you need:</h2>
<p>Amazon EC2 with nginx with a .pem ssh named SSHkey.pem,</p>
<p>sheetAuth.json (sheet authentication, the information will be stored there) to a <a href="https://docs.google.com/spreadsheets/d/1IuEbKSy8YDeLrlz0ngSyRuTjIQoC_BEiEqjS7ZuCGCI/edit?usp=sharing">copy of this</a>,</p>
<p>quickemailverification.com account (if you send e-mails to a non existent account you can be flagged as spam).</p>
<h3>Environment</h3>
<li>PASSWORD_[email in sheets at line 9] (your email password)</li>
<li>EMAIL_[email in sheets at line 9] (your email)</li>
<li>USER (what you want to show on your email name to the receiver)</li>
<li>VALID_VERIFICATION_KEY (key for quickemailverification api)</li>
<li>EC2_IP_ADDRESS (ec2 ip address)</li>
<li>EC2_USERNAME (ec username, normaly is "ubuntu")</li>
<li>BROWSER_IP_ADDRESS (the ip address the email gives to you so you can exclude the emails views by you)</li>
<li>TIME_ZONE (your time zone in pytz format)</li>
<li>SECRET_LOCATION = '' (location where your SSHkey.pem and sheetAuth.json are, "" means root)</li>

<h2>How to use it</h2> 

Clone the repository

    git clone https://github.com/desantesway/EmailBot.git

Go to the directory

    cd EmailBot

Install the libraries

    pip install -r requirements.txt

Then, create an .env with the values above and run your app!



