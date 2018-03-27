from selenium import webdriver
import json, base64

def send_devtools(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  if response['status']:
    raise Exception(response.get('value'))
  return response.get('value')

def save_as_pdf(driver, path, options={}):    
  # https://timvdlippe.github.io/devtools-protocol/tot/Page#method-printToPDF
  result = send_devtools(driver, "Page.printToPDF", options)
  with open(path, 'wb') as file:
    file.write(base64.b64decode(result['data']))


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.google.co.uk/")

save_as_pdf(driver, r'page.pdf', { 'landscape': False })