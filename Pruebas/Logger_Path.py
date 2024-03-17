import flet as ft

import os
from pathlib import Path
import json
import logging

logging.getLogger("flet_core").setLevel(logging.WARNING) # (debug, info, warning, error y critical)
logging.getLogger("flet_runtime").setLevel(logging.WARNING)

logging.basicConfig( 
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler("out.log"),
        logging.StreamHandler()
    ]
    )
Logger = logging.getLogger('planilla')

PATH_HOME = ''

Documentos = os.path.join( Path.home(), 'Documentos' )
Documents = os.path.join( Path.home(), 'Documents' )

if os.path.exists( Documentos ):
    Logger.debug( 'Documentos' )
    PATH_HOME = Documentos

elif os.path.exists( Documents ):
    Logger.debug( 'Documents' )
    PATH_HOME = Documents


PATH = ''



def main(page: ft.Page):

    page.platform

    if page.platform == ft.PagePlatform.ANDROID:

        try:

            import android
            
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path

            from android import mActivity

            
            #Directorio Principal Android

            context = mActivity.getApplicationContext()
            result =  context.getExternalFilesDir(None)   # don't forget the argument
            if result:
                #Directorio Principal Seguro de la app /data/Android/{package-name}/
                PATH_DATA_ANDROID = str(result.toString())
                Logger.debug("PATH SECURE")
            else:
                #Directorio de la app de usuario no seguro
                PATH_DATA_ANDROID = app_storage_path()   # NOT SECURE
                Logger.debug("PATH NOT SECURE")

            PATH = PATH_DATA_ANDROID


        except Exception as err:
            Logger.error(f"PATH ANDROID Unexpected {err=}, {type(err)=}")