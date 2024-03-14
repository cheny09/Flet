import flet as ft
from Logger_Path import Path, Logger
import json

try:
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

except Exception as err:
    Logger.error( f"google import Unexpected {err=}, {type( err )=}" )


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'CredencialsPythonSyncCalendar.json'
CREDENTIALS_DATA = {"installed":{"client_id":"4364081911-d85adgbr01ak0tvm7b9unookc8p5as18.apps.googleusercontent.com","project_id":"pythoncalendar-402422","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}


#if sistema == 'android':
#    #REVISAR CUANDO SE LANCE LA APP EN PLAY STORE
#    CREDENTIALS_DATA = {"installed":{"client_id":"4364081911-jfauau6qb3g25gb6un7v1u0vi8jhpl7h.apps.googleusercontent.com","project_id":"pythoncalendar-402422","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs"}}

def get_calendar_path_token( page: ft.Page ):
    
    if page.client_storage.contains_key( 'token_google' ):

        return page.client_storage.get( 'token_google' )
    
    return None



def get_calendar_service( page: ft.Page ):

    try:
        creds = None

        TOKEN = get_calendar_path_token( page )

        #Logger.info( f"get_calendar_service> token {TOKEN}" )

        if TOKEN:
            
            TOKEN = json.loads( TOKEN )

            creds = Credentials.from_authorized_user_info(TOKEN)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                #si no existe el archivo de creedenciales
                if not os.path.exists(CREDENTIALS_FILE):
                    flow = InstalledAppFlow.from_client_config(CREDENTIALS_DATA, SCOPES)
                #si existe el archivo de creedenciales
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)

                creds = flow.run_local_server(port=8550)

            # Save the credentials for the next run
            page.client_storage.set( 'token_google', creds.to_json() )

            #Logger.info( f"get_calendar_service> {creds.to_json()}" )


        service = build('calendar', 'v3', credentials=creds)
        return service

    except Exception as err:
        Logger.error( f"get_calendar_service Unexpected {err=}, {type( err )=}" )

        return None

