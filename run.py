import solScrape

phrase = "how"
key = "VERB"
solScrape.search(phrase, key)
solScrape.findWord(phrase, key, "know", start_at=43899)
solScrape.closeDriver()
