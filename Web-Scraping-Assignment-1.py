#!/usr/bin/env python
# coding: utf-8

# #### 1) Write a python program to display all the header tags from wikipedia.org and make data frame.

# In[17]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_wikipedia_headers(url):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content)
    
    headers = []
    
    for i in soup.find_all('span',class_="mw-headline"):
        headers.append(i.text)
    
    df = pd.DataFrame(headers, columns=['Headers'])
    
    return df


# In[4]:


url = 'https://en.wikipedia.org/wiki/Main_Page'
df = scrape_wikipedia_headers(url)
print(df)


# #### 2) Write s python program to display list of respected former presidents of India(i.e. Name , Term of office)
# from https://presidentofindia.nic.in/former-presidents.htm and make data frame.

# In[279]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def president_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    names = []
    terms = []
    
    for i in soup.find_all('div', class_="presidentListing"):
        text = i.text.strip()
        parts = text.split('\nTerm of Office: ')
        if len(parts) == 2:
            name, term = parts
            term = term.split(' (')[0]  # Remove the link part
        else:
            name, term = parts[0], None
        names.append(name)
        terms.append(term)

    df = pd.DataFrame({'Presidents': names, 'Term of Office': terms})
    return df

url = 'https://presidentofindia.nic.in/former-presidents.htm'
df = president_names(url)
print(df)


# #### 3) Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape and make data frame
# #### a) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating

# In[216]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_mteam(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('td', class_='rankings-block__banner--pos')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('td', class_='table-body__cell table-body__cell--position u-text-right')
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
     
    teams = []
    for i, team in enumerate(soup.find_all('span', class_='u-hide-phablet'), 1):
        if i > 10:
            break
        teams.append(team.text.strip())
    
    matches=[]
    # Get the first matches from a different class
    first_matches_element = soup.find('td', class_='rankings-block__banner--matches')
    first_matches = first_matches_element.text.strip()
    matches.append(first_matches)
        
    points=[]
    # Get the first points from a different class
    first_points_element = soup.find('td', class_='rankings-block__banner--points')
    first_points = first_points_element.text.strip()
    points.append(first_points)
    
    table_rows = soup.find_all('tr')

    for row in table_rows[1:]:
        columns = row.find_all('td', class_='table-body__cell u-center-text')

        if len(columns) >= 2:
            matches.append(columns[0].text.strip())
            points.append(columns[1].text.strip())
            if len(matches) == 10 and len(points) == 10:
                break
                
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('td', class_='rankings-block__banner--rating u-text-right')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell u-text-right rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    df = pd.DataFrame({'Rank':ranking,'Teams':teams,'Matches': matches,'Points':points,'Rating':ratings})
    return df

url="https://www.icc-cricket.com/rankings/mens/team-rankings/odi"
df = top_mteam(url)
print(df)


# #### 3) b) Top 10 ODI Batsmen along with the records of their team and rating.

# In[237]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_batsmen(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

        
    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('span', class_='rankings-block__pos-number')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('span', class_="rankings-table__pos-number")
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
    
    player=[]
     # Get the first player from a different class
    first_player_element = soup.find('div', class_="rankings-block__banner--name-large")
    first_player = first_player_element.text.strip()
    player.append(first_player)
    
    # Get the remaining players
    player_elements = soup.find_all('td', class_="table-body__cell rankings-table__name name")
    for p in player_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        player.append(p.text.strip())
    
    teams=[]
    # Get the first player team from a different class
    first_team_element = soup.find('div', class_="rankings-block__banner--nationality")
    first_team = first_team_element.text.strip()
    teams.append(first_team)
    
    # Get the remaining teams
    team_elements = soup.find_all('span', class_='table-body__logo-text')
    for t in team_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        teams.append(t.text.strip())
    
   
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('div', class_='rankings-block__banner--rating')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    df = pd.DataFrame({'Rank': ranking,'Player':player,"Team":teams,'Rating':ratings})
    return df

url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting"
df = top_batsmen(url)
print(df)


# #### 3) c) Top 10 ODI bowlers along with the records of their team andrating.

# In[239]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_bowler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

        
    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('span', class_='rankings-block__pos-number')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('span', class_="rankings-table__pos-number")
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
    
    player=[]
     # Get the first player from a different class
    first_player_element = soup.find('div', class_="rankings-block__banner--name-large")
    first_player = first_player_element.text.strip()
    player.append(first_player)
    
    # Get the remaining players
    player_elements = soup.find_all('td', class_="table-body__cell rankings-table__name name")
    for p in player_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        player.append(p.text.strip())
    
    teams=[]
    # Get the first player team from a different class
    first_team_element = soup.find('div', class_="rankings-block__banner--nationality")
    first_team = first_team_element.text.strip()
    teams.append(first_team)
    
    # Get the remaining teams
    team_elements = soup.find_all('span', class_='table-body__logo-text')
    for t in team_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        teams.append(t.text.strip())
    
   
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('div', class_='rankings-block__banner--rating')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    df = pd.DataFrame({'Rank': ranking,'Player':player,"Team":teams,'Rating':ratings})
    return df

url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling"
df = top_bowler(url)
print(df)


# #### 4) Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape and make data frame
# 
# #### a) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating.
# 

# In[207]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_wteam(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('td', class_='rankings-block__banner--pos')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('td', class_="table-body__cell table-body__cell--position u-text-right")
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
    
    teams = []
    for i, team in enumerate(soup.find_all('span', class_="u-hide-phablet"), 1):
        if i > 10:
            break
        teams.append(team.text.strip())
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('td', class_='rankings-block__banner--rating u-text-right')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell u-text-right rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    matches=[]
    # Get the first matches from a different class
    first_matches_element = soup.find('td', class_='rankings-block__banner--matches')
    first_matches = first_matches_element.text.strip()
    matches.append(first_matches)
        
    points=[]
    # Get the first points from a different class
    first_points_element = soup.find('td', class_='rankings-block__banner--points')
    first_points = first_points_element.text.strip()
    points.append(first_points)
    
    table_rows = soup.find_all('tr')

    for row in table_rows[1:]:
        columns = row.find_all('td', class_='table-body__cell u-center-text')

        if len(columns) >= 2:
            matches.append(columns[0].text.strip())
            points.append(columns[1].text.strip())
            if len(matches) == 10 and len(points) == 10:
                break
   
    df = pd.DataFrame({'Rank':ranking,'Teams': teams,'Matches': matches,'Points':points,'Rating':ratings})
    return df

url="https://www.icc-cricket.com/rankings/womens/team-rankings/odi"
df = top_wteam(url)
print(df)


# #### 4) b) Top 10 women’s ODI Batting players along with the records of their team and rating.

# In[240]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_batsmen(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

        
    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('span', class_='rankings-block__pos-number')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('span', class_="rankings-table__pos-number")
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
    
    player=[]
     # Get the first player from a different class
    first_player_element = soup.find('div', class_="rankings-block__banner--name-large")
    first_player = first_player_element.text.strip()
    player.append(first_player)
    
    # Get the remaining players
    player_elements = soup.find_all('td', class_="table-body__cell rankings-table__name name")
    for p in player_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        player.append(p.text.strip())
    
    teams=[]
    # Get the first player team from a different class
    first_team_element = soup.find('div', class_="rankings-block__banner--nationality")
    first_team = first_team_element.text.strip()
    teams.append(first_team)
    
    # Get the remaining teams
    team_elements = soup.find_all('span', class_='table-body__logo-text')
    for t in team_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        teams.append(t.text.strip())
    
   
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('div', class_='rankings-block__banner--rating')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    df = pd.DataFrame({'Rank': ranking,'Player':player,"Team":teams,'Rating':ratings})
    return df

url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting"
df = top_batsmen(url)
print(df)


# #### 4) c) Top 10 women’s ODI all-rounder along with the records of their team and rating.

# In[241]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def allrounder(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

        
    ranking=[]
    # Get the first ranking from a different class
    first_ranking_element = soup.find('span', class_='rankings-block__pos-number')
    first_ranking = first_ranking_element.text.strip()
    ranking.append(first_ranking)
    
    # Get the remaining rankings
    ranking_elements = soup.find_all('span', class_="rankings-table__pos-number")
    for r in ranking_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ranking.append(r.text.strip())
    
    player=[]
     # Get the first player from a different class
    first_player_element = soup.find('div', class_="rankings-block__banner--name-large")
    first_player = first_player_element.text.strip()
    player.append(first_player)
    
    # Get the remaining players
    player_elements = soup.find_all('td', class_="table-body__cell rankings-table__name name")
    for p in player_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        player.append(p.text.strip())
    
    teams=[]
    # Get the first player team from a different class
    first_team_element = soup.find('div', class_="rankings-block__banner--nationality")
    first_team = first_team_element.text.strip()
    teams.append(first_team)
    
    # Get the remaining teams
    team_elements = soup.find_all('span', class_='table-body__logo-text')
    for t in team_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        teams.append(t.text.strip())
    
   
    ratings = []
    
    # Get the first rating from a different class
    first_rating_element = soup.find('div', class_='rankings-block__banner--rating')
    first_rating = first_rating_element.text.strip()
    ratings.append(first_rating)
    
    # Get the remaining ratings
    rank_elements = soup.find_all('td', class_="table-body__cell rating")
    for rank in rank_elements[0:9]:  # Start from the second rank and go up to the tenth rank
        ratings.append(rank.text.strip())
    
    df = pd.DataFrame({'Rank': ranking,'Player':player,"Team":teams,'Rating':ratings})
    return df

url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/all-rounder"
df = allrounder(url)
print(df)


# #### 5) Write a python program to scrape mentioned news details from https://www.cnbc.com/world/?region=world and make data frame
# i) Headline
# ii) Time
# iii) News Link

# In[253]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def cnbc_news(url):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content)
    
    headlines=[]
    
    for i in soup.find_all('a',class_="LatestNews-headline"):
        headlines.append(i.get('title'))
    
    time = []
    
    for i in soup.find_all('time',class_="LatestNews-timestamp"):
        time.append(i.text)
    link=[]
    for i in soup.find_all('a',class_="LatestNews-headline"):
        link.append(i.get('href'))

    df = pd.DataFrame({'Headline':headlines,'Time': time,'News Link':link})
    return df
    
    
url = 'https://www.cnbc.com/world/?region=world'
df = cnbc_news(url)
print(df)


# #### 6) Write a python program to scrape the details of most downloaded articles from AI in last 90 days.https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles
# 
# Scrape below mentioned details and make data frame
# i) Paper Title
# ii) Authors
# iii) Published Date
# iv) Paper URL

# In[258]:



import requests
import pandas as pd
from bs4 import BeautifulSoup

def top_article(url):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content)
    
    title=[]
    
    for i in soup.find_all('h2',class_="sc-1qrq3sd-1 gRGSUS sc-1nmom32-0 sc-1nmom32-1 btcbYu goSKRg"):
        title.append(i.text)
    
    authors=[]
    for i in soup.find_all('span',class_="sc-1w3fpd7-0 dnCnAO"):
        authors.append(i.text)
    date = []
    
    for i in soup.find_all('span',class_="sc-1thf9ly-2 dvggWt"):
        date.append(i.text)
    link=[]
    for i in soup.find_all('a',class_="sc-5smygv-0 fIXTHm"):
        link.append(i.get('href'))

    df = pd.DataFrame({'Title':title,"Authors":authors,"Published date":date,"URL":link})
    return df
    
    
url = 'https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles'
df = top_article(url)
print(df)


# #### 7) Write a python program to scrape mentioned details from dineout.co.inand make data frame
# i) Restaurant name
# ii) Cuisine
# iii) Location
# iv) Ratings
# v) Image URL

# In[ ]:


# I am unable to work with dineout.co.in as I live in the UK. I am using deliveroo.uk instead


# In[274]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def deliveroo(url):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content)
    
    name=[]
    
    for i in soup.find_all('p',class_='ccl-649204f2a8e630fd ccl-a396bc55704a9c8a ccl-ff5caa8a6f2b96d0 ccl-40ad99f7b47f3781'):
        name.append(i.text)
    
    offers=[]
    
    for i in soup.find_all('div','HomeFeedUICard-d38caa5cc97794b4'):
        offers.append(i.text)
    
        
    df = pd.DataFrame({'Restaurant Name':name,"Special Offers":offers})
    return df
    
    
url = 'https://deliveroo.co.uk/restaurants/london/woodford/?geohash=u10j83y9myd1&collection=basket+discounts'
df = deliveroo(url)
print(df)

