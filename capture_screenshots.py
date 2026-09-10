"""Playwright script to capture Achilles chat UI screenshots for FL-07 evidence."""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "achilles_chat.html"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"file:///{HTML_PATH.resolve()}")
        
        # Wait for UI to load and fix userId so preferences persist
        page.wait_for_selector("#userInput", timeout=10000)
        page.evaluate("window.userId = 'screenshot_user_01'")
        time.sleep(1)
        
        # Screenshot 1: Initial empty state
        page.screenshot(path=SCREENSHOTS_DIR / "01-chat-ui-empty.png")
        
        # Query 1: Ethiopian berry
        page.fill("#userInput", "What Ethiopian coffee has berry notes?")
        page.click("#sendBtn")
        page.wait_for_timeout(1500)
        page.screenshot(path=SCREENSHOTS_DIR / "02-chat-ethiopian-berry.png")
        
        # Query 2: Preference learning
        page.fill("#userInput", "I prefer natural processed coffees")
        page.click("#sendBtn")
        page.wait_for_timeout(1500)
        page.screenshot(path=SCREENSHOTS_DIR / "03-chat-preference-learn.png")
        
        # Query 3: Preference recall
        page.fill("#userInput", "What do you recommend from Ethiopia?")
        page.click("#sendBtn")
        page.wait_for_timeout(1500)
        page.screenshot(path=SCREENSHOTS_DIR / "04-chat-preference-recall.png")
        
        # Query 4: No match fallback
        page.fill("#userInput", "Do you have any teas?")
        page.click("#sendBtn")
        page.wait_for_timeout(1500)
        page.screenshot(path=SCREENSHOTS_DIR / "05-chat-no-match.png")
        
        browser.close()
        print("Screenshots captured:")
        for f in sorted(SCREENSHOTS_DIR.glob("*.png")):
            print(f"  - {f.name}")

if __name__ == "__main__":
    capture()
