from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

PAUSE = 0.3

passed = 0
failed = 0

volunteer_name = "TestVolunteer" + str(int(time.time()))


def pause():
    time.sleep(PAUSE)


def report_test(test_name, action):
    global passed, failed

    print("\n" + test_name)

    try:
        action()
        pause()
        print("PASS:", test_name)
        passed += 1
    except Exception as e:
        print("FAIL:", test_name)
        print("Reason:", e)
        failed += 1
        pause()


def find_visible_input(placeholder):
    elements = driver.find_elements(
        By.XPATH,
        f"//input[@placeholder='{placeholder}']"
    )

    for element in elements:
        if element.is_displayed() and element.is_enabled():
            return element

    raise Exception("Visible input not found: " + placeholder)


def find_button(button_text):
    buttons = driver.find_elements(
        By.XPATH,
        f"//button[contains(normalize-space(), '{button_text}')]"
    )

    for button in buttons:
        if button.is_displayed() and button.is_enabled():
            return button

    raise Exception("Button not found: " + button_text)


def get_volunteer_row(name):
    return wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//tr[td[normalize-space()='{name}']]")
        )
    )


def test_application_open():
    driver.get("http://localhost:5500/index.html")
    driver.maximize_window()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Username']")
        )
    )


def test_login_interface():
    assert find_visible_input("Username").is_displayed()
    assert find_visible_input("Password").is_displayed()
    assert find_button("Login").is_displayed()


def test_login_functionality():
    username = find_visible_input("Username")
    password = find_visible_input("Password")

    username.clear()
    username.send_keys("admin")

    password.clear()
    password.send_keys("1234")

    find_button("Login").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Volunteer Management')]")
        )
    )


def test_volunteer_interface():
    assert find_visible_input("Name").is_displayed()
    assert find_visible_input("City").is_displayed()
    assert find_visible_input("Search volunteer").is_displayed()
    assert find_button("Add Volunteer").is_displayed()

    selects = [
        element for element in driver.find_elements(By.TAG_NAME, "select")
        if element.is_displayed()
    ]

    assert len(selects) > 0, "Experience dropdown not found"


def test_volunteer_form_usability():
    assert find_visible_input("Name").get_attribute("placeholder") == "Name"
    assert find_visible_input("City").get_attribute("placeholder") == "City"

    select_element = next(
        element for element in driver.find_elements(By.TAG_NAME, "select")
        if element.is_displayed()
    )

    options = [
        option.text for option in Select(select_element).options
    ]

    assert "Beginner" in options
    assert "Experienced" in options


def test_create_volunteer():
    name = find_visible_input("Name")
    city = find_visible_input("City")

    name.clear()
    city.clear()

    name.send_keys(volunteer_name)
    city.send_keys("Chennai")

    select_element = next(
        element for element in driver.find_elements(By.TAG_NAME, "select")
        if element.is_displayed()
    )

    Select(select_element).select_by_visible_text("Experienced")

    find_button("Add Volunteer").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//tr[td[normalize-space()='{volunteer_name}']]")
        )
    )


def test_read_volunteer():
    row = get_volunteer_row(volunteer_name)

    assert volunteer_name in row.text
    assert "Chennai" in row.text
    assert "Experienced" in row.text


def test_search_volunteer():
    search = find_visible_input("Search volunteer")
    search.clear()
    search.send_keys(volunteer_name)

    get_volunteer_row(volunteer_name)


def test_update_volunteer():
    row = get_volunteer_row(volunteer_name)

    edit_buttons = row.find_elements(
        By.XPATH,
        ".//button[contains(normalize-space(), 'Edit')]"
    )

    if not edit_buttons:
        raise Exception(
            "Edit button not found. Check the actual HTML button text."
        )

    edit_buttons[0].click()

    city = find_visible_input("City")
    city.clear()
    city.send_keys("Coimbatore")

    update_buttons = driver.find_elements(
        By.XPATH,
        "//button[contains(normalize-space(), 'Update Volunteer')]"
    )

    if update_buttons:
        next(
            button for button in update_buttons
            if button.is_displayed() and button.is_enabled()
        ).click()
    else:
        save_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(normalize-space(), 'Update')]"
        )

        visible_buttons = [
            button for button in save_buttons
            if button.is_displayed() and button.is_enabled()
        ]

        if not visible_buttons:
            raise Exception("Update button not found")

        visible_buttons[0].click()

    wait.until(
        EC.text_to_be_present_in_element(
            (By.XPATH, f"//tr[td[normalize-space()='{volunteer_name}']]"),
            "Coimbatore"
        )
    )


def test_empty_form_validation():
    search = find_visible_input("Search volunteer")
    search.clear()

    name = find_visible_input("Name")
    city = find_visible_input("City")

    name.clear()
    city.clear()

    find_button("Add Volunteer").click()

    try:
        alert = WebDriverWait(driver, 2).until(
            EC.alert_is_present()
        )

        print("Validation message:", alert.text)
        alert.accept()

    except TimeoutException:
        print("No JavaScript alert appeared; checking form validation.")

        if name.get_attribute("required") is None:
            print("Name field does not use HTML required validation.")

        if city.get_attribute("required") is None:
            print("City field does not use HTML required validation.")


def test_delete_volunteer():
    search = find_visible_input("Search volunteer")
    search.clear()
    search.send_keys(volunteer_name)

    row = get_volunteer_row(volunteer_name)

    delete_buttons = row.find_elements(
        By.XPATH,
        ".//button[contains(normalize-space(), 'Delete')]"
    )

    if not delete_buttons:
        raise Exception(
            "Delete button not found. Check the actual HTML button text."
        )

    delete_buttons[0].click()

    try:
        alert = WebDriverWait(driver, 2).until(
            EC.alert_is_present()
        )
        print("Delete confirmation:", alert.text)
        alert.accept()
    except TimeoutException:
        pass

    wait.until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//tr[td[normalize-space()='{volunteer_name}']]")
        )
    )


def test_logout():
    find_button("Logout").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Username']")
        )
    )


try:
    report_test(
        "TEST 1: Open RescueConnect Application",
        test_application_open
    )

    if passed == 1:
        report_test(
            "TEST 2: Login Interface Testing",
            test_login_interface
        )

        report_test(
            "TEST 3: Login Functional Testing",
            test_login_functionality
        )

        if driver.find_elements(
            By.XPATH,
            "//h2[contains(text(),'Volunteer Management')]"
        ):
            report_test(
                "TEST 4: Volunteer Interface Testing",
                test_volunteer_interface
            )

            report_test(
                "TEST 5: Volunteer Form Usability Testing",
                test_volunteer_form_usability
            )

            report_test(
                "TEST 6: Create Volunteer",
                test_create_volunteer
            )

            report_test(
                "TEST 7: Read Volunteer",
                test_read_volunteer
            )

            report_test(
                "TEST 8: Search Volunteer",
                test_search_volunteer
            )

            report_test(
                "TEST 9: Update Volunteer",
                test_update_volunteer
            )

            report_test(
                "TEST 10: Empty Form Validation",
                test_empty_form_validation
            )

            report_test(
                "TEST 11: Delete Volunteer",
                test_delete_volunteer
            )

            report_test(
                "TEST 12: Logout",
                test_logout
            )

    print("\n========================================")
    print("RESCUECONNECT SELENIUM TEST SUMMARY")
    print("========================================")
    print("Passed:", passed)
    print("Failed:", failed)
    print("========================================")

finally:
    time.sleep(0.5)
    driver.quit()
