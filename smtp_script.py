import os
import smtplib
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, make_msgid

# Email credentials
EMAIL = "nihalsingh.teamkartkgp@gmail.com"
PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Put in the correct csv file name 
data = pd.read_csv("trainee.csv")

# Add your cc emails here
CC_EMAILS = [ "nihalsinghpubg357@gmail.com" ] 

# Definitions
BROCHURE_URL = "https://online.fliphtml5.com/TeamKart/1-Qt2Y/" 
YOUR_NAME = "Nihal Singh"
TK_LOGO_URL = "https://imgs.search.brave.com/sv9Okf6sV5Cmz8fLS-RwmJ4UnGHgVvUuETOSC-FziQQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly91Z2Mu/cHJvZHVjdGlvbi5s/aW5rdHIuZWUvZTYw/NTFhMTAtMWFiZC00/NWRhLWI4N2QtMzkz/ZDc5MmM5NjE2X3Rl/YW1rYXJ0LWVsZWN0/cmljLWxvZ28td2hp/dGUtc3EucG5nP2lv/PXRydWUmc2l6ZT1h/dmF0YXItdjNfMA"
YOUR_DEPARTMENT = "Department of Bioscience and Biotechnology"
YOUR_YEAR = "First"
YOUR_ROLE_TK = "Corporate and Public Relation Subsystem Trainee"
YOUR_CONTACT = "+91 9831647138"
YOUR_LINKED_IN = "linkedin.com/in/nihal-singh-628215377"
YOUR_FACEBOOK = "https://www.facebook.com/TeamKART/"

SUBJECT = "Greetings from Indian Institute of Technology Kharagpur."

HTML_HEAD = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 600px;
            margin: 0 auto;
        }}
        .content {{
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }}
        .highlight {{
            color: #E31E24;
            font-weight: bold;
        }}
        .links-section {{
            background-color: #f4f4f4;
            padding: 15px;
            border-left: 4px solid #E31E24;
            margin: 20px 0;
        }}
        .links-section a {{
            color: #E31E24;
            text-decoration: none;
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .footer {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>"""

# Template for the body
HTML_BODY = """
<body>
    <div class="content">
        <p>Dear <strong>{recipient_name}</strong>,</p>

        <p>My name is Nihal Singh, a first-year undergraduate student from the Department of Bioscience and Biotechnology at <strong>IIT Kharagpur</strong>, writing to you in my capacity as a Corporate and Public Relation Subsystem Trainee for our institute’s Formula Student team, <span class="highlight">TeamKART</span>.</p>
        
        <p>Active since 2008, TeamKART is a premier student engineering initiative focused on the complete design, manufacturing, and testing of Formula-style race cars. Over the years, the team has successfully built <strong>eight combustion vehicles</strong> and participated in <strong>three international and five national competitions</strong>. Our commitment to engineering excellence has earned us notable recognition, including a <strong>Top 10 finish at Formula Bharat 2023</strong> and <strong>3rd place in the Cost & Manufacturing Event</strong>.</p>

        <p>Building on our strong combustion foundation, TeamKART is now pioneering the future of mobility on campus. We recently <strong>manufactured our first electric vehicle project series</strong> (KE-1 and subsequent models) and are aggressively working on optimizing our custom powertrain and battery management systems for the upcoming competitive season.</p>

        <p>As a leading organization, <strong>{company}</strong>’s commitment to innovation strongly aligns with our vision of pushing the boundaries of student engineering. To execute a technically intensive project of this scale, we rely on the backing of industry leaders. We are actively seeking strategic partnerships in the form of:</p>
        <ul>
            <li><strong>Monetary Sponsorship:</strong> To fund the research, development, and logistical execution of our latest electric vehicle prototype.</li>
            <li><strong>In-Kind Support:</strong> Support through the provision of automotive components, raw materials, manufacturing equipment, software licenses, or specialized technical mentorship.</li>
        </ul>

        <p>Collaborating with TeamKART offers <strong>{company}</strong> premium branding real estate on our race car, team apparel, and digital platforms, alongside direct access to a dedicated talent pool of top-tier engineering students at IIT Kharagpur for potential recruitment.</p>

        <p>I would be highly grateful for the opportunity to share our official sponsorship brochure and explore how we can build a mutually beneficial partnership. Please let me know if you might be available for a brief call or meeting at your convenience.</p>

"""



HTML_TAIL="""
        <p><strong>Kindly refer to:</strong></p>
        <div class="links-section">
            <a href="{brochure_link}">Our Sponsorship Brochure</a>
            <a href="http://www.teamkart.org/">Our Team's Website</a>
            <a href="https://youtube.com/@teamkart3652">15 Years of TeamKART's Combustion Legacy</a>
            <a href="https://www.instagram.com/team.kart/">Our Instagram Handle</a>
            <a href="https://www.facebook.com/teamkart/">Facebook Page</a>
        </div>

        <div class="footer">
            <p>Thank you for your time and consideration.</p>
            <p>Warm regards,</p>
            <table style="border-collapse: collapse; font-family: Arial, sans-serif;">
                <tr>
                    <td style="padding-right: 15px;">
                        <img src="{tk_logo_url}" width="100" style="display: block;">
                    </td>
                    <td style="border-left: 2px solid #E31E24; padding: 0;"></td>
                    <td style="padding-left: 15px; line-height: 1.4; font-size: 10pt;">
                        <span style="font-weight: bold; font-size: 11pt;">{your_name}</span><br>
                        {your_year}-Year Undergraduate Student<br>
                        {your_department}<br>
                        {your_role}, TeamKART<br>
                        IIT Kharagpur<br>
                        Contact: {your_contact}<br>
                        <a href="{your_linkedin}" style="color: #0044cc;">LinkedIn</a> | 
                        <a href="{your_facebook}" style="color: #0044cc;">Facebook</a>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
"""

def send_emails():
    now = datetime.now()

    # Format it as DD-MM-YYYY
    today_date = now.strftime("%d-%m-%Y")
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        print(f"Successfully logged in. Sending emails for {today_date}...")
    except Exception as e:
        print(f"Login failed: {e}")
        return

    for index, row in data.iterrows():
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = formataddr((YOUR_NAME, EMAIL))
            msg["To"] = row["Email"]
            msg["Cc"] = ", ".join(CC_EMAILS)
            msg["Subject"] = SUBJECT
            msg["Message-ID"] = make_msgid(domain="gmail.com")

            html_template = HTML_HEAD+HTML_BODY+HTML_TAIL
            
            html_content = html_template.format(
                recipient_name=row['Name'],
                company=row['Company'], # Fixed: Uncommented this line
                brochure_link = BROCHURE_URL,
                tk_logo_url = TK_LOGO_URL,
                your_name = YOUR_NAME,
                your_year = YOUR_YEAR,
                your_department = YOUR_DEPARTMENT,
                your_role = YOUR_ROLE_TK,
                your_contact = YOUR_CONTACT,
                your_linkedin = YOUR_LINKED_IN,
                your_facebook = YOUR_FACEBOOK
            )

            msg.attach(MIMEText(html_content, "html"))
            recipients = [row["Email"]] + CC_EMAILS
            server.sendmail(EMAIL, recipients, msg.as_string())
            ist_now = datetime.now() + timedelta(hours=5, minutes=30)
            print(f"Sent email to {row['Email']} at {ist_now.strftime('%H:%M:%S')} IST")
            
            time.sleep(random.randint(25, 55))

        except Exception as e:
            print(f"Error sending to {row['Email']}: {e}")

    server.quit()

if __name__ == "__main__":
    send_emails()

