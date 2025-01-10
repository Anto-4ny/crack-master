from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup Selenium WebDriver
driver = webdriver.Chrome()  # Or your preferred driver
driver.get("https://example.com/live-results")

# Wait for elements to load (optional, based on page behavior)
driver.implicitly_wait(10)

# Extract data from live match elements
matches = driver.find_elements(By.CLASS_NAME, "gm")  # Adjust class name
results = []
for match in matches:
    home_team = match.find_element(By.CLASS_NAME, "t-1-j").text
    away_team = match.find_element(By.CLASS_NAME, "t-2-j").text
    home_score = match.find_element(By.CLASS_NAME, "d").text
    away_score = match.find_elements(By.CLASS_NAME, "d")[1].text  # Assuming two 'd' divs
    results.append({
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
    })

# Print results
for result in results:
    print(result)

# Close the browser
driver.quit()
