from playwright.sync_api import sync_playwright

def get_jobdescrip_from_jobpage(job_url, cookie_popup_selector, job_description_selector):
    print(f"CookiePopUpSelector: {cookie_popup_selector}")
    job_description = "Description not found"  # Default value

    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set headless=False to debug visually
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the job page
            print("Navigating to the page...")
            page.goto(job_url, timeout=50000, wait_until="domcontentloaded")
            print("Page loaded successfully.")

            # Handle cookie popup if applicable
            if cookie_popup_selector:
                handle_popup(cookie_popup_selector, page)

            # Extract the job description
            print("Extracting job description...")
            job_description_element = page.query_selector(job_description_selector)
            if job_description_element:
                job_description = job_description_element.inner_text().strip()
                print("Job description retrieved.")
            else:
                print("Job description element not found.")
        except Exception as e:
            print(f"Error processing the page: {str(e)}")
        finally:
            #browser.close()
            print("Browser will be closed in future.")

    # Return the data as a dictionary
    return {
        "Job Description": job_description
    }

def handle_popup(cookie_popup_selector, page):
    try:
        # Check and dismiss the cookie popup if it's visible
        print("Waiting for cookie popup...")
        page.wait_for_selector(cookie_popup_selector, timeout=10000)  # Wait up to 10 seconds for the popup
        print("Finished Waiting for cookie popup")
        if page.is_visible(cookie_popup_selector):
            print("Cookie popup visible")
            page.click(cookie_popup_selector)
            print("Cookie popup dismissed.")
        else:
            print("Cookie popup not found.")
    except Exception as e:
        print(f"Error handling cookie popup: {str(e)}")
