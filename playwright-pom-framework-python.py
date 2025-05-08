# Project structure:
# bdJobs-tests/
# ├── pages/
# │   ├── base_page.py
# │   ├── home_page.py
# │   ├── login_page.py
# │   ├── job_search_page.py
# │   ├── job_details_page.py
# │   ├── registration_page.py
# │   └── profile_page.py
# ├── tests/
# │   ├── test_login.py
# │   ├── test_search.py
# │   ├── test_registration.py
# │   └── test_profile.py
# ├── utils/
# │   ├── test_data.py
# │   └── helpers.py
# ├── conftest.py
# ├── pytest.ini
# └── requirements.txt

# 1. First, let's create the requirements.txt file:

# requirements.txt
"""
playwright==1.40.0
pytest==7.4.3
pytest-playwright==0.4.0
python-dotenv==1.0.0
faker==19.10.0
"""

# 2. Let's create the pytest.ini file:

# pytest.ini
"""
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: marks tests as smoke tests
    regression: marks tests as regression tests
"""

# 3. Let's create the conftest.py file:

# conftest.py
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Return additional arguments for browser launch."""
    return {
        "headless": False,
        "slow_mo": 100,
    }

@pytest.fixture(scope="session")
def browser_context_args():
    """Return additional arguments for browser context creation."""
    return {
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
    }

@pytest.fixture
def context(browser):
    """Create a new browser context with a screenshot path."""
    context = browser.new_context(
        record_video_dir="videos/",
        record_har_path=None,
    )
    
    # Set default navigation timeout
    context.set_default_timeout(30000)
    
    yield context
    context.close()

@pytest.fixture
def page(context):
    """Create a new page in the browser context."""
    page = context.new_page()
    yield page

# 4. Let's create the base_page.py file:

# pages/base_page.py
import logging
from playwright.sync_api import Page, TimeoutError

class BasePage:
    """Base page object that all page objects inherit from."""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://bdjobs.com"
    
    def navigate(self, path=""):
        """Navigate to a specific URL path."""
        url = f"{self.base_url}/{path}"
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def wait_for_page_load(self):
        """Wait for page to finish loading."""
        self.page.wait_for_load_state("networkidle")
    
    def get_title(self):
        """Get page title."""
        return self.page.title()
    
    def get_url(self):
        """Get current URL."""
        return self.page.url
    
    def take_screenshot(self, name):
        """Take a screenshot of the current page."""
        self.page.screenshot(path=f"screenshots/{name}.png")
    
    def is_element_visible(self, selector):
        """Check if an element is visible."""
        try:
            return self.page.is_visible(selector)
        except TimeoutError:
            return False

    def click(self, selector):
        """Click on an element."""
        self.page.click(selector)
    
    def fill(self, selector, text):
        """Fill a form field."""
        self.page.fill(selector, text)
    
    def select_option(self, selector, value):
        """Select an option from a dropdown."""
        self.page.select_option(selector, value)
    
    def wait_for_selector(self, selector, state="visible", timeout=10000):
        """Wait for an element to be in the specified state."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

# 5. Let's create the home_page.py file:

# pages/home_page.py
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page object for the home page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.search_box = "input[name='keyword']"
        self.search_button = "button.search-btn"
        self.login_link = "a.loginText"
        self.registration_link = "a.signupText"
        self.job_category_links = ".category-name"
        self.featured_jobs_section = ".featured-jobs"
    
    def navigate(self):
        """Navigate to the home page."""
        super().navigate()
    
    def search_job(self, keyword):
        """Search for a job using a keyword."""
        self.fill(self.search_box, keyword)
        self.click(self.search_button)
        self.wait_for_page_load()
    
    def click_login(self):
        """Click on the login link."""
        self.click(self.login_link)
        self.wait_for_page_load()
    
    def click_registration(self):
        """Click on the registration link."""
        self.click(self.registration_link)
        self.wait_for_page_load()
    
    def select_job_category(self, category):
        """Select a job category."""
        category_locator = f"{self.job_category_links}:has-text('{category}')"
        self.click(category_locator)
        self.wait_for_page_load()
    
    def verify_featured_jobs_visible(self):
        """Verify that featured jobs section is visible."""
        return self.is_element_visible(self.featured_jobs_section)

# 6. Let's create the login_page.py file:

# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page object for the login page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = ".error-message"
        self.forgot_password_link = "a:has-text('Forgot Password')"
    
    def navigate(self):
        """Navigate to the login page."""
        super().navigate("login")
    
    def login(self, email, password):
        """Login with email and password."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        self.wait_for_page_load()
    
    def get_error_message(self):
        """Get error message if login fails."""
        if self.is_element_visible(self.error_message):
            return self.page.text_content(self.error_message)
        return None
    
    def click_forgot_password(self):
        """Click on forgot password link."""
        self.click(self.forgot_password_link)
        self.wait_for_page_load()

# 7. Let's create the job_search_page.py file:

# pages/job_search_page.py
from pages.base_page import BasePage

class JobSearchPage(BasePage):
    """Page object for the job search page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.search_results_container = ".search-results-container"
        self.job_titles = ".job-title-text"
        self.filter_panel = ".filter-panel"
        self.category_filter = ".category-filter"
        self.location_filter = ".location-filter"
        self.experience_filter = ".experience-filter"
        self.sort_dropdown = "select.sort-options"
        self.pagination = ".pagination"
        self.total_jobs_count = ".total-jobs-count"
    
    def get_search_results_count(self):
        """Get the number of search results."""
        count_text = self.page.text_content(self.total_jobs_count)
        # Extract numbers from text like "1,234 jobs found"
        import re
        numbers = re.findall(r'\d+', count_text.replace(',', ''))
        if numbers:
            return int(numbers[0])
        return 0
    
    def filter_by_category(self, category):
        """Filter jobs by category."""
        category_locator = f"{self.category_filter} label:has-text('{category}')"
        self.click(category_locator)
        self.wait_for_page_load()
    
    def filter_by_location(self, location):
        """Filter jobs by location."""
        location_locator = f"{self.location_filter} label:has-text('{location}')"
        self.click(location_locator)
        self.wait_for_page_load()
    
    def filter_by_experience(self, experience):
        """Filter jobs by experience level."""
        experience_locator = f"{self.experience_filter} label:has-text('{experience}')"
        self.click(experience_locator)
        self.wait_for_page_load()
    
    def sort_by(self, option):
        """Sort search results by the specified option."""
        self.select_option(self.sort_dropdown, option)
        self.wait_for_page_load()
    
    def click_on_job_by_index(self, index):
        """Click on a job by index in the search results."""
        self.page.nth(self.job_titles, index).click()
        self.wait_for_page_load()
    
    def navigate_to_page(self, page_number):
        """Navigate to a specific page in the search results."""
        page_locator = f"{self.pagination} a:has-text('{page_number}')"
        self.click(page_locator)
        self.wait_for_page_load()

# 8. Let's create the job_details_page.py file:

# pages/job_details_page.py
from pages.base_page import BasePage

class JobDetailsPage(BasePage):
    """Page object for the job details page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.job_title = ".job-title"
        self.company_name = ".company-name"
        self.job_description = ".job-description"
        self.apply_button = "button:has-text('Apply Now')"
        self.job_requirements = ".job-requirements"
        self.job_responsibilities = ".job-responsibilities"
        self.salary_info = ".salary-info"
    
    def get_job_title(self):
        """Get the job title from the job details page."""
        return self.page.text_content(self.job_title)
    
    def get_company_name(self):
        """Get the company name from the job details page."""
        return self.page.text_content(self.company_name)
    
    def click_apply(self):
        """Click on the apply button."""
        self.click(self.apply_button)
        self.wait_for_page_load()
    
    def is_salary_visible(self):
        """Check if salary information is visible."""
        return self.is_element_visible(self.salary_info)

# 9. Let's create the registration_page.py file:

# pages/registration_page.py
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    """Page object for the registration page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.name_input = "input[name='name']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.confirm_password_input = "input[name='confirmPassword']"
        self.mobile_input = "input[name='mobile']"
        self.gender_selection = "select[name='gender']"
        self.register_button = "button[type='submit']"
        self.terms_checkbox = "input[type='checkbox'][name='terms']"
        self.error_messages = ".error-message"
    
    def navigate(self):
        """Navigate to the registration page."""
        super().navigate("register")
    
    def register_user(self, user_data):
        """Register a new user with the provided data."""
        self.fill(self.name_input, user_data["name"])
        self.fill(self.email_input, user_data["email"])
        self.fill(self.password_input, user_data["password"])
        self.fill(self.confirm_password_input, user_data["confirm_password"])
        self.fill(self.mobile_input, user_data["mobile"])
        self.select_option(self.gender_selection, user_data["gender"])
        
        if user_data.get("accept_terms", False):
            self.page.check(self.terms_checkbox)
        
        self.click(self.register_button)
        self.wait_for_page_load()
    
    def get_error_messages(self):
        """Get all error messages displayed on the registration page."""
        errors = []
        error_elements = self.page.query_selector_all(self.error_messages)
        
        for element in error_elements:
            errors.append(element.text_content())
        
        return errors

# 10. Let's create the profile_page.py file:

# pages/profile_page.py
from pages.base_page import BasePage

class ProfilePage(BasePage):
    """Page object for the user profile page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.profile_name = ".profile-name"
        self.edit_profile_button = "button:has-text('Edit Profile')"
        self.profile_sections = ".profile-section"
        self.resume_download_button = "button:has-text('Download Resume')"
        self.applied_jobs_tab = "a:has-text('Applied Jobs')"
        self.saved_jobs_tab = "a:has-text('Saved Jobs')"
        self.logout_button = "button:has-text('Logout')"
    
    def navigate(self):
        """Navigate to the profile page."""
        super().navigate("my-bdjobs/my-profile")
    
    def get_profile_name(self):
        """Get the profile name from the profile page."""
        return self.page.text_content(self.profile_name)
    
    def click_edit_profile(self):
        """Click on the edit profile button."""
        self.click(self.edit_profile_button)
        self.wait_for_page_load()
    
    def view_applied_jobs(self):
        """View applied jobs section."""
        self.click(self.applied_jobs_tab)
        self.wait_for_page_load()
    
    def view_saved_jobs(self):
        """View saved jobs section."""
        self.click(self.saved_jobs_tab)
        self.wait_for_page_load()
    
    def logout(self):
        """Click on the logout button."""
        self.click(self.logout_button)
        self.wait_for_page_load()

# 11. Let's create the test_data.py file:

# utils/test_data.py
"""Test data for BD Jobs tests."""

VALID_USER = {
    "email": "test@example.com",
    "password": "Password123!"
}

INVALID_USER = {
    "email": "invalid@example.com",
    "password": "wrongpassword"
}

NEW_USER = {
    "name": "Test User",
    "email": "newuser@example.com",
    "password": "NewUser123!",
    "confirm_password": "NewUser123!",
    "mobile": "01700000000",
    "gender": "M",
    "accept_terms": True
}

SEARCH_TERMS = [
    "Software Engineer",
    "Project Manager",
    "Marketing Executive",
    "HR Manager",
    "Data Analyst"
]

LOCATIONS = [
    "Dhaka",
    "Chittagong",
    "Sylhet",
    "Rajshahi",
    "Khulna"
]

JOB_CATEGORIES = [
    "IT/Telecommunication",
    "Bank/Financial Institution",
    "Marketing/Sales",
    "NGO/Development",
    "Engineering"
]

# 12. Let's create the helpers.py file:

# utils/helpers.py
import time
import random
import string
import json
import os
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_random_email():
    """Generate a random email address."""
    timestamp = int(time.time())
    return f"test{timestamp}@example.com"

def generate_random_name():
    """Generate a random name."""
    return fake.name()

def generate_random_password(length=12):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_phone():
    """Generate a random Bangladesh phone number."""
    return f"017{''.join(random.choice(string.digits) for _ in range(8))}"

def save_test_results(test_name, results):
    """Save test results to a JSON file."""
    if not os.path.exists("results"):
        os.makedirs("results")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/{test_name}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    return filename

def wait_seconds(seconds):
    """Wait for a specified number of seconds."""
    time.sleep(seconds)

# 13. Let's create the test_login.py file:

# tests/test_login.py
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.test_data import VALID_USER, INVALID_USER

class TestLogin:
    """Test cases for login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test."""
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.profile_page = ProfilePage(page)
        
        self.home_page.navigate()
    
    @pytest.mark.smoke
    def test_valid_login(self, page):
        """Test login with valid credentials."""
        self.home_page.click_login()
        self.login_page.login(VALID_USER["email"], VALID_USER["password"])
        
        # Verify successful login (redirected to profile or dashboard)
        assert "my-bdjobs" in page.url
    
    def test_invalid_login(self):
        """Test login with invalid credentials."""
        self.home_page.click_login()
        self.login_page.login(INVALID_USER["email"], INVALID_USER["password"])
        
        error_message = self.login_page.get_error_message()
        assert error_message is not None
    
    def test_logout(self, page):
        """Test logout functionality."""
        self.home_page.click_login()
        self.login_page.login(VALID_USER["email"], VALID_USER["password"])
        
        # Verify logged in first
        assert "my-bdjobs" in page.url
        
        self.profile_page.logout()
        
        # Verify returned to home page or login page
        assert "my-bdjobs" not in page.url

# 14. Let's create the test_search.py file:

# tests/test_search.py
import pytest
from pages.home_page import HomePage
from pages.job_search_page import JobSearchPage
from pages.job_details_page import JobDetailsPage
from utils.test_data import SEARCH_TERMS, JOB_CATEGORIES, LOCATIONS

class TestJobSearch:
    """Test cases for job search functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test."""
        self.home_page = HomePage(page)
        self.search_page = JobSearchPage(page)
        self.details_page = JobDetailsPage(page)
        
        self.home_page.navigate()
    
    @pytest.mark.smoke
    def test_search_by_keyword(self):
        """Test search for jobs by keyword."""
        search_term = SEARCH_TERMS[0]
        self.home_page.search_job(search_term)
        
        results_count = self.search_page.get_search_results_count()
        assert results_count > 0
    
    def test_filter_search_results(self):
        """Test filtering search results."""
        search_term = SEARCH_TERMS[0]
        self.home_page.search_job(search_term)
        
        initial_count = self.search_page.get_search_results_count()
        self.search_page.filter_by_location(LOCATIONS[0])
        
        filtered_count = self.search_page.get_search_results_count()
        # Filtered results should be less than or equal to initial results
        assert filtered_count <= initial_count
    
    def test_view_job_details(self):
        """Test viewing job details."""
        search_term = SEARCH_TERMS[0]
        self.home_page.search_job(search_term)
        
        self.search_page.click_on_job_by_index(0)
        
        job_title = self.details_page.get_job_title()
        assert job_title is not None
        assert len(job_title) > 0
    
    def test_browse_by_category(self):
        """Test browsing jobs by category."""
        category = JOB_CATEGORIES[0]
        self.home_page.select_job_category(category)
        
        results_count = self.search_page.get_search_results_count()
        assert results_count > 0

# 15. Let's create the test_registration.py file:

# tests/test_registration.py
import pytest
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.test_data import NEW_USER
from utils.helpers import generate_random_email

class TestRegistration:
    """Test cases for user registration."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test."""
        self.home_page = HomePage(page)
        self.registration_page = RegistrationPage(page)
        
        self.home_page.navigate()
    
    @pytest.mark.smoke
    def test_valid_registration(self, page):
        """Test registration with valid data."""
        self.home_page.click_registration()
        
        # Generate a unique email to avoid duplicate registration issues
        random_email = generate_random_email()
        user_data = {**NEW_USER, "email": random_email}
        
        self.registration_page.register_user(user_data)
        
        # Verify successful registration (should be redirected to profile completion or dashboard)
        assert "my-bdjobs" in page.url
    
    def test_registration_with_existing_email(self):
        """Test registration with an already registered email."""
        self.home_page.click_registration()
        self.registration_page.register_user(NEW_USER)
        
        errors = self.registration_page.get_error_messages()
        assert len(errors) > 0
        
        # Check for email already exists message
        has_email_error = any(("email" in error.lower() and "exist" in error.lower()) for error in errors)
        assert has_email_error
    
    def test_registration_with_password_mismatch(self):
        """Test registration with mismatched passwords."""
        self.home_page.click_registration()
        
        random_email = generate_random_email()
        user_data = {
            **NEW_USER,
            "email": random_email,
            "confirm_password": "DifferentPassword123!"
        }
        
        self.registration_page.register_user(user_data)
        
        errors = self.registration_page.get_error_messages()
        assert len(errors) > 0
        
        # Check for password mismatch message
        has_password_error = any(
            ("password" in error.lower() and ("match" in error.lower() or "same" in error.lower()))
            for error in errors
        )
        assert has_password_error

# 16. Let's create the test_profile.py file:

# tests/test_profile.py
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.test_data import VALID_USER

class TestProfile:
    """Test cases for user profile functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test with logged in user."""
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.profile_page = ProfilePage(page)
        
        # Login before each test
        self.home_page.navigate()
        self.home_page.click_login()
        self.login_page.login(VALID_USER["email"], VALID_USER["password"])
    
    @pytest.mark.smoke
    def test_view_profile(self):
        """Test viewing the user profile."""
        self.profile_page.navigate()
        
        profile_name = self.profile_page.get_profile_name()
        assert profile_name is not None
        assert len(profile_name) > 0
    
    def test_view_applied_jobs(self):
        """Test viewing applied jobs."""
        self.profile_page.navigate()
        self.profile_page.view_applied_jobs()
        
        # Verify applied jobs page loaded
        current_url = self.profile_page.get_url()
        assert "applied" in current_url
    
    def test_view_saved_jobs(self):
        """Test viewing saved jobs."""
        self.profile_page.navigate()
        self.profile_page.view_saved_jobs()
        
        # Verify saved jobs page loaded
        current_url = self.profile_page.get_url()
        assert "saved" in current_url
