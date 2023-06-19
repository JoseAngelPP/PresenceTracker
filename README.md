# PresenceTracker
PresenceTracker
## Requirements
- pytest

`pip install -r requirements.txt`
## Run tracker
`python PresenceTracker.py input.txt`

## Run test
`pytest`

## Aproche
Se creó una clase `PresenceTracker` para mantener todo organizado y estrecturado.

Los métodos y sus funciones son las siguientes:
- `validate_datetime_format`: validar que una fecha tenga un formato en especifico. La ídea es que pueda ser usado para validar la fecha en diferentes formatos, por ejemplo, se quiere evaluar qué días son los que más presencias se tienen.
- `process_presence`: este método evalua que la hora de entrada sea antes que la de salida, además de ir actualizando los registros de cada estudiante.
- `calculate_total_minutes`: evalua los minutos a los que corresponde un periodo de tiempo
- `read_file`: lee el archivo de entrada, solo evalua las líneas con información para evitar errores.
- `get_attendance`: itera sobre la lista de estudiantes y se imprimen sus resultados.

### Variables globales
- MINIMUM_PRESENCE_MINUTES = minutos minimos para poder ser evaluado
- DETENTION_TIME_FORMAT = formato esperado para el tiempo de inicio y fin de la detención
