from scraper import CrossfitLeaderScraper
import os

def menu():
    
	print ("Selecciona una opción")

	print ("\t1 - Web Scrapping con Selenium")

	print ("\t2 - Web Scrapping usando API")

	print ("\t9 - salir")


scaled = 0
division = 1
page = 1
menu()
output_file = "dataset.csv"
scraper = CrossfitLeaderScraper()
while True:
    opcionMenu = input("inserta un numero valor >> ")
    
    rx = input("quieres obtener los resultados de RX (S/n)? ")
    scaled = "0" if rx=="n" else "1"
    
    sex = input("quieres obtener los datos de los hombres (H) o de las mujeres (M)? ")
    division = "2" if sex=="M" else "1"
    print (scaled + " 1 " + division)
    break
    
    if opcionMenu=="1":
        scraper.scrape(scaled,"1",division)
        break
    elif opcionMenu=="2":
        print ("Inserte cuantas paginas quiere Explorar")
        page = input("inserta un numero valor >> ")
        for x in range(1,(int(page)+1)):
            scraper.scrapeWithJson(scaled,str(x),division)
        break
    elif opcionMenu=="9":
        break
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

scraper.data2csv(output_file)
