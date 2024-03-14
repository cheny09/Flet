from datetime import datetime, timedelta
from custom.GoogleCalendarSetup import get_calendar_service, get_calendar_path_token

from Logger_Path import Logger, PATH

import flet as ft

class MyGoogleCalendar():


    def __init__(self, page = ft.page):

        self.page = page

        self.calendarId = ''

        self.event_title = ""

        self.event_desc = ""

        self.start_date = ""

        self.end_date = ""

        self.AllDay = False

        self.event_color = 0

        self.fecha = []

        self.PATH = ''

        self.SYNC_GOOGLE = False

        self.BORRAR_TODOS_EVENTOS_DEL_DIA = False



    def take_start_date(self):

        self.fecha.clear()
        self.fecha.append(int(self.start_date[0]))
        self.fecha.append(int(self.start_date[1]))
        self.fecha.append(int(self.start_date[2]))

        new_date = str(self.start_date[2]) + '-' + str('%02d' % int(self.start_date[1]))  + '-' + str('%02d' % int(self.start_date[0])) \
            + ' ' + str(self.start_date[3])
        date_isoformat = datetime.fromisoformat(new_date).isoformat()
        return date_isoformat



    def take_end_date(self):
        new_date = str(self.end_date[2]) + '-' + str('%02d' % int(self.end_date[1]))  + '-' + str('%02d' % int(self.end_date[0])) \
            + ' ' + str(self.end_date[3])
        date_isoformat = datetime.fromisoformat(new_date).isoformat()
        
        #en el caso de que la hora de finalizar sea menor que la de inicio, turno de noche sumamos un dia a la fecha de fin
        horas = self.end_date[3].split(":")
        if self.take_start_date() > date_isoformat:
            fecha_sum = datetime(int(self.end_date[2]),int('%02d' % int(self.end_date[1])),int('%02d' % int(self.end_date[0]))) + timedelta(days = 1, hours=int('%02d' % int(horas[0])), minutes=int('%02d' % int(horas[1])))
            date_isoformat = datetime.fromisoformat(str(fecha_sum)).isoformat()
            #print(" Es Mayor " + str(date_isoformat))
        return date_isoformat



    def create_event(self):

        self.fecha.clear()
        self.fecha.append(int(self.start_date[0]))
        self.fecha.append(int(self.start_date[1]))
        self.fecha.append(int(self.start_date[2]))
        try:
            if self.calendarId != '' and self.SYNC_GOOGLE:
                calendar_service = get_calendar_service( self.page ) 

                body={
                        "summary": self.event_title,
                        "description": self.event_desc,
                        "colorId": self.event_color,
                        "location": 'planilla-turnos-de-trabajo',
                    }
                
                if self.AllDay:
                    body['start']={"date": str(self.start_date[2]) + '-' + str(self.start_date[1]) + '-' + str(self.start_date[0]), "timeZone": 'Europe/Madrid'}
                    fecha_sum = datetime(int(self.start_date[2]),int('%02d' % int(self.start_date[1])),int('%02d' % int(self.start_date[0]))) + timedelta(days = 1)

                    #print(fecha_sum)
                    body['end']={ "date": str(fecha_sum.year) + '-' + str(fecha_sum.month) + '-' + str(fecha_sum.day),  "timeZone": 'Europe/Madrid'}
                else:
                    body['start']={"dateTime": self.take_start_date(), "timeZone": 'Europe/Madrid'}
                    body['end']={"dateTime": self.take_end_date(), "timeZone": 'Europe/Madrid'}
                
                event_result = calendar_service.events().insert(calendarId=self.calendarId,
                    body=body
                ).execute()

                Logger.info(f"{self.fecha} > Evento creado con éxito!")
            else:
                Logger.info(f"{self.fecha} > No existe el id de Google Calendar o esta desactivada la sincronizacion!")
        except Exception as err:              
            Logger.error(f"create_event Unexpected {err=}, {type(err)=}")


    def events_day(self):
        page_token = None
        try:
            if self.calendarId != '' and self.SYNC_GOOGLE:
                calendar_service = get_calendar_service( self.page )
                
                date_Min = str(self.start_date[2]) + '-' + str('%02d' % int(self.start_date[1]))  + '-' + str('%02d' % int(self.start_date[0]))  + " 00:00"
                date_Min_isoformat = datetime.fromisoformat(date_Min).isoformat() + '+02:00'
                date_Max = str(self.start_date[2]) + '-' + str('%02d' % int(self.start_date[1]))  + '-' + str('%02d' % int(self.start_date[0]))  + " 23:59:59"
                date_Max_isoformat = datetime.fromisoformat(date_Max).isoformat() + '+02:00'

                list_event_day = {}
                iLeD = 0
                while True:
                    events = calendar_service.events().list(calendarId=self.calendarId , timeMin=date_Min_isoformat, timeMax=date_Max_isoformat , timeZone='Europe/Madrid').execute()
                    for event in events['items']:
                        
                        #con location lo utilizamos para listar solo los eventos creados por la aplicación  
                        if not 'location' in event:
                            event['location'] = ''

                        if event['location'] == 'planilla-turnos-de-trabajo' or self.BORRAR_TODOS_EVENTOS_DEL_DIA:
                            
                            #se selecciona la fecha de inicio del evento ya sea de todo el dia o de tiempo determinado
                            if event['start'].get('date') != None:
                                start = datetime.fromisoformat(event['start']['date']).isoformat() + '+02:00'

                            if event['start'].get('dateTime') != None:
                                start = event['start']['dateTime']
                                
                            #solo muestra los eventos que inician en la fecha seleccionada
                            if start >= date_Min_isoformat:
                                
                                list_event_day[iLeD] = {"summary": event['summary'], "id" : event['id'] }
                                iLeD+=1
                                #print (str(event['summary']) + ' ' + str(event['id'])+ ' ' + str(event['start']) + ' ' + str(event['end']))

                    page_token = events.get('nextPageToken')
                    if not page_token:
                        break

                return list_event_day
            else:
                Logger.info(f"No existe el id de Google Calendar o esta desactivada la sincronizacion!")
                return {}
                
        except Exception as err:              
            Logger.error(f"events_day Unexpected {err=}, {type(err)=}")
            return {}
    


    def delete_event_day(self,id):
        try:
            if self.calendarId != '' and self.SYNC_GOOGLE:
                calendar_service = get_calendar_service( self.page )
                calendar_service.events().delete(calendarId=self.calendarId, eventId=id).execute()
            else:
                Logger.info(f"No existe el id de Google Calendar o esta desactivada la sincronizacion!")
                
        except Exception as err:              
            Logger.error(f"delete_event_day Unexpected {err=}, {type(err)=}")

    



    def get_list_calendars(self):
        page_token = None

        lis_calendars = []
        try:
            calendar_service = get_calendar_service( self.page )

            while True:

                calendar_list = calendar_service.calendarList().list(pageToken=page_token).execute()

                for calendar_list_entry in calendar_list['items']:

                    #print ('nombre',calendar_list_entry['summary'])
                    #print ('id',calendar_list_entry['id'])

                    lis_calendars.append({ 'nombre': calendar_list_entry['summary'], 'id': calendar_list_entry['id'] })

                page_token = calendar_list.get('nextPageToken')

                if not page_token:
                    break
            
            Logger.debug(f"get_list_calendars {lis_calendars}")
            return lis_calendars
        

        except Exception as err:              
            Logger.error(f"get_list_calendars Unexpected {err=}, {type(err)=}")
            return lis_calendars
        
    
    


#MyGoogleCalendar().events_day()
