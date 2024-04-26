# This file is to be run once and produces all the files in data.
from bs4 import BeautifulSoup
import re
import urllib.request

# {'philosopher_name' : ['url1', 'url2', ...]}
urlsDict = {
            'nietzsche':['51356/pg51356-images.html', '19322/pg19322-images.html', '38145/pg38145-images.html', '52263/pg52263-images.html'],
            'confucius':['4094/pg4094-images.html', '3100/pg3100-images.html', '24055/pg24055-images.html', '3330/pg3330-images.html'],
            'kant':['52821/pg52821-images.html', '48433/pg48433-images.html', '4280/pg4280-images.html', '50922/pg50922-images.html'],
            'laozi':['49965/pg49965-images.html', '216/pg216-images.html'],
            'sunzi':['17405/pg17405-images.html', '66706/pg66706-images.html', '44024/pg44024-images.html'],
            'plato':['1497/pg1497-images.html', '1636/pg1636-images.html', '1600/pg1600-images.html', '1656/pg1656-images.html', '1672/pg1672-images.html', '1572/pg1572-images.html']
            }

for philosopher, urls in urlsDict.items():
    for url in urls:
        with urllib.request.urlopen('https://www.gutenberg.org/cache/epub/'+url) as request:
            contents = request.read()

        html_string = contents.decode()
        file_name = url.replace('/','').replace('-images','')

        with open('data/'+philosopher+'/'+file_name, 'w', encoding='utf8') as file:
            file.write(html_string)

for philosopher, urls in urlsDict.items():
    total_text = ""
    for url in urls:
        file_name = url.replace('/','').replace('-images','')
        with open('data/'+philosopher+'/'+file_name, 'r', encoding='utf8') as file:
            html = file.read()
            soup = BeautifulSoup(html, 'lxml')

        text = soup.getText()
        text = text[text.find("*** START OF THE PROJECT GUTENBERG EBOOK"):text.find("*** END OF THE PROJECT GUTENBERG")]
        text = text.replace("*** START OF THE PROJECT GUTENBERG EBOOK ", "")
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        total_text += text

    with open('data/'+philosopher+'/'+philosopher+'.txt', 'w', encoding='utf8') as file:
        file.write(total_text)