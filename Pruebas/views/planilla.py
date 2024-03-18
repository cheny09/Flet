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

import calendar
from datetime import datetime, timedelta




class PagePlanilla( App, ft.View, ddbb ):

    btn_day_planilla = {}
    btn_day_Turno = {}
    btn_day_TurnoExtra = {}

    TuplaMeses = ( "Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre" )
    calendario = calendar.Calendar()
    FechaSeleccionadaHoy = datetime.now()
    FechaSeleccionada = FechaSeleccionadaHoy

    mes_text_planilla = ft.Text( value='Mes', expand=4, text_align='center', size=16, weight=ft.FontWeight.BOLD )
    anio_text_planilla = ft.Text( value='Año', expand=2, text_align='center', size=16, weight=ft.FontWeight.BOLD )


    def __init__(self, page = ft.Page ):
        super().__init__(page)

        self.page = page

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        if not self.page.session.contains_key( "FechaSeleccionada" ):

            self.page.session.set( "FechaSeleccionada", self.FechaSeleccionada )
        
        else:

            self.FechaSeleccionada = self.page.session.get( "FechaSeleccionada" )




    def view_planilla( self ):

        ContenedorPrincipal = ft.Column( expand=1, width = 480, spacing = 10 ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa

        MenuPlanilla = ft.Column( height=60, alignment= ft.MainAxisAlignment.CENTER )
        ContenedorPrincipal.controls.append( MenuPlanilla )


        ContenedorPrincipal.controls.append( 
            ft.Row( 
                    [
                        ft.Text( "Lun", expand=1, text_align='center' ),
                        ft.Text( "Mar", expand=1, text_align='center' ),
                        ft.Text( "Mie", expand=1, text_align='center' ),
                        ft.Text( "Jue", expand=1, text_align='center' ),
                        ft.Text( "Vie", expand=1, text_align='center' ),
                        ft.Text( "Sab", expand=1, text_align='center' ),
                        ft.Text( "Dom", expand=1, text_align='center' ),
                    ],
                    spacing=0, 
                    alignment = ft.MainAxisAlignment.CENTER, 
                    #expand=1,
                    height=30
                )
            )

        ContenedorRow = [ 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER, expand=1 )
            ]


        id_semana_mes_planilla = 0

        for i in range(0, 42):

            if i == 7 or i == 14 or i == 21 or i == 28 or i == 35 or i == 42:

                id_semana_mes_planilla += 1


            if  i == 0 or i == 7 or i == 14 or i == 21 or i == 28 or i == 35:

                ContenedorPrincipal.controls.append( ContenedorRow[ id_semana_mes_planilla ] )


            self.btn_day_planilla[i] = ft.TextButton( 

                text = i, 
                on_click = lambda x, id=i: self.page_detalle_dia( id ),
                #on_click = lambda x: "/detalle/year/:year/month/:month/day/:day"
                data = { 'day': 0, 'month': 0, 'year': 0 },
                height = 20,
                expand = 1,
                style = ft.ButtonStyle(
                    padding=0,
                    #bgcolor=ft.colors.WHITE,
                    shape={
                        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=2),
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=0),
                    },
                ) 
            )

            self.btn_day_Turno[i] = ft.TextButton( 
                text = "T", 
                on_click = lambda x, id=i: self.page_detalle_dia( id ), 
                #data= { 'mes': 0, 'dia': 0, 'year': 0 }, 
                height = 50,
                expand=1,
                style = ft.ButtonStyle(
                    padding=0,
                    bgcolor=ft.colors.YELLOW,
                    color=ft.colors.BLACK,
                    shape={
                        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                    },
                ) 
            )
            
            self.btn_day_TurnoExtra[i] = ft.TextButton(
                text = "M", 
                on_click = lambda x, id=i: self.page_detalle_dia( id ), 
                #data= { 'mes': 0, 'dia': 0, 'year': 0 }, 
                height = 0,                            
                expand=1,
                style = ft.ButtonStyle(
                    padding=0,
                    bgcolor=ft.colors.AMBER,
                    color=ft.colors.BLACK,
                    shape={
                        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                    },
                ) 
            )


            ContenedorRow[ id_semana_mes_planilla ].controls.append(

                ft.Column(
                    [
                        ft.Container(  content = self.btn_day_planilla[i], width = 150, padding = 0, border_radius=0 ),
                        ft.Column(
                            [
                                self.btn_day_Turno[i],
                                self.btn_day_TurnoExtra[i]
                            ],
                            spacing=1,
                            expand=1,
                        )
                    ],
                    spacing=2,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    #height = 80,
                    expand=1,
                )
            )


        RowMenuPlanilla = ft.Row( 
            [ 
                #ft.Container( expand=0.5 ),
                ft.IconButton( 
                    ft.icons.ARROW_BACK,
                    on_click = lambda x: self.fun_dec_mes(), 
                    #expand=1,
                    tooltip='Ir al Mes anterior.',
                ),
                self.mes_text_planilla,
                ft.IconButton( 
                    ft.icons.ARROW_FORWARD,
                    on_click = lambda x: self.fun_inc_mes(), 
                    #expand=1,
                    tooltip='Ir al Mes siguiente.',
                ),
                #ft.Container( expand=0.5 ),
                ft.IconButton( 
                    ft.icons.ARROW_BACK,
                    on_click = lambda x: self.fun_dec_año(), 
                    #expand=1,
                    tooltip='Ir al Año anterior.',
                ),
                self.anio_text_planilla,
                ft.IconButton( 
                    ft.icons.ARROW_FORWARD,
                    on_click = lambda x: self.fun_inc_año(), 
                    #expand=1,
                    tooltip='Ir al Año siguiente.',
                ),
                #ft.Container( expand=0.5 ),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            spacing=0,
            )
        
        MenuPlanilla.controls.append( RowMenuPlanilla )


        # Este contenedor se agrega para añadir un margen inferior
        ContenedorPrincipal.controls.append( ft.Container( height=10 ) )



        self.deslizar_on = False
        # Se ejecutara al arrastrar en pantalla sobre el horizontal y al soltar
        def on_horizontal_drag_update(e: ft.DragUpdateEvent):

            #print(  e.delta_x, e.primary_delta, self.deslizar_on )
            # Deslizamos el dedo o el cursor de izquierda a derecha
            if e.primary_delta > 5 and self.deslizar_on: 

                self.fun_dec_mes()

            # Deslizamos el dedo o el cursor de derecha a izquierda
            if e.primary_delta < -5 and self.deslizar_on:

                self.fun_inc_mes()



        def on_horizontal_drag_start( e: ft.DragStartEvent ):

            #print(e.timestamp)
            self.deslizar_on = True



        StackPrincipal = ft.Stack(
            [
                ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.MOVE,
                        drag_interval=100,
                        on_horizontal_drag_start = on_horizontal_drag_start,
                        on_horizontal_drag_update= on_horizontal_drag_update,
                    ),
                ft.TransparentPointer(ContenedorPrincipal),
            ],
            expand=1,
            width = 480,
        )



        #return ContenedorPrincipal
        self.route= "/"
        self.controls.append( StackPrincipal )

        self.page.views.append( self )

        self.planilla()


        if 'WELCOME' in self.UserConfiguration:

            Logger.debug( f"Welcome is: {self.UserConfiguration['WELCOME']}" )

            if self.UserConfiguration['WELCOME']:

                self.welcome()
                
    



    def actualizar_dia( self, i, dia, titulo_dia, turno, color_turno, turno_extra, color_turno_extra, color_day, color_text_dia, mes, year, color_finde = False, opacity = 1 ):
        
        #print( btn_day_planilla[0].style.bgcolor )
        
        
        if color_day == False:
            color_day_final = ft.colors.INVERSE_PRIMARY
        else:
            color_day_final = rgb2hex(color_day)


        if color_text_dia == False:
            color_text_dia = ft.colors.INVERSE_SURFACE
        else:
            color_text_dia = rgb2hex(color_text_dia)


        if color_turno == False:
            color_turno = ft.colors.ON_PRIMARY


        if color_turno_extra == False:
            color_turno_extra = ft.colors.PRIMARY
        

        if color_finde == False and ( color_day == False ):
            
            color_text_dia = ft.colors.SURFACE
            color_day_final = ft.colors.PRIMARY


        self.btn_day_planilla[ i ].text = titulo_dia
        self.btn_day_planilla[ i ].style.bgcolor = color_day_final
        self.btn_day_planilla[ i ].style.color = color_text_dia

        self.btn_day_Turno[ i ].text = turno
        self.btn_day_Turno[ i ].style.bgcolor = color_turno
        self.btn_day_Turno[ i ].expand = 1

        self.btn_day_TurnoExtra[ i ].text = turno_extra
        self.btn_day_TurnoExtra[ i ].style.bgcolor = color_turno_extra
        self.btn_day_TurnoExtra[ i ].expand = 1

        if turno_extra == '':

            self.btn_day_TurnoExtra[ i ].expand = 0            
        

        self.btn_day_planilla[ i ].data = { 'day': dia, 'month': mes, 'year': year }



    def limpiar_dias( self ):
        
        #print( btn_day_planilla[0].style.bgcolor )

        for i in range(0, 42):

            self.btn_day_planilla[ i ].text = ''
            self.btn_day_planilla[ i ].style.bgcolor = ''
            self.btn_day_planilla[ i ].data = { 'day': 0, 'month': 0, 'year': 0 }

            self.btn_day_Turno[ i ].text = ''
            self.btn_day_Turno[ i ].style.bgcolor = ''
            self.btn_day_Turno[ i ].expand = 1
            #btn_day_Turno[ i ].data = { 'mes': 0, 'dia': 0, 'anio': 0 }

            self.btn_day_TurnoExtra[ i ].text = ''
            self.btn_day_TurnoExtra[ i ].style.bgcolor = ''
            self.btn_day_TurnoExtra[ i ].expand = 0
            #btn_day_TurnoExtra[ i ].data = { 'mes': 0, 'dia': 0, 'anio': 0 }



    def planilla( self ):

        self.limpiar_dias()

        self.page.session.set( "FechaSeleccionada", self.FechaSeleccionada )

        self.TextTitle.value = self.page.title = 'Planilla'

        MesSeleccionado = self.calendario.monthdays2calendar( self.FechaSeleccionada.year,self.FechaSeleccionada.month )
        index = 0
        #print( MesSeleccionado )
        #se crea el calendario a 6 semanas
        id_semana = 0

        for semana in MesSeleccionado:

            for dia in semana:
                
                if dia:
                    #dia[0]#Dia del mes
                    #dia[1]#Dia de la semana

                    #print( ContenedorRow[ id_semana ].controls[ dia[1] ].controls[ 0 ] )

                    color_extra = color_turno = "#FFFFFF"

                    sigla_extra = sigla= ""  

                    horas_ext = ""

                    coment = ""

                    festivo = ""

                    color_day = False # self.theme_cls.secondaryColor #self.mis_colores['primary_light']

                    color_finde = False
                    
                    dia_ = dia[0]
                    month = self.FechaSeleccionada.month
                    year = self.FechaSeleccionada.year

                    opacity = 1.0
                    
                    color_text_dia = False #[0, 0, 0, 1]

                    idsigla_extra = 0

                    #genera los ultimos dias del mes anterior
                    if semana == MesSeleccionado[0] and dia[0] == 0:

                        if self.FechaSeleccionada.month==1:
                            
                            fecha_mes_anterior = datetime( self.FechaSeleccionada.year-1,12,1 ) 

                        else:
                            fecha_mes_anterior = datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month-1,1 )


                        mes_anterior = self.calendario.monthdays2calendar( fecha_mes_anterior.year,( fecha_mes_anterior.month ) )
                        t_mes_ant = len( mes_anterior ) - 1

                        for dia_ant in mes_anterior[t_mes_ant]:

                            if dia_ant[1] == dia[1]:

                                dia_=dia_ant[0]
                                #print( dia_ant[0] )
                                month = fecha_mes_anterior.month
                                year = fecha_mes_anterior.year
                                opacity = 0.3


                    #genera los primeros dias del mes siguiente
                    t_mes = len( MesSeleccionado ) - 1
                    if semana == MesSeleccionado[t_mes] and dia[0] == 0:

                        if self.FechaSeleccionada.month==12:

                            fecha_mes_siguiente = datetime( self.FechaSeleccionada.year+1,1,1 ) 

                        else:
                            fecha_mes_siguiente = datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month+1,1 )
                            

                        mes_siguiente = self.calendario.monthdays2calendar( fecha_mes_siguiente.year,( fecha_mes_siguiente.month ) )
                        
                        for dia_ant in mes_siguiente[0]:

                            if dia_ant[1] == dia[1]:

                                dia_=dia_ant[0]
                                #print( dia_ant[0] )
                                month = fecha_mes_siguiente.month
                                year = fecha_mes_siguiente.year
                                opacity = 0.55

                    self.btn_day_planilla[ index ].text = dia_
                    self.btn_day_Turno[ index ].text = ''
                    self.btn_day_TurnoExtra[ index ].text = ''

                    
                    det_day = self.detalle_dia_ddbb( dia_, month, year )
                    #print( det_day )
                    if det_day != None:
                        
                        idsigla = det_day['turno']

                        if 'turnoDoble' in det_day and det_day['turnoDoble'] != 0: # det_day['turnoDoble'] == 0

                            idsigla_extra=det_day['turnoDoble']
                            horas_ext = "+"

                        
                        if 'horasExtras' in det_day and det_day['horasExtras'] != '0:0':
                            horas_ext = "+"
                        

                        if 'comentario' in det_day and det_day['comentario'] != "":
                            
                            coment = "*"


                        if 'festivo' in det_day and det_day['festivo'] == 1:

                            festivo = "F"

                        
                        if idsigla != 0:

                            ID_Array_Turno = str( idsigla )
                            turno = self.listado_turnos_ddbb_check(ID_Array_Turno)


                            if turno:

                                color_turno=turno['color']
                                
                                sigla=turno['siglas']

                            else:
                                color_turno="#FFFFFF"

                                sigla="" 

                        
                        if idsigla_extra != 0:

                            ID_Array_Turno_Extra = str( idsigla_extra )
                            turno_extra = self.listado_turnos_ddbb_check(ID_Array_Turno_Extra)


                            if turno_extra:

                                color_extra = turno_extra['color']
                                
                                sigla_extra = turno_extra['siglas']

                            else:
                                color_extra="#FFFFFF"

                                sigla_extra="" 
                            
                    else:
                        
                        color_turno="#FFFFFF"

                        sigla=""  

                        horas_ext = ""

                        coment = ""

                        festivo = ""
                    

                    
                    if  dia[1]==5 or dia[1]==6:
                        # Si es sabado o Domingo

                        color_day = False #self.theme_cls.primaryColor #self.mis_colores['primary_dark']#1,0,0,1 #self.theme_cls.primary_palette
                        color_text_dia= False #[0, 0 ,0 ,1]
                        color_finde = True


                    if dia_==self.FechaSeleccionadaHoy.day and self.FechaSeleccionadaHoy.month==month and self.FechaSeleccionadaHoy.year==self.FechaSeleccionada.year:
                        #si la FechaSeleccionada es el dia de hoy  

                        color_day = [0, 0 ,0 ,1]
                        color_text_dia = [1, 1, 1 ,1]

                    
                    if color_day:

                        color_day = color_rgb_aply_opacity( color_day, 1 )

                    self.actualizar_dia( 

                        index, 
                        str( dia_ ),
                        ( str( dia_ ) + str( horas_ext ) + str( coment ) + str( festivo ) ),
                        sigla,
                        ( ( color_turno ) ),
                        sigla_extra,
                        ( ( color_extra ) ),
                        ( color_day ),
                        ( color_text_dia ),
                        month,
                        year,
                        color_finde,
                        opacity
                        )

                index += 1
                
            id_semana += 1

        self.mes_text_planilla.value = self.TuplaMeses[( self.FechaSeleccionada.month-1 )]
        self.anio_text_planilla.value = self.FechaSeleccionada.year

        self.page.update()



    def ir_a_hoy( self ):
        """ Esta funcion remplaza a la que esta en app.py 
            cuando esta la ruta '/' seleccionada.
        """
        self.FechaSeleccionada = self.FechaSeleccionadaHoy

        self.planilla()



    def fun_inc_mes( self ):
        
        if self.FechaSeleccionada.month==12:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year+1,1,1 ) 

        else:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month+1,1 )

        self.planilla()

        self.deslizar_on = False



    def fun_dec_mes( self ):
                    
        if self.FechaSeleccionada.month==1:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year-1,12,1 ) 

        else:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month-1,1 )

        self.planilla()

        self.deslizar_on = False



    def fun_inc_año( self ):
        
        self.FechaSeleccionada=datetime( self.FechaSeleccionada.year+1,self.FechaSeleccionada.month,self.FechaSeleccionada.day )
        #self.convert_db_anios( self.FechaSeleccionada.year )
        self.planilla()



    def fun_dec_año( self ):
        
        self.FechaSeleccionada=datetime( self.FechaSeleccionada.year-1,self.FechaSeleccionada.month,self.FechaSeleccionada.day )
        #self.convert_db_anios( self.FechaSeleccionada.year )
        self.planilla() 




        



    def view_detalleDia( self, data = {} ):

        self.route= f"/detalle/year/{data['year']}/month/{data['month']}/day/{data['day']}"

        ContenedorPrincipal = ft.Column( expand=1, width = 480, spacing = 10, scroll=True )

        #ContenedorPrincipal.controls.append( ft.Container( height=10 ) )
        
        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Turno:', weight='BOLD', size=16, ),
        ) )
        
        self.TurnoDetalle = ft.TextButton( 
                text= "Ninguno", 
                expand=1,
                key = 0,
                style= ft.ButtonStyle(
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
 
        
        self.TurnoDetalle.on_click = lambda x, instance = self.TurnoDetalle: self.listado_turnos( instance = instance, ventana = self.route, titulo_retorno =  self.page.title, modal = False )
        
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.TurnoDetalle,
            width= 1000,
        ) )

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Turno Extra:', weight='BOLD', size=16, ),
        ) )

        self.TurnoExtraDetalle = ft.TextButton( 
                text="Ninguno", 
                expand=1,
                key = 0,
                style= ft.ButtonStyle(
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
        
        self.TurnoExtraDetalle.on_click = lambda x, instance = self.TurnoExtraDetalle: self.listado_turnos( instance = instance, ventana = self.route, titulo_retorno =  self.page.title, modal = False )

        ContenedorPrincipal.controls.append( ft.Container(
            content= self.TurnoExtraDetalle,
            width= 1000,
        ) )

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Horas Extra:', weight='BOLD', size=16, ),
        ) )

        self.HorasExtraDetalle = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(25)
            ],
            label = 'Horas',
            value = 0,
            expand=1
        )

        self.MinutosExtraDetalle = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(60)
            ],
            label = 'Minutos',
            value = 0,
            expand=1
        )

        ContenedorPrincipal.controls.append( 
            ft.Row(
                controls= [
                    self.HorasExtraDetalle,
                    self.MinutosExtraDetalle,
                ],
            )
        )

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Comentario:', weight='BOLD', size=16, ),
        ) )

        self.ComentarioDetalle = ft.TextField(
            value='',
            #label="Comentario", 
            hint_text="Introduce aquí tu comentario.",
            tooltip = 'Introduce aquí un comentario o nota para este día.',
            multiline=True,
            )
        
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.ComentarioDetalle,
        ) )
        
        self.FestivoDetalle = ft.Checkbox( 
            adaptive=True, 
            label="Festivo", 
            value=False, 
            label_position='left',
            tooltip = 'Indica si el dia es festivo o no.',
            width=100,
            scale=1.2
            )

        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.FestivoDetalle,
                alignment = ft.alignment.center_right,
            ) )

        self.GuardarDetalle = ft.FilledButton(
                    text="Guardar",
                    on_click= lambda x: self.fun_guardar_detalles()
                )

        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.GuardarDetalle,
                alignment = ft.alignment.center_right,
                margin=10,
            ) )


        #return ft.Container( content = ContenedorPrincipal, padding=10, expand=1 )
        
        self.controls.append( ft.Container( content = ContenedorPrincipal, padding=10, expand=1 ) )

        self.page.views.append( self )


        self.detalle_dia( dia = data['day'] , mes = data['month'] , anio = data['year']  )
    



    def page_detalle_dia( self , id ):

        #print( 'Prueba de boton', self.btn_day_planilla[ id ].data )

        kwargs = self.btn_day_planilla[ int(id) ].data

        dia = ''
        mes = ''
        anio = ''


        if 'day' in kwargs:
            dia = kwargs['day']

        if 'month' in kwargs:
            mes = kwargs['month']

        if 'year' in kwargs:
            anio = kwargs['year']

        if int(dia) == 0 and int(mes) == 0 and int(anio) == 0:
            return 

        self.menu_callback( route = f"/detalle/year/{anio}/month/{mes}/day/{dia}" )



    def detalle_dia( self, dia = '', mes = '', anio = '' ):
        
        if int(dia) == 0 and int(mes) == 0 and int(anio) == 0:
            return #si se hace click en los dias vacios se detiene para no generar errores
        

        self.FechaSeleccionada = datetime( int( anio ),int( mes ),int( dia ) )
        #print( self.FechaSeleccionada )
        self.TextTitle.value = self.page.title = 'Dia - ' + str( self.FechaSeleccionada.day ) + '/' + str( self.FechaSeleccionada.month ) + '/' + str( self.FechaSeleccionada.year )
        #consulta sql del detalle del dia seleccionado  
        detalle_dia_select = self.detalle_dia_ddbb( self.FechaSeleccionada.day, self.FechaSeleccionada.month, self.FechaSeleccionada.year )
        

        #si no existen resultados para el dia seleccionado
        if not detalle_dia_select:
                                #  ID,      anio,                   mes,                     dia,                   turno,       turnoDoble,     horasExtras,       comentario,color,userID      
            detalle_dia_select = {'ID':0, 'anio':self.FechaSeleccionada.year, 'mes':self.FechaSeleccionada.month, 'dia':self.FechaSeleccionada.day,   'turno':0,  'turnoDoble':0,  'horasExtras':"0:0", 'comentario':"",     'color':"", 'userID':self.UserConfiguration['ID']}
        

        if not 'turnoDoble' in detalle_dia_select:
            detalle_dia_select['turnoDoble'] = 0

        if not 'horasExtras' in detalle_dia_select:
            detalle_dia_select['horasExtras'] = '0:0'
            
        if not 'comentario' in detalle_dia_select:
            detalle_dia_select['comentario'] = ""
            
        if not 'color' in detalle_dia_select:
            detalle_dia_select['color'] = ""
            
        if not 'userID' in detalle_dia_select:
            detalle_dia_select['userID'] = 0
            
        if not 'festivo' in detalle_dia_select:
            detalle_dia_select['festivo'] = 0


        ID_Array_Turno= str( detalle_dia_select['turno'] )
        turno = self.listado_turnos_ddbb_check(ID_Array_Turno)

        ID_Array_Turno= str( detalle_dia_select['turnoDoble'] )
        turnoDoble = self.listado_turnos_ddbb_check(ID_Array_Turno)

        self.TurnoDetalle.text = turno['nombre']
        self.TurnoDetalle.key = turno['ID']
        self.TurnoDetalle.style.bgcolor = turno['color']

        self.TurnoExtraDetalle.text = turnoDoble['nombre']
        self.TurnoExtraDetalle.key = turnoDoble['ID']
        self.TurnoExtraDetalle.style.bgcolor = turnoDoble['color']

        hora = detalle_dia_select['horasExtras']
        hora = hora.split( ":" )

        self.HorasExtraDetalle.value = ( hora[0] )
        self.MinutosExtraDetalle.value = ( hora[1] )

        check_festivo = self.FestivoDetalle

        if 'festivo' in detalle_dia_select:
            if detalle_dia_select['festivo'] == 1:
                detalle_dia_select['festivo'] = True

            check_festivo.value = detalle_dia_select['festivo']
        else:
            check_festivo.value = False

        self.ComentarioDetalle.value = detalle_dia_select['comentario']

        self.page.update()




    def fun_guardar_detalles( self ):

        self.lista_fecha = []
        
        self.lista_fecha.append( self.FechaSeleccionada.day )

        self.lista_fecha.append( self.FechaSeleccionada.month )

        self.lista_fecha.append( self.FechaSeleccionada.year ) 

        Logger.debug( f"{str( self.lista_fecha )} > Guardando nuevos detalles." )
        
        ID_turno_sel = str( self.TurnoDetalle.key )
        
        ID_turno_Doble_sel = str( self.TurnoExtraDetalle.key )

        #turno = self.listado_turnos_ddbb_check(ID_turno_sel)

        sincronizarar_g_calendar = False #Default

        if 'mostrar_g_calendar' in self.listado_turnos_ddbb_check(ID_turno_sel):
            sincronizarar_g_calendar = self.listado_turnos_ddbb_check(ID_turno_sel)['mostrar_g_calendar']
        
        if 'mostrar_g_calendar' in self.listado_turnos_ddbb_check(ID_turno_Doble_sel):
            sincronizarar_g_calendar = self.listado_turnos_ddbb_check(ID_turno_Doble_sel)['mostrar_g_calendar']

        if ID_turno_Doble_sel != 0:
            
            hora_ini = self.listado_turnos_ddbb_check(ID_turno_Doble_sel)['hora_ini']
            hora_fin = self.listado_turnos_ddbb_check(ID_turno_Doble_sel)['hora_fin']

        else:
            hora_ini = self.listado_turnos_ddbb_check(ID_turno_sel)['hora_ini']
            hora_fin = self.listado_turnos_ddbb_check(ID_turno_sel)['hora_fin']

        hora_ini = hora_ini.split( ":" )
        hora_ini = str( '%02d' % int( hora_ini[0] ) ) + ':' + str( '%02d' % int( hora_ini[1] ) )
        #print( hora_ini )

        
        hora_fin = hora_fin.split( ":" )
        hora_fin = str( '%02d' % int( hora_fin[0] ) ) + ':' + str( '%02d' % int( hora_fin[1] ) )

        check_festivo = self.FestivoDetalle
        check_festivo_state = check_festivo.value

        result = {
            "Anio":str( self.lista_fecha[2] ),
            "Mes":str( self.lista_fecha[1] ),
            "Dia":str( self.lista_fecha[0] ),
            "Turno": str( ID_turno_sel ),
            "TurnoDoble": str( ID_turno_Doble_sel ),
            "HorasExtra": str( self.HorasExtraDetalle.value ) + ':' +str( self.MinutosExtraDetalle.value ),
            "Coment": str( self.ComentarioDetalle.value ),
            #"color":str( self.entry_det_dia_color_V.text ),
            "HoraInicio": hora_ini,
            "HoraFin": hora_fin,
            "festivo": bool( check_festivo_state )
            }
        try:
            SeInsertoElDia=self.insert_det_day( 
                user=self.UserConfiguration['ID'], 
                anio=result['Anio'],
                mes=result['Mes'], 
                dia=result['Dia'], 
                turno=result['Turno'], 
                turnoDoble = result['TurnoDoble'], 
                horasExtras = result['HorasExtra'], 
                comentario = result['Coment'], 
                festivo = result['festivo']
                #color = result['color']
                )
        except Exception as err:              
            Logger.error( f"Unexpected {err=}, {type( err )=}" )
        else:
            if SeInsertoElDia == True and self.SYNC_GOOGLE == True:

                self.GuardarDetalle.disabled = True
                self.GuardarDetalle.text = 'Guardando...'
                self.GuardarDetalle.update()

                Festivo = False

                self.GCal.event_title = str( self.listado_turnos_ddbb_check(ID_turno_sel)['nombre'] )

                if result['TurnoDoble'] != 0:
                    
                    ID_turno_sel = ID_turno_Doble_sel

                    self.GCal.event_title = str( self.listado_turnos_ddbb_check(ID_turno_sel)['nombre'] )


                self.GCal.event_desc = result['Coment']

                if Festivo:
                    self.GCal.event_color = self.listado_turnos_ddbb_check(Festivo)['colorGcal']
                else:
                    self.GCal.event_color = self.listado_turnos_ddbb_check(ID_turno_sel)['colorGcal']

                self.GCal.start_date = [result['Dia'],result['Mes'],result['Anio'],result['HoraInicio']]
                #print( self.GCal.start_date )
                self.GCal.end_date = [result['Dia'],result['Mes'],result['Anio'],result['HoraFin']]
                
                if result['HoraInicio'] == '00:00' and result['HoraFin'] == '00:00':
                    self.GCal.AllDay = True

                else:
                    self.GCal.AllDay = False
                

                #se buscan eventos en este dia y se borran los que hay para crear el nuevo
                ReturnValueThread( target=self.sync_events_day,  kwargs={'sincronizarar_g_calendar': sincronizarar_g_calendar } ).start()
                
            
            elif SeInsertoElDia == True:

                msg  = 'Datos guardados correctamente'

                def close_detalle_dialog(e):
                    self.dlg_modal.open = False
                    self.page.update()
                    self.page.go( '/' )

                Actions = [
                    ft.TextButton("Cerrar", on_click=close_detalle_dialog),
                ]

                self.show_alert_dialog( text=str( msg ), title='', Actions= Actions )
                Logger.info( msg )

                #self.page.go( '/' )

            else:
                Logger.error( f"{str( self.lista_fecha )} > {SeInsertoElDia}" )
                self.show_alert_dialog( text=str( SeInsertoElDia ), title='Error' )




    def sync_events_day( self, **kawars ):
        
        sincronizarar_g_calendar = False

        if len( kawars ):

            if 'sincronizarar_g_calendar' in kawars:

                sincronizarar_g_calendar = kawars['sincronizarar_g_calendar']

        events_day = self.GCal.events_day()
        #print( events_day )
        for i in events_day:

            Logger.debug( str( self.lista_fecha ) + " > Eliminando evento anterior... " + str( events_day[i]['id'] ) )
            self.GCal.delete_event_day( events_day[i]['id'] )  
        
        if sincronizarar_g_calendar: #self.GCal.AllDay == False:
            Logger.info( "Creando evento... " )
            self.GCal.create_event()

        self.GuardarDetalle.disabled = False
        self.GuardarDetalle.text = 'Guardar'
        self.GuardarDetalle.update()
        
        def close_detalle_dialog(e):
            self.dlg_modal.open = False
            self.page.update()
            self.page.go( '/' )

        Actions = [
            ft.TextButton("Cerrar", on_click=close_detalle_dialog),
        ]
        
        #print( self.GCal.events_day() )
        msg  = 'Datos sincronizados correctamente'
        self.show_alert_dialog( text=str( msg ), title='', Actions= Actions )
        Logger.info( msg )
        