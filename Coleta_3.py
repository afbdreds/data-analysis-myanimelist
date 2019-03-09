from urllib.request import urlopen as uReq
from urllib.parse import quote
from bs4 import BeautifulSoup as soup
import pandas as pd


dic={
     "names":[],
     #"premiered":[],
     "scores":[],
     "genres":[],
     "s_ranks":[],
     "p_rank":[],
     "studios":[],
     "episodes":[],
     "aired":[],
     "types":[],
     #"v_actors":[],
     #"sources":[],
     #"directors":[],
     "htmls":[],
     "htmls_encoded":[],
     "members":[],
    }

genres = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo', 'Shounen', 'Shounen', 'Slice', 'Space', 'Sports', 'Super', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']

pages = 50
for page in range(1,pages+1):
    if page == 1:
        my_url="https://myanimelist.net/topanime.php?type=bypopularity&limit="
    else:
        my_url= "{}{}".format("https://myanimelist.net/topanime.php?type=bypopularity&limit=",50*(page-1))
    print (page)   

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.body.findAll("tr",{"class":"ranking-list"})
    
    
    for container in containers:
        html = container.findAll("a",{"class","hoverinfo_trigger fl-l fs14 fw-b"})[0]["href"]
        name = container.findAll("a",{"class","hoverinfo_trigger fl-l fs14 fw-b"})[0].get_text()
        #score = container.findAll("td",{"class":"score ac fs14"})[0].get_text().strip()
        #rank = container.findAll("td",{"class":"rank ac"})[0].span.get_text()
        #type_ = container.findAll("div")[0].get_text().strip().split("\n        ")[1].replace(")","").split("(")[0]
        n_episodes = container.findAll("div")[0].get_text().strip().split("\n        ")[1].replace(")","").split("(")[1]
        aired = container.findAll("div")[0].get_text().strip().split("\n        ")[2]
        #pop = container.findAll("div")[0].get_text().strip().split("\n        ")[3]
        dic["names"].append(name)
        dic["episodes"].append(n_episodes)
        dic["aired"].append(aired)
        dic["htmls"].append(html)


for url in dic["htmls"]:
    dic["htmls_encoded"].append(url[:30]+"/".join(list(map(quote,url[30:].split("/")))))



count = 0
for link in dic["htmls_encoded"]:
    count+=1
    my_url = link
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    print(count, link)
    #premiered = page_soup.findAll("span",{"class":"information season"})[0].get_text()
    score = page_soup.findAll("div",{"class":"fl-l score"})[0].get_text().strip()
    rank = page_soup.findAll("div",{"class":"di-ib ml12 pl20 pt8"})[0].get_text().split(" ")[1].replace("Popularity","")
    pop = page_soup.findAll("div",{"class":"di-ib ml12 pl20 pt8"})[0].get_text().split(" ")[2].replace("Members","")
    studio = page_soup.findAll("span",{"class":"information studio author"})[0].get_text()
    type_= page_soup.findAll("span",{"class":"information type"})[0].get_text()
    members = page_soup.findAll("div",{"class":"di-ib ml12 pl20 pt8"})[0].get_text().split(" ")[3]
    genre = [i.get_text() for i in page_soup.td.findAll("a",{"title":True}) if i.get_text() in genres]
    
    dic["scores"].append(score)
    dic["genres"].append(genre)
    dic["s_ranks"].append(rank)
    dic["p_rank"].append(pop)
    dic["studios"].append(studio)
    dic["types"].append(type_)
    dic["members"].append(members)
    
print("lengths")
print(len(dic["names"]))
print(len(dic["scores"]))
print(len(dic["s_ranks"]))
print(len(dic["p_rank"]))
print(len(dic["studios"]))
print(len(dic["episodes"]))
print(len(dic["aired"]))
print(len(dic["types"]))
print(len(dic["htmls"]))
print(len(dic["htmls_encoded"]))
print(len(dic["members"]))


df = pd.DataFrame(data=dic)
datatoexcel = pd.ExcelWriter("ANIMES.xlsx",engine = 'xlsxwriter')
df.to_excel(datatoexcel, sheet_name='Animes_Data')
datatoexcel.save()
print("done")