import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        cookies = await context.cookies()
        for c in cookies:
            if c['name'] in ['sid', 'clientSrc']:
                print(f"Cookie: {c['name']} domain: {c['domain']} path: {c['path']}")
        
        # Also let's check what window.ApexCSIPage or Salesforce session info is in Page 2
        for page in context.pages:
            if "ApexCSIPage" in page.url:
                print("Found Developer Console Page:", page.url)
                # Let's get the sid cookie for that domain
                page_cookies = await context.cookies(page.url)
                for pc in page_cookies:
                    if pc['name'] == 'sid':
                        print("Found sid cookie for dev console! Length:", len(pc['value']))
                        with open("session_id.txt", "w") as f:
                            f.write(pc['value'])
                        print("Saved sid to session_id.txt!")

asyncio.run(main())
