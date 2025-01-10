from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the live results page
    driver.get("https://odibets.com/odileague")  # Replace with the actual URL

    # Wait for elements to load
    driver.implicitly_wait(10)

    # Locate match elements (both live and upcoming)
    matches = driver.find_elements(By.CLASS_NAME, "gm")  # Adjust based on the page's structure

    results = []
    for match in matches:
        # Extract teams
        home_team = match.find_element(By.CLASS_NAME, "t-1-j").text
        away_team = match.find_element(By.CLASS_NAME, "t-2-j").text
        
        # Extract scores or placeholders
        score_elements = match.find_elements(By.CLASS_NAME, "d")
        if len(score_elements) >= 2:
            home_score = score_elements[0].text
            away_score = score_elements[1].text
        else:
            home_score = away_score = "N/A"  # Handle missing scores

        # Identify if it's an upcoming match (e.g., if scores are placeholders like '-')
        if home_score == "-" and away_score == "-":
            match_status = "Upcoming"
            # Optionally extract date and time for upcoming matches
            try:
                match_time = match.find_element(By.CLASS_NAME, "match-time-class").text  # Adjust class name
            except:
                match_time = "TBD"
        else:
            match_status = "Ongoing/Completed"
            match_time = "N/A"

        # Append data to results
        results.append({
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "status": match_status,
            "match_time": match_time,
        })

    # Print results
    for result in results:
        print(result)

finally:
    # Ensure the browser is closed
    driver.quit()
