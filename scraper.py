from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()
# Uncomment to disable headless mode for testing
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the live results page
    driver.get("https://odibets.com/odileague")  # Replace with actual URL
    print("Page loaded successfully.")

    # Wait for match elements to load
    matches = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "gm"))
    )
    print(f"Number of matches found: {len(matches)}")

    results = []
    for match in matches:
        try:
            home_team = match.find_element(By.CLASS_NAME, "t-1-j").text
            away_team = match.find_element(By.CLASS_NAME, "t-2-j").text
            score_elements = match.find_elements(By.CLASS_NAME, "d")
            if len(score_elements) >= 2:
                home_score = score_elements[0].text
                away_score = score_elements[1].text
            else:
                home_score = away_score = "N/A"
            results.append({
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
            })
        except Exception as e:
            print(f"Error extracting match data: {e}")

    # Print results
    for result in results:
        print(result)

finally:
    # Close the browser
    driver.quit()
