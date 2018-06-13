from selenium import webdriver
# from selenium.webdriver.common.keys import Keys as keys
import time, csv, sys, datetime, json


def main():
    pjs_path = 'ignore/phantomjs-2.1.1-windows/bin/phantomjs.exe'
    url = "https://inagoflyer.appspot.com/btcmac"
    driver = webdriver.PhantomJS(executable_path=pjs_path)
    driver.get(url)
    print("Connection successful.")
    for i in range(0,10):
        print("現在回数：" + str(i))
        inago_info = inago(driver)
        print(inago_info)
        time.sleep(10)
    driver.quit()

def inago(driver):
    buy = driver.find_elements_by_id("buyVolumePerMeasurementTime")[0]
    sell = driver.find_elements_by_id("sellVolumePerMeasurementTime")[0]
    bf_fx = driver.find_elements_by_id("bitFlyer_FXBTCJPY_lastprice")[0]
    if bf_fx is None:
        sys.exit()
    return list(map(float, [buy.text, sell.text, bf_fx.text]))
    
    
if __name__ == '__main__':
    main()
        
