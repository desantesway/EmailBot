Python Cold Email Automation with Open & Reply tracking.

What you need:
Amazon EC2 with nginx with a .pem ssh named SSHkey.pem on your root,
sheetAuth.json (sheet authentication, the information will be stored there),

.env (if locally) with:
    PASSWORD_[email in sheets] (your email password)
    EMAIL_[email in sheets] (your email)
    USER (what you want to show on your email name to the receiver)
    VALID_VERIFICATION_KEY (key for quickemailverification api)
    EC2_IP_ADDRESS (ec2 ip address)
    EC2_USERNAME (ec username, normaly is "ubuntu")
    BROWSER_IP_ADDRESS (the ip address the email gives to you so you can exclude the emails views by you)
    TIME_ZONE (your time zone in pytz format)

To deploy on the internet I used detaspace with this in spacefile (complete the env: with the above variables):
    v: 0
    icon: ./icon.png
    micros:
    - name: cold-email
        src: ./
        engine: python3.9
        primary: true
        actions:
        - id: "run_myapp"
            name: "[TRACKED] Cold Email"
            description: "Quykkdev - Tracked Cold Email Automation with smtp & Data Gather"
            trigger: "schedule"
            default_interval: "*/1440 * * * *"       
        - id: "update_stats"
            name: "Stats updater"
            description: "Checks if any e-mail that you sent has new stats"
            trigger: "schedule"
            default_interval: "* * * * *"
        presets:
        env:
            - name: TIME_ZONE
            description: TIME_ZONE
            default: 'Europe/Lisbon'      

