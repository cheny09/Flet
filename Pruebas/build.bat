set parametro=%1
set version=24.03.01
flet build %parametro% -vv --org es.cheny --project plnbeta --product "Planilla Turnos de Trabajo" --build-version %version% --build-number 1021240102 --route-url-strategy "path" 
