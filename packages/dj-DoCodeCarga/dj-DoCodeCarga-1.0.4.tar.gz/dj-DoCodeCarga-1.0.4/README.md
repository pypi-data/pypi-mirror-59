# dj-DoCodeCarga (Django-App)

[![N|Solid](https://docode.com.mx/img/poweredbydocode.png)](https://docode.com.mx/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

DoCodeCarga es una aplicacion para generar un layout en Excel en base a un modelo asi mismo permite cargar dicho layout con informacion masivamente.

### Tecnologia

DoCodeDB se implementa con las siguientes librerias previamente instaladas:

* [Django](https://www.djangoproject.com/) - Python base framework (v2.2)
* [openpyxl](https://pypi.org/project/openpyxl/) - Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

### Instalacion

Instalar por medio de [pip](https://pypi.org/project/pip/)

```sh
$ pip install dj-DoCodeCarga
```
### Estructura de la App
La aplicacion tiene una estructura comun de una app [Django](https://www.djangoproject.com/)
```sh
DoCodeCarga/
	procesos
	static
	templates
	templatetags
  admin.py
	apps.py
  models.py
	urls.py
	views.py
```

### Configuracion:

Agregar la App a "INSTALLED_APPS" dentro de los **settings.py**
```sh
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DoCodeCarga',
]
```


### Uso:

**views.py**
- Se incluye ambos procesos **Proceso para descargar layout** y **Proceso para Leer Excel**
                    
```sh
from DoCodeCarga.procesos import layout

# Proceso para descargar Layout
if layout.verificar(request):
        return layout.descargar(Modelo)

# Metodo para cargar Excel
result = layout.cargar(request,model)
context = {
  'titulo' : titulo,
}
return render(request, 'template.html', context)
```


#### Configuracion de Template
- Se debe incluir el template **layoutCarga.html** para habilitar los botones

```sh
{% include 'layoutCarga.html' %}
```


#### Actualizacion v1.0.4

- Se actualiza para poder utlizar la funcion choices dentro de los modelos
- Se implementa el template **layoutCarga.html**


#### Licencia
----
MIT License

Copyright (c) 2020 DoCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.