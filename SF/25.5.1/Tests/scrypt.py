from settings import email, password, site_url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()

try:
    # переход на страницу авторизации
    driver.get(site_url)
    driver.maximize_window()
    # ввод email и пароля
    driver.implicitly_wait(5)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID,'pass').send_keys(password)

    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    # нажимаем Мои питоцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # проверка авторизации
    result = driver.find_element(By.CSS_SELECTOR, 'h1').text
    assert result == "PetFriends", "login error"

    # проверка элементов карточек
    images = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))

    for i in range(len(names)):
        assert images[i].get_attribute('src') != '', 'Image not found'  # проверка наличия фото
        assert names[i].text != '', 'Name not found'  # проверка наличия имени
        assert descriptions[i].text != '', 'Description not found'  # проверка наличия описания
        assert ', ' in descriptions[i]  #проверка наличия запятой
        parts = descriptions[i].text.split(", ")  # строка делится на части
        assert len(parts[0]) > 0, 'Species not found'  # проверка породы питомца
        assert len(parts[1]) > 0, 'Age not found'  # проверка возраста


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()