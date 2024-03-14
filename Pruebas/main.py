__version__ = "24.03.01"

import flet as ft
import sys



from Logger_Path import Path, Logger, PATH
from config_default import Config, Years, TurnosDefaults

from views.template_route import TemplateRoute
from views.planilla import PagePlanilla
from views.estadisticas import PageEstadisticas
from views.perfil import PagePerfil, PageBackup
from views.turnos import PageTurnos
from views.patron_turnos import PagePatronTurnos
from views.sync_google_calendar import PageSyncGCalendar

from datetime import datetime


def main(page: ft.Page):
    
    page.session.clear()

    page.title = "Planilla"
    page.theme = ft.Theme(color_scheme_seed="teal")
    page.theme_mode = ft.ThemeMode.SYSTEM # Valores soportados: SYSTEM(default), LIGHT, DARK.
    page.window_width = 380
    page.window_height = 800
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    


    def route_change(route):
        troute = TemplateRoute(page.route)
        #page.views.clear()

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


    page.on_route_change = route_change

    def view_pop(view):

        if len(page.views):
            
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)






    

    def show_banner_click( text = ''):

        def close_banner(e):
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                text
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()


    def on_keyboard(e: ft.KeyboardEvent):

        #Logger.info(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")

        if e.key == 'Escape' or e.key == 'Go Back':

            #print( len(page.views) )
            show_banner_click( len(page.views) )
            
            if page.views[0] != page.views[-1]:
                
                if len(page.views) > 2:
                    
                    page.views.pop()
                    top_view = page.views[-1]

                    if top_view.route != page.route and top_view.route != None:

                        page.views.pop()
                        page.go(top_view.route)
            



    page.on_keyboard_event = on_keyboard


    def window_event(e):
        if e.data == "close":
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()

    page.window_prevent_close = True
    page.on_window_event = window_event

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
            ft.ElevatedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    #page.window_center()
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)





if __name__ == "__main__":
    ft.app(
        target=main, 
        #port=8550, 
        #view=ft.AppView.WEB_BROWSER,
        #route_url_strategy="hash"
        )