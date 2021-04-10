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
    if opcionMenu=="1":
        scraper.scrape("0","1","1")
        break
    elif opcionMenu=="2":
        for x in range(1,6):
            scraper.scrapeWithJson("0",str(x),"1")
        break
    elif opcionMenu=="9":
        break
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

scraper.data2csv(output_file)
