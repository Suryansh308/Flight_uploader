"""
All CSS selectors for Lynkit Portal.

Only modify this file if the website UI changes.
"""

# ==========================================================
# LOGIN
# ==========================================================

LOGIN_USERNAME = (
    "#app-container > app-root > div.landing-page > div > "
    "app-login > div > div.login-center-container > "
    "div.lock-body > div > div.login-form-group > "
    "div:nth-child(3) > input"
)

LOGIN_PASSWORD = (
    "#app-container > app-root > div.landing-page > div > "
    "app-login > div > div.login-center-container > "
    "div.lock-body > div > div.login-form-group > "
    "div:nth-child(4) > input"
)

LOGIN_BUTTON = "button.btn-signin"


# ==========================================================
# NAVIGATION
# ==========================================================

SIDEBAR = (
    "#app-container > app-root > app-navbar > nav > "
    "div.d-flex.align-items-center.navbar-left > "
    "a.menu-button.d-none.d-md-block"
)

TRIPS = "#\\36 6a1ed8b8d8e42340f072ff5 > a"

MY_TRIPS = (
    "#\\36 6a1ed8b8d8e42340f072ff5 > "
    "ul > li:nth-child(1) > a > span"
)


# ==========================================================
# SEARCH
# ==========================================================

DATE_INPUT = (
    "#app-container > app-root > app-trip-list > main > div > "
    "div.card.mb-4 > div > div.row.mt-3 > div > div > div > "
    "div > div.cv2-search-group > div.cv2-search-input-wrap > input"
)

DATE_SEARCH_BUTTON = "button.cv2-search-btn"


# ==========================================================
# TABLE
# ==========================================================

TABLE = (
    "#myReactComponentContainer > "
    "app-form-list > div.table-responsive.custom-height"
)

TABLE_ROWS = (
    "#myReactComponentContainer "
    "table tbody tr"
)

# Column Numbers
CHECKBOX_COLUMN = 1
FLIGHT_COLUMN = 9
DATE_COLUMN = 10


# ==========================================================
# PAGINATION
# ==========================================================
# ---------------------------------------------------------
# Pagination
# ---------------------------------------------------------

NEXT_PAGE = "#myReactComponentContainer > div > div:nth-child(2) > div > button.btn.btn-outline-primary"

PREVIOUS_PAGE = "#myReactComponentContainer > div > div:nth-child(2) > div > button.btn.btn-outline-secondary"


# ==========================================================
# UPLOAD
# ==========================================================

UPLOAD_BUTTON = (
    "#myReactComponentContainer > "
    "app-form-list > div.row.fadeIn > "
    "div.col-lg-10.col-md-10.col-sm-6.col-xs-10.button-container > "
    "button:nth-child(3)"
)

FILE_INPUT = "#data_0_upload_view_file"

SUBMIT_BUTTON = (
    "#upload_view_file > div > div > div.modal-body.custom-scrollbar > "
    "div.row.justify-content-center > div > div"
)

OK_BUTTON = "#confirmToa"