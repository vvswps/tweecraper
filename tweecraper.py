from selenium import webdriver
from time import sleep
import pyperclip


def main():
    keyFile = open('tweetScraper/keyFile.txt', 'r')
    accFile = open('tweetScraper/accFile.txt', 'r')
    outFile = open('tweetScraper/outFile.txt', 'w')

    driver = webdriver.Firefox()
    cusses = keyFile.readlines()
    accounts = accFile.readlines()
    tweets = []
    for acc_name in accounts:
        for querry in cusses:
            driver.get(f"https://twitter.com/search?q={querry}%20from%3A{acc_name}&src=typed_query")

            sleep(5)
            # sleeps are used to let the webpages fully load
            # and since we're not performing any major actions
            # we dont need to worry about ip bans
            # BUT STILL A VPN IS RECOMMENDED

            for _ in range(3):  # Change the range(number) to scroll more
                try:
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    sleep(3)
                except Exception:
                    break

            tweets.append(getLinks(driver))
        tweets.append("/n")  # Add a newline after each account finishes

    for i in tweets:
        print(i, "\n", file=outFile)

    keyFile.close()
    accFile.close()
    outFile.close()


def getLinks(driver):
    tweets = []
    i = 2
    while True:
        # Twitter uses two different XPATH formats on its website
        # So if the first one fails then try the second format
        # Sometimes twitter gives its own comments on things
        # One problem that this creates is that we have to leave the
        # first tweet all of the time(There may be a workaround)
        # to keep this code short
        try:
            arr = driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/ol[1]/li[{i}]/div/div[2]/div[1]/div/div/button/div/span[1]')
            arr.click()
            lin = driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/ol[1]/li[{i}]/div/div[2]/div[1]/div/div/div/ul/li[1]/button')
            lin.click()

            tweets.append(pyperclip.paste())
        except Exception:
            try:
                arr = driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[{i}]/div/div[2]/div[1]/div/div/button/div/span[1]')
                arr.click()
                lin = driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[{i}]/div/div[2]/div[1]/div/div/div/ul/li[1]/button')
                lin.click()
                tweets.append(pyperclip.paste())
            except Exception:
                # Faliure of both methods means that there aren't any
                # tweets with the specified keyword
                print("Caught exception: No tweets found")
                return tweets
        i += 1
    return tweets


if __name__ == "__main__":
    main()
