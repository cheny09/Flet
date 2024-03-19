import flet as ft

from Logger_Path import Path, Logger, PATH

from custom.app import App
from custom.funciones import (
    color_rgb_aply_opacity, 
    rgb2hex, 
    hex2rgb,
    str_to_list_fecha,
    ReturnValueThread,
    funciones,
    storage,
)
from custom.MyDataBase import ddbb
from custom.datepicker import DatePicker

from datetime import datetime, timedelta


class PageEstadisticas( App, ft.View, ddbb ):

    FechaSeleccionadaHoy = datetime.now()

    ListadoEstadisticasColumn = ft.Column( spacing = 10, )

    BarGroupStatsBar = []
    BarLabelsStatsBar = []

    SumarDiferenciaAnioAnterior = True


    def __init__(self, page = ft.Page, year = FechaSeleccionadaHoy.year, month = FechaSeleccionadaHoy.month ):
        super().__init__(page)

        self.page = page

        self.AñoSeleccionada = year
        self.MesSeleccionada = month


        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        self.rango_fechas_personalizado = None

        self.view_stats()

    def view_stats( self ):

        ContenedorPrincipalPageEstadisticas = ft.Column( expand=1, width = 480, spacing = 10, scroll=True ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa
        

        ContenedorPrincipalPageEstadisticas.controls.append( ft.Container(
            content= ft.Text( 'Para mostrar todo el año seleccionar mes 0:', weight='BOLD' ),
            height=30,
        ) )

        RangeYears = self.range_anios_en_ddbb()

        self.AnioStats = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range( RangeYears[0], RangeYears[1] )
            ],
            label = 'Año',
            tooltip = 'Año para mostrar las estadísticas.',
            value = self.AñoSeleccionada,
            expand=1,
            on_change= lambda x: self.stats(),
        )

        self.MesStats = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(13)
            ],
            label = 'Mes',
            tooltip = 'Mes para mostrar las estadísticas.',
            value = self.MesSeleccionada,
            expand=1,
            on_change= lambda x: self.stats(),
        )

        self.AmpliarBusquedaStats = ft.IconButton( ft.icons.DATE_RANGE, icon_size=40, tooltip="Realizar busqueda concreta", on_click= lambda _: self.seleccionar_rango_de_fechas_personalizado_stats() )

        ContenedorPrincipalPageEstadisticas.controls.append( ft.Row(
            [
                self.AnioStats,
                self.MesStats,
                self.AmpliarBusquedaStats
            ],
        ) )
        
        ContenedorPrincipalPageEstadisticas.controls.append( ft.Container( height=10 ) )
        #self.ListadoEstadisticasColumn = ft.Column( height=200, spacing = 10, )

        ContenedorPrincipalPageEstadisticas.controls.append( self.ListadoEstadisticasColumn )
        
        ContenedorPrincipalPageEstadisticas.controls.append( ft.Container( height=10 ) )
        
        ContenedorPrincipalPageEstadisticas.controls.append( ft.Container(
            content= ft.Text( 'Estadísticas en días de los turnos:', weight='BOLD' ),
        ) )


        chart = ft.BarChart(
            bar_groups=self.BarGroupStatsBar,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=self.BarLabelsStatsBar,
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
            interactive=True,
            expand=True,
        )

        self.stats()

        ContenedorPrincipalPageEstadisticas.controls.append( ft.Container( chart ) )



        
        #return ContenedorPrincipalPageEstadisticas
    
        self.route= "/stats"
        self.controls.append( ContenedorPrincipalPageEstadisticas )

        self.page.views.append(self)




    def seleccionar_rango_de_fechas_personalizado_stats( self ):

        RangeYears = self.range_anios_en_ddbb()
        
        self.rango_fechas_personalizado = []

        Logger.debug( f"rango_fechas_personalizado: {self.rango_fechas_personalizado}" )

        content = []
            
        
        date_picker = DatePicker(
            page= self.page,
            #on_change=change_date,
            #on_dismiss=date_picker_dismissed,
            first_date=datetime(RangeYears[0], 1, 1),
            last_date=datetime(RangeYears[1], 12, 31),
        )

        fecha_inicio = ft.TextField( value='', label='Fecha de inicio', expand=1, )

        inicio = ft.IconButton( icon=ft.icons.CALENDAR_MONTH, on_click= lambda _, x = fecha_inicio: date_picker.pick_date( x ),  ) # 


        
        content.append(
            ft.Row(
                controls=[
                    inicio,
                    fecha_inicio
                ]
            )
        )



        def limitar_fecha_fin_desde_inicio( x ):

            date_picker2 = DatePicker(
                page= self.page,
                #on_change=change_date,
                #on_dismiss=date_picker_dismissed,
                first_date=datetime(RangeYears[0], 1, 1),
                last_date=datetime(RangeYears[1], 12, 31),
            )
            if fecha_inicio.value == '':

                return self.show_alert_dialog( text= f"Primero debe seleccionar la fecha de inicio.", title=f"Error en fecha" )
            
            inicio = str_to_list_fecha( fecha_inicio.value )

            if not inicio:

                return self.show_alert_dialog( text= f"Formato de fecha incorrecto, debe ser: dd-mm-yyyy.", title=f"Error en fecha" )
            
            date_picker2.first_date = datetime(inicio[2], inicio[1], inicio[0])
            date_picker2.pick_date( x )



        fecha_fin = ft.TextField( value='', label='Fecha de fin', expand=1, )
        fin = ft.IconButton( icon=ft.icons.CALENDAR_MONTH, on_click= lambda _, x = fecha_fin: limitar_fecha_fin_desde_inicio( x ), )
        content.append(
            ft.Row(
                controls=[
                    fin,
                    fecha_fin
                ]
            )
        )


        



        def mostrar():

            inicio = str_to_list_fecha( fecha_inicio.value )

            fin = str_to_list_fecha( fecha_fin.value )

            if not inicio or not fin:

                return self.show_alert_dialog( text= f"Formato de fecha incorrecto, debe ser: dd-mm-yyyy.", title=f"Error en fecha" )
     


            self.rango_fechas_personalizado = [
                inicio,
                fin
            ]

            Logger.debug( f"Rango de fechas a buscar: {self.rango_fechas_personalizado}" )
            
            self.stats( False )

            self.close_banner('')



        actions = [
            ft.OutlinedButton( 'Cerrar', on_click= self.close_banner ),
            ft.FilledButton( 'Mostrar', on_click= lambda x: mostrar()  ),    
        ]



        self.page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_50,
            #leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content= ft.Column( controls= content, spacing=10, alignment= ft.MainAxisAlignment.CENTER, ),
            actions= actions,
        )

        self.page.banner.open = True
        self.page.update()




    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()




    def show_banner_click(self, e):
        self.page.banner.open = True
        self.page.update()







    def stats(self, recarga = True):

        anio = self.AnioStats.value
        mes = self.MesStats.value

        self.AñoSeleccionada = anio
        self.MesSeleccionada = mes

        if recarga:
            self.rango_fechas_personalizado = None

        personalizado = self.rango_fechas_personalizado

        if personalizado != None:

            stats = self.estadisticas_ddbb_v2( RangoFechas = personalizado )

        elif mes != '0':

            stats = self.estadisticas_ddbb_v2( anio, mes )

        else:

            stats = self.estadisticas_ddbb_v2( anio )

        #print(stats['siglas'])

        self.ListadoEstadisticasColumn.controls = []

        self.BarGroupStatsBar.clear()
        self.BarLabelsStatsBar.clear()

        if stats:
        
            for stat in stats:

                if stat != 'siglas':
                    
                    color_personalizado = ft.ColorScheme.on_surface

                    if stat == 'DiferenciaConvenio' or stat == 'DifConvenioAnioAnterior':
                        
                        if stats[stat].find( '-' ) >= 0:
                            color_personalizado = ft.colors.RED
                        else:
                            color_personalizado = ft.colors.GREEN

                    self.ListadoEstadisticasColumn.controls.append(
                        ft.Container( ft.Row(
                                [
                                    ft.Text( stat, weight='BOLD', expand=2, color= color_personalizado ),
                                    ft.Text( stats[stat], weight='BOLD', expand=1, color= color_personalizado ),
                                ],
                                alignment= ft.alignment.center,
                            ),
                            on_click= lambda x, stat = stat: self.on_ItemListStats( stat )
                        )
                    )



            index = 0
            for turno in stats['siglas']:

                dias = int(stats['siglas'][turno]['dias'])

                self.BarGroupStatsBar.append( ft.BarChartGroup(
                    x=index,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=dias,
                            width=25,
                            color=stats['siglas'][turno]['color'],
                            tooltip=f"{stats['siglas'][turno]['nombre']} - {dias} días",
                            border_radius=0,
                        ),
                    ],
                ) )

                self.BarLabelsStatsBar.append(
                    ft.ChartAxisLabel(
                        value=index, label=ft.Container(
                            ft.Text( 
                                f"{turno}", 
                            ),
                            padding=10, 
                            tooltip=f"{stats['siglas'][turno]['nombre']} - {dias} días" )
                        )
                    )

                index += 1

        self.page.update()
        


    def on_ItemListStats( self, x ):
        #print( 'tests: ',x)

        if x == 'Convenio':

            self.edit_convenio_anual()



    def edit_convenio_anual( self, **kwargs ):

        anio = self.AñoSeleccionada
        mes = self.MesSeleccionada

        if kwargs:

            if 'instance' in kwargs:

                horas_convenio_edit_anual = self.validar_formato_horas_minutos( kwargs['instance'].value )

                if not horas_convenio_edit_anual:

                    return

                if str( anio ) in self.DataYears:

                    self.DataYears[str( anio )]['horas_convenio'] = horas_convenio_edit_anual

                    try:
                        self.storage.set("years", self.DataYears)

                    except:
                        self.show_alert_dialog( text= f"No se a actualizado tu convenio para el año {anio}.", title=f"Error Convenio {anio}" )
                    else:
                        self.show_alert_dialog( text= f"Se a actualizado tu convenio para el año {anio}.", title=f"Convenio {anio}" )

                        self.stats()


            return #Si exiten kawars los analiza pero si no carga la ventana de edicion
        

        horasConvenio = self.UserConfiguration['horas_convenio']

        if str( anio ) in self.DataYears:

            if 'horas_convenio' in self.DataYears[str( anio )]:
                
                horasConvenio = self.DataYears[str( anio )]['horas_convenio']

            
        #print( 'El convenio actual es', horasConvenio )

        try:
            
            contentMain = ft.Column( spacing=20 )
            
            descripcion = ft.Text( 
                value = 'Aquí puede modificar las horas y minutos de su convenio para este año en concreto.',
            )

            horas_convenio_edit_anual =  ft.TextField( 

                label= 'Horas Convenio ( Horas:Minutos )',
                #mode= "filled", # filled , outlined KiviMD
                value= str( horasConvenio ),
                #use_bubble= False, #Desactiva Copia y Pega KiviMD
            )

            btn_save = ft.FilledButton( text= 'Guardar', on_click=lambda _, x=horas_convenio_edit_anual: self.edit_convenio_anual( instance=x ) )
            
            contentMain.controls.append( descripcion )
            contentMain.controls.append( horas_convenio_edit_anual )
            #contentMain.append( btn_save )


            self.show_alert_dialog( Content=[contentMain], Actions=[btn_save, ft.OutlinedButton("Cerrar", on_click=self.close_dlg),], title=f"Convenio {anio}"  )


        except Exception as err:
            Logger.error( f"edit_convenio_anual Unexpected {err=}, {type( err )=}" )
