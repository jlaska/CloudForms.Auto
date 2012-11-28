import apps.locators
from selenium.webdriver.common.by import By

class AeolusLocators(apps.locators.BaseLocators):
    """
    Locators for aeolus pages are contained within.
    """

    # util
    page_title = "Aeolus Conductor"
    username_text_field = (By.NAME, "username")
    password_text_field = (By.ID, "password-input")
    login_locator = (By.NAME, "commit")
    login_logo = (By.XPATH, "//img[@alt='Login-card-logo-upstream']")
    logo_link = (By.XPATH, "//a[contains(text(),'Aeolus Conductor')]")
    select_all = (By.ID, "select_all")
    save_button = (By.ID, "save_button")

    # Notification
    error_notification_locator = (By.XPATH, "//div[@class='error']")

    # flash confirmation message
    response = (By.XPATH, "//ul[@class='flashes']")

    # new user fields
    user_first_name_field = (By.ID, "user_first_name")
    user_last_name_field = (By.ID, "user_last_name")
    user_email_field = (By.ID, "user_email")
    user_username_field = (By.ID, "user_username")
    user_password_field = (By.ID, "user_password")
    user_password_confirmation_field = (By.ID, "user_password_confirmation")
    user_quota_max_running_instances_field = (By.ID, "user_quota_attributes_maximum_running_instances")
    user_submit_locator = (By.ID, "user_submit")
    user_delete_locator = (By.CSS_SELECTOR, "input.button.danger")

    # new user group fields
    user_group_name_field = (By.ID, "user_group_name")
    user_group_description_field = (By.ID, "user_group_description")
    user_group_submit_locator = (By.ID, "user_group_submit")
    user_group_delete_locator = (By.ID, "delete")

    # add user to group
    # dup of save_button
    user_group_save = (By.ID, "save_button")
    user_group_delete = (By.ID, "delete_button")

    # self-service
    instances_quota = (By.ID, "self_service_default_quota_maximum_running_instances")

    # new provider account fields
    prov_acct_details_locator = (By.ID, "details_accounts")
    prov_acct_new_account_field = (By.ID, "new_provider_account")
    prov_acct_name_field = (By.ID, "provider_account_label")
    prov_acct_access_key_field = (By.ID, "provider_account_credentials_hash_username")
    prov_acct_secret_access_key_field = (By.ID, "provider_account_credentials_hash_password")
    prov_acct_number_field = (By.ID, "provider_account_credentials_hash_account_id")
    prov_acct_x509_private_field = (By.ID, "provider_account_credentials_hash_x509private")
    prov_acct_x509_public_field = (By.ID, "provider_account_credentials_hash_x509public")
    prov_acct_prior_field = (By.ID, "provider_account_priority")
    prov_acct_quota_field = (By.ID, "quota_instances")
    prov_acct_save_locator = (By.ID, "save")
    prov_acct_delete_locator = (By.ID, "delete_button")

    # new environment pool family
    env_name_field = (By.ID, "pool_family_name")
    env_max_running_instances_field = (By.ID, "pool_family_quota_attributes_maximum_running_instances")
    env_submit_locator = (By.ID, "pool_family_submit")
    pool_family_delete_locator = (By.ID, "delete_pool_family_button")
    env_prov_acct_details = (By.ID, "details_provider_accounts")
    env_add_prov_acct_button = (By.ID, "add_provider_accounts_button")

    # new pool
    pool_name = (By.ID, "pool_name")
    pool_family_parent_field = (By.ID, "pool_pool_family_id")
    pool_quota_field = (By.ID, "quota_instances")
    pool_unlim_quota_checkbox = (By.ID, "unlimited_quota")
    pool_enabled_checkbox = (By.ID, "pool_enabled")
    # dup of save_button
    pool_save = (By.ID, "save_button")
    pool_deleter = (By.ID, "delete_pool_button")

    # new catalog
    catalog_name_field = (By.ID, "catalog_name")
    catalog_family_parent_field = (By.ID, "catalog_pool_id")
    # dup of save_button
    catalog_save_locator = (By.ID, "save_button")
    catalog_delete_locator = (By.ID, "delete")

    # new cloud resource profile
    hwp_name_field = (By.ID, "hardware_profile_name")
    hwp_memory_field = (By.ID, "hardware_profile_memory_attributes_value")
    hwp_cpu_field = (By.ID, "hardware_profile_cpu_attributes_value")
    hwp_storage_field = (By.ID, "hardware_profile_storage_attributes_value")
    hwp_arch_field = (By.ID, "hardware_profile_architecture_attributes_value")

    # new cluster
    cluster_name = (By.ID, "frontend_realm_name")
    cluster_desc = (By.ID, "frontend_realm_description")
    cluster_save = (By.ID, "frontend_realm_submit")
    cluster_map_provider = (By.ID, "mapping_to_provider_button")
    cluster_provider_select = (By.ID, "realm_backend_target_realm_or_provider_id")
    cluster_provider_submit = (By.ID, "realm_backend_target_submit")

    # new image
    image_details = (By.ID, "details_images")
    #new_image_name_field = (By.ID, "name")
    # "(//input[@id='name'])[2]"
    new_image_name_field = (By.XPATH, "(//input[@id='name'])[2]")
    new_image_url_field = (By.ID, "image_url")
    new_image_edit_box = (By.XPATH, "(//input[@id='edit'])[2]")
    new_image_textbox = (By.ID, "image_xml")
    new_image_continue_button = (By.ID, "url_button")
    save_image = (By.ID, "save_image")

    # new app blueprint
    app_catalog_id = (By.ID, "catalog_id_")
    catalog_dropdown = (By.XPATH, "(//span[@class='catalog_link'])")
    catalog_item = (By.XPATH, "(//input[@id='catalog_id_'])")

    # build, push, launch
    # TODO: 'Build' with single provider; 'Build All' with multiple providers
    # is there an alternate way to access button?
    build_all = (By.XPATH, "(//input[@value='Build'])")
    push_all = (By.XPATH, "(//input[@value='Push all'])")
    blueprint_name = (By.ID, "deployable_name")
    resource_profile_dropdown = (By.ID, "hardware_profile")
    launch = (By.ID, "launch_deployment_button")
    app_name_field = (By.ID, "deployment_name")
    next_button = (By.ID, "next_button")

    # configserver
    #add_configserver = (By.ID, "config_server_control")
    configserver_endpoint = (By.ID, "config_server_endpoint")
    configserver_key = (By.ID, "config_server_key")
    configserver_secret = (By.ID, "config_server_secret")

    # blueprint
    new_deployable = (By.ID, "new_deployable_button")
    #deployable_name = (By.ID, "deployable_name")
    deployable_description = (By.ID, "deployable_description")
    deployable_url = (By.ID, "url")
    deployable_xml = (By.ID, "deployable_xml")
    new_deployable = (By.ID, "new_deployable_button")
    edit_xml = (By.ID, "edit_xml_button")

    # special blueprint params
    katello_register_tab = (By.ID, "KATELLO_REGISTER")
    submit_params = (By.ID, "submit_params")

    # verification
    image_pushed = (By.CSS_SELECTOR, "div.build_status > span")
    app_table = (By.XPATH, "(//table)")

    # search
    permissions_filter = (By.ID, "entities_preset_filter")
    entities_search = (By.ID, "entities_search")
    role_dropdown = (By.NAME, "entity_role_selected[]")
