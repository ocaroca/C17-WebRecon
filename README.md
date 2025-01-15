# C17-WebRecon

## Descripción
Script en python para detectar cambios en el contenido de páginas web.

Se descarga el contenido de las webs especificadas en el archivo urls.txt, se crea un hash y se compara con el anterior.

Si han habido cambios en la web, se envía una notificación mediante el comando notify a telegram.

## Utilizar el script
```bash
python3 c17-webrecon.py
```
