__version__ = "24.03.01"

import flet as ft

from Logger_Path import Logger

from views.template_route import TemplateRoute
from views.planilla import PagePlanilla
from views.estadisticas import PageEstadisticas
from views.perfil import PagePerfil, PageBackup
from views.turnos import PageTurnos
from views.patron_turnos import PagePatronTurnos
from views.sync_google_calendar import PageSyncGCalendar


def main(page: ft.Page):

    page.splash = ft.Container( content= ft.ProgressRing(width=50, height=50, stroke_width = 15), alignment=ft.alignment.center )

    page.update()

    page.session.clear()

    page.title = "Planilla"
    theme = ft.Theme(color_scheme_seed="teal")

    theme.page_transitions.android = ft.PageTransitionTheme.ZOOM
    theme.page_transitions.ios = ft.PageTransitionTheme.CUPERTINO
    theme.page_transitions.macos = ft.PageTransitionTheme.FADE_UPWARDS
    theme.page_transitions.linux = ft.PageTransitionTheme.ZOOM
    theme.page_transitions.windows = ft.PageTransitionTheme.ZOOM
    
    
    page.theme = theme

    page.theme_mode = ft.ThemeMode.SYSTEM # Valores soportados: SYSTEM(default), LIGHT, DARK.
    
    page.window_width = 380
    page.window_height = 800
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #print( page.client_storage.get_keys('') )
    #page.client_storage.clear()


    Views_history = []

    def route_change(route):
        troute = TemplateRoute(page.route)
        page.views.clear()

        Views_history.append( page.route )

        page.views.append(
            ft.View(
                "/",
                [],
            )
        )

        if page.route == "/":

            page_planilla = PagePlanilla( page )

            page_planilla.view_planilla()


        if troute.match("/detalle/year/:year/month/:month/day/:day"):

            #print("Year:", troute.year, "Month:", troute.month)

            year = int(troute.year)
            month = int(troute.month)
            day = int(troute.day)
            data = { 'day': day, 'month': month, 'year': year }

            page_planilla = PagePlanilla( page )
            page_planilla.view_detalleDia( data )


        elif page.route == "/stats" or troute.match("/stats/year/:year/month/:month"):

            if troute.match("/stats/year/:year/month/:month"):
                print("Year:", troute.year, "Month:", troute.month)

                PageEstadisticas( page, int(troute.year), int(troute.month) )

            else:

                if page.session.contains_key( "FechaSeleccionada" ):

                    FechaSeleccionada = page.session.get( "FechaSeleccionada" )

                    PageEstadisticas( page, int(FechaSeleccionada.year), int(FechaSeleccionada.month) )

                else:
                
                    PageEstadisticas( page )


        elif page.route == "/perfil":

            PagePerfil( page )


        elif page.route == "/turnos_edit":
            
            PageTurnos( page )

        
        elif page.route == "/crear_patron":
            
            View = PagePatronTurnos( page )
            
            View.view_patron()


        elif page.route == "/leer_qr":
            
            View = PagePatronTurnos( page )

            View.view_lectorQR()


        elif page.route == "/backup":
            
            PageBackup( page )

        
        elif page.route == "/sync_g_calendar":
            
            if page.session.contains_key( "FechaSeleccionada" ):

                FechaSeleccionada = page.session.get( "FechaSeleccionada" )

                PageSyncGCalendar( page, int(FechaSeleccionada.year), int(FechaSeleccionada.month) )

            else:
                
                PageSyncGCalendar( page )


        page.update()




    def view_pop(view):

        if len(Views_history) > 1:

            Views_history.pop()
            top_view = Views_history[-1]
            Views_history.pop()
            page.go(top_view)

        #else:

        #    page.dialog = confirm_dialog
        #    confirm_dialog.open = True
        #    page.update()





    def on_keyboard(e: ft.KeyboardEvent):


        Logger.debug(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")

        Logger.debug( Views_history )

        if e.key == "Escape" or e.key == "Go Back":

            view_pop(e)
            



    def window_event(e):

        Logger.warning( f" Dada WINDOW: {e.data}" )

        if e.data == "close":
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
            


    def yes_click(e):
        page.window_destroy()

    def no_click(e):
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Por favor confirme"),
        content=ft.Text("¿Realmente quieres salir de esta aplicación?"),
        actions=[
            ft.ElevatedButton("Si", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )



    page.on_route_change = route_change
    page.on_keyboard_event = on_keyboard
    page.window_prevent_close = True
    page.on_window_event = window_event
    #page.window_center()
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.splash = None
    page.go( page.route )

   



 
ft.app(
    target=main, 
    #port=8550, 
    #view=ft.AppView.FLET_APP_WEB,
    route_url_strategy="path",
    #use_color_emoji=True,
    )