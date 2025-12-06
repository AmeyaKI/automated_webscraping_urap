from playwright.async_api import async_playwright
import asyncio
import random, sys
from datetime import date

# random wait to avoid detection
def rnd_wait():
    return random.uniform(1.0, 2.5)
    

async def run_coroutines(page, url):
    ...



# scrape each url
async def scrape_page(page, url=""):
    email_list = []
    
    for _ in range(2):
        # Reply Button
        await asyncio.sleep(rnd_wait())
        reply_button = page.locator("button.reply-button")
        await reply_button.wait_for(state="visible")
        await reply_button.click()
        print("[INFO] Clicked reply button")

        # Email Button
        await asyncio.sleep(rnd_wait())
        email_button = page.locator(":text-matches('email', 'i')")
        await email_button.wait_for(state="visible")
        await email_button.click()
        print("[INFO] Clicked email button")

        # Craigslist Email
        await asyncio.sleep(rnd_wait())
        email_link_el = page.locator("a[href^='mailto:']")
        await email_link_el.wait_for()

        href = await email_link_el.get_attribute("href")
        email_link = href.replace("mailto:", "").split("?")[0]
        print("[INFO] Extracted email:", email_link)
        
        email_list.append(email_link)
        
        # Refresh
        await page.reload(wait_until='load')
        
    # format each url's list of emails
    def format_emails(url, email_list):
        formatted = f"{url}:::{email_list[0]}, {email_list[1]}"
        return formatted
    
    formatted = format_emails(url, email_list)
    return formatted

# convert results into txt file format
def results_to_txt(entries):
    today = date.today()
    filename = f'{today}_Emails.txt'
    with open(filename, 'a') as file:
        for line in entries:
            file.write(line + '\n')
        print("Saved to txt file.")
        file.close() 
    
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Paste all urls. Press Enter and Cntrl + D to proceed. ")
        url_list = sys.stdin.readlines()
        
        print("Urls Received. Starting collection of emails.")
        
        coroutines = [run_coroutines(page, url) for url in url_list]
        results = await asyncio.gather(*coroutines)
        
        results_to_txt(results)
        
        # 1 url test case
        # url = 'https://newyork.craigslist.org/brk/roo/d/brooklyn-crown-heights-room-3br-2ba/7897488854.html'
        # await page.goto(url)
        # email_list = await scrape_page(page, url)
        # print(email_list)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())