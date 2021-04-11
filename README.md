# Web Scrapping Crossfit Leaderboard

Practica 1 de la asignatura _Tipología y ciclo de vida de los datos_, del Máster en Ciencia de Datos de la Universitat Oberta de Catalunya.

## Miembros del equipo

Ha sido realiada por [Ivan Aguilar](https://github.com/koubura) y [Alexander Holler](https://github.com/sirHoller)

## Instalación

Para ejecutar el script es necesarió la instalación de estas bibliotecas:

```
pip install beautifulsoup4
pip install selenium
```

Para usar selenium se necesita un driver que haga de interficie con el navegador, estos drivers estan en la carpeta Drivers, en este proyecto el driver que se esta utilizando es el de Chrome para la version 89.
Para descargar los drivers utiliza los siguientes enlaces:

```
Chrome: 	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge: 	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox: 	https://github.com/mozilla/geckodriver/releases
Safari: 	https://webkit.org/blog/6900/webdriver-support-in-safari-10/
```
En caso de usar otro driver cambiar la linea de uso del driver en la funcion \__donwoload_html del fichero [Scraper.py](https://github.com/Koubura/web-scraping-crossfit-leaderboard/blob/main/src/scraper.py).

Para ejecutar el codigo, debereis escoger el python que tengais las dependencias instaladas y ejecutar en el terminal :

```
(vuestro python) src/main.py
```
