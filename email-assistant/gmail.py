import os
import pickle

#Gmail API Utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachment MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

#globals
SCOPES = 'https://mail.google.com/'
OUR_EMAIL = 'branchleaf.creations@gmail.com'

# utility functions
def _get_size_format(b, factor=1024, suffix="B"):
    # print bytes in a nice readable format
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def _clean(text):
    # _clean text for create a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials = creds)

def parse_parts(service, parts, folder_name, message):
    """
    Parses content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = parts.get("headers")
            if part.get("parts"):
                # recursion baby!
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            elif mimeType == "text/html":
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to ", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            print("Saving the file: ", filename, " size: ", _get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))



# Add attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(destination, obj, body, attachments=[]):
    if not attachments:
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = OUR_EMAIL
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = OUR_EMAIL
        message['subject'] = obj
        message.attach(MIMEText(body)) 
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
        userId='me',
        body=build_message(destination, obj, body, attachments)
    )

def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get('headers')
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        #print basic email info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                print("From: ", value)
            if name.lower() == "to":
                print("To: ", value)
            if name.lower() == "subject":
                has_subject = True
                folder_name = _clean(value)
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject: ", value)
            if name.lower() == "date":
                print("Date: ", value)
    if not has_subject:
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("="*50)

def mark_as_read(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'removeLabelIds': ['UNREAD']
        }
    ).execute()

def mark_as_unread(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'addLabelIds': ['UNREAD']
        }
    ).execute()

def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    return service.users().messages().batchDelete(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_delete]
        }
    ).execute()