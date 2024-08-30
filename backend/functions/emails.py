import os.path
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

dotenv_path = '.env'
load_dotenv(dotenv_path=dotenv_path)
MY_EMAIL = os.getenv('EMAIL')
EMAIL_RECEIVER1 = os.getenv('EMAIL_RECEIVER1')
EMAIL_RECEIVER2 = os.getenv('EMAIL_RECEIVER2')

def get_header(headers, name):
    for header in headers:
        if header['name'] == name:
            return header['value']
    return f"(No {name})"

def get_email_content(payload):
    parts = payload.get('parts')
    if not parts:
        body = payload.get('body')
        data = body.get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part.get('body').get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    return "(No Content)"

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    access_code = None
    days = None

    # Find the access code
    h3_tags = soup.find_all('h3', string='ENTER ACCESS CODE')
    if h3_tags:
        table = h3_tags[0].find_next('table')
        if table:
            td = table.find('td')
            if td:
                access_code = td.get_text(strip=True)

    # Find the package message
    p_tags = soup.find_all('p', class_='cont')
    for p_tag in p_tags:
        if 'Great news! Your package is here!' in p_tag.get_text():
            # package_message = p_tag.get_text(strip=True)
            days = 0
            break
        elif 'Your package is still waiting for you!' in p_tag.get_text():
            # package_message = p_tag.get_text(strip=True)
            days = 1
            break
        elif 'Your package needs you!' in p_tag.get_text():
            # package_message = p_tag.get_text(strip=True)
            days = 2
            break
        elif 'It has now been 4 days' in p_tag.get_text():
            # package_message = p_tag.get_text(strip=True)
            days = 4
            break
        elif 'It has now been 7 days' in p_tag.get_text():
            # package_message = p_tag.get_text(strip=True)
            days = 7
            break
        

    # package_message = p_tags[1].get_text(strip=True)
        
    return access_code, days

def convert_to_pst(date_str):
    # Parse the date string to a datetime object
    email_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    date_utc = email_date.astimezone(pytz.utc)
    # Convert the datetime object to PST
    pst_tz = pytz.timezone('US/Pacific')
    email_date_pst = date_utc.astimezone(pst_tz)
    return email_date_pst.strftime('%Y-%m-%d %H:%M:%S %Z')

def create_message(to, subject, body_text):
    message = MIMEText(body_text)
    message['to'] = to
    message['from'] = MY_EMAIL
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {sent_message['id']}")
        return sent_message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    
def get_new_luxer_one_email():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
      # Call the Gmail API
      service = build("gmail", "v1", credentials=creds)

      sender = 'support@luxerone.com'
      today = datetime.today().astimezone(pytz.utc)
      today2 = today.strftime('%Y/%m/%d')
      two_days_ago = (today - timedelta(days=2)).strftime('%Y/%m/%d')
      one_day_ago = (today - timedelta(days=1)).strftime('%Y/%m/%d')
      seven_days_ago = (today - timedelta(days=7)).strftime('%Y/%m/%d')
    #   query = f'from:{sender} after:{seven_days_ago}'
    #   query = f'from:{sender} after:{one_day_ago} before:{today2}'
      query = f'from:{sender} after:{today2}'

      # List the messages in the user's account
      results = service.users().messages().list(userId="me", labelIds=["INBOX"], q=query).execute()
      messages = results.get("messages", [])

      if not messages:
          print("No messages found.")
          return

      email_details = []
      for message in messages:
          msg = service.users().messages().get(userId="me", id=message["id"]).execute()
          # print(f"Message snippet: {msg['snippet']}")
          headers = msg['payload']['headers']
          subject = get_header(headers, 'Subject')
          date = get_header(headers, 'Date')
          date_pst = convert_to_pst(date)
          content = get_email_content(msg['payload'])
          access_code, days = parse_html_content(content)
          print(f"Subject: {subject}\nDate: {date_pst}\nAccess Code: {access_code}\nDays: {days}\n")

          email_details.append({
            'date': date_pst,
            'access_code': access_code,
            'days': days
          })

          email_receivers = [EMAIL_RECEIVER1, EMAIL_RECEIVER2]
          for email_receiver in email_receivers:
            email_message = create_message(email_receiver, subject, content)
            send_message(service, "me", email_message)

      return email_details

  except HttpError as error:
      # TODO: Handle errors from Gmail API.
      print(f"An error occurred: {error}")
      return error