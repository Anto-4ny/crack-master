from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome resource issues

# Initialize WebDriver with options
driver = webdriver.Chrome(options=chrome_options)  # Specify ChromeDriver path if necessary

try:
    # Navigate to the live results page
    driver.get("https://odibets.com/odileague")  # Replace with the actual URL

    # Wait for elements to load
    driver.implicitly_wait(10)

    # Extract data from live match elements
    matches = driver.find_elements(By.CLASS_NAME, "gm")  # Adjust 'gm' based on your webpage structure
    results = []
    for match in matches:
        # Extract home team
        home_team = match.find_element(By.CLASS_NAME, "t-1-j").text
        
        # Extract away team
        away_team = match.find_element(By.CLASS_NAME, "t-2-j").text
        
        # Extract scores
        score_elements = match.find_elements(By.CLASS_NAME, "d")  # Assuming there are two 'd' divs for scores
        if len(score_elements) >= 2:  # Ensure there are enough elements
            home_score = score_elements[0].text
            away_score = score_elements[1].text
        else:
            home_score = away_score = "N/A"  # Handle cases with missing scores

        # Append extracted data to results
        results.append({
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
        })

    # Print results
    for result in results:
        print(result)

finally:
    # Ensure the browser is closed after script execution
    driver.quit()
