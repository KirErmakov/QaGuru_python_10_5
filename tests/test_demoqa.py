from selene import browser, command, be, have, by
from selene.support.shared.jquery_style import s
from selenium.webdriver import Keys
import os
from pathlib import Path
import tests


def test_fill_form_user_flow():
    browser.open('/automation-practice-form')
    # Убрать баннер и footer, закрывающие кнопку "Submit"
    browser.execute_script('document.querySelector("#fixedban").remove()')
    browser.execute_script('document.querySelector("footer").remove()')
    # Ввести личную информацию пользователя
    browser.element('#firstName').should(be.blank).type('Kuraj')
    browser.element('#lastName').should(be.blank).type('Bombei')
    browser.element('#userEmail').should(be.blank).type('kjb@gmail.com')
    browser.element("label[for='gender-radio-1']").click()
    browser.element('#userNumber').type('9876543210')
    # Выбрать дату рождения
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').s(by.text('December')).click()
    browser.element('.react-datepicker__year-select').s(by.text('1991')).click()
    browser.element("div[aria-label*='31st']").click()
    # Ввести название предмета
    browser.element('#subjectsInput').type('Computer Science').press_enter()
    # Выбрать увлечения
    browser.element("label[for='hobbies-checkbox-1']").click()

    # Загрузить картинку
    browser.element('#uploadPicture').send_keys(os.path.abspath('files/Rajesh.jpg'))
    # Ввести текущий адрес
    browser.element('#currentAddress').should(be.blank).type('Somewhere in India')
    # Выбрать штат
    browser.element('#state').click()
    browser.all('#state div').element_by(have.exact_text('NCR')).click()
    # Выбрать город
    browser.element('#city').click()
    browser.all('#city div').element_by(have.exact_text('Delhi')).click()
    # Нажать кнопку "Submit"
    browser.element('#submit').click()

    # Проверить, что появилось сообщение об успешном заполнении формы
    browser.element('#example-modal-sizes-title-lg').should(have.exact_text('Thanks for submitting the form'))
    # Проверить соответствие данных в таблице отправленным данным
    browser.element('.table').all('td').even.should(
        have.texts(
        'Kuraj Bombei',
        'kjb@gmail.com',
        'Male',
        '9876543210',
        '31 December,1991',
        'Computer Science',
        'Sports',
        'Rajesh.jpg',
        'Somewhere in India',
        'NCR Delhi'
        )
    )


def test_fill_form_automation_flow():
    browser.open('/automation-practice-form')
    browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).should(
        have.size_greater_than_or_equal(3)
    ).perform(command.js.remove)

# WHEN
    s('#firstName').should(be.blank).type('Kuraj')
    s('#lastName').should(be.blank).type('Bombei')
    s('#userEmail').should(be.blank).type('kjb@gmail.com')
    browser.all('[for^=gender-radio]').element_by(have.exact_text('Male')).click()
    s('#userNumber').type('9876543210')
    s('#dateOfBirthInput').send_keys(Keys.CONTROL, 'a').type('31 December 1991').press_enter()

    s('#subjectsInput').set_value('Computer Science').press_enter()
    browser.all('[for^=hobbies-checkbox]').element_by(have.exact_text('Sports')).click()

    s('#uploadPicture').set_value(str(Path(tests.__file__).parent.joinpath('files/Rajesh.jpg').absolute()))
    s('#currentAddress').should(be.blank).perform((command.js.set_value('Somewhere in India')))
    s('#state').click()
    browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('NCR')).click()
    s('#city').click()
    browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('Delhi')).click()
    s('#submit').perform(command.js.click)

# THEN
    browser.element('#example-modal-sizes-title-lg').should(have.exact_text('Thanks for submitting the form'))
    browser.element('.table').all('td').even.should(
        have.texts(
            'Kuraj Bombei',
            'kjb@gmail.com',
            'Male',
            '9876543210',
            '31 December,1991',
            'Computer Science',
            'Sports',
            'Rajesh.jpg',
            'Somewhere in India',
            'NCR Delhi'
        )
    )
