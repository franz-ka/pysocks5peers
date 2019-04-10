**! ! EN PRODUCCIÓN ! !**

# Red de peers socks5 en python 

La idea principal es que cada peer hostee una onion y se conecte a otros peers en otras onions. Hay una peer pool compartida entre todos los peers, que representaria la red entera, la subred, y cuando un nuevo peer se introduce se distribuye su peer id a todos los peers y se le da los peer ids de toda la peer pool.

Para el primer uso: 
1. en la raiz creamos un virtual env `python3 -m venv /venv`
2. activamos el venv `source venv/bin/activate`
3. instalamos dependencias `pip install -r requirements.txt`

El servidor escucha en el puerto tcp 65432. Por ende debemos abrir el puerto en el router (port fowarding) y settear la variable `HOST` en `ser.py` con la ip interna lan.

El cliente se conecta al servidor usando `tor`. Por ende debemos tenerlo instalado. Se asume que tor esta en el puerto por defecto 9050.

Arrancamos el servidor `python3 ser.py`

Para arrancar el cliente con un id aleatorio `python3 cli.py`

Para que el cliente tenga siempre el mismo id pasarle un numero, p.ej. `python3 cli.py 33`

Archivos principales:
* `ser.py`
* `cli.py`
