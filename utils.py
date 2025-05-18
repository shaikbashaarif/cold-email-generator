from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def extract_job_description(url: str) -> str:
    """
    Extracts the job description text from a given job posting URL.

    Parameters:
        url (str): The URL of the job listing.

    Returns:
        str: The extracted job description text.
    """
    # Setup Chrome options
    options = Options()
    options.headless = True  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start driver
    driver = webdriver.Chrome(options=options)
    
    try:
        
        # Load the job URL
        driver.get(url)

        # Wait for the page to fully render
        time.sleep(5)

        # Get full rendered HTML
        html = driver.page_source

        # Parse using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Try extracting based on known class
        description = soup.find("div", {"class": "phw-job-description phw-g-i-ezrVIv"})
        if not description:
            # Fallback to first available section or div
            description = soup.find("section") or soup.find("div")

        # Get cleaned up text
        content = description.get_text(strip=True, separator="\n") if description else "No description found"
        return content

    finally:
        driver.quit()
