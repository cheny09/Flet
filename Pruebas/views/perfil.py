import flet as ft

import json
import os
from datetime import datetime

from Logger_Path import Path, Logger, PATH, PATH_HOME

from custom.app import App
from custom.funciones import (
    color_rgb_aply_opacity, 
    rgb2hex, 
    hex2rgb,
    ReturnValueThread,
    funciones,
    storage
)
from custom.MyDataBase import ddbb
from custom.GoogleCalendarSetup import (
    get_token_google, 
    get_calendar_service, 
    GOOGLE_PROVIDER,
    SCOPES,
    get_calendar_service_v2,
    encrypt, decrypt,
    SECRET_KEY
)

from config_default import Config, Years, TurnosDefaults

from flet.auth.providers import GoogleOAuthProvider


class PagePerfil( App, ft.View, ddbb ):

    def __init__(self, page = ft.Page ):
        super().__init__(page)

        self.page = page

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        self.scroll= ft.ScrollMode.ALWAYS
        self.expand = 1
        self.padding = 5

        self.route= "/perfil"
        self.controls.append( self.view_perfil() )

        self.page.views.append(self)

        self.page.on_login = self.on_login

        self.mi_perfil()



        #self.show_alert_dialog( text= str( get_token_google( self.page ) ), title='Token_google' )




    def view_perfil( self ):

        ContenedorPrincipal = ft.Column( width = 480, spacing = 20,  ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa
        
        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Convenio:', weight='BOLD' ),
        ) )

        self.ConvenioPerfil = ft.TextField(
            value='',
            label="Horas:Minutos", 
            hint_text="Introduce aquí tu convenio.",
            tooltip = 'Introduce aquí las horas por convenio que te pertenecen.',
            )
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.ConvenioPerfil,
        ) )

        self.CheckboxSumarDiferenciaAnioAnterior = ft.Checkbox( 
            adaptive=True, 
            label="Sumar diferencia Convenio año anterior", 
            value=True, 
            label_position='right',
            tooltip = 'Si esta marcado Sumar diferencia convenio año anterior acumula el resultado año tras año en las estadisticas.',
            )

        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.CheckboxSumarDiferenciaAnioAnterior,
                alignment = ft.alignment.center_right,
            ) )

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Sincronización con Google Calendar:', weight='BOLD' ),
        ) )
        
        self.IDGcalendarPerfil = ft.TextField(
            value='',
            label="ID de Google Calendar", 
            hint_text="Introduce aquí tu ID de Google Calendar.",
            tooltip = 'Introduce aquí tu ID de Google Calendar que desee sincronizar.',
            disabled=True,
            )
        
        

        self.ObtenerIDsGoogleCalendar = ft.TextButton(
                    text="Seleccionar Calendario de Google",
                    on_click= lambda x, btn= self.IDGcalendarPerfil: self.calendars_google_list_dialog( btn )
                )
        

        ContenedorPrincipal.controls.append( ft.Container(
            content= self.ObtenerIDsGoogleCalendar,
        ) )

        

        
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.IDGcalendarPerfil,
        ) )

        self.CheckboxSyncGoogleCalendar = ft.Checkbox( 
            adaptive=True, 
            label="Sincronizar con Google Calendar", 
            value=False, 
            label_position='right',
            tooltip = 'Si esta marcado Sincronizar con Google Calendar, se sincronizará de forma automatica la planilla al crear nuevos patrones o editar un día concreto.',
            )

        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.CheckboxSyncGoogleCalendar,
                alignment = ft.alignment.center_right,
            ) )
        

        """
        def login_click(e):
            self.page.login(GOOGLE_PROVIDER)


        def on_login(e):
            print("Login error:", e.error)
            print("Access token:", self.page.auth.token.to_json())
            print("User ID:", self.page.auth.user.id)

            self.page.client_storage.set( 'token_google', encrypt(self.page.auth.token.to_json(), SECRET_KEY ) )

        self.page.on_login = on_login
        """



        self.SesionGoogleCalendar = ft.ElevatedButton(
                    text="Iniciar en Google",
                    on_click= lambda x, btn= self.IDGcalendarPerfil: self.calendars_google_list_dialog( btn )
                )
        
        if get_token_google( self.page ):

            self.SesionGoogleCalendar.text="Salir de Google"
            self.SesionGoogleCalendar.on_click= lambda x, btn= self.IDGcalendarPerfil: self.exit_google_calendar( btn )
        
        else:

            self.ObtenerIDsGoogleCalendar.disabled = True

            self.CheckboxSyncGoogleCalendar.disabled = True

            if self.CheckboxSyncGoogleCalendar.value == True:

                self.CheckboxSyncGoogleCalendar.value = False

                self.CheckboxSyncGoogleCalendar.update()

                self.guardar_perfil()








        self.GuardarPerfil = ft.FilledButton(
                    text="Guardar",
                    on_click= lambda x: self.guardar_perfil()
                )
                
        ContenedorPrincipal.controls.append( 
            ft.Row(
                [ 
                    #ft.ElevatedButton("Log", on_click=lambda x: self.log_read()), 
                    self.SesionGoogleCalendar,
                    ft.Container(content=self.GuardarPerfil, alignment = ft.alignment.center_right, expand=1) ],
                
            ) )
        

        ContenedorPrincipal.controls.append( 
            ft.IconButton( 
                ft.icons.LOGIN, 
                tooltip="Iniciar sesion en google",
                on_click= lambda x: self.login_google()
            ) 
        )
                
        

        return ft.Container( content = ContenedorPrincipal, padding=20 )


    




    def mi_perfil( self ):
        
        self.TextTitle.value = self.page.title ="Mi Perfil"

        #GcalendarID
        self.IDGcalendarPerfil.value = str( self.UserConfiguration['GcalendarID'] )

        #Horas Convenio
        self.ConvenioPerfil.value = str( self.UserConfiguration['horas_convenio'] )

        #Sumar horas convenio año anterio
        self.CheckboxSumarDiferenciaAnioAnterior.value = bool( self.UserConfiguration['SumarDiferenciaAnioAnterior'] )

        #Sincronizar Google Calendar
        self.CheckboxSyncGoogleCalendar.value = bool( self.UserConfiguration['sync_google'] )

        self.page.update()
        #Guardar



    def calendars_google_list_dialog( self, button ):
        try:
            
            if get_token_google( self.page ):

                contentMain = []

                layout = ft.Column()
                
        
                titulo_calendarios = ft.Text( 
                        value='Mis calendarios de Google',
                        weight='bold'
                    )
                contentMain.append( titulo_calendarios )

                self.GCal.page = self.page
                
                calendarios = self.GCal.get_list_calendars()

                if calendarios != []:

                    for i in range( len( calendarios ) ):
                        label = ft.TextButton( 
                            text= calendarios[i]['nombre'], 
                            on_click=lambda _, x=button, id=calendarios[i]['id']: self.callback_for_dialog( x, value = id ),
                        )
                        layout.controls.append( label )

                contentMain.append( layout )


                self.show_alert_dialog( Content=contentMain, title='Seleccione un calendario'  )

                self.page.update()

            else:

                service = get_calendar_service( self.page )

                if not service:
                    contentMain = [ ft.Text( service ) ]

                    self.show_alert_dialog( Content=contentMain, title='Error al iniciar sesion'  )

                    self.page.update()

                else:
                    self.page.go( '/reload' )
                    self.page.go( '/perfil' )    
                

        except Exception as err:
            Logger.error( f"calendars_google_list_dialog Unexpected {err=}, {type( err )=}" )



    def exit_google_calendar(self, btn):

        token = get_token_google( self.page )

        Logger.debug( f"Saliendo de Google" )

        if token:

            self.storage.remove( "token_google" )

        btn.value = ''

        self.CheckboxSyncGoogleCalendar.value = False

        self.guardar_perfil()

        self.page.go( '/reload' )
        self.page.go( '/perfil' )




    def guardar_perfil_activar_sync(self, force = True):

        self.CheckboxSyncGoogleCalendar.value = force

        self.page.update()

        self.guardar_perfil( force_sync_google = force )



    def guardar_perfil( self, alert = True, force_sync_google = True ):

        result = False
        Actions = False
        title = 'Actualizar perfil'

        #GcalendarID
        GcalendarID = self.IDGcalendarPerfil.value

        #Horas Convenio
        Horas_Convenio = self.ConvenioPerfil.value

        #Sumar horas convenio año anterio
        SumarDiferenciaAnioAnterior = self.CheckboxSumarDiferenciaAnioAnterior.value

        #Sincronizar Google Calendar
        CheckboxSyncGoogleCalendar = self.CheckboxSyncGoogleCalendar.value

        #print( 'CheckboxSyncGoogleCalendar', CheckboxSyncGoogleCalendar )
        #print( 'GcalendarID', GcalendarID )

        if CheckboxSyncGoogleCalendar == False and GcalendarID != '' and force_sync_google == True:

            result = 'Tiene una ID de Google Calendar, ¿desea activar la sincronización?' 
            Actions = [
                ft.ElevatedButton("Si", on_click=lambda x: self.guardar_perfil_activar_sync()),
                ft.OutlinedButton("No", on_click=lambda x: self.guardar_perfil_activar_sync( force = False )),
                ]
            
        
        if CheckboxSyncGoogleCalendar == True and GcalendarID == '':
            
            CheckboxSyncGoogleCalendar = self.CheckboxSyncGoogleCalendar.value = False

            self.page.update()

            result = 'No se puede activar la sincronizacion sin una ID de Google Calendar'



        respu = self.validar_formato_horas_minutos( Horas_Convenio )

        if respu == False:
            return

        if result == False:
            
            result=self.update_user_ddbb( str( Horas_Convenio ), str( GcalendarID ), bool(SumarDiferenciaAnioAnterior), bool(CheckboxSyncGoogleCalendar) )


        if alert or ( alert == False and result != 'Perfil actualizado con éxito.' ):
            
            self.show_alert_dialog( Actions = Actions, text=str( result ), title= title ) 

            self.reload_menu()





    def login_google( self ):

        self.page.login(
            GOOGLE_PROVIDER,
            scope= SCOPES,
            on_open_authorization_url=lambda url: self.page.launch_url(url, web_window_name="_blank" )
        )

    def on_login(self, e):
        print("Login error:", e.error)
        print("Access token:", self.page.auth.token.to_json())
        print("User ID:", self.page.auth.user.id)

        self.page.client_storage.set( 'token_google', encrypt(self.page.auth.token.to_json(), SECRET_KEY ) )

        self.show_notify( f"User ID:, {self.page.auth.user}" )

        









class PageBackup( App, ft.View, ddbb ):

    def __init__(self, page = ft.Page ):
        super().__init__(page)

        self.page = page

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        self.scroll= ft.ScrollMode.ALWAYS
        self.expand = 1
        self.padding = 5

        self.route= "/backup"
        self.controls.append( self.view_backup() )

        self.page.views.append(self)




    


    def view_backup( self ):

        self.TextTitle.value = self.page.title = "Copias de Seguridad"
    
        def save_file_result( e: ft.FilePickerResultEvent, notify = True ):

            
            if e.path != None: # comprueba que se a seleccionado un directorio/archivo
                try:
                    #path = os.path.dirname(e.path) # extra la ruta del directorio padre

                    path = e.path

                    archivos_para_hacer_backup = ['years', 'configuration'] # , 'token'
                        
                    error = False
                    
                    if Path( path ).exists():

                        fichero_backup = {}

                        for storage in archivos_para_hacer_backup:

                            #solo se hace el backup de los ficheros que exiesten en la lista archivos_para_hacer_backup
                            if self.storage.exists(storage):

                                try:
                        
                                    fichero_backup[storage] = self.storage.get( storage )
                
                                except Exception as err:              
                                    Logger.error( f"Al leeer archivo Unexpected {err=}, {type( err )=}" )
                                    error = True


                        try:

                            now = datetime.now()
                            # Formato: XXXX-MM-DD_hh.mm-backup.json
                            new_name = ( str( now.year ) + '-' + 
                                        str( self.cero_izquierda( now.month ) ) + '-' + 
                                        str( self.cero_izquierda( now.day ) ) + '_' + 
                                        str( self.cero_izquierda( now.hour ) ) + '.' + 
                                        str( self.cero_izquierda( now.minute ) ) + 
                                        "-backup.json" )

                            #filename = os.path.join( SharedStorage().get_cache_dir(), new_name )

                            filename = os.path.join( path, new_name )

                            with open( filename, "w" ) as file:

                                json.dump( fichero_backup, file, indent = 4 )


                            #SharedStorage().copy_to_shared( private_file=filename, collection = Environment.DIRECTORY_DOCUMENTS )

                            Logger.debug( f"Archivo {filename} creado." )

                            
                        except Exception as err:              
                            Logger.error( f"al crear archivo Unexpected {err=}, {type( err )=}" )
                            error = True

                    else:
                        Logger.error( f"al acceder a la ruta {path}" )
                        error = True

                    if notify:

                        if not error:
                            
                            self.show_notify( msg= f"Se ha creado el backup.", color='GREEN' )
                        
                        else:
                            self.show_notify( msg= f"Se ha producido algun error al crear el backup." )
                    
                    elif error:

                        Logger.error( 'Se ha producido algun error al crear el backup' )

                        self.show_notify( msg= f"Se ha producido algun error al crear el backup." )

                except Exception as err:              
                    Logger.error( f"Al crear backup Unexpected {err=}, {type( err )=}" )

                    self.show_notify( msg= f"Error al crear backup." )




        def backup_end( error ):
            if not error:

                #self.login_db( self.planilla )

                self.show_notify( msg= f"Se ha instalado el backup correctamente.", color='GREEN' )

                self.reload_config()

            else:
                self.show_notify( msg= f"Se ha producido algun error al restaurar el backup." )



        def pick_files_result(e: ft.FilePickerResultEvent):
            self.selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )

            if e.files != None: # comprueba que se a seleccionado un directorio/archivo

                fichero = e.files[0].path

                error = False

                try:

                    error = self.file_json_to_store( fichero )

                except Exception as e:
                    pass

                else:

                    Logger.error( error )
                    backup_end( error )
                        
                self.selected_files.update()


        pick_files_dialog = ft.FilePicker(on_result=pick_files_result, )
        save_file_dialog = ft.FilePicker(on_result=save_file_result, )

        self.selected_files = ft.Text()

        self.page.overlay.append(pick_files_dialog)

        self.page.overlay.append(save_file_dialog)



        def restablecer_configuracion():

            self.storage.set('configuration', Config )

            self.reload_config()

            self.show_notify( msg= f"Se ha restablecido la configuración.", color='GREEN' )



        def restablecer_years():

            self.storage.set('years', Years )

            self.reload_config()

            self.show_notify( msg= f"Se ha restablecido la base de datos.", color='GREEN' )



        ContenedorPrincipal = ft.Column( width = 480, spacing = 20, ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa
        
        # Este contenedor se agrega para añadir un margen superior
        ContenedorPrincipal.controls.append( ft.Container( height=10 ) )

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Copia de seguridad:', weight='BOLD' ),
        ) )

        RowBtnBackup = ft.Row()

        ContenedorPrincipal.controls.append( RowBtnBackup )

        self.CrearBackup = ft.FilledButton(
                    text="Crear",
                    icon=ft.icons.SAVE,
                        on_click=lambda _: save_file_dialog.get_directory_path( initial_directory=PATH_HOME, ),
                )
        
        RowBtnBackup.controls.append( 
            ft.Container(
                content= self.CrearBackup,
                alignment = ft.alignment.center_left,
                margin=10,
            ) )


        self.RestaurarBackup = ft.FilledButton(
                    text="Restaurar",
                    icon=ft.icons.SETTINGS_BACKUP_RESTORE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=False,
                            file_type= ft.FilePickerFileType.CUSTOM ,
                            allowed_extensions= ['json'],
                            initial_directory=PATH_HOME,
                        ),
                )
        
        RowBtnBackup.controls.append( 
            ft.Container(
                content= self.RestaurarBackup,
                alignment = ft.alignment.center_left,
                margin=10,
            ) )
        
        ContenedorPrincipal.controls.append( self.selected_files )


        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Limpiar base de datos:', weight='BOLD' ),
        ) )

        self.LimpiarDBBackup = ft.FilledButton(
                    text="Limpiar",
                    icon=ft.icons.CLEANING_SERVICES,
                        on_click=lambda _: self.limpiar_ddbb_years(),
                )
        
        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.LimpiarDBBackup,
                alignment = ft.alignment.center_left,
                margin=10,
            ) )
        


        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Eliminar la base de datos:', weight='BOLD' ),
        ) )

        self.RestablecerDBBackup = ft.FilledButton(
                    text="Restablecer Años",
                    icon=ft.icons.DELETE,
                        on_click=lambda _: restablecer_years(),
                )
        
        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.RestablecerDBBackup,
                alignment = ft.alignment.center_left,
                margin=10,
            ) )
        

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Restablecer la configuracion inicial:', weight='BOLD' ),
        ) )

        self.RestablecerConfigBackup = ft.FilledButton(
                    text="Restablecer configuración",
                    icon=ft.icons.DELETE,
                        on_click=lambda _: restablecer_configuracion(),
                )
        
        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.RestablecerConfigBackup,
                alignment = ft.alignment.center_left,
                margin=10,
            ) )
        

        RowPruebas = ft.Row()

        ContenedorPrincipal.controls.append(RowPruebas)


        RowPruebas.controls.append( 
            ft.IconButton( 
                ft.icons.PATTERN_SHARP, 
                on_click= lambda x: self.show_notify( os.path.abspath(__file__) , 'GREEN' )
            ) 
        )

        RowPruebas.controls.append( 
            ft.IconButton( 
                ft.icons.PATTERN_SHARP, 
                on_click= lambda x: self.show_notify( os.path.abspath(os.getcwd()) , 'GREEN' )
            ) 
        )

        RowPruebas.controls.append( 
            ft.IconButton( 
                ft.icons.PATTERN_SHARP, 
                on_click= lambda x: self.show_notify( os.path.dirname(os.path.abspath(__file__)) , 'GREEN' )
            ) 
        )

        RowPruebas.controls.append( 
            ft.IconButton( 
                ft.icons.DELETE, 
                tooltip="Eliminar toda la base de datos 'Storage.clean()'",
                on_click= lambda x: self.show_notify( self.page.client_storage.clear() , 'GREEN' )
            ) 
        )

        
        return ft.Container( content = ContenedorPrincipal, padding=20 )