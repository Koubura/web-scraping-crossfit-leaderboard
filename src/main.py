from scraper import CrossfitLeaderScraper

output_file = "dataset.csv"

scraper = CrossfitLeaderScraper("0")
scraper.scrape()
scraper.data2csv(output_file)
