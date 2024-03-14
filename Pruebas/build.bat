set parametro=%1
set version=24.03.01
flet build %parametro% -vv --org es.cheny --project pruebas --build-version %version% --route-url-strategy hash 