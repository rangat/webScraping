from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

from twilio.rest import Client
import config

import json
import rowData as rd
from rowData import rowData
import time
import csv
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://corpus.byu.edu/coca/")
time.sleep(2)

numListInt = 0

def putInCSV(listStuff, name):
    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/'+name+'.json', 'a') as outfile:
        json.dump(listStuff, outfile)

def sendSMSMessage(message:str):
    message = twilio_client.messages.create(to='+17329978242', from_="+17325323088", body=message)
    print("Sent message: {}".format(message))

#search on first screen of copa
def search(phrase, key, num_hits=None):
    print("starting search")

    #switch to frame inside page
    frame = driver.find_element_by_name('x1')
    driver.switch_to.frame(frame)

    #find callocates button and select it
    tab_switch = driver.find_element_by_id('label3')
    #print(elem)
    tab_switch.click()

    #begin looping here

    #populate word/phrase
    time.sleep(2)
    word = driver.find_element_by_xpath('//*[@id="p"]')
    word.send_keys(phrase)

    #populate collocates
    coll = driver.find_element_by_xpath('//*[@id="w2"]')
    coll.send_keys(key)

    #make five visible
    show = driver.find_element_by_xpath('//*[@id="collocatesSpanRow"]/td/table/tbody/tr/td[1]/a')
    show.click()

    #select five before
    collRow = driver.find_element_by_xpath('//*[@id="cellL5"]')
    collRow.click()

    if num_hits:
        #find options button
        options = driver.find_element_by_xpath('//*[@id="optionsRow"]/td/a[4]')
        options.click()

        #delete default text in hits txt box and then type 4000
        hits = driver.find_element_by_xpath('//*[@id="numhits"]')
        for i in range(0, 4):
            hits.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        hits.send_keys('{}'.format(num_hits))

    time.sleep(2)

    #search!
    search = driver.find_element_by_xpath('//*[@id="submit1"]')
    search.click()
    print("\tpressed search")
    driver.switch_to_default_content()
    time.sleep(20)

def getData(phrase, key, context, start_at = None):
    try:
        print("Started data collection on {} {} {}".format(phrase, key, context))
        #print(numListInt)
        frame = driver.find_element_by_name('x3')
        driver.switch_to.frame(frame)

        if start_at:
            run = True
            while(run):
                firstNum = driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a')
                firstNumInt = (int(firstNum.text))

                listStuff = []
                count = 1
                fullCount = firstNumInt
                while (count<100 and firstNumInt>start_at):
                    try:
                        resNumber = driver.find_element_by_xpath('//*[@id="showCell_1_'+str(count)+'"]/a')
                        year = driver.find_element_by_xpath('//*[@id="showCell_2_'+str(count)+'"]/a')
                        medium = driver.find_element_by_xpath('//*[@id="showCell_3_'+str(count)+'"]/a')
                        publication = driver.find_element_by_xpath('//*[@id="showCell_4_'+str(count)+'"]/a')
                        sentence = driver.find_element_by_xpath('//*[@id="t1_'+str(count)+'"]')
                    except:
                        count = 101
                        print("\tRan Out of elements to check")
                        break

                    listStuff.append(rd.serialze(rowData(int(resNumber.text), int(year.text), medium.text, publication.text, sentence.text)))
                    if(fullCount%10 == 0):
                        print(fullCount)
                    count = count + 1
                    fullCount = fullCount + 1

                name = '{}_{}_{}'.format(phrase, key, context)
                if listStuff:
                    putInCSV(listStuff, name)
                print("\twrote to {}.json finished".format(name))

                #nextButton = driver.find_element_by_css_selector('//*[@id="resort"]/table/tbody/tr/td/a[6]') #//*[@id="resort"]/table/tbody/tr/td/text()[6] //*[@id="resort"]/table/tbody/tr/td/a[7]

                nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[6]')
                print("|"+nextButton.text+"|")
                if not (nextButton.text=='>  '):
                    print("Switched > element")
                    nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[7]')

                print(time.strftime('%a %H:%M:%S'))
                nextButton.click()

                time.sleep(10)

                nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
                print("Next number after page turn is " + str(nextNum))
                print("The previous page's first number before switching was " + str(firstNumInt))
                if(nextNum == firstNumInt):
                    print("ran out of elements in " + context + " to look at.")
                    sendSMSMessage("Ran out of elements in {context} to look at after starting at {start_at}. \nEnding Number: {fullCount} \nTIME: {time}".format(context=context, start_at=start_at, fullCount=fullCount, time=time.strftime('%a %H:%M:%S')))
                    run = False

        else:
            run = True
            while(run):
                firstNum = driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a')
                firstNumInt = (int(firstNum.text))

                listStuff = []
                count = 1
                fullCount = firstNumInt
                while (count<100 and firstNumInt>3399):
                    try:
                        resNumber = driver.find_element_by_xpath('//*[@id="showCell_1_'+str(count)+'"]/a')
                        year = driver.find_element_by_xpath('//*[@id="showCell_2_'+str(count)+'"]/a')
                        medium = driver.find_element_by_xpath('//*[@id="showCell_3_'+str(count)+'"]/a')
                        publication = driver.find_element_by_xpath('//*[@id="showCell_4_'+str(count)+'"]/a')
                        sentence = driver.find_element_by_xpath('//*[@id="t1_'+str(count)+'"]')
                    except:
                        count = 101
                        print("\tRan Out of elements to check")
                        break

                    listStuff.append(rd.serialze(rowData(int(resNumber.text), int(year.text), medium.text, publication.text, sentence.text)))
                    if(fullCount%10 == 0):
                        print(fullCount)
                    count = count + 1
                    fullCount = fullCount + 1

                name = '{}_{}_{}'.format(phrase, key, context)
                putInCSV(listStuff, name)
                print("\twrote to {}.json finished".format(name))

                #nextButton = driver.find_element_by_css_selector('//*[@id="resort"]/table/tbody/tr/td/a[6]') #//*[@id="resort"]/table/tbody/tr/td/text()[6] //*[@id="resort"]/table/tbody/tr/td/a[7]

                nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[6]')
                print("|"+nextButton.text+"|")
                if not (nextButton.text=='>  '):
                    print("Switched > element")
                    nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[7]')

                print(time.strftime('%a %H:%M:%S'))
                nextButton.click()

                time.sleep(10)

                nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
                print("Next number after page turn is " + str(nextNum))
                print("The previous page's first number before switching was " + str(firstNumInt))
                if(nextNum == firstNumInt):
                    print("ran out of elements in " + context + " to look at.")
                    sendSMSMessage("Ran out of elements in {context} to look at. \nEnding Number: {fullCount} \nTIME: {time}".format(context=context, fullCount= fullCount, time=time.strftime('%a %H:%M:%S')))
                    run = False

        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frameset/frame'))
        freq = driver.find_element_by_xpath('//*[@id="label2"]')
        freq.click()
        print("clicked back to frequencies")
        time.sleep(5)
        driver.switch_to_default_content()
    except:
        sendSMSMessage("Script {phrase}_{key}_{context} failed at {time}".format(phrase=phrase, key=key, context=context, time=time.strftime('%a %H:%M:%S')))

def findWord(phrase, key, cont, start_at=None):
    frame = driver.find_element_by_name('x2')
    driver.switch_to.frame(frame)
    itCount = 2   #to test: change value to 101 and change while to: itCount>=100 || Should be 2 otherwise
    while(itCount<=101):
        num = itCount-1
        sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[3]/a')
        context = sel.text

        if context.lower() == cont.lower():
            print("Found context: {}".format(context))
            sel.click()
            driver.switch_to_default_content()
            time.sleep(10)
            print("\tfinished clicking element " + str(num) + " --" + context)
            getData(phrase, key, context, start_at)
            break
        itCount += 1
        

def itThroughWords(phrase, key):
    itCount = 2   #to test: change value to 101 and change while to: itCount>=100 || Should be 2 otherwise
    while(itCount<=101):
        num = itCount-1
        print("clicking element " + str(num))
        #switch frames
        frame = driver.find_element_by_name('x2')
        driver.switch_to.frame(frame)

        sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[3]/a')
        context = sel.text
        sel.click()
        driver.switch_to_default_content()
        time.sleep(10)
        print("\tfinished clicking element " + str(num) + " --" + context)
        getData(phrase, key, context)
        itCount += 1

def closeDriver():
    driver.close()
