import base64
import json
import uuid
from os import path, makedirs
from selenium import webdriver


def _make_outfile_name(url: str) -> str:
    found_unique_name = False
    while not found_unique_name:
        file_name = (
            url
            .replace('https://', '')
            .replace('http://', '')
            .replace('.', '-dot-')
            .replace('/', '-')
            .replace('?', '-q-')
            .replace('&', '-and-')
        )
        file_path = path.join(
            'out',
            'chrome',
            f'{file_name}-{str(uuid.uuid4())}.pdf'
        )
        found_unique_name = not path.isfile(file_path)
    return str(file_path)


def _send_devtools(driver):
    resource = f'/session/{driver.session_id}/chromium/send_command_and_get_result'
    url = driver.command_executor._url + resource
    pdf_options = json.dumps(
        {
            'cmd': 'Page.printToPDF',
            'params': {
                'paperWidth': 11,
                'paperHeight': 11,
            }
        }
    )
    response = driver.command_executor._request('POST', url, pdf_options)
    if response['status']:
        raise Exception(response.get('value'))
    return response['value']


def _save_to_file(driver, url: str) -> None:
    driver.get(url)
    result = _send_devtools(driver)
    out_file_name = _make_outfile_name(url)
    out_dir = path.dirname(out_file_name)
    if not path.exists(out_dir):
        makedirs(out_dir)
    with open(out_file_name, 'wb+') as file:
        file.write(base64.b64decode(result['data']))


def generate_pdf(url: str) -> None:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    _save_to_file(driver, url)


if __name__ == '__main__':
    # generate_pdf('http://google.com')  # static
    # generate_pdf('http://peterfonseca.gq')  # react
    generate_pdf('https://you.23andme.com/public/lucky-you/')
