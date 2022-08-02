from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
# Sitio web
website = 'https://www.wsj.com/market-data/quotes/index/DJIA/historical-prices'

# Directorio de webdriver
path = 'C:/webdrivers/chromedriver'

# Abrimos la pagina
driver = webdriver.Chrome(executable_path=path)
driver.get(website)

#agrandamos la pantalla
driver.maximize_window()

#bajamos hasta llegar al lugar que queremos
time.sleep(2)
driver.execute_script("window.scrollTo(0,1400)","")

# Traemos los datos a guardar
bolsa = driver.find_elements(By.TAG_NAME,'tr')

data = []
for i in [1,2,3]:
    for date in bolsa:
      if date.text != '':
          print(date.text)
          data.append(date.text)
    
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,1400)","")
    time.sleep(2) 
    next = driver.find_element(By.CLASS_NAME, 'next')
    next.click()
    


print(len(data))
print(data)

# Cerramos el driver y trabajamos con Dataframes
driver.quit()


def regex(fila):
    dataset = []
    if fila != 'DATE OPEN HIGH LOW CLOSE' and fila != None:
        fecha = re.findall(r'[0-2][0-9]\/[0-3][0-9]\/[0-2][0-9]',fila)
        monto = re.findall(r'(\d{3,}.\d{1,})',fila)
    
        dataset.append(fecha[0])
        dataset.append(monto[0])
        dataset.append(monto[1])
        dataset.append(monto[2])
        dataset.append(monto[3]) 
        return dataset
    

dataframe = map(regex, data)
dataframe = list(dataframe)

# Eliminamos los datos 'None' de la lista, lo de arriba no funcionó 
clean_df = [i for i in dataframe if i]
print(clean_df)

import pandas as pd

df_bolsa = pd.DataFrame(clean_df)
print(df_bolsa.shape)

#La pagina tiene para descargar un .csv pero decidí hacerlo de esta manera para practicar 
df_bolsa.to_csv('2022_wsj.csv', index= False)


