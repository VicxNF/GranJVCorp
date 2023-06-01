# GranJVCorp

# Requisitos
- Python
- Pip

# Clonar Repositorio
Lo primero que hay que realizar es la clonacion del repositorio en Virtual Studio Code, empezando por abrir el Visual Studio Code, luego darle a "Ver" ("View") luego seleccionar la paleta de comandos y ahi poner Git Clone, y ahí se pega el link del proyecto, selecciona una carpeta y el proyecto se abrirá.

# Instalar Requerimientos
Este proyecto utiliza varias dependencias, que pueden ser instaladas a través del documento Requirements.txt, lo unico que tienes que hacer es colocar el siguiente comando en el directorio en donde está el proyecto: 

```
pip install -r requirements.txt 
```
Con esto ya tendras todas las dependencias instaladas.

# Realizar migraciones
Para que la pagina pueda ser utilizada, hay que realizar las migraciones correspondientes de los modelos necesarios para el funcionamiento de la pagina, para esto, es muy sencillo, precisas de dos codigos:

```
python manage.py makemigrations
python manage.py migrate
```
Con esto, tendras todas las migraciones realizadas

# Arrancar la app
Lo ultimo ya es arrancar la pagina para que funcione, para arrancar la pagina, lo que tienes que hacer es colocar el siguiente codigo en la consola:

```
python manage.py runserver
```
y con esto, la pagina ya estará funcionando correctamente, y para ir a la pagina, debes colocar el siguiente dominio en tu navegador:

```
localhost:8000/home
```
Y con esto, ya estaras navegando en la pagina de GranJVCorp!

# Extra

Para acceder a la api Django Rest Framework de esta pagina, necesitas colocar el siguiente link: 

```
localhost:8000/api/v1/pedidos
```

Y para acceder al documento de la api, se necesita el siguiente link: 

```
localhost:8000/docs
```


