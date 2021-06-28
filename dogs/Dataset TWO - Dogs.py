#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[2]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[3]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows = 30000)


# In[4]:


df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[5]:


df.shape


# In[6]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# ### Answer : 
# Each row is a dog that has a license in NYC. `Owner Zip Code` shows the Zip code where a dog owner lives, `Animal Birth` displays a day when a dog was born.

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# ### My questions : 
# 1. Which Zipcode most dog owners live?
# 2. What is the most popular name among NYC dogs?
# 3. What is the average age?
# 4. How many dogs are vaccinated?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[7]:


df['Primary Breed'].value_counts().head(10)


# In[8]:


df['Primary Breed'].value_counts().head(10).plot(kind = 'barh')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[9]:


import numpy as np
df['Primary Breed'] = df['Primary Breed'].replace("Unknown", np.nan)
df['Primary Breed'].value_counts().head(10).plot(kind = 'barh')


# ## What are the most popular dog names?

# In[10]:


df['Animal Name'] = df['Animal Name'].replace(['UNKNOWN', 'Unknown'], np.nan)
df['Animal Name'].value_counts()


# ### Answer :
# `"Max"` is the most popular dog name.

# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[11]:


df_name = df['Animal Name'] 
df[df_name == 'Hiro']


# In[12]:


df_name[df_name == 'Max'].value_counts()


# In[13]:


df_name[df_name == 'Maxwell'].value_counts()


# ### Answer :
# There are no dogs named `"Hiromi"` but two dogs named `"Hiro"`.
# 
# 202 dogs are named `"Max"`, while 11 dogs are `"Maxwell"`.

# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[14]:


df['Guard or Trained'].value_counts(normalize=True)*100


# ### Answer :
# `0.085746%` of dogs are guard or trained dogs. (# I noticed it wasn't right later because of NaN issue.)

# ## What are the actual numbers?

# In[15]:


df['Guard or Trained'].value_counts()


# ### Answer :
# `17 dogs` are guard or trained dogs.

# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[16]:


df['Guard or Trained'].head()


# In[17]:


df['Guard or Trained'].value_counts(dropna = False)


# ### Answer : 
# There are lots of `NaN` rows. I found them with `.value_counts(dropna = False)`

# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[18]:


df['Guard or Trained'] = df['Guard or Trained'].replace(np.nan , 'No')
df['Guard or Trained'].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[19]:


df_guard = df[df['Guard or Trained'] == 'Yes']
df_guard['Primary Breed'].value_counts()


# ### Answer : 
# `German Shepherd Dog` is top dog breeds for guard dogs.

# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[20]:


df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)
df.head(2)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[21]:


df['age'] = 2021 - df['year'] 
df.head(2)


# In[22]:


round(df['age'].mean(),1)


# ### Answer : 
# The mean of NYC dogs is `11.7`  years old.

# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[23]:


df_zipc = pd.read_csv("zipcodes-neighborhoods.csv")
df_zipc.head(2)


# In[24]:


df = df.merge(df_zipc, left_on = "Owner Zip Code" , right_on = "zip")
df.head(2)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[25]:


df.borough.value_counts()


# In[26]:


df.neighborhood.value_counts()


# In[27]:


df[df.borough == 'Bronx']['Animal Name'].value_counts().head(1)


# In[28]:


df[df.borough == 'Brooklyn']['Animal Name'].value_counts().head(1)


# In[29]:


df[df.neighborhood == 'Upper East Side']['Animal Name'].value_counts().head(1)


# ### Answer : 
# `"Bella"` is the most popular dog name in Bronx while `"Max"` in Brooklyn. In the Upper East Side, `"Charlie"` is the most popular.

# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[30]:


# I did this 2 way. First, I use groupby(level=0) & .nlargest. Then created the new DataFrame.
df_each = pd.DataFrame(df.groupby('neighborhood')['Primary Breed'].value_counts().groupby(level=0).nlargest(1))
df_each


# In[46]:


#Second, I created new DataFrame at the beginning, then groupby(level = 0) & .head
df_each2 = pd.DataFrame(df.groupby('neighborhood')['Primary Breed'].value_counts())
df_each2.groupby(level=0).head(1)


# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[31]:


import numpy as np
df['Spayed or Neut'] = df['Spayed or Neut'].replace(np.nan, 'No')  #I did. but on this data, maybe I didn't have to do.
df['Spayed or Neut'].value_counts()


# In[32]:


df_nosp = df[df['Spayed or Neut'] == 'No']
df_nosp['Primary Breed'].value_counts()


# In[33]:


df_nosp['Animal Gender'].value_counts()


# ### Answer :
# `Yorkshire Terrier` is the least likely to be spayed. `Male` is less spayed than `Female`. 

# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[34]:


df_dc = df['Animal Dominant Color'].str.lower() .isin(['black', 'white','gray'])
df_sc = df['Animal Secondary Color'].str.lower() .isin(['black', 'white','gray'])
df_tc = df['Animal Third Color'].str.lower() .isin(['black', 'white','gray'])
df['monochrome'] = df_dc & df_sc & df_tc
df['monochrome'].value_counts()


# ### Answer : 
# `404` dogs are monochrome.

# ## How many dogs are in each borough? Plot it in a graph.

# In[35]:


df.borough.value_counts().plot(kind = 'barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[36]:


df_pop = pd.read_csv("boro_population.csv")
df_pop.head()


# In[37]:


df_borodog = pd.DataFrame(df.borough.value_counts())
df_borodog = df_borodog.reset_index()
df_borodog.columns = ['borough', 'dogs']


# In[38]:


df_borodog = df_borodog.merge(df_pop , on= 'borough')


# In[40]:


df_borodog['dog_per_capita'] = df_borodog.dogs / df_borodog.population *100
df_borodog


# ### Answer : 
# `Manhattan` has the highest dog per capita.

# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[71]:


df_top5 = pd.DataFrame(df.groupby('borough')['Primary Breed'].value_counts())
df_top5.groupby(level=0).head(5).plot(kind = 'bar' , figsize=(12,6)  )

# I aslo tried this. Almost same, but xlabel is less beautiful.
# df_topf = pd.DataFrame(df.groupby('borough')['Primary Breed'].value_counts().groupby(level=0).nlargest(5))
# df_topf.plot(kind = 'bar' , figsize=(12,6) )


# In[ ]:





# ## What percentage of dogs are not guard dogs?

# In[72]:


df['Guard or Trained'].value_counts(normalize=True)*100


# ### Answer : 
# `99.943333%` of dogs are not guard dogs. Guard dogs are just 0.056667% instead of 0.085746%.

# In[ ]:




