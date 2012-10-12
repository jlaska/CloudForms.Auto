import apps.locators
from selenium.webdriver.common.by import By

class KatelloLocators(apps.locators.BaseLocators):
    """
    Locators for katello pages are contained within.
    """

    # Page title
    page_title = "Katello - Open Source Systems Management"
    login_logo = (By.XPATH, "//img[@alt='Katello Logo']")
    logo_link = (By.XPATH, "//a[contains(text(),'Katello')]")

    # Home Page and login related locators
    username_text_field = (By.ID, "username")
    password_text_field = (By.ID, "password-input")
    login_locator = (By.XPATH, "//input[@id='login_btn']")
    logout_locator = (By.XPATH, "//a[contains(text(),'Log Out')]")

    # Dashboard locators
    dashboard_dropbutton_locator = (By.XPATH, "//div[contains(@class, 'dropbutton')]")
    dashboard_subscriptions_locator = (By.ID, "dashboard_subscriptions")
    dashboard_nofications_locator = (By.ID, "dashboard_notifications")

    # Account controller
    account_controller_locator = (By.CSS_SELECTOR, "li.hello")

    # Org switcher
    org_switcher_locator = (By.XPATH, "//a[@id='switcherButton']/div")
    org_switcher_org_locator = (By.CSS_SELECTOR, "a[href*='org_id=2']")
    org_input_filter_locator = (By.CSS_SELECTOR, "input#orgfilter_input")
    org_filtered_button_locator = (By.CSS_SELECTOR, "button.filter_button")
    switcher_org_box_locator = (By.ID, "switcherBox")
    switcher_org_list_locator = (By.CSS_SELECTOR, "a.fl.clear")

    # Roles
    role_list_locator = (By.CSS_SELECTOR, "div.block")
    role_original_title_locator = (By.XPATH, "//span[@original-title='%s']")
    role_permissions_locator = (By.ID, "role_permissions")
    role_users_locator = (By.ID, "role_users")
    role_customize_window_locator = (By.CSS_SELECTOR, "div.slider_one.slider.will_have_content.has_content")
    tree_breadcrumb_locator = (By.CSS_SELECTOR, "div.tree_breadcrumb")
    roles_role_breadcrumb_locator = (By.CSS_SELECTOR, "span#roles.currentCrumb.one-line-ellipsis")
    role_user_list_locator = (By.CSS_SELECTOR, "li.no_slide")
    role_user_remove_locator = (By.CSS_SELECTOR, "a.fr.content_add_remove.remove_user.st_button")
    role_new_name_locator = (By.ID, "role_name")
    role_new_description_locator = (By.ID, "role_description")
    role_save_button_locator = (By.ID, "role_save")
    role_orgs_list_locator = (By.CSS_SELECTOR, "ul.filterable li.slide_link")
    roles_add_permission_locator = (By.ID, "add_permission")
    roles_resource_type_locator = (By.ID, "resource_type")
    roles_permission_name_locator = (By.ID, "permission_name")
    roles_permission_done_locator = (By.ID, "save_permission_button")
    roles_permission_desc_locator = (By.ID, "description")
    roles_locator = (By.CSS_SELECTOR, "span#roles.one-line-ellipsis")
    current_page_locator = (By.CSS_SELECTOR, ".paginator .num > a:nth-child(1)")

    # Notification dialog
    success_notification_locator = (By.CSS_SELECTOR, "div.jnotify-notification.jnotify-notification-success")
    error_notification_locator = (By.CSS_SELECTOR, "div.jnotify-notification.jnotify-notification-error")
    close_notification_locator = (By.CSS_SELECTOR, "a.jnotify-close")

    # Search form
    search_form_locator = (By.XPATH, "//form[@id='search_form']")
    search_input_locator = (By.XPATH, "//input[@id='search']")
    search_button_locator = (By.XPATH, "//button[@id='search_button']")

    # Search Queries
    # query_button = (By.CSS_SELECTOR, "div.queries.open")
    query_button = (By.XPATH, "//form[@id='search_form']/div[@class='queries open']")
    query_clear = (By.ID, "search_clear")
    # FIXME - locator for existing search entries
    query_save = (By.ID, "search_favorite_save")
    query_list = (By.ID, "search_list")

    sam_header_locator = (By.CSS_SELECTOR, "#head header h1")
    sam_h1_locator = (By.CSS_SELECTOR, "h1")
    hello_link_locator = (By.XPATH, "//a[contains(@href, '/users?id=')]")
    footer_version_text_locator = (By.CSS_SELECTOR, "div.grid_16.ca.light_text")
    new_item_locator = (By.ID, "new")
    remove_item_locator = (By.CSS_SELECTOR, "a.remove_item")
    close_item_locator = (By.CSS_SELECTOR, "a.close")
    confirmation_yes_locator = (By.XPATH, "//span[@class='ui-button-text'][text()='Yes']")
    next_button_locator = (By.ID, "next_button")
    activation_key_new_name_locator = (By.ID, "activation_key_name")
    organization_new_name_locator = (By.ID, "new")
    close_locator = (By.CLASS_NAME, "close")
    login_org_name_selector_css = ('a')
    login_org_selector = (By.CSS_SELECTOR, "div.row.clickable")
    admin_drop_down = (By.ID, "admin")
    new_template = (By.ID, "new")
    system_template_name = (By.ID, "system_template_name")
    system_template_description = (By.ID, "system_template_description")
    template_save = (By.ID, "template_save")
    remove_template = (By.ID, "remove_template")

    # Tabs
    def selected_tab(self, tab_name):
        # HACK!
        if tab_name == 'administration':
            return (By.CSS_SELECTOR, "li#admin.operations.top_level.active.selected".format(name=tab_name))
        else:
            return (By.CSS_SELECTOR, "li#{name}.{name}.top_level.active.selected".format(name=tab_name))

    tab_elements = {"dashboard" : (By.ID, "dashboard"),
                    "content" : (By.ID, "content"),
                        "providers" : (By.XPATH, "//a[.='Content Providers']"),
                    "systems" : (By.ID, "systems"),
                        "systems_all" : (By.ID, "registered"),
                        "systems_by_environment" : (By.ID, "env") ,
                        "activation_keys" : (By.XPATH, "//a[.='Activation Keys']"),
                    "organizations" : (By.XPATH, "//a[.='Organizations']"),  # By.ID didn't work in firefox
                    "administration" : (By.ID, "admin"),
                        "roles" : (By.ID, "roles"),}
