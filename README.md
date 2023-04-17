<h1>Python Cold Email Automation with Open & Reply tracking.</h1>

<h2>What you need:</h2>
Amazon EC2 with nginx with a .pem ssh named SSHkey.pem on your root,<br>
sheetAuth.json (sheet authentication, the information will be stored there),<br>

.env (if locally) with:<br>
    PASSWORD_[email in sheets] (your email password)<br>
    EMAIL_[email in sheets] (your email)<br>
    USER (what you want to show on your email name to the receiver)<br>
    VALID_VERIFICATION_KEY (key for quickemailverification api)<br>
    EC2_IP_ADDRESS (ec2 ip address)<br>
    EC2_USERNAME (ec username, normaly is "ubuntu")<br>
    BROWSER_IP_ADDRESS (the ip address the email gives to you so you can exclude the emails views by you)<br>
    TIME_ZONE (your time zone in pytz format)<br>

To deploy on the internet I used detaspace with this in spacefile (complete the env: with the above variables):<br>
    v: 0<br>
    icon: ./icon.png<br>
    micros:<br>
    - name: cold-email<br>
        src: ./<br>
        engine: python3.9<br>
        primary: true<br>
        actions:<br>
        - id: "run_myapp"<br>
            name: "[TRACKED] Cold Email"<br>
            description: "Quykkdev - Tracked Cold Email Automation with smtp & Data Gather"<br>
            trigger: "schedule"<br>
            default_interval: "*/1440 * * * *"       <br>
        - id: "update_stats"<br>
            name: "Stats updater"<br>
            description: "Checks if any e-mail that you sent has new stats"<br>
            trigger: "schedule"<br>
            default_interval: "* * * * *"<br>
        presets:<br>
        env:<br>
            - name: TIME_ZONE<br>
            description: TIME_ZONE<br>
            default: 'Europe/Lisbon'    <br>  

