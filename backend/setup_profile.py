import asyncio
import urllib.parse
from playwright.async_api import async_playwright

async def setup_profile():
    # 1. Ask which profile you want to log into
    profile_name = input("Enter profile name (e.g., personal, work, other): ").strip()
    folder_path = f"./chrome_profiles/{profile_name}"
    
    async with async_playwright() as p:
        print(f"\n Opening profile folder at: {folder_path}")
        
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=folder_path,
            headless=False,  
        )
        
        # 3. Open Gmail page
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://mail.google.com")
        
        print("\n Browser opened!")
        print("Please log into your email account in the opened Chrome window.")
        
        
        input("\nPress ENTER here in your terminal once you are completely logged in...")
        
        
        await context.close()
        print(f"Profile '{profile_name}' saved successfully to {folder_path}!\n")


async def extract_emails_by_date(
    profile_name: str = "college", 
    before_date: str = "2026/09/20", 
    max_chars: int = 4000
) -> str:
    folder_path = f"./chrome_profiles/{profile_name}"
    
    # Build Gmail search query (e.g., "is:unread before:2026/09/20")
    search_query = f"is:unread before:{before_date}"
    encoded_query = urllib.parse.quote(search_query)
    search_url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"
    
    async with async_playwright() as p:
        print(f"Opening '{profile_name}' profile for emails before {before_date}")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=folder_path,
            headless=False
        )
        
        page = context.pages if context.pages else await context.new_page()
        
        # 1. Navigate directly to filtered search results
        await page[0].goto(search_url)
        await page[0].wait_for_selector("body")
        
        # Give search results 2 seconds to render in DOM
        await page[0].wait_for_timeout(2000)
        
        # 2. Extract visible text from filtered results
        raw_text = await page[0].evaluate("() => document.body.innerText")
        
        await context.close()
        
        # 3. Limit characters for Ollama context window
        return raw_text[:max_chars]

if __name__ == "__main__":
    profile = input("Which profile? (e.g., personal, work): ").strip()
    target_date = input("Enter 'before' date (YYYY/MM/DD, e.g. 2026/09/20): ").strip()
    
    email_text = asyncio.run(extract_emails_by_date(
        profile_name=profile, 
        before_date=target_date, 
        max_chars=4000
    ))
    
    print("\n--- Extracted Text Preview ---")
    print(email_text[:600])