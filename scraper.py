from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_linkedin_jobs(query, location="", max_results=50):
    # Setup the driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless for no GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # LinkedIn job search page
    url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    job_list = []
    job_count = 0

    # Scroll to load more jobs and scrape them
    while job_count < max_results:
        # Scrape job details on current page
        jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
        for job in jobs:
            try:
                title = job.find_element(By.CSS_SELECTOR, ".job-card-list__title").text
                company = job.find_element(By.CSS_SELECTOR, ".job-card-container__company-name").text
                location = job.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item").text
                link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                description = job.find_element(By.CSS_SELECTOR, ".job-card-list__description").text
                job_list.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                    "description": description
                })
                job_count += 1
                if job_count >= max_results:
                    break
            except Exception as e:
                continue

        if job_count >= max_results:
            break

        # Scroll down the page to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for more jobs to load

    driver.quit()
    return job_list
