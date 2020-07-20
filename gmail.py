from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64


# If there is an error occur. Just delete the "token.pickle" file. And re run this script to authorization.
SCOPES = ['https://mail.google.com/']

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }

def send_message(service, user_id, message):
  try:
    message = service.users().messages().send(userId=user_id, body=message).execute()
    #print('Message Id: %s' % message['id'] + 'Gönderildi')
    return message
  except Exception as e:
    print('An error occurred: %s' % e)
    return None


if __name__ == '__main__':

  #TEST İÇİN KULLANILIYOR.
  service = main()
  
  # Single mail send
  message = create_message('from@address.com', 'to@address.com', 'Test Mesajı YENİ!!!!', 'Bu bir test mesajıdır dikkate almayın!')
  send_message(service, 'me', message)
  print("Mesaj Gönderildi!")
  
  # Multiple mail send
  mail_list = ['birincimail@gmail.com', 'ikincimail@gmail.com', 'ucuncumail@gmail.com']
  
  for element in mail_list:
    message = create_message('from@address.com', element, 'Test Mesajı YENİ!!!!', 'Bu bir test mesajıdır dikkate almayın!')
    send_message(service, 'me', message)
    print("Mesaj Gönderildi!")
  
  
