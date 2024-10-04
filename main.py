import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule # type: ignore
import time
import datetime

def get_menu(url):
    try:
        # Abrufen der Webseite
        response = requests.get(url)

        # Überprüfen, ob der Abruf erfolgreich war
        if response.status_code == 200:
            # HTML der Webseite parsen
            soup = BeautifulSoup(response.text, 'html.parser')

            # Suchen nach allen span mit data-hook="wixrest-menus-item-title"
            menu_items = soup.find_all('span', {'data-hook': 'wixrest-menus-item-title'})

            # Extrahieren des Textes aus den gefundenen span-Elementen
            titles = [item.get_text(strip=True) for item in menu_items]

            # Überprüfen, ob Titel gefunden wurden
            if titles:
                menu = "\n"+ titles[0] +"\n\n Einen guten Apetit wünscht Ihnen \n MAVID"
                return menu
            else:
                return "Keine Menüelemente gefunden."
        else:
            return f"Fehler beim Abrufen der Webseite: Statuscode {response.status_code}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"
    
    

def send_email(menu, recipient_email):
    subject = "Franky's Wochenhit"
    sender = "mavidpython@gmail.com"
    password = "qpsu lcyq gutx okvt"

    try:
        msg = MIMEText(menu)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipient_email)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print("Message sent to "+recipient_email+"!")
    except Exception as e:
        print(f"Email konnte nicht gesendet werden: {e}")



def job():
    menu_url = 'https://apps.wixrestaurants.com/?type=wixmenus.client&pageId=lhq2p&compId=TPASection_ije2yufi&viewerCompId=TPASection_ije2yufi&siteRevision=5&viewMode=site&deviceType=desktop&locale=de&tz=Europe%2FZurich&regionalLanguage=de&width=980&height=2041&instance=qTGD4dhBOno1RekehPd-2J254--x7usASxWFKCFtU5g.eyJpbnN0YW5jZUlkIjoiMDhlZDdiY2EtMzFiMS00ZmQwLTgyZWItMTkzOTQ5YzM4OTNiIiwiYXBwRGVmSWQiOiIxM2MxNDAyYy0yN2YyLWQ0YWItNzQ2My1lZTdjODllMDc1NzgiLCJtZXRhU2l0ZUlkIjoiODZhNmU0OTAtM2RjZS00ZGE4LTliOGYtZjc2OTkyNDRmYzlkIiwic2lnbkRhdGUiOiIyMDI0LTEwLTAzVDExOjMyOjMyLjIxOVoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJyZXN0X3BybyIsImRlbW9Nb2RlIjpmYWxzZSwib3JpZ2luSW5zdGFuY2VJZCI6IjdiNjI4Njg3LTFjNGEtNDY3OC1iYTJjLWEyNzBmYzZhNGRlZiIsImFpZCI6ImM4ODgxZWNhLWY5ODQtNGZmMy05YjNmLWI0N2Y5OTU1ZGNjYSIsImJpVG9rZW4iOiI4ZTRiOWY1YS0wYzdmLTAyNzgtMTk2NC1lZTUwZGI4Nzc1YTYiLCJzaXRlT3duZXJJZCI6ImE2ZjdmZTNjLWRhOTEtNDZmZi1hNDY5LWI0N2M5M2YxZTQ3OCJ9&currency=CHF&currentCurrency=CHF&commonConfig=%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22bsi%22%3A%2222713403-2c3d-41dc-a6e0-b0208279e2b2%7C1%22%2C%22siteRevision%22%3A%225%22%2C%22branchId%22%3A%22f8d1d120-7878-4685-8ef0-11e7465881d9%22%2C%22renderingFlow%22%3A%22NONE%22%2C%22language%22%3A%22de%22%2C%22locale%22%3A%22de-ch%22%2C%22BSI%22%3A%2222713403-2c3d-41dc-a6e0-b0208279e2b2%7C1%22%7D&currentRoute=.%2Fmenu&target=_top&section-url=https%3A%2F%2Fwww.frankysbbq.com%2Fmenu%2F&vsi=a464f0b8-8cdd-4d6e-a62d-75f5effad5b0'

    recipients = [
        "david.pires2003.dp@gmail.com", 
        "marcel.voegeli@endress.com",
        "david.pires@endress.com"
    ]
    
    try:
        menu = get_menu(menu_url)
        print(f"Abgerufenes Menü: \n{menu}")
        for recipient in recipients:
            send_email(menu, recipient)
    except Exception as e:
        print(f"Fehler: {e}")

schedule.every().friday.at("11:00:00").do(job)




if __name__ == "__main__":
    while True:
        schedule.run_pending()
        now = datetime.datetime.now()
        print (now.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(60)  


