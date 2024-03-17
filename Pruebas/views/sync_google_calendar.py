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


from datetime import datetime


class PageSyncGCalendar( App, ft.View, ddbb ):

    FechaSeleccionadaHoy = datetime.now()

    ProgressBarSyncGCal = ft.ProgressBar( value=0, width=400 )


    def __init__(self, page = ft.Page, year = FechaSeleccionadaHoy.year, month = FechaSeleccionadaHoy.month ):
        super().__init__(page)

        self.page = page

        self.AñoSeleccionada = year
        self.MesSeleccionada = month

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER


        if not self.page.session.contains_key( "FechaSeleccionada" ):

            self.page.session.set( "FechaSeleccionada", self.FechaSeleccionada )
        
        else:

            self.FechaSeleccionada = self.page.session.get( "FechaSeleccionada" )

        self.view_sync()



    def view_sync( self ):

        ContenedorPrincipalPageSyncGCalendar = ft.Column( expand=1, width = 480, spacing = 10, scroll=True ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa
        
        ContenedorPrincipalPageSyncGCalendar.controls.append( ft.Container(
            content= ft.Text( 'Para mostrar todo el año seleccionar mes 0:', weight='BOLD' ),
        ) )

        RangeYears = self.range_anios_en_ddbb()

        self.AnioSync = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range( RangeYears[0], RangeYears[1] )
            ],
            label = 'Año',
            tooltip = 'Año para sincronizar en google calendar.',
            value = self.AñoSeleccionada,
            expand=1,
        )

        self.MesSync = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(13)
            ],
            label = 'Mes',
            tooltip = 'Mes para sincronizar en google calendar.',
            value = self.MesSeleccionada,
            expand=1,
        )
        ContenedorPrincipalPageSyncGCalendar.controls.append( ft.Row(
            [
                self.AnioSync,
                self.MesSync,
            ],
        ) )
        
        self.BtnSyncGCalendar = ft.ElevatedButton(
                    text="Sync",
                    on_click= lambda x: self.sync_g_cal(),
                    disabled= False,
                )
        
        ContenedorPrincipalPageSyncGCalendar.controls.append( 
            ft.Container(
                content= self.BtnSyncGCalendar ,
                alignment = ft.alignment.center_right,
                margin=10,
            ) )
        
        ContenedorPrincipalPageSyncGCalendar.controls.append( ft.Container( height=10 ) )
        #self.ListadoSyncGCalendarColumn = ft.Column( height=200, spacing = 10, )

        ContenedorPrincipalPageSyncGCalendar.controls.append( self.ProgressBarSyncGCal )
        
        self.ProgressBarText = ft.Text( value='', )
        
        ContenedorPrincipalPageSyncGCalendar.controls.append( self.ProgressBarText )

        #return ContenedorPrincipalPageSyncGCalendar
    
        self.route= "/sync_g_calendar"
        self.controls.append( ContenedorPrincipalPageSyncGCalendar )

        self.page.views.append(self)

        self.add_fechas_g_cal()





    def sync_events( self, **kawars ):
        #se instancia de nuevo GCal() en cada llamada a la funcion sync_events(), para no sobre escribir cuando hay varios hilos ejecutados
        
        G_Cal = MyGoogleCalendar()
        G_Cal.PATH = self.GCal.PATH
        G_Cal.SYNC_GOOGLE = self.GCal.SYNC_GOOGLE
        G_Cal.calendarId = self.GCal.calendarId
        G_Cal.BORRAR_TODOS_EVENTOS_DEL_DIA = self.GCal.BORRAR_TODOS_EVENTOS_DEL_DIA

        self.BtnSyncGCalendar.disabled = True
        self.BtnSyncGCalendar.text = 'Sincronizando...'
        self.BtnSyncGCalendar.update()

        self.page.update()

        lista_mes_sync = {}
        
        if 'year' in kawars and 'mes' in kawars:

            year = kawars['year']

            mes = kawars['mes']

            lista_mes_sync = self.list_cal_anio[str( year )][str( mes )]

            if len( lista_mes_sync ) == 0:
                Logger.info( 'No hay datos que mostrar para este mes.' )
                
                self.BtnSyncGCalendar.disabled = False
                self.BtnSyncGCalendar.text = 'Sync'
                self.page.update()
                return
            
        else:
            Logger.info( 'No se an pasado las variables año y mes.' )
            
            self.BtnSyncGCalendar.disabled = False
            self.BtnSyncGCalendar.text = 'Sync'
            self.page.update()
            return
        
        for day in lista_mes_sync:

            Festivo = False
            
            if 'turnoDoble' in lista_mes_sync[day] and lista_mes_sync[day]['turnoDoble'] != 0:
                               
                ID_turno_sel =  str( lista_mes_sync[day]['turnoDoble'] )
                                    
            else:
                ID_turno_sel =  str( lista_mes_sync[day]['turno'] )

            
            dia = lista_mes_sync[day]['dia']
            titulo = self.ListadoTurnos[ID_turno_sel]['nombre']
            
            comentario = ''
            if 'comentario' in lista_mes_sync[day]:
                comentario = lista_mes_sync[day]['comentario']

            hora_ini = self.ListadoTurnos[ID_turno_sel]['hora_ini']
            hora_fin = self.ListadoTurnos[ID_turno_sel]['hora_fin']
            
            #Default no mostrar salvo que se le haya indicado en el turno que se desea sincronizar con google
            sincronizarar_g_calendar = False 

            if 'mostrar_g_calendar' in self.ListadoTurnos[ID_turno_sel]:
                
                sincronizarar_g_calendar = self.ListadoTurnos[ID_turno_sel]['mostrar_g_calendar']
    

            hora_ini = hora_ini.split( ":" )
            hora_ini = str( '%02d' % int( hora_ini[0] ) ) + ':' + str( '%02d' % int( hora_ini[1] ) )
            #print( hora_ini )

            
            hora_fin = hora_fin.split( ":" )
            hora_fin = str( '%02d' % int( hora_fin[0] ) ) + ':' + str( '%02d' % int( hora_fin[1] ) )
            #print( hora_fin )

            #Logger.info( f" Dia {str( dia )} Mes {str( lista_mes_sync[day]['mes'] )} año {str( lista_mes_sync[day]['anio'] )} {titulo} {comentario} {hora_ini} {hora_fin}" )
            #print( self.ListadoTurnos )
        
            G_Cal.event_title = self.ListadoTurnos[ID_turno_sel]['nombre']

            G_Cal.event_desc = comentario

            G_Cal.event_color = self.ListadoTurnos[ID_turno_sel]['colorGcal']

            G_Cal.start_date = [ dia, lista_mes_sync[day]['mes'], lista_mes_sync[day]['anio'], hora_ini ]
            #print( G_Cal.start_date )
            G_Cal.end_date = [ dia, lista_mes_sync[day]['mes'], lista_mes_sync[day]['anio'], hora_fin ]
            
            if hora_fin == '00:00' and hora_ini == '00:00':
                G_Cal.AllDay = True

            else:
                G_Cal.AllDay = False
            
            #se buscan eventos en este dia y se borran los que hay para crear el nuevo
            events_day = G_Cal.events_day()
            for i in events_day:

                Logger.info( "Eliminando evento anterior... " + str( events_day[i]['id'] ) )
                G_Cal.delete_event_day( events_day[i]['id'] )  
            
            if sincronizarar_g_calendar: #G_Cal.AllDay == False:
                Logger.info( "Creando evento... " )
                G_Cal.create_event()
                
            self.progress+=1
            
            self.actualizar_progress_sync_google()



    def actualizar_progress_sync_google( self ):

        self.BtnSyncGCalendar.disabled = True
        self.BtnSyncGCalendar.text = 'Sincronizando...'
        self.BtnSyncGCalendar.update()

        pro = int( self.progress )
        max = int( self.progressMax )

        progreso = ( max - ( max - pro ) ) / max

        self.ProgressBarSyncGCal.value = progreso

        self.ProgressBarText.value = str( self.progress ) + ' de ' +  str( self.progressMax )

        if int( self.progress ) == int( self.progressMax ):
            
            self.BtnSyncGCalendar.disabled = False
            self.BtnSyncGCalendar.text = 'Sync'
            self.BtnSyncGCalendar.update()

            Logger.info( 'Sincronizacion finalizada' )
        
        self.page.update()




    def add_fechas_g_cal( self ):
        #self.page.go( '/sync_g_calendar' )
        self.TextTitle.value = self.page.title = 'Sync Google Calendar'
        self.page.update()
        
        #Si el boton esta activo resetea los datos, si hay una sincronizacion en segundo plano la muestra
        if self.BtnSyncGCalendar.disabled == False:

            self.ProgressBarSyncGCal.value = 0
            self.ProgressBarText.value = ''
            self.AnioSync.value = str( self.FechaSeleccionada.year )
            self.MesSync.value = str( self.FechaSeleccionada.month )
        



    def sync_g_cal( self ):

        if self.UserConfiguration['GcalendarID'] != '' and self.SYNC_GOOGLE:
            #ids.syn_g_cal_boxs
            self.ProgressBarSyncGCal.value = 0
            self.progress = 0
            self.progressMax = 1

            self.page.update()
            
            anio = self.AnioSync.value
            mes = self.MesSync.value

            # si no se indica el mes sincronizamos el año completo
            if mes == '0' and anio != '':

                self.progressMax = str( self.total_dias_anio_calendar( anio ) )
                self.ProgressBarText.value = str( self.progress ) + ' de ' +  str( self.progressMax )
                
                self.list_cal_anio = {}
                self.list_cal_anio[str( anio )] = {}

                for mes_ in range( 13 ):
                    if mes_ > 0:
                        self.list_cal_anio[str( anio )][str( mes_ )] = self.listado_calendar_ddbb( mes_,anio )

                        if len( self.list_cal_anio[str( anio )][str( mes_ )] )>0:
                            print('algo')
                            ReturnValueThread( target=self.sync_events, kwargs={'mes': mes_, 'year': anio} ).start()

            # si se indica año y mes sincronizamos el mes concreto
            elif mes != '0' and anio != '':
                
                self.list_cal_anio = {}
                self.list_cal_anio[str( anio )] = {}

                self.list_cal_anio[str( anio )][str( mes )] = self.listado_calendar_ddbb( mes, anio )

                self.progressMax = str( len( self.list_cal_anio[str( anio )][str( mes )] ) )
                self.ProgressBarText.value = str( self.progress ) + ' de ' +  str( self.progressMax )

                
                thread_sync_event = ReturnValueThread( target=self.sync_events, kwargs={'mes': mes, 'year': anio} )
                thread_sync_event.start()

            self.page.update()

        else:

            self.show_alert_dialog( text='Para sincronizar con Google Calendar debe agregar la ID de su calendario y activar la sincronización.', title='Error' )
            self.page.go( "/perfil" )

