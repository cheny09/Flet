import flet as ft

from Logger_Path import Path, Logger, PATH, PATH_HOME

from datetime import datetime
import calendar

class DatePicker():

    margen_vertical = 40
    margen_horizontal = 10

    modal = True

    btn_day_date_picker = {}

    TuplaMeses = ( "Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre" )
    calendario = calendar.Calendar()
    FechaSeleccionadaHoy = datetime.now()
    FechaSeleccionada = FechaSeleccionadaHoy

    mes_text_date_picker = ft.Text( value='Mes', expand=4, text_align='center', size=16, weight=ft.FontWeight.BOLD )
    anio_text_date_picker = ft.Text( value='Año', expand=2, text_align='center', size=16, weight=ft.FontWeight.BOLD )



    def __init__(
            self, 
            page = ft.Page, 
            Title = [], 
            title = 'Seleccione una fecha',
            first_date = None, 
            last_date = None 
        ) -> None:

        self.page = page

        self.first_date = first_date
        self.last_date = last_date


        self.Actions = [ 

            ft.Container( 
                content= ft.FilledButton( 'Hoy', tooltip = 'Ir al día de hoy', on_click= lambda x: self.ir_a_hoy() ),
                expand=1,
                alignment= ft.alignment.center_right
            ),
            ft.OutlinedButton( 'Cerrar', on_click= self.close_date ),
            
        ]

        self.Content = self.view_calendar()

        if Title == []:

            Title = [
                ft.Text( title ),
            ]
        
        self.date_picker = ft.AlertDialog(
            modal=self.modal, # Si el diálogo se puede descartar haciendo clic en el área de fuera de él.
            title= ft.Row( controls= Title, ),
            content= self.Content,
            actions= [ft.Row( controls= self.Actions )],
            actions_alignment=ft.MainAxisAlignment.END,
            #on_dismiss=lambda e: print("Modal dialog dismissed!"),
            inset_padding= ft.padding.symmetric( vertical= self.margen_vertical, horizontal= self.margen_horizontal ),
        ) 

        self.page.overlay.append(self.date_picker)  

        



    def pick_date( self, x = None ):

        self.retorno = x

        print( self.first_date, self.last_date )

        self.date_picker_load()

        self.date_picker.open = True
        self.page.update()



    def close_date(self, e):
        self.date_picker.open = False
        self.page.update()




    def view_calendar( self ):

        ContenedorPrincipal = ft.Column( spacing = 10, width = 480, tight=True, scroll=True ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa

        self.notify_text = ft.Text(f"", bgcolor= ft.colors.RED, )
        ContenedorPrincipal.controls.append( self.notify_text )
        
        Menudate_picker = ft.Column( height=60, alignment= ft.MainAxisAlignment.CENTER )
        ContenedorPrincipal.controls.append( Menudate_picker )


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
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  ), 
            ft.Row( spacing=2, alignment = ft.MainAxisAlignment.CENTER,  )
            ]

        
        id_semana_mes_date_picker = 0

        for i in range(0, 42):

            if i == 7 or i == 14 or i == 21 or i == 28 or i == 35 or i == 42:

                id_semana_mes_date_picker += 1


            if  i == 0 or i == 7 or i == 14 or i == 21 or i == 28 or i == 35:

                ContenedorPrincipal.controls.append( ContenedorRow[ id_semana_mes_date_picker ] )


            self.btn_day_date_picker[i] = ft.ElevatedButton( 

                text = i, 
                on_click = lambda x, id=i: self.callback( id ),
                #on_click = lambda x: "/detalle/year/:year/month/:month/day/:day"
                data = { 'day': 0, 'month': 0, 'year': 0 },
                #height = 20,
                expand = 1,
                style = ft.ButtonStyle(
                    padding=0,
                    #bgcolor=ft.colors.WHITE,
                    shape={
                        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=40),
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                    },
                ) 
            )



            ContenedorRow[ id_semana_mes_date_picker ].controls.append(

                ft.Column(
                    [
                        ft.Container(  content = self.btn_day_date_picker[i], width = 150, padding = 0, border_radius=0 ),
                    ],
                    spacing=2,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    #height = 80,
                    expand=1,
                )
            )


        RowMenudate_picker = ft.Row( 
            [ 
                #ft.Container( expand=0.5 ),
                ft.IconButton( 
                    ft.icons.ARROW_BACK,
                    on_click = lambda x: self.fun_dec_mes(), 
                    #expand=1,
                    tooltip='Ir al Mes anterior.',
                ),
                self.mes_text_date_picker,
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
                self.anio_text_date_picker,
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
        
        Menudate_picker.controls.append( RowMenudate_picker )


        return ContenedorPrincipal
                
    


    def callback(self, id):

        kwargs = self.btn_day_date_picker[ int(id) ].data

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
        
        Logger.debug( f"DatePicker Fecha seleccionada {dia}-{mes}-{anio}" )

        if self.retorno:
            
            DTselect = datetime(int(anio), int(mes), int(dia))

            if self.first_date <= DTselect and self.last_date >= DTselect:

                Logger.debug( f"DatePicker RETORNAR fecha seleccionada" )

                self.retorno.value = f"{dia}-{mes}-{anio}"

                self.close_date(None)
            
            else:

                Logger.debug( f"DatePicker No Puede RETORNAR fecha seleccionada" )
                
                self.notify_text.value = f"La fecha seleccionada no esta permitida."
                self.page.update()




    def actualizar_dia( self, i, dia, color_day, color_text_dia, mes, year, color_finde = False, opacity = 1 ):
        
        #print( btn_day_date_picker[0].style.bgcolor )
        
        
        if color_day == False:
            color_day_final = ft.colors.INVERSE_PRIMARY
        else:
            color_day_final = (color_day)


        if color_text_dia == False:
            color_text_dia = ft.colors.INVERSE_SURFACE
        else:
            color_text_dia = (color_text_dia)
        
        

        if color_finde == False and ( color_day == False ):
            
            color_text_dia = ft.colors.SURFACE
            color_day_final = ft.colors.PRIMARY


        self.btn_day_date_picker[ i ].text = dia
        self.btn_day_date_picker[ i ].style.bgcolor = ft.colors.with_opacity( opacity, color_day_final)
        self.btn_day_date_picker[ i ].style.color = color_text_dia

        self.btn_day_date_picker[ i ].data = { 'day': dia, 'month': mes, 'year': year }



    def limpiar_dias( self ):
        
        #print( btn_day_date_picker[0].style.bgcolor )

        for i in range(0, 42):

            self.btn_day_date_picker[ i ].text = ''
            self.btn_day_date_picker[ i ].style.bgcolor = ''
            self.btn_day_date_picker[ i ].data = { 'day': 0, 'month': 0, 'year': 0 }





    def date_picker_load( self ):

        self.limpiar_dias()

        self.page.session.set( "FechaSeleccionada", self.FechaSeleccionada )

        MesSeleccionado = self.calendario.monthdays2calendar( self.FechaSeleccionada.year,self.FechaSeleccionada.month )
        index = 0
        #print( MesSeleccionado )
        #se crea el calendario a 6 semanas
        id_semana = 0

        for semana in MesSeleccionado:

            for dia in semana:
                
                if dia:

                    color_day = False
                    color_text_dia = False
                    color_finde = False
                    
                    dia_ = dia[0]
                    month = self.FechaSeleccionada.month
                    year = self.FechaSeleccionada.year

                    opacity = 1.0
                    
                    color_text_dia = False #[0, 0, 0, 1]

                    

                    if dia_ != 0:  

                        self.btn_day_date_picker[ index ].text = dia_
      
                    
                    if  dia[1]==5 or dia[1]==6:
                        # Si es sabado o Domingo

                        color_day = False #self.theme_cls.primaryColor #self.mis_colores['primary_dark']#1,0,0,1 #self.theme_cls.primary_palette
                        color_text_dia= False #[0, 0 ,0 ,1]
                        color_finde = True


                    if dia_==self.FechaSeleccionadaHoy.day and self.FechaSeleccionadaHoy.month==month and self.FechaSeleccionadaHoy.year==self.FechaSeleccionada.year:
                        #si la FechaSeleccionada es el dia de hoy  

                        color_day = '#000000'
                        color_text_dia = '#ffffff'

                    

                    

                    if dia_ != 0:

                        DTselect = datetime(int(year), int(month), int(dia_))
                        if self.first_date > DTselect or self.last_date < DTselect:

                            opacity = 0.3

                        self.actualizar_dia( 

                            index, 
                            str( dia_ ),
                            ( color_day ),
                            ( color_text_dia ),
                            month,
                            year,
                            color_finde,
                            opacity
                            )

                index += 1
                
            id_semana += 1

        self.mes_text_date_picker.value = self.TuplaMeses[( self.FechaSeleccionada.month-1 )]
        self.anio_text_date_picker.value = self.FechaSeleccionada.year

        self.page.update()



    def ir_a_hoy( self ):
        self.FechaSeleccionada = self.FechaSeleccionadaHoy

        self.date_picker_load()



    def fun_inc_mes( self ):
        
        if self.FechaSeleccionada.month==12:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year+1,1,1 ) 

        else:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month+1,1 )

        self.date_picker_load()

        



    def fun_dec_mes( self ):
                    
        if self.FechaSeleccionada.month==1:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year-1,12,1 ) 

        else:

            self.FechaSeleccionada=datetime( self.FechaSeleccionada.year,self.FechaSeleccionada.month-1,1 )

        self.date_picker_load()

        



    def fun_inc_año( self ):
        
        self.FechaSeleccionada=datetime( self.FechaSeleccionada.year+1,self.FechaSeleccionada.month,self.FechaSeleccionada.day )
        #self.convert_db_anios( self.FechaSeleccionada.year )
        self.date_picker_load()



    def fun_dec_año( self ):
        
        self.FechaSeleccionada=datetime( self.FechaSeleccionada.year-1,self.FechaSeleccionada.month,self.FechaSeleccionada.day )
        #self.convert_db_anios( self.FechaSeleccionada.year )
        self.date_picker_load() 


