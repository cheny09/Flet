import flet as ft

from Logger_Path import Path, Logger, PATH, PATH_HOME
from config_default import Config, Years, TurnosDefaults

from custom.funciones import (
    color_rgb_aply_opacity, 
    rgb2hex, 
    hex2rgb,
    ReturnValueThread,
    funciones,
    storage
)
from custom.GoogleCalendar import MyGoogleCalendar



from views.template_route import TemplateRoute

from datetime import datetime
import json

import os

LECTOR_QR_IMPORT = False

try:
    # INSTALL YOU OPENCV WITH PIP - lector qr
    import numpy as np
    import cv2
    import ast

    LECTOR_QR_IMPORT = True

except Exception as err:
    Logger.error( f"lector qr import Unexpected {err=}, {type( err )=}" )



class App( funciones ):

    SYNC_GOOGLE = False

    MyCamera = None

    def __init__(self, page = ft.Page ):
        super().__init__()

        self.page = page

        if self.page.banner:
            self.page.banner.open = False

        #self.page.platform = ft.PagePlatform.ANDROID
        Logger.debug( f"Platform, {self.page.platform}")

        self.storage = storage( self.page )


        self.UserConfiguration = Config
        self.DataYears = Years

        try: 

            if not self.storage.exists("configuration"):

                self.storage.set("configuration", Config)
                
                config_json = '/storage/emulated/0/Android/data/es.cheny.plnbeta/files/Planilla/configuration.json'
                
                if os.path.exists( config_json ):
                    Logger.info( "Existe el archivo configuration.json restaurando configuracion." )

                    self.file_json_to_store( config_json )

                else:
                    Logger.info( f"No existe el archivo de conguracion.json")
                #Archivo /storage/emulated/0/Android/data/es.cheny.plnbeta/files/Planilla/configuration.json creado.
                

            if not self.storage.exists("years"):

                self.storage.set("years", Years)

                years_json = '/storage/emulated/0/Android/data/es.cheny.plnbeta/files/Planilla/years.json'
                
                if os.path.exists( years_json ):
                    Logger.info( "Existe el archivo years.json restaurando years." )

                    self.file_json_to_store( years_json )

                else:
                    Logger.info( f"No existe el archivo de years.json")
                

                #Archivo /storage/emulated/0/Android/data/es.cheny.plnbeta/files/Planilla/years.json creado.
            

            self.UserConfiguration = self.storage.get("configuration")

            self.DataYears = self.storage.get("years")
        
        except Exception as err: 
            Logger.error( f"UserConfiguration - DataYears Unexpected {err=}, {type( err )=}" )
                  

        self.TextTitle = ft.Text( value = self.page.title, size=18, weight=ft.FontWeight.BOLD, )
        
        self.BtnPlanillaIrAHoy = ft.IconButton( ft.icons.TODAY, scale = 1.25, tooltip = 'Ir al día de hoy', on_click= lambda x, route="/", fun=self.ir_a_hoy: self.menu_callback( x, route = route, funcion = fun, title = 'Planilla' ) ) #
        if self.page.route == '/' :
            
            self.BtnPlanillaIrAHoy.icon = ft.icons.TODAY
            self.BtnPlanillaIrAHoy.tooltip = 'Ir al día de hoy'
            self.BtnPlanillaIrAHoy.on_click = lambda x, route="/", fun=self.ir_a_hoy: self.menu_callback( x, route = route, funcion = fun, title = 'Planilla' )

        else:

            self.BtnPlanillaIrAHoy.icon = ft.icons.CALENDAR_MONTH
            self.BtnPlanillaIrAHoy.tooltip = 'Ir a la planilla'
            self.BtnPlanillaIrAHoy.on_click = lambda x, route="/": self.menu_callback( x, route = route, title = 'Planilla' )
        
        self.ItemsMenu = []
        self.ItemsMenuLista = [
            {
                
                "text": f"Planilla",
                "icon": ft.icons.CALENDAR_MONTH,
                "on_click": lambda x, route="/": self.menu_callback( x, route = route, title = 'Planilla' ),
            },
            {
                
                "text": f"Estadisticas",
                "icon": ft.icons.BAR_CHART,
                "on_click": lambda x, route="/stats": self.menu_callback( x, route = route, title = 'Estadisticas' ),
            },
            {
                
                "text": f"Turnos",
                "icon": ft.icons.TODAY,
                "on_click": lambda x: self.page_turnos(),

            },
            {
                
                "text": f"Crear Patron",
                "icon": ft.icons.DATE_RANGE,
                "on_click": lambda x: self.page_patron_turnos(),
                
            },
            {
                
                "text": f"Sync G. Calendar",
                "icon": ft.icons.SYNC,
                "on_click": lambda x, current=f"/sync_g_calendar": self.menu_callback( route = current ),
                "exclusivo_sync_google": True,
            },
            {
                
                "text": f"Mi perfil",
                "icon": ft.icons.MANAGE_ACCOUNTS,
                "on_click": lambda x: self.page_mi_perfil(),
            },
            {
                
                "text": f"Copias de seguridad",
                "icon": ft.icons.SETTINGS_BACKUP_RESTORE,
                "on_click": lambda x, current=f"/backup": self.menu_callback( route = current, title = 'Copias de seguridad' ),

            },
        ]

        if LECTOR_QR_IMPORT == True:

            self.ItemsMenuLista.append( {
                    "text": f"Leer QR",
                    "icon": ft.icons.QR_CODE,
                    "on_click": lambda x, current=f"/leer_qr": self.menu_callback( route = current, title = 'Leer QR' ),
                
                } )

        self.MainAppBar = ft.AppBar(
                leading = ft.PopupMenuButton(
                        tooltip = 'Mostrar Menú',
                        icon= ft.icons.MENU,
                        items = self.ItemsMenu,
                        scale = 1.25,
                    ),
                leading_width = 40,
                toolbar_height = 80,
                title = self.TextTitle,
                center_title = False,
                bgcolor = ft.colors.PRIMARY_CONTAINER,
                actions = [
                    #ft.IconButton( ft.icons.DOCUMENT_SCANNER, on_click=lambda x: self.log_read()),
                    ft.IconButton( ft.icons.QUESTION_MARK, scale = 1.25, tooltip = 'Mostrar Ayuda', on_click=lambda _: self.ayuda() ),
                    self.BtnPlanillaIrAHoy,
                ],
                adaptive=False,
            )
        

        self.ListadoTurnos = {}

        self.id_turnos_eliminados = [] #utilizado para que al crear un turno nuevo se reutilice el ID de los turnos eliminados


        self.GCal = MyGoogleCalendar()

        self.GCal.PATH = PATH

        self.GCal.BORRAR_TODOS_EVENTOS_DEL_DIA = False


        self.reload_config()

        





    
    def welcome(self):
            
        cont = []

        cont.append(ft.Text(
            value= "Indica la cantidad de horas que debes trabajar al año, para que las estadisticas seán reales, en Horas convenio.",
            size=15,
            )
        )

        cont.append(ft.Text(
            value= "No te preocupes si no lo sabes ahora, podrás modificarlo mas tarde en Mi Perfil.",
            size=15,
            )
        )
        cont.append(ft.Text(
            value= "Si su total de horas anuales tiene minutos, indique las horas seguido de dos puntos y luego los minutos sin espacios.",
            size=15,
            )
        )

        cont.append( ft.Container(
            content= ft.Text( 'Convenio:', weight='BOLD' ),
        ) )

        self.horas_convenio_welcome = ft.TextField(
            value= '',
            label= 'Horas:Minutos'
            )
        
        cont.append(
            ft.Container( content= self.horas_convenio_welcome, padding=10 )
        )
        

        actions = [
            ft.FilledButton(
                text= 'Continuar',
                on_click= lambda _: self.fun_guardar_welcome( 0 )
            )
        ]

        self.show_alert_dialog( Content=cont, Actions=actions, title='Primeros pasos' )





    def fun_guardar_welcome( self, continuar = 0 ):

        cont = []

        if continuar == 0: 

            Horas_Convenio = self.horas_convenio_welcome.value
            
            config_user = self.UserConfiguration

            if Horas_Convenio == '':
                Horas_Convenio = '1760'
            else:
                respu = self.validar_formato_horas_minutos( Horas_Convenio )

                if respu == False:

                    self.welcome()

            config_user['horas_convenio'] = Horas_Convenio
            config_user['WELCOME'] = False

            Logger.debug( 'Guardamos el convenio y desactivamos la variable welcome.' )

            respuesta = self.storage.set( 'configuration', config_user )

            if respuesta:
                Logger.info( 'Continuamos con la bienvenida.' )
                self.fun_guardar_welcome( 1 )

        
        if continuar > 0:
            
            
            mensajes = ["",
                "El simbolo __?__ arriba a la derecha significa Ayuda, y en él encontrará informacion sobre que significa cada apartado y como utilizarlo.",
                "Ahora debes crear o modificar los turnos a tu necesidad, entrando en Menú, Turnos y toca en cada turno para ver sus detalles y modificarlos.",
                "Cuando hayas verificado tus turnos, luego debes crear tu patron de turnos.",
                "Recuerda para utilizar correctamente todas las funciones revisa siempre __?__ para ver como utilizarlas."
            ]
            
            if continuar < len( mensajes ):

                #print( mensajes[continuar] )

                cont.append( ft.Markdown( mensajes[continuar] ) )

                atras = continuar - 1

                if continuar == 1:
                    atras = 0

                continuar+=1

                actions = [
                    ft.OutlinedButton(
                        text= 'Atrás',
                        on_click= lambda _: self.fun_guardar_welcome( atras ) if atras != 0 else self.welcome()
                    ),
                    ft.FilledButton(
                        text= 'Continuar',
                        on_click= lambda _: self.fun_guardar_welcome( continuar )
                    )
                ]

                Title = [
                    ft.Text(f"Primeros pasos {continuar} - {len( mensajes )}"),
                    ft.Container( 
                        content= ft.IconButton( 
                            ft.icons.CLOSE, 
                            icon_color=ft.colors.RED,
                            tooltip="Salir de la bienvenida.",
                            scale= 1.2,
                            on_click= self.close_dlg
                        ), expand=1, 
                        alignment= ft.alignment.center_right 
                    )
                ]

                self.show_alert_dialog( Content=cont, Actions=actions, Title=Title )


            elif continuar == len( mensajes ):

                self.close_dlg( continuar )





    def log_read(self):
        
        log = []
        try:
            read = None

            archivo = "out.log"

            if os.path.exists( archivo ):

                Logger.debug( f"Abriendo el archivo {archivo}" )

                with open( archivo, "r") as f:
                    read = f.readlines()
                    Logger.debug( f"Leyendo el archivo {archivo}" )

                if read:

                    for line in read:

                        log.append( ft.Text( line ) )


                    self.show_alert_dialog( Content=log, title='Log')
            else:

                Logger.debug( f"No existe el archivo {archivo}" )

        except Exception as err:

            line = f"Error al abrir el archivo {archivo} {err=}, {type( err )=}" 
            log.append( ft.Text( line ) )
            Logger.error( line )
                         

        
    




    def ir_a_hoy( self ):
        """ Esta funcion sustituye a la que esta en planilla.py 
            cuando esta la ruta seleccionada no es '/'.
        """

        self.FechaSeleccionada = datetime.now()

        if not self.page.session.contains_key( "FechaSeleccionada" ):

            self.page.session.set( "FechaSeleccionada", self.FechaSeleccionada )
        
        else:

            self.FechaSeleccionada = self.page.session.get( "FechaSeleccionada" )

        self.page.go( '/' )




    def page_turnos(self):

        if self.page.route == '/turnos_edit':

            self.listado_turnos( ventana = '/turnos_edit' )

        else:

            self.page.go( '/turnos_edit' )



    def page_patron_turnos(self):

        if self.page.route == '/crear_patron':

            self.page_patron_de_turnos()

        else:

            self.page.go( '/crear_patron' )


    

    def page_mi_perfil(self):

        if self.page.route == '/perfil':

            self.mi_perfil()

        else:

            self.page.go( '/perfil' )




    def reload_config( self ):
        
        #inicio de sesion
        self.UserConfiguration = self.user_ddbb()


        if 'ID' in self.UserConfiguration:

            self.listado_turnos_ddbb()

            if 'GcalendarID' in self.UserConfiguration:

                self.GCal.calendarId = self.UserConfiguration['GcalendarID']

            if 'error' in self.UserConfiguration:
                pass

            if 'sync_google' in self.UserConfiguration:

                self.GCal.SYNC_GOOGLE = self.SYNC_GOOGLE = self.UserConfiguration['sync_google']

            if 'SumarDiferenciaAnioAnterior' in self.UserConfiguration:
                
                self.SumarDiferenciaAnioAnterior = self.UserConfiguration['SumarDiferenciaAnioAnterior']

            else:
                
                self.UserConfiguration['SumarDiferenciaAnioAnterior'] = self.SumarDiferenciaAnioAnterior

            try:
                self.DataYears = self.storage.get("years")
                
            except Exception as err:  
                Logger.error( f"reload_config Unexpected {err=}, {type( err )=}" )
                            
            self.reload_menu()

            self.page.update()

        else:
            Logger.warning( self.UserConfiguration )
            self.show_alert_dialog( text=str( self.UserConfiguration ), title='Error' )




    def reload_menu(self):

        self.ItemsMenu.clear()
        
        total_items_menu = len(self.ItemsMenuLista)

        if total_items_menu > 0:

            for item in self.ItemsMenuLista:
                
                mostrar = True

                if 'exclusivo_sync_google' in item:
                    
                    mostrar = ( self.SYNC_GOOGLE and item['exclusivo_sync_google'] )


                if mostrar == True:

                    if not 'icon' in item:

                        item['icon'] = ''

                    if not 'on_click' in item:

                        item['on_click'] = None

                    self.ItemsMenu.append( 
                        ft.PopupMenuItem(
                            text = item['text'],
                            on_click = item['on_click'],
                            icon = item['icon'],
                            )
                        )
                    
            self.page.update()




    def menu_callback( self, event = None, route = None, **kwargs ):
        
        #print( kwargs )
        if self.MyCamera != None:

            self.MyCamera = None


        if route != None:
            
            self.page.go( route )


        for key, value in kwargs.items():

            if key == 'title' and value != None:

                self.page.title = value

            elif key == 'title':
                
                if route != None:

                    self.page.title = route

            
            if key == 'funcion':

                if len( kwargs ) > 2:

                    value( kwargs )
                
                else:

                    value()


        self.TextTitle.value = self.page.title

        self.page.update()




    def listado_turnos( self, *args, **kwargs ):
        """ Ejemplo:    Instancia,                     Pagina de retorno,      Titulo de la pagina de retorno
        listado_turnos( id_select = 'TurnoExtraSelect', ventana = 'detalle_dia', titulo_retorno =  self.page.title )
        """
        try:
            contentMain = []

            content = ft.Column( spacing=2 )

            if not kwargs:
                
                kwargs = args[0]


            for i in self.ListadoTurnos:

                nombre = self.ListadoTurnos[i]['nombre']
                siglas = self.ListadoTurnos[i]['siglas']

                if kwargs['ventana'] == '/turnos_edit' and nombre == 'Ninguno':
                    nombre = 'Nuevo'
                    siglas = '+'

                data = {
                    'nombre': nombre,
                    'color': self.ListadoTurnos[i]['color'],
                    'ventana': kwargs['ventana'],
                    'id_turno': self.ListadoTurnos[i]['ID']
                        }
                
                if 'instance' in kwargs:

                    data['instance'] = kwargs['instance']

                if 'id_select' in kwargs:

                    data['id_select'] = kwargs['id_select']

                
                name  = f"( {siglas} ) {nombre}"

                
                content.controls.append( 
                    ft.Container(
                        content= ft.TextButton( 
                            text=str( name ), 
                            expand=1,
                            data = data,
                            on_click=lambda x, data=data: self.change_turno( ( data ) ),
                            style= ft.ButtonStyle(
                                bgcolor= self.ListadoTurnos[i]['color'],
                                color=ft.colors.BLACK,
                                side={
                                    ft.MaterialState.DEFAULT: ft.BorderSide(1),
                                    ft.MaterialState.HOVERED: ft.BorderSide(2),
                                },
                                shape={
                                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                                },
                            ),
                        ),
                        width= 1000,
                    )
                )

            modal = True

            if 'modal' in kwargs:

                modal = kwargs['modal']

            contentMain.append( content ) 
            self.show_alert_dialog( Content=contentMain, title='Seleccione un Turno', modal = modal )

        except Exception as err:
            Logger.error( f"list_turnos Unexpected {err=}, {type( err )=}" )



    def change_turno( self, data ):

        self.page.go( data['ventana'] )
        self.page.dialog.open = False

        if data['ventana'] == '/turnos_edit':

            self.edit_turno( data )

        
        if 'instance' in data:

            data['instance'] = data['instance']

            if data['instance']:

                data['instance'].text = data['nombre']
                data['instance'].key = data['id_turno']
                data['instance'].style.bgcolor = data['color']

                self.page.update()

            else:
                Logger.error( 'No tiene selector' + str( data ) )





    def color_google_calendar_dialog( self, button ):
        try:
            
            contentMain = []

            new_widgets = ft.Column( spacing=2, )
            
            colores = self.list_colors_google_calendar()

            for i in colores:
                new_widgets.controls.append( 
                    ft.Container(
                        ft.TextButton( 
                            text=str( colores[i]['name'] ),
                            style= ft.ButtonStyle(
                                bgcolor= colores[i]['code'],
                                color=ft.colors.BLACK,
                                side={
                                    ft.MaterialState.DEFAULT: ft.BorderSide(1),
                                    ft.MaterialState.HOVERED: ft.BorderSide(2),
                                },
                                shape={
                                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                                },
                            ),
                            key= i,
                            on_click= lambda x, button=button, color = colores[i]['code'], name = colores[i]['name'], value = i: self.callback_for_dialog( button, style_bgcolor = color, key = value, text = name ),
                        ),
                        width= 1000
                    )
                )

            contentMain.append( new_widgets )

            self.show_alert_dialog( Content=contentMain, title='Seleccione un color', modal = False )
        

        except Exception as err:
            Logger.error( f"color_google_calendar_dialog Unexpected {err=}, {type( err )=}" )




    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

        

    def show_alert_dialog( self, title = '', text = '', Content = False, Actions = False, Title = False, modal = True, margen_vertical=40, margen_horizontal=10 ):

        if Actions == False:

            Actions = [
                ft.Container( 
                    content= ft.IconButton( 
                        ft.icons.DOCUMENT_SCANNER,
                        icon_color= '#00000000', # OCULTA DE FORMA TRANSPARENTE EL BOTON
                        on_click=lambda x: self.log_read()
                    ),
                    expand=1,
                    alignment= ft.alignment.center_left
                ),
                ft.OutlinedButton("Cerrar", on_click=self.close_dlg ),
            ]

        if Content == False and text != '':
            Content = []
            Content.append( ft.Markdown( text ) )

        if Title == False:
            Title = []
            Title.append( ft.Text( title ) )



        self.dlg_modal = ft.AlertDialog(
            modal=modal, # Si el diálogo se puede descartar haciendo clic en el área de fuera de él.
            title= ft.Row( controls= Title, ),
            content= ft.Column( controls= Content, width = 480, spacing=10, alignment= ft.MainAxisAlignment.CENTER, tight=True, scroll= ft.ScrollMode.ALWAYS, ),
            actions= [ft.Row( controls= Actions )],
            actions_alignment=ft.MainAxisAlignment.END,
            #on_dismiss=lambda e: print("Modal dialog dismissed!"),
            inset_padding= ft.padding.symmetric( vertical= margen_vertical, horizontal= margen_horizontal ),
        )   

        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()



    def callback_for_dialog( self, x, *args, **kwargs ):
        try: 

            if kwargs:
            
                if 'bgcolor' in kwargs:
                
                    x.bgcolor =  kwargs['bgcolor']

                if 'style_bgcolor' in kwargs:
                
                    x.style.bgcolor =  kwargs['style_bgcolor']


                if 'color' in kwargs:
                
                    x.color =  kwargs['color']

  
                if 'value' in kwargs:

                    x.value = str( kwargs['value'] )


                if 'text' in kwargs:

                    x.text = str( kwargs['text'] )

                if 'key' in kwargs:

                    x.key = str( kwargs['key'] )


                if 'fun' in kwargs:

                    kwargs['fun']()

                

        except Exception as err:
            Logger.error( f"callback_for_dialog Unexpected {err=}, {type( err )=}" )


        self.dlg_modal.open = False
        self.dlg_modal = False
        self.page.update()



    

    def show_notify( self, msg = '', color = ft.colors.RED ):

        self.page.snack_bar = ft.SnackBar( ft.Text(f"{msg}"), bgcolor=color )
        self.page.snack_bar.open = True

        self.page.update()




    
    def open_camera( self ):
        
        try:

            cam = cv2.VideoCapture(0)

            self.MyCamera = True
            
            while True:

                ret, frame = cam.read()

                if not ret:
                    break

                if self.MyCamera == None:
                    
                    cam.release()
                    # AND CLOSE WINDOW WEBCAM IF FOUND TEXT FROM QRCODE
                    cv2.destroyAllWindows()
                    break
    
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                detector = cv2.QRCodeDetector()
                data,points,_ = detector.detectAndDecode(gray)
    
                # AND IF THE OPENCV FOUND YOU QR CODE AND GET TEXT FROM QRCODE
                if data:
                    
                    cv2.polylines(frame,[np.int32(points)],True,(255,0,0),2,cv2.LINE_AA)
                    print(f"QR Code YOu Data is : {data}")

                    self.qr_text = data

                    self.read_qr_text()
                    # AND PUSH TO TEXT WIDGET IF FOUND 
    
                    self.LeerQRCode.controls.append(
                        ft.Text(data,size=25,weight="bold")
                        )
                    self.page.update()
    
                    cam.release()
                    # AND CLOSE WINDOW WEBCAM IF FOUND TEXT FROM QRCODE
                    cv2.destroyAllWindows()

                    self.MyCamera = None
                    break
    
                    # AND IF YOU PRESS q IN WEBCAM WINDOW THEN CLOSE THE WEBCAM
                cv2.imshow("QR CODE DETECTION ",frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):

                    cam.release()
                    # AND CLOSE WINDOW WEBCAM IF FOUND TEXT FROM QRCODE
                    cv2.destroyAllWindows()

                    self.MyCamera = None
                    break
                    # STOP YOU WINDOW
                
            if self.MyCamera != None: 

                if cam.isOpened():

                    cam.release()
                    cv2.destroyAllWindows()

                    self.MyCamera = None
        
        except Exception as err:
            Logger.error( f"No se puede abrir el lectorQR Unexpected {err=}, {type( err )=}" )

            self.show_alert_dialog( text= f"No se puede abrir el lectorQR Unexpected {err=}, {type( err )=}", title='Error' )




    def read_qr_text( self ):

        if not self.qr_text == "":
                    
    
            #print( "YOu Qr is : ",self.qr_text )
            
            read = ast.literal_eval( self.qr_text ) # Se convierte de string a diccionario
            
            if 'patron_de_turnos' in read:
                
                Logger.info( 'Hay patron' )

                for nombre in read['patron_de_turnos']:

                    name = nombre.decode( 'utf-8' )

                    if not 'patron_de_turnos' in self.UserConfiguration:
                        self.UserConfiguration['patron_de_turnos'] = {}

                    self.UserConfiguration['patron_de_turnos'][name] = read['patron_de_turnos'][nombre]

                
            if 'turnos' in read:
                
                Logger.info( 'Hay turnos' )

                for Id in read['turnos']:

                    
                    read['turnos'][Id]['nombre'] = read['turnos'][Id]['nombre'].decode( 'utf-8' )
                    read['turnos'][Id]['siglas'] = read['turnos'][Id]['siglas'].decode( 'utf-8' )
                    t = read['turnos'][Id]

                    if not 'computo' in t:

                        t["computo"] = '0:0'
                    
                    if not 'nocturno' in t:

                        t["nocturno"] = '0:0'
                    
                    if not 'color' in t:

                        t["color"] = '#ffffff'
                    
                    if not 'userID' in t:
                    
                        t["userID"] = 0
                    
                    if not 'hora_ini' in t:

                        t["hora_ini"] = '0:0'
                    
                    if not 'hora_fin' in t:
                    
                        t["hora_fin"] = '0:0'
                    
                    if not 'colorGcal' in t:
                    
                        t["colorGcal"] = 0
                    

                    self.UserConfiguration['turnos'][Id] = t

            self.storage.set("configuration", self.UserConfiguration)


            self.listado_turnos_ddbb()

            self.page.go( '/crear_patron' )





    def file_json_to_store( self, fichero ):

        try:

            with open( fichero, 'r' ) as file:
            
                conf = json.load( file )
                name = os.path.basename( file.name )

                file_name_sin_extension = Path(name).stem

        except Exception as err:              
            Logger.error( f"Al leeer archivo Unexpected {err=}, {type( err )=}" )
            error = True
        
        else:

            try:
                
                #si el fichero es del tipo backup
                if name.find( 'backup.json' )>=0:
                
                    for file_name in conf:
                        
                        file_name_sin_extension = Path(file_name).stem

                        self.storage.set( file_name_sin_extension, conf[file_name] )

                        Logger.debug( f"Archivo {file_name_sin_extension} creado." )

                #si son ficheros sueltos del tipo json
                else:
                    
                    self.storage.set( file_name_sin_extension, conf )

                    Logger.debug( f"Archivo {file_name_sin_extension} restaurado." )

                
            except Exception as err:              
                Logger.error( f"al crear archivo Unexpected {err=}, {type( err )=}" )
                error = True

        return error


    
    def ayuda( self, *args ):

        
        current = self.page.route

        troute = TemplateRoute(self.page.route)
        
        try:
               
            contentMain = []

            if current == '/':

                text = ["Para personalizar un día tocar dos veces en el día que desee y se abrirá el panel detallado.",
                        "Si al lado del día aparece alguno de los siguientes simbolos quiere decir que:",
                        "__*__, El día tiene un comentario.",
                        "__+__, El día tiene horas extra.",
                        "__F__, El día es festivo.",
                        "Si aparece el simbolo  __-__  con el fondo blanco, es porque hay un turno asignado que se ha eliminado. Esto ocurre si ha personalizado un turno y ha restablecido la configuracion de la aplicación."]
                
            elif current == '/stats':

                text = ["Todos los valores que aparecen separados por dos puntos, el primer valor son horas y el segundo minutos horas:minutos.",
                        "__Convenio__, es el valor asignado en el perfil, pero si tocas sobre las horas en las estadísticas las puedes personalizar para cada año, son el total de horas anuales que hay que trabajar, horas:minutos",
                        "__Computo__, es el valor total de horas:minutos anuales o mensuales",
                        "__DifConvenioAnioAnterior__, es el resultado de horas del año anterior ( DiferenciaConvenio )",
                        "__DiferenciaConvenio__, si es positiva son las horas a favor, o si es negativa se le deben a la empresa.",
                        "Si no has trabajado un año completo, debes hacer el cálculo de horas que debes trabajar ese año y cambiar el convenio tocando sobre él."]
            
            elif current == '/sync_g_calendar':

                text = ["Seleccione el año que quiere tener en Google Calendar.",
                        "Seleccione el mes, si quiere que sea el año entero elija 0.",
                        "Ahora pulse en Sync y espere que se complete el proceso, el año completo puede tardar unos minutos."]
            

            elif current == '/perfil':   
                

                text = ["__Horas Convenio__, es el total de horas y minutos que se deben trabajar al año.",
                        "Puede elegir si el resultado de Diferencia Convenio Año Anterior se sume o no a las horas Convenio.", 
                        "Si desea acumular el resultado año tras año debe estar marcado.",
                        "__Sincronizar con Google Calendar__",
                        "Su calendario por defecto de google es su correo electronico.",
                        "Puede crear uno exclusivo para esta aplicacion, por ejemplo llamelo planilla, si no sabe como hacerlo, seleccione su correo.",
                        "Si ha decidido crear un calendario exclusivo, una vez creado vuelva aquí y seleccione su calendario.",
                        "Luego active Sincronizar con google y ya le aparecera en el menu ( Sync G. Calendar ) para sincronizar un mes o un año completo de forma manual.",
                        "Si la sincronizacion esta activa y el ID del calendario seleccionado, cada vez que edita un día o crea un patrón este se sincronizará con nuestro calendario de google de forma automatica.",
                        ]
            elif current == '/backup':

                text = ["__Copias de seguridad__"]

                text.append( f"Los archivos tienen el nombre de la fecha y hora de creación, seguido de __backup.json__." )

                text.append( f"Las copias de seguridad se guardan en: {PATH_HOME}" )
                text.append( f"Para restaurar una copia de seguridad seleccionar el archivo __backup.json__ de la carpeta: {PATH_HOME}" )
            
                text.append( f"__Limpiar base de datos__" )
                text.append( f"Sirve para reducir el tamaño de la base de datos, y eliminar datos redundantes." )
                
                text.append( f"__Restablecer años__" )
                text.append( f"Sirve para eliminar la base de datos completa, sin modificar la configuracion del perfil y los turnos." )

                text.append( f"__Restablecer configuración__" )
                text.append( f"Sirve para restablecer la configuración por defecto de la aplicación, sin modificar los años. __CUIDADO__ si has personalizado los turnos se perdera la configuración." )


            elif current == '/crear_patron':

                text = ["Para crear un patron lo primero es agregar los turnos en el orden deseado pulsando en elegir turno y luego en el simbolo __+__, recuerda indicar los días libres.",
                        "Si se a equivocado en un turno, pulsando sobre él se puede eliminar del patrón.",
                        "Una vez completado el ciclo, indica la fecha de inicio y de fin.",
                        "Ahora pulsa sobre el botón ( __Crear__ ), si el patron se ha creado correctamente recibira un mensaje como:",
                        "Se ha creado el patrón desde el",
                        f"['1', '2', '{datetime.now().year}'] al ['31', '12', '{datetime.now().year +1}']",
                        "Puede reiniciar el fromulario pulsando sobre el botón __Limpiar__."]
            
            elif current == '/turnos_edit':

                text = ["Indica el nombre del turno.",
                        "Las __Siglas__, del turno se recomienda entre 1 y 2 caracteres.",
                        "El __Computo__, son las horas que cuentan como trabajadas.",
                        "__Nocturno__, son las horas que cuentan como nocturnidad.",
                        "__Entrada__, es la hora de entrada.",
                        "__Salida__, es la hora de salida.",
                        "__Entrada y Salida__, no se utilizan para las estadisticas.",
                        "__Color__, el color que representa al turno en el calendario.",
                        "__Color G. Calendar__, son los colores disponibles de Google Calendar, este color solo se visualiza si se sincroniza el turno con nuestro calendario de google, se debe activar en Mi Perfil.",
                        "__Mostrar en google calendar__ si esta marcado y la sincronizacion esta activada en Mi Perfil, este turno se sincronizará, si no se marca este trurno, aun que esté la sincronización activa en el perfil no aparecera en Google Calendar."]


            elif troute.match("/detalle/year/:year/month/:month/day/:day"):

                text = ["__Turno__, son aquellos que se suman al computo total.",
                        "__Turno Extra__, no se suma al computo total, solo aparece en las estadísticas el total de horas de los turnos extras.",
                        "__Horas y Minutos Extra__, pasa igual que con Turno Extra no se suman al computo total.",
                        "__Comentario__, aqui puedes poner la informacion que sea, por ejemplo porque hiciste horas extra.",
                        "__Festivo__, si este dia lo marcas como festivo, aparecera en las estadísticas el total de dias festivos trabajados y en el dia del mes en el calendario aparecera la letra __F__.",
                        "Las horas y Minutos que se sumarán a las estadísticas son las configuradas para cada Turno"]  

                """
            elif current == '/info_version':
                
                text = [f"Sistema Operativo: {sistema}"]

                if sistema == 'android':
                    text.append( f"Verison de API: {api_version}" )
                """
            elif current == '/compartir_qr':

                text = ["Escanea con el Lector QR de la aplicacion que quiera recibir este patron de turnos.",
                        "El QR __Compartir patrón__, comparte el patrón unicamente, si ha modificado los turnos, tambien deberá escanear el QR __Compartir turnos del patrón__."] 

            elif current == '/leer_qr':

                text = ["Escanea el QR de la aplicacion que quiera recibir el patron de turnos."]  
                
            else:

                text = ["No hay nada para mostrar aquí."]

            for i in text:

                contentMain.append( ft.Markdown( 
                            value= str( i ),
                        ))
                #label.bind( on_release=lambda _, x=button, num=i: self.callback_for_dialog( x, num ) )


            self.show_alert_dialog( Content=contentMain, title=f"Ayuda {self.page.title}", modal = False )

        except Exception as err:
            Logger.error( f"ayuda Unexpected {err=}, {type( err )=}" )
        