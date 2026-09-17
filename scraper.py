import concurrent.futures
from playwright.sync_api import sync_playwright

def fetch_swiggy_html(url: str) -> str:
    """
    Fetches raw HTML from a Swiggy restaurant URL bypassing anti-bot measures.
    Uses Playwright sync API wrapped for thread execution with auto-scroll logic.
    """
    def _fetch():
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ]
            )
            
            context = browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                geolocation={"latitude": 23.0225, "longitude": 72.5714},
                permissions=["geolocation"]
            )
            
            page = context.new_page()
            
            print(f"Fetching URL: {url}")
            
            # FIX 1: Wait until network is idle so full JS loads properly
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # FIX 2: Wait explicitly for H1 (Restaurant Title) to render
            try:
                page.wait_for_selector("h1", timeout=8000)
            except Exception:
                pass
            
            # FIX 3: Auto-scroll to load dynamic menu items and descriptions
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(1000)
            
            # Final buffer wait to capture complete HTML
            page.wait_for_timeout(2000)
            
            content = page.content()
            browser.close()
            return content

    # Run in ThreadPoolExecutor to prevent Jupyter/Windows asyncio event loop conflicts
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(_fetch)
        return future.result()