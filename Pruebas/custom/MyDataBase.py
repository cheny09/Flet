from datetime import datetime, timedelta

import os

from Logger_Path import Path, Logger
from custom.funciones import funciones, storage
from config_default import TurnosDefaults


class ddbb( funciones ):

    #ListadoTurnoID = []
    #ListadoTurnoName = []
    #ListadoTurnoSigla = []

    ListadoTurnos = {}

    UserConfiguration = {}

    MODO_DB = False

    PATH = ''

    DataYears = {}

    id_turnos_eliminados = [] #utilizado para que al crear un turno nuevo se reutilice el ID de los turnos eliminados


    def __init__( self, **kwargs ):
        super( ddbb, self ).__init__( **kwargs )
        


    def listado_turnos_ddbb(self):
            
        self.ListadoTurnos.clear()
        #self.ListadoTurnoID.clear()
        #self.ListadoTurnoName.clear()
        #self.ListadoTurnoSigla.clear()

        cT = 0
        out = []
        list_turnos = []


        if len( self.UserConfiguration['turnos'] ) == 0:

            self.UserConfiguration['turnos'] = TurnosDefaults


        if not "7" in self.UserConfiguration['turnos']: #Turno Obsoleto
            self.UserConfiguration['turnos']['7'] = {}


        for i in  self.UserConfiguration['turnos']:
            
            if self.UserConfiguration['turnos'][i] != {}:

                self.ListadoTurnos[str(i)] = self.UserConfiguration['turnos'][i] 
                
                cT+=1
                out.append( self.UserConfiguration['turnos'][i] )

            else: #utilizado para que al crear un turno nuevo se reutilice el ID de los turnos eliminados

                if not str( i ) in self.id_turnos_eliminados:

                    self.id_turnos_eliminados.append( str( i ) )


        for i in out:
            #print( i[1] )
            list_turnos.append( i['nombre'] )
            #self.ListadoTurnoID.append( i['ID'] )
            #self.ListadoTurnoName.append( i['nombre'] )
            #self.ListadoTurnoSigla.append( i['siglas'] )
            
        return list_turnos



    def detalle_dia_ddbb( self, dia, mes, anio, user_ID = None ):

        year = str( anio )
        mes = str( mes )
        dia = str( dia )

        detalle_del_dia = {}

        if year in self.DataYears:
            
            if mes in self.DataYears[year]:
                
                if dia in self.DataYears[year][mes]:
                    
                    detalle = self.DataYears[year][mes][dia]

                    for de in detalle:
                        
                        detalle_del_dia[de] = detalle[de]
                        
                    return detalle_del_dia
                
                else:
                    return None
            else:
                return None
        else:
            return None
        


    def insert_det_day( self, user, anio, mes, dia, turno, turnoDoble = 0, horasExtras = '0:0', comentario = False, color = '', festivo = 0 ):

        self.fecha=datetime( int( anio ),int( mes ),int( dia ) ) 

        if anio != '' and mes != '' and dia != '':

            try:

                existe = 3
                if str( anio ) not in self.DataYears:
                    self.DataYears[str( anio )] = {}
                    existe-=1
        
                if str( mes ) not in self.DataYears[str( anio )]:
                    self.DataYears[str( anio )][str( mes )] = {}
                    existe-=1
        
                if str( dia ) not in self.DataYears[str( anio )][str( mes )]:
                    self.DataYears[str( anio )][str( mes )][str( dia )] = {}
                    existe-=1

                if ( comentario == False ) :
                    if existe == 3:
                        comentario = self.DataYears[str( anio )][str( mes )][str( dia )]['comentario']
                    else:
                        comentario = ''
                
                    

                self.DataYears[str( anio )][str( mes )][str( dia )] = {
                    'anio': int( anio ), 
                    'mes': int( mes ), 
                    'dia': int( dia ), 
                    'turno': int( turno )
                    }
                 

                if int( turnoDoble ) != 0:
                    self.DataYears[str( anio )][str( mes )][str( dia )]['turnoDoble'] = int( turnoDoble )
                    
                if str( horasExtras ) != '0:0':    
                    self.DataYears[str( anio )][str( mes )][str( dia )]['horasExtras'] = str( horasExtras ) 
                    
                if comentario != False and comentario != '':    
                    self.DataYears[str( anio )][str( mes )][str( dia )]['comentario'] = str( comentario )
                    
                if color != '':    
                    self.DataYears[str( anio )][str( mes )][str( dia )]['color'] = str( color )
                    
                if int( user ) != 0:   
                    self.DataYears[str( anio )][str( mes )][str( dia )]['userID'] = int( user )
                    
                if int( festivo ) != 0:    
                    self.DataYears[str( anio )][str( mes )][str( dia )]['festivo'] = int( festivo )
                

                Logger.debug( self.DataYears[str( anio )][str( mes )][str( dia )] )

            except Exception as err:              
                Logger.error( f"Unexpected {err=}, {type( err )=}" )
                return 'Error en la funcion insert_det_day -> DataYears'
                        

        self.storage.set("years", self.DataYears )

        return True
    



    def limpiar_ddbb_years( self ):
        
        new_data_anios = {}

        #Comprueba si existe la base de datos de los años
        if self.storage.exists("years"):

            self.DataYears = self.storage.get("years")

            #Si se ha producido algun error detiene la ejecucion
            if 'error' in self.DataYears:

                Logger.error( self.DataYears['error'] )
                return


            # Recorremos la base de datos y la limpiamos
            for anio in self.DataYears:

                if not anio in new_data_anios:
                    new_data_anios[str( anio )] = {}
                
                for mes in self.DataYears[str( anio )]:

                    #Si no es un mes lo dejamos como esta en él else:
                    if 'DiferenciaConvenio' != mes and 'horas_convenio' != mes:

                        if not mes in new_data_anios[anio]:
                            new_data_anios[str( anio )][str( mes )] = {}
                        
                        for dia in self.DataYears[str( anio )][str( mes )]:
                            

                            if not dia in new_data_anios[str( anio )][str( mes )]:
                                new_data_anios[str( anio )][str( mes )][str( dia )] = {}
                            
                            detalle = self.DataYears[str( anio )][str( mes )][str( dia )]
                            
                            # IMPLEMENTAR SI EL TURNO NO ES 0 Y SON TODOS LOS VALORES POR DEFECTO NO GUARDAR EL DIA
                            #if detalle['turno'] != 0:

                            new_data_anios[str( anio )][str( mes )][str( dia )] = {
                                'anio': detalle['anio'], 
                                'mes': detalle['mes'], 
                                'dia': detalle['dia'], 
                                'turno': detalle['turno']
                                }

                            if 'turnoDoble' in detalle and detalle['turnoDoble'] != 0:
                                new_data_anios[str( anio )][str( mes )][str( dia )]['turnoDoble'] = detalle['turnoDoble']
                                
                            if 'horasExtras' in detalle and detalle['horasExtras'] != '0:0':    
                                new_data_anios[str( anio )][str( mes )][str( dia )]['horasExtras'] = detalle['horasExtras']
                                
                            if 'comentario' in detalle and detalle['comentario'] != '':    
                                new_data_anios[str( anio )][str( mes )][str( dia )]['comentario'] = detalle['comentario']
                                
                            #if 'color' in detalle and detalle['color'] != '':    
                            #    new_data_anios[str( anio )][str( mes )][str( dia )]['color'] = detalle['color']
                                
                            if 'userID' in detalle and detalle['userID'] != 0:   
                                new_data_anios[str( anio )][str( mes )][str( dia )]['userID'] = detalle['userID']
                            
                            if 'festivo' in detalle and detalle['festivo'] != 0:   
                                new_data_anios[str( anio )][str( mes )][str( dia )]['festivo'] = detalle['festivo']

                    else:
                        #Aqui se dejan los datos que no son meses tal y como estan guardados
                        new_data_anios[str( anio )][str( mes )] = self.DataYears[str( anio )][str( mes )]

                                
            self.storage.set("years", new_data_anios )

            Logger.info('La base de datos se ha limpiado.')
            self.show_alert_dialog( text= "La base de datos se ha limpiado.", title='Base de datos'  )
     


    def range_anios_en_ddbb( self ):#utilizado para crear el rango de años en el listado de estadisticas

        rang = []
        i=0
        
        keys = self.DataYears.keys()
        sorted_keys = sorted( keys )

        ultimo = len( sorted_keys )

        #si hay mas de un año en la base de datos
        if ultimo > 1:

            for anio in sorted_keys:

                if i == 0:
                    rang.append( int( anio ) )

                if i == ( ultimo - 1 ):
                    rang.append( int( anio ) )

                i+=1
        
        #si solo hay un año en la base de datos
        elif ultimo == 1:

            rang.append( int( sorted_keys[0] ) )
            rang.append( int( sorted_keys[0] ) )

        elif ultimo == 0:
            #creado para no producir error cuando no hay años
            rang.append( 0 )
            rang.append( 0 )

        return rang#[::-1]



    def user_ddbb( self ):
        try:
            self.UserConfiguration = self.storage.get("configuration")

        except Exception as err:  
            Logger.error( f"user_ddbb Unexpected {err=}, {type( err )=}" )

        return self.UserConfiguration
    


    def update_user_ddbb( self, horas_convenio, GcalendarID, SumarDiferenciaAnioAnterior, SyncGoogleCalendar ):

        try:

            self.UserConfiguration["horas_convenio"] = horas_convenio
            self.GCal.calendarId = self.UserConfiguration["GcalendarID"] =  GcalendarID
            self.SumarDiferenciaAnioAnterior = self.UserConfiguration["SumarDiferenciaAnioAnterior"] =  SumarDiferenciaAnioAnterior
            self.SYNC_GOOGLE = self.UserConfiguration['sync_google'] = SyncGoogleCalendar
            #self.UserConfiguration = self.conf_json( self.CONFIGURATION_DB, 'w', self.UserConfiguration )
            self.storage.set("configuration", self.UserConfiguration )

            return 'Perfil actualizado con éxito.'
        except:
            
            return 'Error al actualizar el perfil.'
        


    def update_turno( self, userID, ID, nombre, siglas, computo, nocturno, hora_ini, hora_fin, color, colorGcal, mostrar_g_calendar = False ):

            
        if ( nombre == '' ) :
            return 'Debe indicar un nombre'
        
        if '' == siglas :
            return 'Debe indicar una sigla.'
        
        if ( ':' == computo ) :
            computo = f"0:0"
        
        if ( ':' == nocturno ) :
            nocturno = f"0:0"

        if ( ':' == hora_ini ) :
            hora_ini = f"0:0"

        if ( ':' == hora_fin ) :
            hora_fin = f"0:0"

        if ( '' == color ) :
            color = f"#ffffff"
        
        if ( '' == ( colorGcal ) ) :
            colorGcal = 0
        
        try:

            if str( ID ) not in self.UserConfiguration['turnos']:

                #se comprueba si existen ID de turnos eliminados anteriormente y si no agregamos una nueva
                if self.id_turnos_eliminados != []:

                    Logger.warning( self.id_turnos_eliminados )
                    ID = self.id_turnos_eliminados[0]
                    self.id_turnos_eliminados.pop( 0 )
                    Logger.warning( self.id_turnos_eliminados )

                else:
                    ID = len( self.UserConfiguration['turnos'] )

            self.UserConfiguration['turnos'][str( ID )] = {
                "ID": int( ID ),
                "nombre": str( nombre ),
                "siglas": str( siglas ),
                "computo": str( computo ),
                "nocturno": str( nocturno ),
                "color": str( color ),
                "userID": int( userID ),
                "hora_ini": str( hora_ini ),
                "hora_fin": str( hora_fin ),
                "colorGcal": int( colorGcal ),
                "mostrar_g_calendar": mostrar_g_calendar,
            }

        except Exception as err:  

            Logger.error( f"Unexpected {err=}, {type( err )=}" )
            return 'Error al crear o modificar el Turno.' 
        
        else:

            try:
                
                self.storage.set("configuration", self.UserConfiguration )

            except Exception as err: 

                Logger.error( f"Unexpected {err=}, {type( err )=}" )
                return 'Error al guardar el Turno.'
            
            else:

                return 'Turno guardado con éxito.'
    



    def eliminar_turno( self, ID ):

        ID = str( ID )

        if ID != '' and ID != '0':

            anios = self.DataYears

            for anio in anios:

                for mes in anios[str( anio )]:

                    if 'DiferenciaConvenio' != mes and 'horas_convenio' != mes:

                        for dia in anios[str( anio )][str( mes )]:

                            dia_detallado = anios[str( anio )][str( mes )][str( dia )]

                            if 'turno' in dia_detallado and int( ID ) == dia_detallado['turno'] or 'turnoDoble' in dia_detallado and int( ID ) == dia_detallado['turnoDoble']:

                                return 'Error el Turno esta siendo utilizado en el calendario.'

            try:

                self.UserConfiguration['turnos'][str( ID )] = {}

            except Exception as err:      

                Logger.error( f"Unexpected {err=}, {type( err )=}" )
                return 'Error al eliminar el Turno.' 
            
            else:

                try:

                    self.storage.set("configuration", self.UserConfiguration )

                except Exception as err:  

                    Logger.error( f"Unexpected {err=}, {type( err )=}" )
                    return 'Error al actualizar el Turno eliminado.'
                
                else:
                    return 'Turno eliminado con éxito.'
                    
        else:
            return 'Error no se puede eliminar este Turno.'
        


    def estadisticas_ddbb( self, anio, mes = None ):

        if mes == None:
            Logger.debug( f"Buscando estadisticas para el {str( anio )}" )
        else:
            Logger.debug( f"Buscando estadisticas para el {str( mes )} del {str( anio )}" )
        
        IDuser = self.UserConfiguration['ID']

        if str( anio ) in self.DataYears:

            if 'horas_convenio' in self.DataYears[str( anio )]:
                
                horasConvenio = self.DataYears[str( anio )]['horas_convenio']
            else:

                horasConvenio = self.UserConfiguration['horas_convenio']

        else:

            horasConvenio = self.UserConfiguration['horas_convenio']

        if ( mes != None ):
            if self.MODO_DB: #MODO DB True
                mes = f"AND mes = '{mes}'"
            anual = False
        else:
            mes = ''
            anual = True

        Array = {}

        if ( anual == True ):

            Array['Convenio'] = self.format_hora_hh_mm_ss( f"{horasConvenio}" )
            Array['Computo'] = "0:0"
            Array['DifConvenioAnioAnterior'] = "0:0"
            Array['DiferenciaConvenio']="0"
            Array['TotalHorasNocturnas'] = "0:0"
            SumarConvenio = True
        else:

            Array['Computo'] = "0:0"
            Array['TotalHorasNocturnas'] = "0:0"
            SumarConvenio = False
        
        Array['siglas'] = {}
        

        mostrar = {}

        if str( anio ) in self.DataYears:

            for meses in self.DataYears[str( anio )]:

                if anual == False and str( meses ) == str( mes ) or anual == True:

                    if 'DiferenciaConvenio' != meses and 'horas_convenio' != meses:

                        for dias in self.DataYears[str( anio )][str( meses )]:

                            mostrar = self.detalle_dia_ddbb( dias, meses, anio, self.UserConfiguration['ID'] )
                            
                            id_turno = mostrar['turno']
                            mostrar['computo'] = self.UserConfiguration['turnos'][str( id_turno )]['computo']
                            mostrar['siglas'] = self.UserConfiguration['turnos'][str( id_turno )]['siglas']
                            mostrar['nombre'] = self.UserConfiguration['turnos'][str( id_turno )]['nombre']
                            mostrar['color'] = self.UserConfiguration['turnos'][str( id_turno )]['color']
                            mostrar['nocturno'] = self.UserConfiguration['turnos'][str( id_turno )]['nocturno']

                            Array = self.sumar_stadisticas( mostrar, anual, horasConvenio, Array, SumarConvenio )
                            SumarConvenio = False

            
        if ( anual == True ):

            Array['DiferenciaConvenio'] = self.sumar_horas( Array['DiferenciaConvenio'], Array['Computo'] )
            
            next_year = str( int( anio ) + 1 )
            
            if not next_year in self.DataYears:

                self.DataYears[next_year] = {}

            if not 'DiferenciaConvenio' in self.DataYears[next_year] or self.DataYears[( next_year )]['DiferenciaConvenio']  !=  Array['DiferenciaConvenio']:

                self.DataYears[( next_year )]['DiferenciaConvenio']  =  Array['DiferenciaConvenio']

                #self.conf_json( self.YEARS_DB, 'w', self.DataYears )


            if str( anio ) in self.DataYears:

                if not 'horas_convenio' in self.DataYears[str( anio )]:

                    self.DataYears[str( anio )]['horas_convenio']  =  Array['Convenio']

                    #self.conf_json( self.YEARS_DB, 'w', self.DataYears )

            
        return Array          



    def sumar_stadisticas( self, mostrar, anual, horasConvenio, Array, SumarConvenio = False ):

        if ( anual == True and SumarConvenio == True ): # and ( mostrar['mes'] == 1 and mostrar['dia'] == 1 )
            
            if 'DiferenciaConvenio' in self.DataYears[str( mostrar['anio'] )]:

                dif_anio_anterior = self.DataYears[str( mostrar['anio'] )]['DiferenciaConvenio']

            else:
                dif_anio_anterior = "0"

            if self.SumarDiferenciaAnioAnterior:#Solo suma si se elige en el perfil. Defaults: True

                Array['DiferenciaConvenio'] = self.sumar_horas( '-'+horasConvenio, dif_anio_anterior )
            else:
                Array['DiferenciaConvenio'] = self.sumar_horas( '-'+horasConvenio, '0' )
            
            Array['DifConvenioAnioAnterior'] = self.sumar_horas( '0', dif_anio_anterior )


        Array['Computo'] = self.sumar_horas( Array['Computo'], mostrar['computo'] )



        if ( mostrar['computo'] != "0:0" ) :

            if not 'DiasComputables' in Array:
                Array['DiasComputables'] = 0

            Array['DiasComputables']+=1
        

        
        #if ( mostrar['computo'] != "0:0" ) :

        if 'horasExtras' in mostrar:

            horasExtras = mostrar['horasExtras'].split( ":" )

            if ( int( horasExtras[0] ) > 0 or int( horasExtras[1] ) > 0 ) :
                #suma las horas extras
                if not 'HorasExtras' in Array:

                    Array['HorasExtras'] = '0:0'

                Array['HorasExtras'] = self.sumar_horas( Array['HorasExtras'], mostrar['horasExtras'] )



        if not mostrar['siglas'] in Array['siglas']:
            
            Array['siglas'][mostrar['siglas']]={'dias':0,'color':'','nombre':'','computo':'0:0'}
            
        Array['siglas'][mostrar['siglas']]['dias'] += 1
        Array['siglas'][mostrar['siglas']]['color'] = mostrar['color']# ?? null
        Array['siglas'][mostrar['siglas']]['nombre'] = mostrar['nombre']# ?? null
        Array['siglas'][mostrar['siglas']]['computo'] = mostrar['computo']# ?? null



        if ( mostrar['nocturno'] != "0:0" ) :
            #suma las noches
            Array['TotalHorasNocturnas'] = self.sumar_horas( Array['TotalHorasNocturnas'], mostrar['nocturno'] )

            if not 'Noches' in Array:

                Array['Noches'] = 0

            Array['Noches']+= 1



        if 'festivo' in mostrar:

            if ( int( mostrar['festivo'] ) == 1 ):

                if not 'Festivos' in Array:

                    Array['Festivos'] = 0

                Array['Festivos'] += 1



        if 'turnoDoble' in mostrar and ( mostrar['turnoDoble'] != 0 ) :#suma las horas de turnos extras
            
            resultTurnoExtra = self.ListadoTurnos[str( mostrar['turnoDoble'] )]

            if not 'TotalTurnosExtras' in Array:

                Array['TotalTurnosExtras'] = '0:0'
            
            Array['TotalTurnosExtras'] = self.sumar_horas( Array['TotalTurnosExtras'], resultTurnoExtra['computo'] )

            if ( resultTurnoExtra['nocturno'] != "0:0" ) :
                #suma las noches de horas extras
                Array['TotalHorasNocturnas'] = self.sumar_horas( Array['TotalHorasNocturnas'], resultTurnoExtra['nocturno'] )
                
                if not 'Noches' in Array:

                    Array['Noches'] = 0

                Array['Noches'] += 1


        return Array
    


    def total_dias_anio_calendar( self, anio, mes_ = '0' ):

        listado = {}
        i=0
        if str( anio ) in self.DataYears:
            for mes in self.DataYears[str( anio )]:

                if 'DiferenciaConvenio' != mes and 'horas_convenio' != mes and ( mes_ == '0' or mes ==  str( mes_ ) ):

                    for dia in self.DataYears[str( anio )][str( mes )]:

                        listado[i] = self.DataYears[str( anio )][str( mes )][str( dia )]
                        i+=1
                
        return len( listado )
    


    def listado_calendar_ddbb( self, mes, anio ):

        listado = {}
        i=0

        if str( anio ) in self.DataYears and str( mes ) in self.DataYears[str( anio )]:

            for dia in self.DataYears[str( anio )][str( mes )]:

                listado[i] = self.DataYears[str( anio )][str( mes )][str( dia )]
                i+=1

        return listado
    


    def listado_turnos_ddbb_check( self, id ):

        turno = self.ListadoTurnos['0']
        try:
            if str(id) in self.ListadoTurnos:
                
                turno = self.ListadoTurnos[str(id)]
        
        except Exception as err:  

            Logger.error( f"listado_turnos_ddbb_check Unexpected {err=}, {type( err )=}" )

        else:

            return turno