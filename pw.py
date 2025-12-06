from playwright.async_api import async_playwright
import asyncio
import random 
from datetime import date


# use asyncio to scrape multiple webpages AT ONCE

# asyncio.gather(
#     ...,
#     ...
# )

# random wait to avoid automation
def rnd_wait():
    return random.uniform(1.0, 2.5)
    
async def scrape_email(page):
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

    return email_list

def clean_emails(email_list):
    ...
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

        await page.goto("https://newyork.craigslist.org/brk/roo/d/brooklyn-crown-heights-room-3br-2ba/7897488854.html")
        email_list = await scrape_email(page)

        print("Emails:", email_list)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())