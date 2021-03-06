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

def sendSMSMessage(message:str, log):
    message = twilio_client.messages.create(to='+17329978242', from_="+17325323088", body=message)
    log.status("Sent message: {}".format(message))

#search on first screen of copa
def search(phrase, key, log, driver, num_hits=None):
    log.info("starting search")

    #switch to frame inside page
    frame = driver.find_element_by_name('x1')
    driver.switch_to.frame(frame)

    #find callocates button and select it
    tab_switch = driver.find_element_by_id('label3')
    #print(elem)
    tab_switch.click()

    #populate word/phrase
    time.sleep(2)
    word = driver.find_element_by_xpath('//*[@id="p"]')
    word.send_keys(phrase)

    #populate collocates
    coll = driver.find_element_by_xpath('//*[@id="w2"]')
    coll.send_keys(key)

    #make five visible
    show = driver.find_element_by_xpath('//*[@id="collocatesSpanRow"]/td/table/tbody/tr/td[23]/a')
    show.click()

    #select five before/after (L for before, R for after)
    collRow = driver.find_element_by_xpath('//*[@id="cellR5"]')
    collRow.click()

    if num_hits:
        #find options button
        options = driver.find_element_by_xpath('//*[@id="optionsRow"]/td/a[4]')
        options.click()

        #delete default text in hits txt box and then type 4000
        hits = driver.find_element_by_xpath('//*[@id="numhits"]')
        for _ in range(0, 4):
            hits.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        hits.send_keys('{}'.format(num_hits))

    time.sleep(2)

    #search!
    search = driver.find_element_by_xpath('//*[@id="submit1"]')
    search.click()
    log.info("\tpressed search")
    driver.switch_to_default_content()
    log.info("Start 20 sec sleep")
    time.sleep(20)
    log.info("End 20 sec sleep")

def getData(phrase, key, context, log, driver, start_at = None):
    try:
        log.info("Started data collection on {} {} {}".format(phrase, key, context))
        log.info("Start at number: {}".format(start_at))
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
                while (count<100 and firstNumInt>=start_at):
                    try:
                        resNumber = driver.find_element_by_xpath('//*[@id="showCell_1_'+str(count)+'"]/a')
                        year = driver.find_element_by_xpath('//*[@id="showCell_2_'+str(count)+'"]/a')
                        medium = driver.find_element_by_xpath('//*[@id="showCell_3_'+str(count)+'"]/a')
                        publication = driver.find_element_by_xpath('//*[@id="showCell_4_'+str(count)+'"]/a')
                        sentence = driver.find_element_by_xpath('//*[@id="t1_'+str(count)+'"]')
                    except:
                        count = 101
                        log.warning("\tRan Out of elements to check")
                        break

                    listStuff.append(rd.serialze(rowData(int(resNumber.text), int(year.text), medium.text, publication.text, sentence.text)))
                    if(fullCount%10 == 0):
                        log.info(str(fullCount))
                    count = count + 1
                    fullCount = fullCount + 1

                name = '{}_{}_{}'.format(phrase, key, context)
                if listStuff:
                    putInCSV(listStuff, name)
                log.success("\twrote to {}.json finished".format(name))

                #nextButton = driver.find_element_by_css_selector('//*[@id="resort"]/table/tbody/tr/td/a[6]') #//*[@id="resort"]/table/tbody/tr/td/text()[6] //*[@id="resort"]/table/tbody/tr/td/a[7]

                nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[1]')
                i = 1
                while(True):
                    nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[{}]'.format(i))
                    if ('>' in nextButton.text):
                        log.success("Switched > element")
                        break
                    i += 1

                log.info(time.strftime('%a %H:%M:%S'))
                nextButton.click()

                time.sleep(10)

                nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
                log.info("Next number after page turn is " + str(nextNum))
                log.info("The previous page's first number before switching was " + str(firstNumInt))
                if(nextNum == firstNumInt):
                    log.warning("ran out of elements in " + context + " to look at.")
                    sendSMSMessage("Ran out of elements in {context} - {phrase} to look at after starting at {start_at}. \nEnding Number: {fullCount} \nTIME: {time}".format(context=context, phrase=phrase, start_at=start_at, fullCount=fullCount, time=time.strftime('%a %H:%M:%S')), log)
                    run = False

        else:
            run = True
            while(run):
                firstNum = driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a')
                firstNumInt = (int(firstNum.text))

                listStuff = []
                count = 1
                fullCount = firstNumInt
                while (count<100):
                    try:
                        resNumber = driver.find_element_by_xpath('//*[@id="showCell_1_'+str(count)+'"]/a')
                        year = driver.find_element_by_xpath('//*[@id="showCell_2_'+str(count)+'"]/a')
                        medium = driver.find_element_by_xpath('//*[@id="showCell_3_'+str(count)+'"]/a')
                        publication = driver.find_element_by_xpath('//*[@id="showCell_4_'+str(count)+'"]/a')
                        sentence = driver.find_element_by_xpath('//*[@id="t1_'+str(count)+'"]')
                    except:
                        count = 101
                        log.warning("\tRan Out of elements to check")
                        break

                    listStuff.append(rd.serialze(rowData(int(resNumber.text), int(year.text), medium.text, publication.text, sentence.text)))
                    if(fullCount%10 == 0):
                        log.info(str(fullCount))
                    count = count + 1
                    fullCount = fullCount + 1

                name = '{}_{}_{}'.format(phrase, key, context)
                putInCSV(listStuff, name)
                log.success("\twrote to {}.json finished".format(name))

                #nextButton = driver.find_element_by_css_selector('//*[@id="resort"]/table/tbody/tr/td/a[6]') #//*[@id="resort"]/table/tbody/tr/td/text()[6] //*[@id="resort"]/table/tbody/tr/td/a[7]

                nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[1]')
                i = 1
                while(True):
                    nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[{}]'.format(i))
                    if ('>' in nextButton.text):
                        log.success("Switched > element")
                        break
                    i += 1

                log.info(time.strftime('%a %H:%M:%S'))
                nextButton.click()

                time.sleep(10)

                nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
                log.info("Next number after page turn is " + str(nextNum))
                log.info("The previous page's first number before switching was " + str(firstNumInt))
                if(nextNum == firstNumInt):
                    log.warning("ran out of elements in " + context + " to look at.")
                    sendSMSMessage("Ran out of elements in {context} - {phrase} to look at. \nEnding Number: {fullCount} \nTIME: {time}".format(context=context, phrase=phrase, fullCount= fullCount, time=time.strftime('%a %H:%M:%S')), log)
                    run = False

        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frameset/frame'))
        freq = driver.find_element_by_xpath('//*[@id="label2"]')
        freq.click()
        log.info("clicked back to frequencies")
        time.sleep(5)
        driver.switch_to_default_content()
    except KeyboardInterrupt:
        sendSMSMessage("Script {phrase}_{key}_{context} was canceled at {time}".format(phrase=phrase, key=key, context=context, time=time.strftime('%a %H:%M:%S')), log)
    except:
        sendSMSMessage("Script {phrase}_{key}_{context} failed at {time}".format(phrase=phrase, key=key, context=context, time=time.strftime('%a %H:%M:%S')), log)

def findWord(phrase, key, cont, log, driver, start_at=None):
    frame = driver.find_element_by_name('x2')
    driver.switch_to.frame(frame)
    itCount = 2   #to test: change value to 101 and change while to: itCount>=100 || Should be 2 otherwise
    while(itCount<=1000):
        num = itCount-1
        if type(cont) == int:
            sel_num = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[1]')
            sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[3]/a')
            context = sel.text
            context_num = int(sel_num.text)

            if cont == context_num:
                log.success("Found context: {} number: {}".format(context, context_num))
                sel.click()
                driver.switch_to_default_content()
                time.sleep(10)
                log.success("\tfinished clicking element " + str(context_num) + " --" + context)
                getData(phrase, key, context, log, driver, start_at)
                break
        else:
            sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[3]/a')
            context = sel.text

            if context.lower() == cont.lower():
                log.success("Found context: {}".format(context))
                sel.click()
                driver.switch_to_default_content()
                time.sleep(10)
                log.success("\tfinished clicking element " + str(num) + " --" + context)
                break
        itCount += 1
        

def itThroughWords(phrase, key, log, driver):
    itCount = 2   #to test: change value to 101 and change while to: itCount>=100 || Should be 2 otherwise
    while(itCount<=101):
        num = itCount-1
        log.info("clicking element " + str(num))
        #switch frames
        frame = driver.find_element_by_name('x2')
        driver.switch_to.frame(frame)

        sel = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr['+str(itCount)+']/td[3]/a')
        context = sel.text
        sel.click()
        driver.switch_to_default_content()
        time.sleep(10)
        log.success("\tfinished clicking element " + str(num) + " --" + context)
        getData(phrase, key, context, log, driver)
        itCount += 1

def closeDriver(driver):
    driver.close()

def save_htmls(phrase, key, context, log, driver, start_at=1):
    frame = driver.find_element_by_name('x3')
    driver.switch_to.frame(frame)

    log.info('Started save_html')
    directory = 'html/{phrase}_{key}_{context}/'.format(phrase=phrase, key=key, context=context)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    run = True
    cnt = 1
    while(run):
        firstNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)

        if cnt >= start_at:
            fname = '{dir}{cnt}.html'.format(dir=directory, cnt=cnt)
            with open(fname, 'w') as w:
                w.write(driver.page_source)
                log.info('Wrote {}'.format(fname))

        # Click the next button
        nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[1]')
        i = 1
        while(True):
            nextButton = driver.find_element_by_xpath('//*[@id="resort"]/table/tbody/tr/td/a[{}]'.format(i))
            if ('>' in nextButton.text):
                log.success("Switched > element")
                break
            i += 1
        log.info(time.strftime('%a %H:%M:%S'))
        nextButton.click()
        cnt += 1

        # Wait for page to refresh
        log.info('\tStart 10 sec sleep')
        time.sleep(10)
        log.info('\tEnd 10 sec sleep')

        nextNum = int(driver.find_element_by_xpath('//*[@id="showCell_1_1"]/a').text)
        log.info("Next number after page turn is " + str(nextNum))
        log.info("The previous page's first number before switching was " + str(firstNum))
        if(nextNum == firstNum):
            log.warning("ran out of elements in " + context + " to look at.")
            run = False