#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import bs4 as bs
import requests
import pandas as pd
import numpy as np
import json


# *Getting data from URL*

# In[2]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
res = requests.get(url)
soup = bs.BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
data = pd.read_json(df[0].to_json(orient='records'))


# In[3]:


data.head()


# + *Only process the cells that have an assigned borough. Ignore cells with a borough*

# In[4]:


dff = data[data['Borough'] != 'Not assigned']
dff


# + *More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.*

# In[5]:


dff = dff.groupby(['Borough', 'Postal code'], as_index=False).agg(','.join)
dff


# + *If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.*

# In[6]:


dff['Neighborhood']=np.where(dff['Neighborhood'] == 'Not assigned', dff['Borough'], dff['Neighborhood'])
dff.head()


# In[7]:


dff.shape

