# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:09:27 2023

@author: Jerome Roeser
"""

from selenium.webdriver import Chrome
import time
import pandas as pd

#SETTINGS
n_topologies = 202
n_topologies_nets = 3552


# C:\Users\roeser\Downloads\install_files\chromedriver_win32
# W:/Documents/finxter/projects/chromedriver.exe
# C:/Users/Jerome Roeser/Documents/chromedriver.exe
webdriver = r"W:/Documents/finxter/projects/chromedriver.exe" #change me!
#^Download from: https://chromedriver.chromium.org/

driver = Chrome(executable_path=webdriver)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

topologies = []
df = pd.DataFrame([])
url_tags = ['nets'] # ['layers', 'nets']
print('Scraping topology names..')

# for url_tag in url_tags:
url = "http://rcsr.anu.edu.au/"+url_tags[0]+"#details"
driver.get(url)
time.sleep(10)
driver.find_elements_by_xpath('//*[@id="react-main"]/div/div[2]/ul/li[2]/div/ul/li[1]/a')[0].click()
for i in range(1,n_topologies+1):
	topologies.append(driver.find_elements_by_xpath('//*[@id="react-main"]/div/div[2]/ul/li[2]/div/div/ul/li['+str(i)+']/a')[0].text)


print('Scraping topology data...')
for i, top in enumerate(topologies[18:24]):

    url = 'http://rcsr.anu.edu.au/nets/'+top
    driver.get(url)
    if i == 0:
        time.sleep(10)
    else:
        time.sleep(1)
    
    dfs = pd.read_html(driver.page_source)
    all_vert_info = [dfs[2].loc[j,'cn':'z'].to_list() for j in range(0, len(dfs[2]))]
    all_edge_info = [dfs[4].loc[j,'x':'z'].to_list() for j in range(0, len(dfs[4]))]
    
    df = pd.concat([df, pd.DataFrame({'topology': top,'spacegroup': dfs[0].iloc[0,1],'cellparams': str(dfs[1].iloc[0].to_list()), 'vertices': str(all_vert_info), 'edges': str(all_edge_info)}, index=[0])], ignore_index=True)
    if url_tags[0] == 'nets':
    	df.to_csv('rcsr_3D.csv')
    elif url_tags[0] == 'layers':
    	df.to_csv('rcsr_2D.csv')

driver.close()
print('Done!')