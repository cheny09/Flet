import flet as ft
from flet.auth.providers import GoogleOAuthProvider

from Logger_Path import Path, Logger

try:
    from flet.security import encrypt, decrypt

except Exception as err:
    Logger.error( f"from flet.security import Unexpected {err=}, {type( err )=}" )

    def encrypt( encrypted_data: str, secret_key: str ):

        Logger.warn( "Atencion no se pueden encriptar los datos." )
        return encrypted_data
    
    def decrypt( encrypted_data: str, secret_key: str ):

        Logger.warn( "Atencion no se pueden encriptar los datos." )
        return encrypted_data



import json

try:
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

except Exception as err:
    Logger.error( f"google import Unexpected {err=}, {type( err )=}" )

SECRET_KEY = "VP9WN8E567has"

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    #'https://www.googleapis.com/auth/userinfo.email',
    #'https://www.googleapis.com/auth/userinfo.profile',
        ]
CREDENTIALS_FILE = 'CredencialsPythonSyncCalendar.json'
CREDENTIALS_DATA = {"installed":{"client_id":"4364081911-d85adgbr01ak0tvm7b9unookc8p5as18.apps.googleusercontent.com","project_id":"pythoncalendar-402422","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}


#GOOGLE_CLIENT_ID = CREDENTIALS_DATA["installed"]['client_id']
#GOOGLE_CLIENT_SECRET = CREDENTIALS_DATA["installed"]['client_secret']

GOOGLE_CLIENT_ID = "4364081911-7p9a5hega532hlvpsvdu0rvhbh0tbkjt.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

GOOGLE_REDIRECT = "http://localhost:8550/oauth_callback"

GOOGLE_PROVIDER = GoogleOAuthProvider(
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                redirect_url=GOOGLE_REDIRECT,
            )   #access_type="offline",

#if sistema == 'android':
#    #REVISAR CUANDO SE LANCE LA APP EN PLAY STORE
#    CREDENTIALS_DATA = {"installed":{"client_id":"4364081911-jfauau6qb3g25gb6un7v1u0vi8jhpl7h.apps.googleusercontent.com","project_id":"pythoncalendar-402422","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs"}}




def get_token_google( page: ft.Page ):
    
    if page.client_storage.contains_key( 'token_google' ):

        #return page.client_storage.get( 'token_google' )

        return decrypt( page.client_storage.get( 'token_google' ), SECRET_KEY )
    
    return None




def get_credentials_google( page: ft.Page ):

    try:
        creds = None

        TOKEN = get_token_google( page )

        Logger.debug( f"get_calendar_service> token {TOKEN}" )

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

                creds = flow.run_local_server(port=8550, success_message= "La autenticación se ha completado. Puede cerrar esta ventana.")

            # Save the credentials for the next run
            
            page.client_storage.set( 'token_google', encrypt( creds.to_json(), SECRET_KEY ) )

            Logger.debug( f"get_calendar_service> {creds.to_json()}" )

        return creds

    except Exception as err:
        Logger.error( f"get_credentials_google Unexpected {err=}, {type( err )=}" )

        return None
    



def get_calendar_service( page: ft.Page ):

    try:
        creds = get_credentials_google( page )

        service = build( 'calendar', 'v3', credentials=creds )
        return service

    except Exception as err:
        Logger.error( f"get_calendar_service Unexpected {err=}, {type( err )=}" )

        return None








def convert_token_google( token ):

    return {
        "token": token['access_token'], 
        "refresh_token": None, 
        "token_uri": "https://oauth2.googleapis.com/token", 
        "client_id": GOOGLE_CLIENT_ID, 
        "client_secret": GOOGLE_CLIENT_SECRET, 
        "scopes": token['scope'], 
        "universe_domain": "googleapis.com", 
        "account": "", 
        "expiry": token['expires_at']#"2024-03-17T15:58:57.745437Z"
    }









def get_calendar_service_v2( page: ft.Page ):

    try:
        creds = None

        TOKEN = page.auth.token.to_json()

        if TOKEN:

            TOKEN = json.loads( TOKEN )

            token_ = {
                "token": TOKEN['access_token'],
                "refresh_token": None,
                "scopes": TOKEN['scope'],
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'token_uri': 'https://oauth2.googleapis.com/token'
            }

            Logger.debug( f"get_calendar_service_v2> token {TOKEN}" )



            #creds = Credentials.from_authorized_user_debug(TOKEN)

            service = build( 'calendar', 'v3', credentials=token_ )

            calendar_list = service.calendarList().list(pageToken=None).execute()

            return service
        
        else:

            return None
        
 
    except Exception as err:
        Logger.error( f"get_calendar_servicev2 Unexpected {err=}, {type( err )=}" )

        return None