# Archive URLs to archive.org Wayback Machine with Python, Selenium and Firefox
# Copyright 2020 andrij krasotkin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.common.exceptions import TimeoutException
import time


def archive_urls(source_urls_file="URLs_source.txt",
                 archived_urls_file="URLs_archived.txt"):
    '''This function processes URLs in source_urls_file and try to add them to Wayback Machine'''
    #
    #    Set Firefox Pprofile
    #      If you want to use clean Firefox Profile
    fp = FirefoxProfile()
    #      If you want  block tracking and cookies use next several lines
    #      read http://kb.mozillazine.org/Network.cookie.cookieBehavior
    # fp.set_preference("privacy.donottrackheader.enabled", True)
    # fp.set_preference("privacy.trackingprotection.enabled", True)
    # fp.set_preference("privacy.trackingprotection.fingerprinting.enabled", True)
    # fp.set_preference("privacy.trackingprotection.cryptomining.enabled", True)
    # fp.set_preference("privacy.trackingprotection.socialtracking.enabled", True)
    # fp.set_preference("network.cookie.cookieBehavior", 3)
    # fp.update_preferences()
    #
    #      If you want to use existing Firefox Profile use next line
    # fp = FirefoxProfile('c:/path/to/existing/FirefoxProfile/')
    #
    #    Open browser window
    #      either using driver from 'executable_path' — Full path to geckodriver.exe
    # driver = Firefox(firefox_profile=fp, executable_path="c:/path/to/geckodriver.exe")
    #      or if driver's location is available on the system PATH using it
    driver = Firefox(firefox_profile=fp)
    #
    #    Set the amount of time to wait for a page load to complete before throwing an error
    driver.set_page_load_timeout(1200)
    #
    #    Replace 'Example Domain' with what you want to check in Page Title
    string_in_title = "Example Domain"

    def check_url_startswith(start_string):
        '''This function checks if the url has correct prefix'''
        url = driver.current_url
        return url.startswith(start_string)

    def process_url_after_loading():
        '''This function checks a url after the URL is loaded. It may help with catch "Wayback Exception" error.'''
        check_url_wait_time = 0
        # how long check url
        check_url_wait_time_limit = 120

        while True:

            time.sleep(5)

            if check_url_startswith("https://web.archive.org/web/") is True:
                time.sleep(5)
                check_title(string_in_title)
                break

            if check_url_wait_time > check_url_wait_time_limit:
                print(
                    "\t",
                    time.strftime("%H:%M:%S", time.localtime()),
                    "URL NOT processed correctly due wait_time is over. I will try to process it again."
                )
                process_url(url)
                break
            else:
                check_url_wait_time += 5

    def check_title(string_in_title):
        '''This function checks the page title to see if the page has been archived or not.'''
        title = driver.title

        if "Wayback" in title:
            print(
                "\t",
                time.strftime("%H:%M:%S", time.localtime()),
                "URL is NOT archived Wayback in title",
                driver.title,
            )

        elif string_in_title in title:
            archived_urls_file.write(url + "\n")
            print(
                "\t",
                time.strftime("%H:%M:%S", time.localtime()),
                "URL is archived"
            )

        else:
            print(
                "\t",
                time.strftime("%H:%M:%S", time.localtime()),
                "URL is NOT archived 'string_in_title' is not in title",
                driver.title,
            )

    def process_url(url):
        '''This function processes one URL to get added'''

        print("\n\n", url)
        print(
            "\t",
            time.strftime("%H:%M:%S", time.localtime()),
            "start URL processing"
        )

        try:
            driver.get("https://web.archive.org/save/" + url)

        except TimeoutException:
            print(
                "\t",
                time.strftime("%H:%M:%S", time.localtime()),
                "URL NOT processed correctly due TimeoutException. I will try to process it again after pause. Please wait."
            )
            time.sleep(60)
            process_url(url)

        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)

        else:
            print("\t", time.strftime("%H:%M:%S", time.localtime()), "URL loaded")
            process_url_after_loading()

            # Pause after adding a url to avoid your IP blocking, do not decrease this value!!!
            time.sleep(30)

    # wait to complete browser start
    time.sleep(30)

    with open(source_urls_file, encoding="utf8") as source_urls_file,\
            open(archived_urls_file, "a", encoding="utf8") as archived_urls_file:

        for url in source_urls_file:
            url = url.rstrip()
            process_url(url)

    # close web browser window
    driver.quit()


def create_not_archived_urls_file(
        source_urls_file="URLs_source.txt",
        archived_urls_file="URLs_archived.txt",
        new_source_urls_file="URLs_for_archiving.txt"):
    '''This function creates a file with not added URLs'''

    print(
        "\n\n",
        time.strftime("%H:%M:%S", time.localtime()),
        "create_not_archive_urls_file",
    )

    with open(source_urls_file, encoding="utf8") as source_file,\
            open(new_source_urls_file, "w", encoding="utf8", newline="\n") as new_source_file:

        for source_line in source_file:
            archived = False
            with open(archived_urls_file, encoding="utf8") as archived_file:
                for archived_line in archived_file:
                    if source_line.rstrip() == archived_line.rstrip():
                        archived = True
                        break
                if archived is False:
                    new_source_file.write(source_line.rstrip() + "\n")


try:
    archive_urls()
except Exception as e:
    print(type(e))
    print(e.args)
    print(e)
finally:
    create_not_archived_urls_file()
