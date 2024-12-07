from playwright.sync_api import sync_playwright, Position
print("Just so I can commit")
def get_jobdescrip_from_jobpage(job_url):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Use headless=False to debug visually
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the job page
        page.goto(job_url, timeout=0)
        page.wait_for_load_state('networkidle', timeout=0)  # Ensure all network requests are complete

        # Extract the job description
        try:
            # Replace the CSS selector below with the actual selector for the job description
            job_description_element = page.query_selector(".job-description-selector")
            job_description = job_description_element.inner_text() if job_description_element else "Description not found"
        except Exception as e:
            job_description = f"An error occurred: {str(e)}"

        # Close the browser
        browser.close()

    # Return the data as a dictionary
    return {
        "Job Description": job_description
    }