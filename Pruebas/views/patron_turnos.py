import flet as ft

from Logger_Path import Path, Logger, PATH

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
from custom.GoogleCalendar import MyGoogleCalendar
from custom.GoogleCalendarSetup import get_token_google
from custom.datepicker import DatePicker

from datetime import datetime, timedelta


QRCODE_IMPORT = False
LECTOR_QR_IMPORT = False

try:
    # FOR INSTALL USE pip install qrcode
    import qrcode
    import base64
    from io import BytesIO

    QRCODE_IMPORT = True
    
except Exception as err:
    Logger.error( f"qrcode import Unexpected {err=}, {type( err )=}" )

try:
    # INSTALL YOU OPENCV WITH PIP - lector qr
    import numpy as np
    import cv2
    import ast

    LECTOR_QR_IMPORT = True

except Exception as err:
    Logger.error( f"lector qr import Unexpected {err=}, {type( err )=}" )





class PagePatronTurnos( App, ft.View, ddbb ):

    ProgressBarSyncGCal = ft.ProgressBar( value=0, width=400 )

    patron_de_turnos = []

    ImagenQRCodePatron = ft.Icon( ft.icons.QR_CODE )

    ImagenQRCodeTurnos = ft.Icon( ft.icons.QR_CODE )

    MyCamera = None


    def __init__(self, page = ft.Page ):
        super().__init__(page)

        self.page = page

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        self.scroll= ft.ScrollMode.ALWAYS
        self.expand = 1
        self.padding = 5



    def view_patron( self ):

        ContenedorPrincipal = ft.Column( width = 480, spacing = 15, ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa


        CardConfigPatronTurnos = ft.Column()
        
        CardConfigPatronTurnos.controls.append( 
            ft.Row(
                [
                    ft.Container( content= ft.Text( 'Elegir Turno', weight='BOLD', size=16, expand=1 ), alignment= ft.alignment.center_left, expand=1 ),
                    ft.Container( content= ft.Text( 'Agregar al patron', weight='BOLD', size=16, expand=1 ), alignment= ft.alignment.center_right, expand=1 )
                ],
            )
        )
        
        RowElegirTurnoPatronTurnos = ft.Row()

        CardConfigPatronTurnos.controls.append( RowElegirTurnoPatronTurnos )

        

        self.TurnosSelectPatronTurnos = ft.TextButton( 
                text= "Ninguno", 
                expand=1,
                key = 0,
                style = ft.ButtonStyle(
                    bgcolor= ft.colors.WHITE,
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
            )
        
        self.TurnosSelectPatronTurnos.on_click = lambda x, instance = self.TurnosSelectPatronTurnos: self.listado_turnos( instance = instance, ventana = '/crear_patron', titulo_retorno =  self.page.title, modal = False )


        RowElegirTurnoPatronTurnos.controls.append( ft.Container(
            content= self.TurnosSelectPatronTurnos,
            expand=4
        ) )

        
        RowElegirTurnoPatronTurnos.controls.append( ft.Container(
            content= ft.IconButton( 
                icon= ft.icons.ADD_CIRCLE, 
                #icon_color='RED', 
                icon_size=40, 
                on_click= lambda x: self.agregar_al_patron()
            ),
            expand=1
        ) )


        RowFechasInicioPatronTurnos = ft.Row()

        CardConfigPatronTurnos.controls.append( RowFechasInicioPatronTurnos )

        
        RowFechaFinPatronTurnos = ft.Row()

        CardConfigPatronTurnos.controls.append( RowFechaFinPatronTurnos )





        date_picker = DatePicker(
            page= self.page,
        )



        self.FechaInicioPatronTurnos = ft.TextField(
            value='',
            label="Fecha de inicio", 
            hint_text="D-M-YYYY",
            tooltip = 'Introduce aquí la fecha de inicio para el patron de turnos.',
            multiline=False,
            expand=1,
            text_align= ft.TextAlign.CENTER,
            )
        #self.FechaInicioPatronTurnos.on_focus= lambda _, x = self.FechaInicioPatronTurnos: date_picker.pick_date( x )
        
        RowFechasInicioPatronTurnos.controls.append( ft.Row(
            controls= [
                ft.IconButton( icon=ft.icons.TODAY, on_click= lambda _, x = self.FechaInicioPatronTurnos: date_picker.pick_date( x ) ),
                self.FechaInicioPatronTurnos,
            ],
            expand=1
        ) )
        

        self.FechaFinPatronTurnos = ft.TextField(
            value='',
            label="Fecha de fin", 
            hint_text="D-M-YYYY",
            tooltip = 'Introduce aquí la fecha de fin para el patron de turnos.',
            multiline=False,
            expand=1,
            text_align= ft.TextAlign.CENTER,
            )
        
        RowFechaFinPatronTurnos.controls.append( ft.Row(
            controls= [
                ft.IconButton( icon=ft.icons.TODAY, on_click= lambda _, x = self.FechaFinPatronTurnos: date_picker.pick_date( x ) ),
                self.FechaFinPatronTurnos,
            ],
            expand=1
        ) )


        ContenedorPrincipal.controls.append( ft.Card( content= ft.Container( content= CardConfigPatronTurnos, padding=10 ) ) )




        self.CardPatronPatronTurnos = ft.GridView( expand=1, runs_count=7, spacing=5, run_spacing=5, )

        ContenedorPrincipal.controls.append( ft.Card( 
            content= ft.Container( 
                content= self.CardPatronPatronTurnos, 
                padding=10,
                expand=1,
                ),
            ) 
        )


        ContenedorPrincipal.controls.append( 
            ft.Card( 
                content= ft.Container( 
                    content= ft.Row(
                        [
                            ft.OutlinedButton( text= 'Limpiar', icon= ft.icons.CLEANING_SERVICES, icon_color= ft.colors.RED, expand=1,
                            on_click=lambda x: self.borrar_del_patron_de_turnos(),    
                            ),
                            ft.FilledButton( text= 'Crear', icon= ft.icons.SAVE, expand=1,
                            on_click=lambda x: self.crear_patron_de_turnos(),    
                            ),
                        ]
                    ), 
                    padding=10,
                ) 
            ) 
        )


        #return ContenedorPrincipal

        self.route= "/crear_patron"
        self.controls.append( ft.Container( content = ContenedorPrincipal, padding=15 ) )

        self.page.views.append(self)

        self.page_patron_de_turnos()

        self.page.update()





    def view_qrcode( self ):

        ContenedorPrincipal = ft.Column( spacing = 20 ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa
        
        ContenedorPrincipal.controls.append( ft.Container( height=10 ) )

        ContenedorPrincipal.controls.append( ft.Text( "Compartir Patrón.", weight='BOLD',  ) )

        ContenedorPrincipal.controls.append( self.ImagenQRCodePatron )
            
        ContenedorPrincipal.controls.append( ft.Container( height=10 ) )

        ContenedorPrincipal.controls.append( ft.Text( "Compartir Turnos del patrón.", weight='BOLD',  ) )

        ContenedorPrincipal.controls.append( self.ImagenQRCodeTurnos )    
        
        ContenedorPrincipal.controls.append( ft.Container( height=10 ) )

        return ContenedorPrincipal
        self.route= "/compartir_qr"
        self.controls.append( ContenedorPrincipal )

        self.page.views.append(self)




    def view_lectorQR( self ):

        ContenedorPrincipal = ft.Column( width = 480, spacing = 15, ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa

        self.LeerQRCode = ft.Column()
        
        ContenedorPrincipal.controls.append( self.LeerQRCode )    

        #return ContenedorPrincipal
        self.route= "/leer_qr"
        self.controls.append( ft.Container( content = ContenedorPrincipal, padding=20 ) )

        self.page.views.append(self)

        self.page.update()

        self.open_camera()




    def page_patron_de_turnos( self ):

        self.TextTitle.value = self.page.title = "Crear Patrón de Turnos"
    
        TurnoSelectPatron = self.TurnosSelectPatronTurnos
        TurnoSelectPatron.text='Ninguno'
        TurnoSelectPatron.key = '0'
        TurnoSelectPatron.style.bgcolor = '#ffffff'

        self.FechaInicioPatronTurnos.value = ''
        self.FechaFinPatronTurnos.value = ''

        if 'patron_de_turnos' in self.UserConfiguration:

            if self.UserConfiguration['patron_de_turnos'] != {}:

                self.listado_patrones_guardados_dialog()
        
        self.page.update()
        


    
    def agregar_al_patron( self ):
        
        patron = self.CardPatronPatronTurnos
        sigla = int( self.TurnosSelectPatronTurnos.key )


        if sigla >=0:

            ID_Array_Turno = str( sigla )

            turno = self.ListadoTurnos[ID_Array_Turno]
            sigla = str( turno['siglas'] )

            id= len( self.patron_de_turnos )

            self.create_btn_patron_turnos( patron, turno, id )

            self.patron_de_turnos.append( turno['ID'] )

            Logger.debug( 'Turno agregado al array, ' + str( sigla ) + ' Array='+str( self.patron_de_turnos ) )
        else:
            Logger.debug( 'Este turno no se puede seleccionar para el patron, ' + sigla )
            self.show_alert_dialog( text=str( 'Este turno no se puede seleccionar para el patron, ' + sigla ), title='Error' )

    


    def borrar_del_patron_de_turnos( self, data='False' ):

        patron = self.CardPatronPatronTurnos
        patron.controls.clear()
        
        new = []

        total_patron = len( self.patron_de_turnos )

        if data != 'False':
            #Logger.warning( 'Eliminar la posicion ' + str( data ) )
            
            if total_patron > 1:

                for i in range( total_patron ):

                    if i != data:

                        id = len( new )
                        new.append( self.patron_de_turnos[i] )
                        
                        ID_Array_Turno= self.patron_de_turnos[i]
                        if ID_Array_Turno >= 0:

                            turno = self.ListadoTurnos[ str(ID_Array_Turno) ]
                            sigla = str( turno['siglas'] )

                            
                            self.create_btn_patron_turnos( patron, turno, id, reload = False )

            else:
                self.FechaInicioPatronTurnos.value = ''
                self.FechaFinPatronTurnos.value = ''
                new = []

            self.patron_de_turnos = new
            
            Logger.debug( 'Patron de turnos ' + str( new ) )

        else:
            
            self.patron_de_turnos = []
            self.FechaInicioPatronTurnos.value = ''
            self.FechaFinPatronTurnos.value = ''

            TurnoSelectPatron = self.TurnosSelectPatronTurnos
            TurnoSelectPatron.text='Ninguno'
            TurnoSelectPatron.key = '0'
            TurnoSelectPatron.style.bgcolor = '#ffffff'

            Logger.debug( 'Patron de turnos vaciado' + str( self.patron_de_turnos ) )
            self.show_alert_dialog( text=str( 'Patron de turnos vaciado.' ), title='Patrón de Turnos' )
    

        self.page.update()



    
    def create_btn_patron_turnos( self, patron, turno, id, reload = True ):

        #width = ( self.page.window_width ) - 30
        #width = ( width/7 ) - 5


        patron.controls.append( 
            ft.TextButton( 
                text = turno['siglas'], 
                on_click = lambda x, id=id: self.borrar_del_patron_de_turnos( id ), 
                #data= { 'id': id, 'turno': turno }, 
                content = ft.Stack(
                    controls= [
                        ft.Container( 
                            content= ft.Text( turno['siglas'], scale= 1.2, ),
                            alignment= ft.alignment.center
                        ),
                        ft.Container( 
                            content= ft.Icon( 
                                ft.icons.CLOSE,
                                scale= 0.5,
                            ),
                            #alignment= ft.alignment.top_right
                            top = -5,
                            right = -5,
                        )
                    ],
                ),
                style = ft.ButtonStyle(
                    padding=0,
                    bgcolor= turno['color'],
                    color=ft.colors.BLACK,
                    shape={
                        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                    },
                ) 
            )
        )

        if reload == True:
            self.page.update()



    
    def crear_patron_de_turnos( self ):

        fecha_ini = self.FechaInicioPatronTurnos.value
        fecha_fin = self.FechaFinPatronTurnos.value

        fecha_ini = fecha_ini.split( '-' )
        fecha_fin = fecha_fin.split( '-' )

        Actions = []

        if len( self.patron_de_turnos ) > 0 and len( fecha_ini ) == 3 and len( fecha_fin ) == 3:

            try:

                inicio = datetime( int( fecha_ini[2] ),int( fecha_ini[1] ),int( fecha_ini[0] ) )
                fin    = datetime( int( fecha_fin[2] ),int( fecha_fin[1] ),int( fecha_fin[0] ) )
                
                if inicio > fin:
                    Logger.error( f"Fecha inicio > fin" )
                    self.show_alert_dialog( text=str( 'Error la fecha de inicio debe ser mayor a la de fin' ), title='Error' ) 
                    return
                
            except Exception as err:     

                Logger.error( f"Fecha Unexpected {err=}, {type( err )=}" )
                self.show_alert_dialog( text=str( 'Error en las fechas' ), title='Error' ) 

            else:

                lista_fechas = [( inicio + timedelta( days=d ) ).strftime( "%d-%m-%Y" ) for d in range( ( fin - inicio ).days + 1 )] 

                cont = 0
                for dia in lista_fechas:

                    fecha = dia.split( '-' )

                    day = int( fecha[0] )
                    month = int( fecha[1] )
                    year = int( fecha[2] )

                    try:
                        ID_Turno =self.patron_de_turnos[cont]
                        
                    except Exception as err:    

                        Logger.error( f"patron_de_turnos Unexpected {err=}, {type( err )=}" )
                        return 'Error patron_de_turnos'
                
                    if year != '' and month != '' and day != '':

                        try:
                            
                            existe = 3

                            if str( year ) not in self.DataYears:
                                self.DataYears[str( year )] = {}
                                existe-=1
                    
                            if str( month ) not in self.DataYears[str( year )]:
                                self.DataYears[str( year )][str( month )] = {}
                                existe-=1
                    
                            if str( day ) not in self.DataYears[str( year )][str( month )]:
                                self.DataYears[str( year )][str( month )][str( day )] = {}
                                existe-=1

                            #reseteos
                            comentario = ''
                            turnoDoble = 0
                            horasExtras = '0:0'
                            color = ''

                            if existe == 3:

                                detalles_dia = self.DataYears[str( year )][str( month )][str( day )]

                                if 'comentario' in detalles_dia:
                                    comentario = detalles_dia['comentario']
                                
                                if 'turnoDoble' in detalles_dia:
                                
                                    turnoDoble = detalles_dia['turnoDoble']
                                
                                if 'horasExtras' in detalles_dia:
                                
                                    horasExtras = detalles_dia['horasExtras']
                                
                                if 'color' in detalles_dia:
                                
                                    color = detalles_dia['color']

                                


                            self.DataYears[str( year )][str( month )][str( day )] = {
                                'anio': int( year ), 
                                'mes': int( month ), 
                                'dia': int( day ), 
                                'turno': int( ID_Turno )
                                }
                            

                            if int( turnoDoble ) != 0:
                                self.DataYears[str( year )][str( month )][str( day )]['turnoDoble'] = int( turnoDoble )
                                
                            if str( horasExtras ) != '0:0':    
                                self.DataYears[str( year )][str( month )][str( day )]['horasExtras'] = str( horasExtras ) 
                                
                            if comentario != '':    
                                self.DataYears[str( year )][str( month )][str( day )]['comentario'] = str( comentario )
                                
                            if color != '':    
                                self.DataYears[str( year )][str( month )][str( day )]['color'] = str( color )
                                
                            if int( self.UserConfiguration['ID'] ) != 0:   
                                self.DataYears[str( year )][str( month )][str( day )]['userID'] = int( self.UserConfiguration['ID'] )
                                
 

                        except Exception as err:              
                            Logger.error( f"data_anios Unexpected {err=}, {type( err )=}" )
                            return 'Error en la funcion crear_patron_de_turnos -> data_anios'



                    if len( self.patron_de_turnos )-1 == cont:
                        cont=0
                    else:
                        cont+=1

                self.storage.set( "years", self.DataYears )
                #self.show_alert_dialog( text=str( f"Se ha creado el patron desde el {fecha_ini} al {fecha_fin}" ), title='' )



                contentMain = []

                contentMain.append( 
                    ft.Text( 
                            value= str( f"Se ha creado el patron desde el {fecha_ini} al {fecha_fin}" ),
                        )
                    )

                #Pregunta si se quiere guardar el patron o no si el patron tiene mas de un turno
                if len( self.patron_de_turnos ) > 1:

                    contentMain.append( 
                        ft.Text( 
                                value= str( f"¿Quieres guardar para reutilizar otra vez este patron?" ),
                            )
                        )
                    

                    instace_nombre = ft.TextField( 
                        
                        label='Nombre del patrón',
                    )
                                    

                    contentMain.append( instace_nombre )

                    btn_si = ft.FilledButton( 
                        icon= "content-save-move",
                        text= 'Si',
                        on_click = lambda x, name= instace_nombre, fecha_ini=fecha_ini: self.guardar_patron_de_turnos( name, fecha_ini )
                    )
                    

                    btn_no = ft.FilledButton( 
                        icon= "calendar-month",
                        text= 'No',
                        on_click = lambda x, fecha_ini=fecha_ini: self.no_guardar_patron_de_turnos( fecha_ini )
                    )

                    Actions.append( btn_si )
                    Actions.append( btn_no )
                
                else:
                    self.no_guardar_patron_de_turnos( fecha_ini )


                if self.UserConfiguration['GcalendarID'] != '' and self.SYNC_GOOGLE:

                    progressMax = 0
                    
                    self.list_cal_anio = {}

                    for dia in lista_fechas:

                        fecha = dia.split( '-' )

                        day = int( fecha[0] )
                        month = int( fecha[1] )
                        year = int( fecha[2] )

                    
                        if  not ( str( year ) in self.list_cal_anio ):

                            self.list_cal_anio[str( year )] = {}

                        if  not ( str( month ) in self.list_cal_anio[str( year )] ):

                            progressMax += int( self.total_dias_anio_calendar( year, month ) )

                            self.list_cal_anio[str( year )][str( month )] = self.listado_calendar_ddbb( month, year )

                                

                    self.progressMax = str( progressMax )
                    self.ProgressBarSyncGCal.value = 0
                    self.progress = 0

                    for anio in self.list_cal_anio:
                        
                        for mes in self.list_cal_anio[str( anio )]:


                            if len( self.list_cal_anio[str( anio )][str( mes )] )>0:
                                """ Sincronizar el patron con google calendar """
                                #Thread( target=self.sync_events,  kwargs={'mes': str( mes ), 'year': str( anio )} ).start()


                
                self.show_alert_dialog( Content=contentMain, Actions=Actions, title='' )

        else:
            Logger.error( 'Debe rellenar los campos de fecha y al menos insertar un turno' )
            self.show_alert_dialog( text=str( 'Debe rellenar los campos de fecha y al menos insertar un turno' ), title='Error' )




    def guardar_patron_de_turnos( self, instance_nombre, fecha_ini ):

        nombre = instance_nombre.value

        if 'patron_de_turnos' in self.UserConfiguration:

            self.UserConfiguration['patron_de_turnos'][nombre] = self.patron_de_turnos

        else:
            self.UserConfiguration['patron_de_turnos'] = {}

            self.UserConfiguration['patron_de_turnos'][nombre] = self.patron_de_turnos

            
        #print( self.UserConfiguration['patron_de_turnos'] )

        self.storage.set( "configuration", self.UserConfiguration )

        FechaSeleccionada=datetime( int( fecha_ini[2] ),int( fecha_ini[1] ),int( fecha_ini[0] ) )

        self.page.session.set( "FechaSeleccionada", FechaSeleccionada )

        self.borrar_del_patron_de_turnos()

        self.page.go( '/' )



    
    def listado_patrones_guardados_dialog( self ):

        try:
            
            contentMain = []
            
            if 'patron_de_turnos' in self.UserConfiguration:
                self.UserConfiguration['patron_de_turnos']

            patron_de_turnos = self.UserConfiguration['patron_de_turnos']

            for i in patron_de_turnos:

                layout = ft.Row()

                cargar = ft.Container(
                    content= ft.Markdown( 
                        value='__' + str( i ) + '__',            
                    ),
                    expand=1,
                    on_click=lambda _, name=i: self.cargar_patron_guardado( name )
                )
                eliminar = ft.IconButton( 
                    icon= "delete",
                    on_click=lambda _, name=i: self.eliminar_patron_guardado( name ),
                    icon_color = 'RED'
                )

                if QRCODE_IMPORT == True:

                    compartir = ft.IconButton( 
                        icon= ft.icons.SHARE,
                        on_click=lambda _, name=i: self.compartir_patron_guardado( name )
                    )
                
                    layout.controls.append( compartir )
                    
                layout.controls.append( cargar )
                layout.controls.append( eliminar )
                contentMain.append( layout )

            self.show_alert_dialog( Content=contentMain, title='Seleccione un Patron'  )

        except Exception as err:
            Logger.error( f"listado_patrones_guardados_dialog Unexpected {err=}, {type( err )=}" )


        self.page.update()

    
    def cargar_patron_guardado( self, nombre ):

        patron = self.CardPatronPatronTurnos
        patron.controls.clear()

        self.patron_de_turnos = self.UserConfiguration['patron_de_turnos'][nombre]

        total_patron = len( self.patron_de_turnos )

        if total_patron > 0:

            for i in range( total_patron ):
                
                #Se comprueba si la Id del turno guardado en el patron sigue existiendo como turno o se a eliminado,
                # en el caso de haber eliminado se muestra el turno 0 o turno en blanco para no probocar error
                if str(self.patron_de_turnos[i]) in self.ListadoTurnos:

                    ID_Array_Turno = self.patron_de_turnos[i]

                else:
                    ID_Array_Turno = 0

                if ID_Array_Turno >= 0:

                    turno = self.ListadoTurnos[ str(ID_Array_Turno) ]
  
                    self.create_btn_patron_turnos( patron, turno, i , reload = False )


        self.dlg_modal.open = False
        self.page.update()





    def eliminar_patron_guardado( self, nombre ):
        
        if nombre in self.UserConfiguration['patron_de_turnos']:

            self.UserConfiguration['patron_de_turnos'].pop( nombre )

            if 'patron_de_turnos' in self.UserConfiguration:

                if self.UserConfiguration['patron_de_turnos'] != {}:

                    self.listado_patrones_guardados_dialog()
                
                else:

                    self.dlg_modal.open = False
                    self.page.update()

            self.storage.set( "configuration", self.UserConfiguration )



    def create_qr(self, s):
        
        try:
            
            qr = qrcode.QRCode( version = 1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size = 20, border = 1 )
            qr.add_data( s )
            qr.make( fit = True )
            img = qr.make_image( fill = 'black', back_color = 'white' )
            
            buffered = BytesIO()
        
            # SAVE IMAGE QRCODE TO JPEG OR WHATEVER
            img.save( buffered, format="JPEG" )
            s1 = base64.b64encode( buffered.getvalue() )
            resultOfQrCode = s1.decode("utf-8")
        
            return (resultOfQrCode)

            
        except Exception as err:
            
            Logger.error( f"al crear QR {err=}, {type( err )=}" )
            return False



    def compartir_patron_guardado( self, nombre ):

        
        data = {}

        if nombre in self.UserConfiguration['patron_de_turnos']:
            
            name = nombre.encode( 'utf-8' )

            data['patron_de_turnos'] = {}
            data['patron_de_turnos'][name] = self.UserConfiguration['patron_de_turnos'][nombre]
            data['turnos'] = {}

            for turno in self.UserConfiguration['turnos']:

                t = self.UserConfiguration['turnos'][str( turno )]
                t_clear = {}

                if int( turno ) in data['patron_de_turnos'][name]:#si el turno no esta en el patron a compartir no se comparte

                    if t != {}:# para turnos eliminados

                        t_clear["ID"] = t["ID"]
                        
                        t_clear["nombre"] = t["nombre"].encode( 'utf-8' )

                        t_clear["siglas"] = t["siglas"].encode( 'utf-8' )
                        
                        if t["computo"] != '0:0':

                            t_clear["computo"] = t["computo"]
                        
                        if t["nocturno"] != '0:0':

                            t_clear["nocturno"] = t["nocturno"]
                        
                        if t["color"] != '#ffffff':

                            t_clear["color"] = t["color"]
                        
                        if t["userID"] != 0:

                            t_clear["userID"] = t["userID"]
                        
                        if t["hora_ini"] != '0:0':

                            t_clear["hora_ini"] = t["hora_ini"]
                        
                        if t["hora_fin"] != '0:0':

                            t_clear["hora_fin"] = t["hora_fin"]
                        
                        if t["colorGcal"] != 0:

                            t_clear["colorGcal"] = t["colorGcal"]
                        
                        if 'mostrar_g_calendar' in t and t["mostrar_g_calendar"] != False:

                            t_clear["mostrar_g_calendar"] = t["mostrar_g_calendar"]

                        data['turnos'][str( turno )] = t_clear

            img_qr_patron = ''
            img_qr_turnos = ''   

            try:
                
                img_qr_patron = self.create_qr( data['patron_de_turnos'] )

                img_qr_turnos = self.create_qr( data['turnos'] )

            except Exception as err:

                Logger.error( f"al crear QR {err=}, {type( err )=}" )
            else:

                Logger.debug( f"Data: {str( data )}" )
                Logger.info( f"Compartiendo el patron de turnos { str( nombre ) }." )

                #Mostramos el QR en pantalla
                if img_qr_patron:
                    
                    self.ImagenQRCodePatron = ft.Image( src_base64 = img_qr_patron, tooltip= f"QR para compartir el patrón de turnos, {nombre}" )
                
                #Mostramos el QR en pantalla
                if img_qr_turnos:
                    
                    self.ImagenQRCodeTurnos = ft.Image( src_base64 = img_qr_turnos, tooltip= f"QR para compartir el los turnos del patrón, {nombre}" )
                


                self.show_alert_dialog( Content= [ self.view_qrcode() ], title=f"{nombre}" )





    
    def no_guardar_patron_de_turnos( self, fecha_ini ):
        
        #Se limpia el patron creado
        self.patron_de_turnos = []
        self.FechaInicioPatronTurnos.value = ''
        self.FechaFinPatronTurnos.value = ''

        patron = self.CardPatronPatronTurnos
        patron.controls.clear()

        FechaSeleccionada = datetime( int( fecha_ini[2] ),int( fecha_ini[1] ),int( fecha_ini[0] ) )

        self.page.session.set( "FechaSeleccionada", FechaSeleccionada )

        self.borrar_del_patron_de_turnos()

        self.page.go( '/' )

        self.dlg_modal.open = False
        self.page.update()
    




