import time
import os
import requests  
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SECURITY_ANSWER_1 = os.getenv("SECURITY_ANSWER_1")
SECURITY_ANSWER_2 = os.getenv("SECURITY_ANSWER_2")

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def solve_captcha(driver):
    """Prompt the user to enter the CAPTCHA manually."""
    try:
        wait = WebDriverWait(driver, 10)
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, "captchaImage")))
        print("✅ CAPTCHA detected.")

        # Ask user to enter CAPTCHA manually
        captcha_text = input("📌 Enter CAPTCHA manually: ")
        return captcha_text.strip()

    except Exception as e:
        print(f"❌ CAPTCHA error: {e}")
        return None

try:
    # Step 1: Open the login page
    driver.get("https://atlasauth.b2clogin.com/f50ebcfb-eadd-41d8-9099-a7049d073f5c/b2c_1a_atoproduction_atlas_susi/oauth2/v2.0/authorize?client_id=607d08d6-b63b-4735-ad82-05dfcff7efa4&redirect_uri=https%3A%2F%2Fwww.usvisascheduling.com%2Fsignin-aad-b2c_1&response_type=code%20id_token&scope=openid")

    wait = WebDriverWait(driver, 10)

    # Step 2: Enter email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "signInName")))
    email_input.send_keys(EMAIL)

    # Step 3: Enter password
    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(PASSWORD)

    # Step 4: Solve CAPTCHA manually
    captcha_text = solve_captcha(driver)
    if captcha_text:
        captcha_input = wait.until(EC.presence_of_element_located((By.ID, "extension_atlasCaptchaResponse")))
        captcha_input.send_keys(captcha_text)
    else:
        print("❌ Failed to extract CAPTCHA.")

    # Step 5: Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()

    # Step 6: Wait for security questions page to load
    time.sleep(5)

    # Step 7: Check for iframe (some sites load security questions inside an iframe)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        driver.switch_to.frame(iframes[0])  # Switch to the first iframe

    # Step 8: Fetch security questions dynamically
    try:
        question_1_element = wait.until(EC.presence_of_element_located((By.ID, "kbq2aReadOnly")))
        question_1 = question_1_element.text.strip()
        print(f"🔐 Security Question 1: {question_1}")

        question_2_element = wait.until(EC.presence_of_element_located((By.ID, "kbq3ReadOnly")))
        question_2 = question_2_element.text.strip()
        print(f"🔐 Security Question 2: {question_2}")

        # Step 9: Enter answers from .env
        answer_1_input = driver.find_element(By.ID, "kba2_response")
        answer_1_input.send_keys(SECURITY_ANSWER_1)

        answer_2_input = driver.find_element(By.ID, "kba3_response")
        answer_2_input.send_keys(SECURITY_ANSWER_2)

        # Step 10: Click the continue button
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        continue_button.click()
        print("✅ Security questions answered successfully!")

    except Exception as e:
        print("❌ Security questions not found:", e)

    # Step 11: Navigate to appointment page
    driver.get("https://www.usvisascheduling.com/en-US/applicant_details/")
    time.sleep(5)

    # Step 12: Check for available slots
    try:
        slots = driver.find_elements(By.CLASS_NAME, "appointment-slot")
        if slots:
            print("✅ Available Slots Found! Booking now...")
            slots[0].click()
            time.sleep(2)

            # Step 13: Confirm booking
            confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirm-button")))
            confirm_button.click()
            print("🎉 Appointment booked successfully!")

            # Step 14: Handle OTP manually
            otp_input = wait.until(EC.presence_of_element_located((By.ID, "otp-input")))
            otp_code = input("📩 Enter OTP received: ")
            otp_input.send_keys(otp_code)

            submit_otp = wait.until(EC.element_to_be_clickable((By.ID, "submit-otp")))
            submit_otp.click()
            print("✅ OTP Submitted Successfully!")
        else:
            print("⚠️ No available slots found.")
    except Exception as e:
        print("❌ Error:", e)

finally:
    time.sleep(5)
    driver.quit()
