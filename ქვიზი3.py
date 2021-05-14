import requests
import json
import sqlite3

conn = sqlite3.connect('books.sqlite')
c = conn.execute("""CREATE TABLE IF NOT EXISTS book (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50),
                    type VARCHAR(10),
                    info_link VARCHAR(100))""")

key = '410346-ndim-7AYZMXFC'
payload = {'q': 'Book:Gone with the wind', 'k': key, 'info':1}
r = requests.get('https://tastedive.com/api/similar?', params=payload)
txt = r.json()
res = json.dumps(txt, indent=4)

with open('books.json', 'w') as f:
    json.dump(txt, f, indent=4)

lst = []
for each in txt['Similar']['Results']:
    name = each['Name']
    type = each['Type']
    info_link = each['wUrl']
    row = (name, type, info_link)
    lst.append(row)


print(r.status_code)
print(r.headers)
print(txt)
print(res)
# ბეჭდავს მოცემული წიგნის მოკლე შინაარსს
print(txt['Similar']['Info'][0]['wTeaser'])


"""ბაზაში ინახება ქარწაღებულნის მსგავსი ფილმების მონაცემები, კერძოდ სახელი, ტიპი ანუ წიგნი და წიკიპედდიის ლინკი სადაც შეგვიძლია ვნახოთ ინფორმაცია ამ წიგნზე"""
c.executemany("INSERT INTO book (name, type, info_link) VALUES (?, ?, ?)", lst)
conn.commit()
conn.close()




