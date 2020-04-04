# add files to archive.org Wayback Machine
# install selenium libraries https://selenium.dev/documentation/en/
# install fresh Firefox driver https://github.com/mozilla/geckodriver/
# add its location to PATH or use 'executable_path'
# read https://firefox-source-docs.mozilla.org/testing/geckodriver/
# verified as working in Firefox 72
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
import time

fp = FirefoxProfile()
# block local tracking
fp.set_preference("privacy.donottrackheader.enabled", True)
fp.set_preference("privacy.trackingprotection.enabled", True)
fp.set_preference("privacy.trackingprotection.fingerprinting.enabled", True)
fp.set_preference("privacy.trackingprotection.cryptomining.enabled", True)
fp.set_preference("privacy.trackingprotection.socialtracking.enabled", True)
fp.set_preference("network.cookie.cookieBehavior", 3)  # http://kb.mozillazine.org/Network.cookie.cookieBehavior
fp.update_preferences()

# start Firefox browser
# either using driver from 'executable_path' — Full path to geckodriver.exe
# driver = Firefox(firefox_profile=fp, executable_path="geckodriver.exe")
# or if driver's location is available on the system PATH
driver = Firefox(firefox_profile=fp)

# waiting before adding first url to complete browser start
time.sleep(30)

stringForChecking = "Example Domain"  # replace 'Example Domain' with what you want

# create a utf-8 encoded file URLs.txt with urls, which you want to add to archive.org, one url per line
with open("URLs.txt", encoding="utf8") as file:
    for line in file:
        # start and end time is used for useful logging of adding process
        # every line of file has to be a URL for example https://example.org/example.html
        line = line.rstrip()
        print(time.strftime("%H:%M:%S", time.localtime()), line, "start page loading")
        driver.get("https://web.archive.org/save/" + line)
        # you may check what you want in Web Page Title for errors, for example the same for every page part of a Title
        assert stringForChecking in driver.title
        print(time.strftime("%H:%M:%S", time.localtime()), line, "end page loading", driver.current_url)
        # pause after adding of one url to avoid your IP blocking
        time.sleep(60)
        assert stringForChecking in driver.title
        print(time.strftime("%H:%M:%S", time.localtime()), "page added", line, driver.current_url)
driver.quit()
