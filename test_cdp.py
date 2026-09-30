import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        print("Connected! Contexts:", len(browser.contexts))
        pages = browser.contexts[0].pages
        for i, page in enumerate(pages):
            print(f"Page {i}: {page.title()} | {page.url}")

asyncio.run(main())
