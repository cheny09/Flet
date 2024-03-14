import flet as ft

from Logger_Path import Path, Logger
import os, sys
from threading import Thread
from datetime import datetime, timedelta


def rgb2hex(rgba):

    r = ( rgba[0] * 255 )
    g = ( rgba[1] * 255 )
    b = ( rgba[2] * 255 )

    if len(rgba) == 4:
        a = rgba[3]
    else:
        a = 'FF'

    return "#{:02x}{:02x}{:02x}".format(r,g,b)



def hex2rgb(hex):
    value = hex.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))



def color_rgb_aply_opacity( color, opacity ):
    try:
        #print( color )
        color  = [color[0] ,color[1] ,color[2], opacity]
        #print( color )
        return color
    
    except Exception as err:
        Logger.error( f"color_rgb_aply_opacity Unexpected {err=}, {type( err )=}" )


class funciones():    


    def cero_izquierda( self, numero ):
        return str( '%02d' % int( numero ) )
    

    def format_hora_hh_mm_ss( self, hora, conSegundos = False ):

        hora = hora.split( ":" )

        if not 1 in hora:
            hora.append( 0 )

        if not 2 in hora:
            hora.append( 0 )
    
        if conSegundos:
            return self.cero_izquierda( hora[0] ) + ':' + self.cero_izquierda( hora[1] ) + ':' + self.cero_izquierda( hora[2] )
        
        return self.cero_izquierda( hora[0] ) + ':' + self.cero_izquierda( hora[1] )


    def validar_formato_horas_minutos( self, horas_minutos ):

        mensaje_error = "Solo se puede introducir de forma que sea __numero:numero__ o __numero__."

        horas_minutos = str( horas_minutos )

        if horas_minutos.find( ':' )>=0:
            
            horas = horas_minutos.split( ":" )
            
            if len( horas ) <= 2:
                for i in range( len( horas ) ):

                    if not horas[i].isdigit():

                        self.show_alert_dialog( text= f"{mensaje_error}", title=f"Error en convenio" )

                        return False

            else:
                self.show_alert_dialog( text= f"{mensaje_error}", title=f"Error en convenio" )

                return False
                
            return str( horas_minutos )
                
        elif horas_minutos.isdigit():
            
            return str( horas_minutos )
        
        else:

            self.show_alert_dialog( text= f"{mensaje_error}", title=f"Error en convenio" )

            return False
        


    def sumar_horas( self, hora1, hora2, conSegundos = False ):
        
        n = '-'
        hora1 = str( hora1 )
        hora2 = str( hora2 )
        
        if hora1.find( n )>=0:
            hora1 = hora1.replace( n, '' )
            sum1 = '-'
        else:
            sum1 = ''
        
        if hora2.find( n ) >=0:
            hora2 = hora2.replace( n, '' )
            sum2 = '-'
        else:
            sum2 = ''
       
        hora1 = self.format_hora_hh_mm_ss( hora1 )
        hora2 = self.format_hora_hh_mm_ss( hora2 )

        hora1 = hora1.split( ":" )

        horas1 = hora1[0]
        min1 = hora1[1]
        if not 2 in hora1:
            hora1.append( '00' )
        seg1 = hora1[2] 

        hora2 = hora2.split( ":" )

        horas2 = hora2[0]
        min2 = hora2[1]
        if not 2 in hora2:
            hora2.append( '00' )
        seg2 = hora2[2] 

        date1 = datetime( 2017,1,1 )
        date2 = datetime( 2017,1,1 )

        if sum1 == '-':
            date2 = date2 - timedelta( hours=int( horas1 ) )
            date2 = date2 - timedelta( minutes=int( min1 ) )
            date2 = date2 - timedelta( seconds=int( seg1 ) )
        else:
            date2 = date2 + timedelta( hours=int( horas1 ) )
            date2 = date2 + timedelta( minutes=int( min1 ) )
            date2 = date2 + timedelta( seconds=int( seg1 ) )

        if sum2 == '-':
            date2 = date2 - timedelta( hours=int( horas2 ) )
            date2 = date2 - timedelta( minutes=int( min2 ) )
            date2 = date2 - timedelta( seconds=int( seg2 ) )
        else:
            date2 = date2 + timedelta( hours=int( horas2 ) )
            date2 = date2 + timedelta( minutes=int( min2 ) )
            date2 = date2 + timedelta( seconds=int( seg2 ) )


        
        date3 = date2 - date1
        
        horas = 0

        horas = date3.days * 24

        totalMinute, second = divmod( date3.seconds, 60 )
        hour, minute = divmod( totalMinute, 60 )
        
        hour = horas + hour

        if conSegundos:
            return f"{hour}:{minute:02}:{second:02}"
        
        return f"{hour}:{minute:02}"

        

    def list_colors_google_calendar( self,id = 'False' ): #Paleta de colores de Google Calendar
        palet = {}
        try:
            #ID                 Nombre                         Hex Code
            palet[0] =     { "name":"Default",	        "code":"#ffffff" }
            palet[1] =     { "name":"Lavanda",	        "code":"#7986cb" }
            palet[2] =     { "name":"Sage",	            "code":"#33b679" }
            palet[3] =     { "name":"Grafito",	        "code":"#8e24aa" }
            palet[4] =     { "name":"Flamingo",	        "code":"#e67c73" }
            palet[5] =     { "name":"Amarillo Huevo",   "code":"#f6c026" }
            palet[6] =     { "name":"Tangerine",	    "code":"#f5511d" }
            palet[7] =     { "name":"Peacock",	        "code":"#039be5" }
            palet[8] =     { "name":"Grafito",	        "code":"#616161" }
            palet[9] =     { "name":"Blueberry",	    "code":"#3f51b5" }
            palet[10] =    { "name":"Basil",	        "code":"#0b8043" }
            palet[11] =    { "name":"Tomate",	        "code":"#d60000" }
            if id != 'False':
                return palet[int( id )]
            
        except Exception as err:
            Logger.error( f"list_colors_google_calendar Unexpected {err=}, {type( err )=}" )
        else:
            return palet








class storage:

    def __init__(self, page = ft.Page) -> None:
        
        self.page = page

    
    def exists( self, key ):
        try:

            return self.page.client_storage.contains_key( key )
            
        except Exception as err:
            Logger.error( f"Storage exists Unexpected {err=}, {type( err )=}" )
            return None


    def set( self, key, value ):
        try:

            self.page.client_storage.set( key, value )
            
        except Exception as err:
            Logger.error( f"Storage set Unexpected {err=}, {type( err )=}" )
            return None


    def get( self, key ):
        try:

            if self.exists( key ):

                return self.page.client_storage.get( key )
            
        except Exception as err:
            Logger.error( f"Storage get Unexpected {err=}, {type( err )=}" )    
            return None


    def remove( self, key ):
        try:

            if self.exists( key ):

                self.page.client_storage.remove( key )
            
        except Exception as err:
            Logger.error( f"Storage remove Unexpected {err=}, {type( err )=}" )
            return None






class ReturnValueThread( Thread ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.result = None

    def run( self ):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target( *self._args, **self._kwargs )
        except Exception as exc:
            print( f'{type( exc ).__name__}: {exc}', file=sys.stderr )  # properly handle the exception

    def join( self, *args, **kwargs ):
        super().join( *args, **kwargs )
        return self.result