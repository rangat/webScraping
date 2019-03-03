import solScrape

p = input("What phrase do you want to search for? ")
w = input("What word do you want to search for (know)? ")
start = input("What number do you want to start at? ")

if start == "":
    start = None
print(start)

phrase = p
key = "VERB"
solScrape.search(phrase, key)
solScrape.findWord(phrase, key, w, start_at=start)
solScrape.closeDriver()
