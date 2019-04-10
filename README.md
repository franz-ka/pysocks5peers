**! ! EN PRODUCCIÓN ! !**

# pyflaskapp

Para el primer uso: 
1. en la raiz creamos un virtual env `python3 -m venv /venv`
2. activamos el venv `source venv/bin/activate`
3. instalamos dependencias `pip install -r requirements.txt`
4. setteamos la variable `export FLASK_APP=flask1`
5. `flask run` para hostear la app en http://127.0.0.1:5000
6. `flask init-db` para inicializar y cargar la db

Posteriormente solo hace falta hacer `flask run` para hostear o `python3 run.py`

Archivos principales:
* `models.py` tiene la estructura de la db
* `db.py` carga registros a la db (al usar `flask init-db`)
* `routes.py` tiene las acciones por url
* `templates/` contiene los html

Unas screens:
![alt text](https://i.ibb.co/M2LJ83d/11.png)
![alt text](https://i.ibb.co/qWxDMsM/22.png)
