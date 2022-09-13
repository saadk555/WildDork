import requests,lxml
from bs4 import BeautifulSoup
import re
import pandas
import os

head = "Add User agent here if you'd like, and then add it with header on line 32"


query = input('Enter Your query :\n')
search = query.replace(' ', '+')
results = int(input('Enter the number of results: '))
results += 1
url = (f"https://www.google.com/search?q=" + str(search) + f"&num={results}")

a = []
b = []
dp = []

requests_results = requests.get(url, headers={'Cache-Control': 'no-cache'})
soup = BeautifulSoup(requests_results.content, "lxml")
links = soup.find_all("a")
soup2 = soup.select(".s3v9rd.AP7Wnd")

for i in soup2:
    if len(str(i)) >= 143 and not "href" in str(i):
        dp.append(str(i.getText))
    else:
        pass


for i in links:
    link = i.get('href')
    if "url?q=" in link:
        t = i.find_all('h3')
        if len(t) > 0:
            a.append(link.split("?q=")[1].split("&sa=U")[0])
            b.append(t[0].getText())


 
words = int(input('How many words do you want to find from the title?\n'))
char = ''
for num in range(words):
    char += input('Enter the initial characters:\nNOTE:Please add uppercase and lowercase letters seperately\n')

c = []
c2 = []

for i in b:
     c.append(re.findall(fr'\b[{char}]\w+', i))

for i in dp:
     c2.append(re.findall(fr'\b[{char}]\w+', i))

st2 = []
st = []

for e in c:
    st.append(str(e))

for e in c2:
    st2.append(str(e))

d = dict(zip(a, st))

pd = pandas

df = pd.DataFrame(list(d.items()),columns=['Links','Words found from Title'])
df2 = pd.DataFrame({'Words found from Description':st2})

dff = df.join(df2)

print(dff)

increment = 0
filename = "result{}.csv"
while os.path.isfile(filename.format(increment)):
    increment += 1
filename = filename.format(increment)

dff.to_csv(filename)
os.system(filename)

          