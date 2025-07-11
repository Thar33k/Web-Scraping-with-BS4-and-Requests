from bs4 import BeautifulSoup
import requests
import pandas as pd

#END POINT
url = 'https://www.boxofficemojo.com/brand/?ref_=bo_nb_cso_tab'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#TABLE HEADERS
Total = soup.find(class_="a-color-state").text
Brand = soup.find('span',title="Brand").text
Releases = soup.find('a',title="Releases").text
Gross = soup.find('a',title="Lifetime Gross").text
Title = 'Movie Name'

#BRAND AND MOVIE NAMES DATA
datas = soup.find_all('a',class_="a-link-normal")[17:110]

#BRAND NAMES
indices_for_brand = list(range(0, len(datas), 2))
brand_names =[datas[index].text for index in indices_for_brand ]
del brand_names[-1] # remove empty string
print(brand_names)

#MOVIE NAMES
indices_for_data= list((range(0, len(datas),1)))
movie_names =[]
for x in indices_for_data:
    if x not in indices_for_brand:
        movie_names.append(datas[x].text)
print(movie_names)

#TOTAL GROSSINNG AND LIFETIME GROSSING
number_data_list = soup.find_all('td',class_="a-text-right")
number_data= [item.text for item in number_data_list]


compiled_list=[]
start =0
end = 3
count = 0
segmentd_list = []

def get_three_items(start: int, end: int, count: None):
    for x in range(start, end):
        try:
            segmentd_list.append(number_data[x])
        except IndexError:
            break
    compiled_list.append(segmentd_list)
    count +=1
    start = start+3
    end = end+3
    result =[start, end, count,segmentd_list]
    return result

result = get_three_items(start=start, end=end, count=count)
continue_loop = True

#LOOP
while continue_loop:
    segmentd_list = []
    count += 1
    start = start + 3
    end = end + 3
    result1 = get_three_items(start=start, end=end, count=count)
    if (count == 45):
        continue_loop = False

#MERGE DATA
raw_data = {

    'Brand':brand_names,
    'Movie_Released': movie_names,
    'Total_movie_released':[x[1] for x in compiled_list],
    'Total_Grossing_for_all_Movies':[x[0] for x in compiled_list],
    'LIfe_Time_Grossing_for_Movie':[x[2] for x in compiled_list]


}

df = pd.DataFrame(raw_data)

df.to_csv('Movies_raw_data.csv', index=False)
