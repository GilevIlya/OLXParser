import requests
import os
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter as tk

class Getinf():
    def __init__(self, url, value=0):
        if not isinstance(url, str) or not isinstance(value, (int, float)):
            raise ValueError('url/value incorrect')
        self.__url = url
        self.__value = value
        self.__dictofadverts = {}
        html = requests.get(self.__url).text
        htmltext = BeautifulSoup(html, 'html.parser')
        addvertisment = htmltext.find_all('div', {'data-cy': "l-card"})
        category = htmltext.find('div', class_="css-1a9sj2a")
        if not len(addvertisment) > 0:
            raise ValueError('Nothing to add')
        for i in addvertisment:
            __advname = i.find('h4', class_="css-hzlye5")
            __advprice = i.find('p', {'data-testid': "ad-price"})
            __advprice = 0 if __advprice is None else __advprice.text
            if isinstance(__advprice, (int,float)):
                continue
            else:
                __advprice = int(''.join(x for x in __advprice if x.isdigit()))
            __advlink = i.find('a', class_="css-1tqlkj0")
            if __advlink and __advlink.get('href'):
                __advlink = "https://www.olx.ua" + __advlink['href']
            if __advprice <= value:
                self.__dictofadverts[__advname.text] = {}
                self.__dictofadverts[__advname.text]['Name'] = __advname.text
                self.__dictofadverts[__advname.text]['Price'] = str(__advprice)+' грн'
                self.__dictofadverts[__advname.text]['Link'] = __advlink
        with open(f'C:/Users/Ilya/Desktop/{category.text}.txt', 'w', encoding='utf-8') as x:
            count = 0
            for key, value in self.__dictofadverts.items():
                count += 1
                x.write(f"{count}"+":\n")
                x.write(f'Name: {value['Name']}\n')
                x.write(f"Price: {value['Price']}\n")
                x.write(f"Url: {value['Link']}\n")
                x.write("\n")
            
        os.startfile(f"C:/Users/Ilya/Desktop/{category.text}.txt")

import tkinter as tk

root = tk.Tk()
root.title("PythonParserOLX")
root.geometry("700x300")
root.configure(bg="grey")
left_block = tk.Frame(root, bg="white", width=220, height=200)
left_block.pack(side="left", padx=20, pady=40)
left_block.pack_propagate(False)
label_link = tk.Label(left_block, text="Ввести ссылку OLX раздела,\n БУ работает только с\n англ. раскладкой:", bg="white", font=10)
label_link.pack(pady=10)
entry_link = tk.Entry(left_block, width=20,)
entry_link.pack(pady=5)
def save_link():
    global saved_link
    saved_link = entry_link.get()
button_link = tk.Button(left_block, text="Сохранить ссылку", command=save_link, bg="gray", fg="white")
button_link.pack(pady=10)

right_block = tk.Frame(root, bg="white", width=220, height=200)
right_block.pack(side="right", padx=20, pady=40)
right_block.pack_propagate(False)
label_price = tk.Label(right_block, text="Ввести цену:\nРаботает только с целыми\n числами", bg="white", font=10)
label_price.pack(pady=10)
entry_price = tk.Entry(right_block, width=20)
entry_price.pack(pady=5)
def save_price():
    global saved_price
    saved_price = int(entry_price.get())
button_price = tk.Button(right_block, text="Сохранить макс. цену", command=save_price, bg="gray", fg="white")
button_price.pack(pady=10)
def start_parcing():
    url = saved_link
    value = saved_price
    parcingexamp = Getinf(url, value)
button_start = tk.Button(root, text='Start parsing olx',command = start_parcing, bg='white', width=800, height=2, font=16)
button_start.pack(side='bottom', padx=10, pady=10)
root.mainloop()