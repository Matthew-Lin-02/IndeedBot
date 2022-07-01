import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialise the user
# user 1

# LinkedIn Username and Password
from selenium.webdriver.support.wait import WebDriverWait

username = "usernameoremail"
password = "password"
# The page with all the job applications on linkedIn with easy apply field selected

# pick ur job search page in lnkedIn make sure to add easyapply
jobSearchLink = "https://www.linkedin.com/jobs/search/?f_AL=true&geoId=102241850&keywords=customer&location=Victoria%2C%20Australia"

# path to ur chrome driver
chrome_driver_path = "/Program Files/Chromedriver/chromedriver"


# software Resume insert ur resume path
resume_path =  "C:/Users/matth/Desktop/Resume/Software/Matthew_Lin_Software_Resume.doc"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
##########################
time.sleep(2)

# Open page and Sign in

driver.get(jobSearchLink)
sign_in_button = driver.find_element_by_link_text("Sign in")
sign_in_button.click()

email_field = driver.find_element_by_id("username")
email_field.send_keys(username)

password_field = driver.find_element_by_id("password")
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)


#all_listings = driver.find_elements_by_css_selector(".job-card-container--clickable")

wantApply = 100
applied = 0

#     driver.execute_script("arguments[0].scrollIntoView(true);", listing)


currentPage = 1

# for i in range(6):
#     all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
#     no_listings =len(all_listings)
#     driver.execute_script("arguments[0].scrollIntoView(true);", all_listings[no_listings - 1])
#     time.sleep(1)


def preload():
    loaded_first = False
    prev_no_listings = -1

    i=0
    while i < 6:
        all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

        no_listings = len(all_listings)
        if loaded_first == True and no_listings == prev_no_listings:

            break

        prev_no_listings = len(all_listings)
        driver.execute_script("arguments[0].scrollIntoView(true);", all_listings[no_listings - 1])
        time.sleep(1)
        i +=1
    return all_listings

def findListingIndex(listing):
    classString = listing.get_attribute("class")
    m = re.search(r'\d+$', classString)
    return int(m.group())
currentListingIndex = 0
while wantApply > applied:
    pageDone = False

    finalPageAttempted = False
    while finalPageAttempted == False:
        time.sleep(2)
        all_listings = preload()
        print("entered outer loop")
        for listing in all_listings[currentListingIndex:]:
            currentListingIndex = findListingIndex(listing)
            if listing == all_listings[-1]:
                finalPageAttempted = True
            if wantApply == applied:
                break
            print("called")
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView(true);", listing)
            listing.click()
            time.sleep(1)
            try:
                # First Form
                apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
                apply_button.click()
                time.sleep(1)
                phone = driver.find_element_by_class_name("fb-single-line-text__input")
                #phone.send_keys("0451600920")
                next_button = driver.find_element_by_css_selector("footer button")
                if next_button.get_attribute("aria-label") == "Continue to next step":
                    next_button.click()
                elif next_button.get_attribute("aria-label") == "Submit application":
                    next_button.click()
                    time.sleep(3)
                    close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                    close_button.click()
                    time.sleep(1)

                    applied +=1
                    print("breaking")
                    break
                else:
                    close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                    close_button.click()
                    time.sleep(1)
                    discard_button = driver.find_element_by_xpath(
                        "//button[contains(@class, 'artdeco-button')]//*[contains(.,'Discard')]/..")
                    discard_button.click()
                    time.sleep(1)
                    print("Complex application, skipped..")
                    continue

                # form 2
                time.sleep(1)
                try:
                    deleteUploadButton = driver.find_element_by_css_selector(".jobs-document-upload__remove-file .artdeco-button--tertiary")
                    deleteUploadButton.click()

                except:
                    close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                    close_button.click()
                    time.sleep(1)
                    discard_button = driver.find_element_by_xpath(
                        "//button[contains(@class, 'artdeco-button')]//*[contains(.,'Discard')]/..")
                    discard_button.click()
                    continue

                upload_resume_button = driver.find_element_by_css_selector(".js-jobs-document-upload__container input")
                upload_resume_button.send_keys(resume_path)
                print("trying to upload")
                time.sleep(1)
                review_button = driver.find_element_by_class_name("artdeco-button--primary")
                if review_button.get_attribute("aria-label") == "Continue to next step":

                    close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                    close_button.click()
                    time.sleep(1)
                    discard_button = driver.find_element_by_xpath("//button[contains(@class, 'artdeco-button')]//*[contains(.,'Discard')]/..")
                    discard_button.click()
                    time.sleep(1)
                    print("Complex application, skipped..")
                    continue
                else:
                    review_button.click()
                    time.sleep(1)
                    # Form 3
                    submit_button = driver.find_element_by_class_name("artdeco-button--primary")
                    if submit_button.get_attribute("aria-label") == "Submit application":
                        currentListingIndex = findListingIndex(listing)
                        submit_button.click()
                        time.sleep(3)
                        close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")

                        close_button.click()
                        time.sleep(1)
                        applied += 1

                        print("breaking")
                        break
                    else:
                        close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                        close_button.click()
                        time.sleep(1)
                        discard_button = driver.find_element_by_xpath(
                            "//button[contains(@class, 'artdeco-button')]//*[contains(.,'Discard')]/..")
                        discard_button.click()
                        time.sleep(1)
                        print("Complex application, skipped..")
                        continue
            except NoSuchElementException:

                print("No application button, skipped.")
                continue
            except StaleElementReferenceException:
                print("stale ele reference button, skipped.")
                continue


    currentPage += 1
    nextPageLabel = "Page " + str(currentPage)
    print(nextPageLabel)
    pageButtons = driver.find_elements_by_css_selector(".artdeco-pagination__indicator button")
    try:
        for pageButton in pageButtons:
            if pageButton.get_attribute("aria-label") == nextPageLabel:
                print(pageButton.get_attribute("aria-label"))
                nextPageButton = pageButton


        nextPageButton.click()
    except:
        break






