from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import rowData as rd
import time
import csv

driver = webdriver.Chrome()
driver.get("https://corpus.byu.edu/coca/")
time.sleep(2)

numListInt = 0

def putInCSV(listStuff):
    with open('try.txt', 'a') as file:
        for add in listStuff:
            file.write(str(add))
            file.write('\n')

#search on first screen of copa
def Search(phrase):
    print("starting search")

    #switch to frame inside page
    frame = driver.find_element_by_name('x1')
    driver.switch_to.frame(frame)

    #find callocates button and select it
    tab_switch = driver.find_element_by_id('label3')
    #print(elem)
    tab_switch.click()

    #populate word/phrase
    time.sleep(1)
    word = driver.find_element_by_xpath('//*[@id="p"]')
    word.send_keys(phrase)

    #populate collocates
    coll = driver.find_element_by_xpath('//*[@id="w2"]')
    coll.send_keys("VERB")

    #make five visible
    show = driver.find_element_by_xpath('//*[@id="collocatesSpanRow"]/td/table/tbody/tr/td[1]/a')
    show.click()

    #select five before
    collRow = driver.find_element_by_xpath('//*[@id="cellL5"]')
    collRow.click()

    time.sleep(1)

    #search!
    search = driver.find_element_by_xpath('//*[@id="submit1"]')
    search.click()
    print("\tpressed search")

def itThroughWords():
    print("clicking element 1")
    #time.sleep(2)

    #switch frames
    frame = driver.find_element_by_name('x2')
    driver.switch_to.frame(frame)

    #numList = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[4]/font')
    #numListInt = int(numList.text)

    sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[3]/a')
    sel.click()
    print("\tfinished clicking element 1")
    #return numListInt

def getData():
    print("collecting data")
    #print(numListInt)
    frame = driver.find_element_by_name('x3')
    driver.switch_to.frame(frame)

    run = True
    while(run):
        firstNum = driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a')
        firstNumInt = int(firstNum.text)

        listStuff = []
        count = 1
        fullCount = firstNumInt
        while (fullCount<(firstNumInt+100)):
            resNumber = driver.find_element_by_xpath('//*[@id="showCell_1_'+str(count)+'"]/a')
            year = driver.find_element_by_xpath('//*[@id="showCell_2_'+str(count)+'"]/a')
            medium = driver.find_element_by_xpath('//*[@id="showCell_3_'+str(count)+'"]/a')
            publication = driver.find_element_by_xpath('//*[@id="showCell_4_'+str(count)+'"]/a')
            sentence = driver.find_element_by_xpath('//*[@id="t1_'+str(count)+'"]')

            listStuff.append(rd.rowData(int(resNumber.text), int(year.text), medium.text, publication.text, sentence.text))
            if(fullCount%10 == 0):
                print(fullCount)
            count = count + 1
            fullCount = fullCount + 1

        putInCSV(listStuff)
        print("\twrote to txt finished")

        nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[7]')
        nextButton.click()
        time.sleep(5)
        nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
        if(nextNum == firstNumInt):
            run = False





phrase = "who"
Search(phrase)
driver.switch_to_default_content()

time.sleep(20)
#numlistInt =
itThroughWords()
driver.switch_to_default_content()

time.sleep(10)
getData()


#driver.close()
