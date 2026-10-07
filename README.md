# Social Media Monitoring Automation

- Python script to extract follower counts from Instagram, YouTube, Facebook, and LinkedIn using Selenium and BeautifulSoup.
- WARNING: The code has not been updated since it was published; the websites may have changed, and the code may no longer work with them.

## Features
- Opens the Edge browser with a real user profile (saved cookies)
- Collects follower counts from public pages (benchmarking and web scraping)
- Saves the history to an Excel spreadsheet
- Error handling for LinkedIn scraping

## How to Use
1. Install the dependencies: "pip install -r requirements.txt"
2. Configure the folder paths in the script
3. Run the ".py" file

## How to Automate on Windows
To run the script daily, I recommend using Windows Task Scheduler.
1. Open Task Scheduler and click "Create Task"
2. In the General tab, check "Run with highest privileges"
3. In the Triggers tab, set the time
4. In the Actions tab, configure:
   - Program: Path to the Python executable (e.g., "C:\Python39\python.exe")
   - Add arguments: The full path to the script (e.g., "C:\Projetos\bot_redes_sociais.py")
5. In the Conditions tab, check "Wake the computer to run this task"
