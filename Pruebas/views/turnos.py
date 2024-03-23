import flet as ft


from Logger_Path import Path, Logger, PATH

from custom.app import App
from custom.MyDataBase import ddbb

class PageTurnos( App, ft.View, ddbb ):

    def __init__(self, page = ft.Page ):
        super().__init__(page)

        self.page = page

        self.appbar= self.MainAppBar
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER

        self.route= "/turnos_edit"

        self.controls.append( self.view_turnos() )

        self.page.views.append(self)

        self.listado_turnos( ventana = '/turnos_edit' )




    def view_turnos( self):

        ContenedorPrincipal = ft.Column( expand=1, width = 480, spacing = 15, scroll= ft.ScrollMode.ALWAYS ) # Con el width se asigna el ancho maximo de la app aun que se pongo en pantalla completa

        #ContenedorPrincipal.controls.append( ft.Container( height=10 ) )
        

        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Nombre del Turno:', weight='BOLD', size=16, ),
        ) )

        self.NombreTurnoEdit = ft.TextField(
            value='',
            #label="Comentario", 
            hint_text="Introduce aquí el nombre.",
            tooltip = 'Introduce aquí el nombre para este turno.',
            multiline=False,
            )
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.NombreTurnoEdit,
        ) )


        ContenedorPrincipal.controls.append( ft.Container(
            content= ft.Text( 'Siglas del Turno:', weight='BOLD', size=16, ),
        ) )

        self.SiglasTurnoEdit = ft.TextField(
            value='',
            #label="Comentario", 
            hint_text="Introduce aquí las siglas.",
            tooltip = 'Introduce aquí las siglas para este turno se recomienda entre uno y dos caracteres.',
            multiline=False,
            )
        ContenedorPrincipal.controls.append( ft.Container(
            content= self.SiglasTurnoEdit,
        ) )




        ContenedorPrincipal.controls.append( 
            ft.Row(
                [
                    ft.Text( 'Computo:', weight='BOLD', size=16, expand=1 ),
                    ft.Text( 'Nocturno:', weight='BOLD', size=16, expand=1 )
                ],
            )
        )
        
        RowComputoYNocturno = ft.Row()

        ContenedorPrincipal.controls.append( RowComputoYNocturno )

        self.ComputoHorasTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(25)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Horas',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowComputoYNocturno.controls.append( ft.Container(
            content= self.ComputoHorasTurnoEdit,
            expand=1
        ) )

        
        self.ComputoMinutosTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(60)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Minutos',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowComputoYNocturno.controls.append( ft.Container(
            content= self.ComputoMinutosTurnoEdit,
            expand=1
        ) )


        self.NocturnoHorasTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(25)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Horas',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowComputoYNocturno.controls.append( ft.Container(
            content= self.NocturnoHorasTurnoEdit,
            expand=1
        ) )


        self.NocturnoMinutosTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(60)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Minutos',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowComputoYNocturno.controls.append( ft.Container(
            content= self.NocturnoMinutosTurnoEdit,
            expand=1
        ) )




        ContenedorPrincipal.controls.append( 
            ft.Row(
                [
                    ft.Text( 'Entrada:', weight='BOLD', size=16, expand=1 ),
                    ft.Text( 'Salida:', weight='BOLD', size=16, expand=1 )
                ],
            )
        )
        
        RowEntradaYSalida = ft.Row()

        ContenedorPrincipal.controls.append( RowEntradaYSalida )

        self.EntradaHorasTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(24)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Horas',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowEntradaYSalida.controls.append( ft.Container(
            content= self.EntradaHorasTurnoEdit,
            expand=1
        ) )

        
        self.EntradaMinutosTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(60)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Minutos',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowEntradaYSalida.controls.append( ft.Container(
            content= self.EntradaMinutosTurnoEdit,
            expand=1
        ) )


        self.SalidaHorasTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(24)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Horas',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowEntradaYSalida.controls.append( ft.Container(
            content= self.SalidaHorasTurnoEdit,
            expand=1
        ) )


        self.SalidaMinutosTurnoEdit = ft.Dropdown(
            options=[
                ft.dropdown.Option( i )
                for i in range(60)
            ],
            value = '0',
            
            text_style= ft.TextStyle(
                weight='bold',
                color='BLACK',
            ),
            text_size=16,
            label='Minutos',
            label_style = ft.TextStyle(
                size=14,
            ),
            alignment= ft.alignment.center,
        )

        RowEntradaYSalida.controls.append( ft.Container(
            content= self.SalidaMinutosTurnoEdit,
            expand=1
        ) )




        ContenedorPrincipal.controls.append( 
            ft.Container(
                ft.Text( 'Color:', weight='BOLD', size=16, expand=1 )
            )
        )
        
        
        RowColor = ft.Row()

        ContenedorPrincipal.controls.append( RowColor )



        self.IconColorTurnoEdit = ft.Icon( name=ft.icons.PALETTE, color= '', )

        RowColor.controls.append( ft.Container(
            content= self.IconColorTurnoEdit,
        ) )

        self.ColorTurnoEdit = ft.TextField(
            value='',
            #label="Comentario", 
            hint_text="Introduce aquí el nombre.",
            tooltip = 'Introduce aquí el nombre para este turno.',
            multiline=False,
            )
        RowColor.controls.append( ft.Container(
            content= self.ColorTurnoEdit,
            expand=1
        ) )


        ContenedorPrincipal.controls.append( 
            ft.Container( 
                ft.Text( 'Color G. Calendar:', weight='BOLD', size=16, expand=1 ) 
            ) 
        )
        
        self.ColorGCalendarTurnoEdit = ft.ElevatedButton(
            text='Default',
            key = '0',
            #label="Comentario", 
            tooltip = 'Selecciona aquí el color para este turno en google calendar.',
            style= ft.ButtonStyle(
                color='BLACK',
            ),
            width=1000,
            expand=1
        )
        
        self.ColorGCalendarTurnoEdit.on_click = lambda x: self.color_google_calendar_dialog( self.ColorGCalendarTurnoEdit )

        ContenedorPrincipal.controls.append( ft.Container(
            content= self.ColorGCalendarTurnoEdit,
        ) )

        

        self.MostrarEnGoogleCalendarTurno = ft.Checkbox( 
            adaptive=True, 
            label="Mostrar en Google Calendar", 
            value=False, 
            label_position='right',
            tooltip = 'Mostrar este turno en Google calendar o no, cuando se sincroniza.',
        )

        ContenedorPrincipal.controls.append( 
            ft.Container(
                content= self.MostrarEnGoogleCalendarTurno,
                alignment = ft.alignment.center_right,
            ) )
        

        self.GuardarTurnoEdit = ft.FilledButton(
                    text="Guardar",
                    on_click= lambda x: self.fun_guardar_turno()
                )
        
        ContenedorPrincipal.controls.append( 
            ft.Row(
                [
                    ft.IconButton( icon= ft.icons.DELETE, icon_color='RED', icon_size=40, on_click= lambda x: self.fun_eliminar_turno()),
                    ft.Container( self.GuardarTurnoEdit, alignment = ft.alignment.center_right, expand=1 ),
                ],
                
            ) )

        return ft.Container( content = ContenedorPrincipal, padding=10, expand=1 )




    def edit_turno( self, data ):
        try:
            self.idTurnoEdit = ''

            #obtenemos los datos reales
            if data['id_turno'] != '0' and data['id_turno'] != 0:

                self.TextTitle.value = self.page.title = 'Editar Turno'

                ID_Array_Turno= str( data['id_turno'] )
                turno = self.ListadoTurnos[ID_Array_Turno]

                if not 'mostrar_g_calendar' in turno:
                    turno['mostrar_g_calendar'] = False

                self.idTurnoEdit = str( turno['ID'] )

                self.NombreTurnoEdit.value = str( turno['nombre'] )
                self.SiglasTurnoEdit.value = str( turno['siglas'] )

                computo=turno['computo']
                computo = computo.split( ":" )
                self.ComputoHorasTurnoEdit.value = str( computo[0] )
                self.ComputoMinutosTurnoEdit.value = str( computo[1] )
                
                nocturno=turno['nocturno']
                nocturno = nocturno.split( ":" )
                self.NocturnoHorasTurnoEdit.value = str( nocturno[0] )
                self.NocturnoMinutosTurnoEdit.value = str( nocturno[1] )

                hora_ini=turno['hora_ini']
                hora_ini = hora_ini.split( ":" )
                self.EntradaHorasTurnoEdit.value = str( hora_ini[0] )
                self.EntradaMinutosTurnoEdit.value = str( hora_ini[1] )

                hora_fin=turno['hora_fin']
                hora_fin = hora_fin.split( ":" )
                self.SalidaHorasTurnoEdit.value = str( hora_fin[0] )
                self.SalidaMinutosTurnoEdit.value = str( hora_fin[1] )
                
                self.ColorTurnoEdit.value = str( turno['color'] )
                self.IconColorTurnoEdit.color = turno['color']

                self.ColorGCalendarTurnoEdit.text = str( self.list_colors_google_calendar( turno['colorGcal'] )['name'] )

                self.ColorGCalendarTurnoEdit.key = str( turno['colorGcal'] )
                self.ColorGCalendarTurnoEdit.style.bgcolor= self.list_colors_google_calendar( turno['colorGcal'] )['code']
                #self.IconColorGCalendarTurnoEdit.color = self.list_colors_google_calendar( turno['colorGcal'] )['code']

                self.MostrarEnGoogleCalendarTurno.value = turno['mostrar_g_calendar']

            else:

                self.TextTitle.value = self.page.title = 'Nuevo Turno'

                self.NombreTurnoEdit.value = ''
                self.SiglasTurnoEdit.value = ''

                self.ComputoHorasTurnoEdit.value = 0
                self.ComputoMinutosTurnoEdit.value = 0

                self.NocturnoHorasTurnoEdit.value = 0
                self.NocturnoMinutosTurnoEdit.value = 0

                self.EntradaHorasTurnoEdit.value = 0
                self.EntradaMinutosTurnoEdit.value = 0

                self.SalidaHorasTurnoEdit.value = 0
                self.SalidaMinutosTurnoEdit.value = 0

                self.ColorTurnoEdit.value = '#ffffff'
                self.IconColorTurnoEdit.color = '#ffffff'

                self.ColorGCalendarTurnoEdit.key = 0
                self.ColorGCalendarTurnoEdit.text = 'Default'
                self.ColorGCalendarTurnoEdit.style.bgcolor = '#ffffff'
                #self.IconColorGCalendarTurnoEdit.color = '#ffffff'

                self.MostrarEnGoogleCalendarTurno.value = False
            
        except Exception as err:              
            Logger.error( f"Editar Turno Unexpected {err=}, {type( err )=}" )

        self.page.update()




    def fun_guardar_turno( self ):

        nombre = self.NombreTurnoEdit.value

        siglas = self.SiglasTurnoEdit.value

        hora = self.ComputoHorasTurnoEdit.value
        min = self.ComputoMinutosTurnoEdit.value
        computo = str( hora ) + ':' + str( min )

        hora = self.NocturnoHorasTurnoEdit.value
        min = self.NocturnoMinutosTurnoEdit.value
        nocturno = str( hora ) + ':' + str( min )

        hora = self.EntradaHorasTurnoEdit.value
        min = self.EntradaMinutosTurnoEdit.value
        hora_ini = str( hora ) + ':' + str( min )

        hora = self.SalidaHorasTurnoEdit.value
        min = self.SalidaMinutosTurnoEdit.value
        hora_fin = str( hora ) + ':' + str( min )

        color = self.ColorTurnoEdit.value

        colorGcal = self.ColorGCalendarTurnoEdit.key

        check_mostrar_g_calendar = self.MostrarEnGoogleCalendarTurno.value

        res = self.update_turno( self.UserConfiguration['ID'],self.idTurnoEdit, nombre, siglas, computo, nocturno, hora_ini, hora_fin, color, colorGcal, bool(check_mostrar_g_calendar) )
        
        if res == 'Nada que actualizar' or res == 'Turno guardado con éxito.':
            self.listado_turnos_ddbb()
            self.listado_turnos( ventana = '/turnos_edit' )

        self.show_alert_dialog( text=str( res ), title='' )



    def fun_eliminar_turno( self ):

        res = self.eliminar_turno( self.idTurnoEdit )
        if res == 'Turno eliminado con éxito.':
            self.listado_turnos_ddbb()
            self.listado_turnos( ventana = '/turnos_edit' )
        else:
            Logger.warning( res )
            self.show_alert_dialog( text=str( res ), title='Error' )