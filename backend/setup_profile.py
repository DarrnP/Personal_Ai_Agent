import asyncio
import urllib.parse
from playwright.async_api import async_playwright

async def setup_profile():
    profile_name = input("Enter profile name (e.g., personal, work, other): ").strip()
    folder_path = f"./chrome_profiles/{profile_name}"
    
    async with async_playwright() as p:
        print(f"\n Opening profile folder at: {folder_path}")
               
        context = await p.chromium.launch_persistent_context(
            user_data_dir=folder_path,
            headless=False,  
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://mail.google.com")        
        print("\n Browser opened!")
        print("Please log into your email account in the opened Chrome window.")
                
        input("\nPress ENTER here in your terminal once you are completely logged in...")
                
        await context.close()
        print(f"Profile '{profile_name}' saved successfully to {folder_path}!\n")

if __name__ == "__main__":
    asyncio.run(setup_profile())