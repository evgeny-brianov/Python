from telnetlib import EC

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import settings


# RT1
def test_open_page_auth(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Авторизация', 'Auth fail'

# RT2
def test_agreements(browser):
    browser.find_elements(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[5]/a')[0].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'

# RT3
def test_agreements_non_empty(browser):
    browser.find_elements(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[5]/a')[0].click()
    browser.switch_to.window(browser.window_handles[1])
    # driver.execute_script('window.scrollTo(0,1000);')
    headers = browser.find_elements(By.XPATH, '//*[@id="root"]/ol/li')
    assert len(headers) > 1, 'FAIL' 

# RT4
def test_auth_by_phone_empty_all_field(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]').click()
    browser.find_element(By.ID, 'username').send_keys('')
    browser.find_element(By.ID, 'password').send_keys('')
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Введите номер телефона')]") 

# RT5
def test_auth_by_phone_empty_password(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.unknown_phone)
    browser.find_element(By.ID, 'password').send_keys('')
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Неверный логин или пароль')]")

# RT6
def test_auth_by_phone_empty_phone(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]').click()
    browser.find_element(By.ID, 'username').send_keys('')
    browser.find_element(By.ID, 'password').send_keys(settings.unknown_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Введите номер телефона')]")

# RT7
@pytest.mark.xfail(reason='captcha')
def test_auth_by_phone_incorrect(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.unknown_phone)
    browser.find_element(By.ID, 'password').send_keys(settings.unknown_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Неверный логин или пароль')]")

# RT8
def test_auth_by_mail_empty_all_field(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]').click()
    browser.find_element(By.ID, 'username').send_keys('')
    browser.find_element(By.ID, 'password').send_keys('')
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Введите адрес, указанный при регистрации')]")

# RT9
def test_auth_by_mail_empty_password(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.unknown_mail)
    browser.find_element(By.ID, 'password').send_keys('')
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Неверный логин или пароль')]")

# RT10
def test_auth_by_mail_empty_mail(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]').click()
    browser.find_element(By.ID, 'username').send_keys('')
    browser.find_element(By.ID, 'password').send_keys(settings.unknown_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Введите адрес, указанный при регистрации')]")

# RT11
@pytest.mark.xfail(reason='captcha')
def test_auth_by_mail_incorrect(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.unknown_mail)
    browser.find_element(By.ID, 'password').send_keys(settings.unknown_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Неверный логин или пароль')]")

# RT12
def test_auth_by_login_empty_all_field(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]').click()
    browser.find_element(By.ID, 'username').send_keys('')
    browser.find_element(By.ID, 'password').send_keys('')
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.XPATH, "//span[contains(text(), 'Введите логин, указанный при регистрации')]")

# RT13
def test_auth_by_login_x_username(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.x_login)
    browser.find_element(By.ID, 'password').send_keys(settings.unknown_password)
    browser.find_element(By.ID, 'kc-login').click()
    browser.implicitly_wait(5)
    assert browser.find_element(By.XPATH,"//h2[contains(text(), 'Ваш запрос был отклонен из соображений безопасности.')]")

# RT14
def test_auth_by_login_x_password(browser):
    browser.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]').click()
    browser.find_element(By.ID, 'username').send_keys(settings.unknown_login)
    browser.find_element(By.ID, 'password').send_keys(settings.x_password)
    browser.find_element(By.ID, 'kc-login').click()
    browser.implicitly_wait(5)
    assert browser.find_element(By.XPATH,"//h2[contains(text(), 'Ваш запрос был отклонен из соображений безопасности.')]")

# RT-015
@pytest.mark.xfail(reason='Аккаунт уже зарегистрирован')
def test_registration(browser):
    browser.find_element(By.ID, 'kc-register').click()
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys('Иван')
    inputs[1].send_keys('Тестович')
    inputs[2].send_keys('Москва')
    inputs[3].send_keys('test@test.ru')
    inputs[4].send_keys('testtest')
    inputs[5].send_keys('testtest')
    browser.find_element(By.NAME, 'register').click()
    title = browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text
    assert title == 'Подтверждение email', 'Такой пользователь зарегистрирован'

# RT16
@pytest.mark.xfail(reason='капча')
def test_reset_password_by_mail(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'captcha').send_keys()  # сюда вводим капчу
    browser.find_element(By.ID, 'reset')

# RT17
def test_vk_auth_allowed(browser):
    browser.find_element(By.ID, 'oidc_vk').click()
    href = browser.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert href == 'https://vk.com/', 'VK auth not allowed'
    assert browser.current_url.startswith('https://oauth.vk.com/authorize?'), 'VK site not redirected'

# RT18
def test_ok_auth_allowed(browser):
    browser.find_element(By.ID, 'oidc_ok').click()
    title = browser.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text
    assert title == 'Одноклассники', 'Ok auth not allowed'
    assert browser.current_url.startswith('https://connect.ok.ru/'), 'Ok site not redirected'

# RT19
def test_email_auth_allowed(browser):
    browser.find_element(By.ID, 'oidc_mail').click()
    header_text = browser.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert header_text == 'мой мир@mail.ru', 'mail.ru auth not allowed'
    assert browser.current_url.startswith('https://connect.mail.ru/oauth/'), 'mail.ru site not redirected'

# RT20
def test_google_auth_allowed(browser):
    browser.find_element(By.ID, 'oidc_google').click()
    header_text = browser.find_element(By.XPATH, '//*[@id="initialView"]/div[2]/div/div[1]/div/div[2]').text
    assert header_text == 'Войдите в аккаунт Google', 'Google auth not allowed'
    assert browser.current_url.startswith('https://accounts.google.com/'), 'google site not redirected'

# RT21
def test_yandex_auth_allowed(browser):
    browser.find_element(By.XPATH, '//*[@id="oidc_ya"]').click()
    browser.find_element(By.XPATH, '//*[@id="oidc_ya"]').click()
    header_text = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/h1/span').text
    assert header_text == 'Войдите с Яндекс ID', 'Yandex auth not allowed'
    assert browser.current_url.startswith('https://passport.yandex.ru/auth?'), 'yandex site not redirected'
