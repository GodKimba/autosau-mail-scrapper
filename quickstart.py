from __future__ import print_function

import os.path
from time import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())



    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        # Get Messages
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])

        if not labels:
            message_count = int(input("How many messages do you want to see?"))
        if not messages:
            print("No labels found.")
            return
        print("Labels:")
        # For function that gets the snippet of a message if it was send by 'puc-rio'
        for message in messages[:60]:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
             )
            #print(msg['payload']['headers'])
            if 'puc-rio' in msg['payload']['headers'][6]['value']:
                print(msg['snippet'])
            #print(msg['payload']['headers'][6]['value'])

        autosau_address_getter = service.users().messages().list(userId='me', q='from:autosau@puc-rio.br').execute()
        autosau_messages = autosau_address_getter.get('messages', [])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
