# Archive URL to [archive.org WayBack Machine](https://archive.org/web/)

You can use this program to add URLs to [Archive.org WayBack Machine](https://archive.org/web/) using [Python](https://www.python.org/), [Selenium WebDriver](https://www.selenium.dev/) and [Firefox](https://www.mozilla.org/en-US/firefox/new/).

* Install Python <https://www.python.org>.
* Install Selenium libraries <https://selenium.dev/documentation/en/>.
* Read <https://www.selenium.dev/selenium/docs/api/py/index.html>.
* Read <https://selenium-python.readthedocs.io/>.
* Install fresh Firefox driver <https://github.com/mozilla/geckodriver/> and add its location to system PATH or use 'executable_path'.
* Read <https://firefox-source-docs.mozilla.org/testing/geckodriver/>.
* Read comments in [main.py](main.py).
* Create a utf-8 encoded file URLs_source.txt with urls, which you want to add to archive.org, one url per line every line of file has to be a URL for example <https://example.org/example.html>.
* I use timestamped messages to visually log the steps in URL processing. You can comment it.
* If you see a message that the URL is NOT archived — do not worry about it. You will see not archived URLs in a new file (it will be created after processing of all URLs) and you can try to archive them again. Pause at least a few minutes before re-adding such URLs.

Verified in October 2020 that this program works in Firefox 81.
