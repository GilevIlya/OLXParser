import requests
import os
from bs4 import BeautifulSoup
import tkinter as tk
class GetInf():
    def __init__(self, url, value=0):
        if not isinstance(url, str) or not isinstance(value, (int, float)):
            raise ValueError('url/value incorrect')
        self.__url = url
        self.__value = value
        self.__dictofadverts = {}
        self.__get_txt_from_olx(self.__value)

    def __get_txt_from_olx(self, __value):
        __html = requests.get(self.__url).text
        __html_text = BeautifulSoup(__html, 'html.parser')
        __addvertisment = __html_text.find_all('div', {'data-cy': "l-card"})
        __category = __html_text.find('div', class_="css-1a9sj2a")
        self.__verify_inf(__addvertisment, __category, __value)

    def __verify_inf(self, __addvertisment, __category, __value):
        if len(__addvertisment) <= 0:
            raise ValueError('Nothing to add')
        for i in __addvertisment:
            __adv_name = i.find('h4', class_="css-hzlye5")
            __adv_price = i.find('p', {'data-testid': "ad-price"})
            __adv_price = 0 if __adv_price is None else __adv_price.text
            __adv_link = i.find('a', class_="css-1tqlkj0")
            self.__checkout_price_and_link(__adv_link,__adv_price,__adv_name, __value)
        self.__create_txt_file(__category)
        
    def __checkout_price_and_link(self, __adv_link,__adv_price, __adv_name, __value):
            if not isinstance(__adv_price, (int, float)):
                __adv_price = int(''.join(x for x in __adv_price if x.isdigit())) 
            else:
                pass
            if __adv_link and __adv_link.get('href'):
                __adv_link = "https://www.olx.ua" + __adv_link['href']
            if __adv_price <= __value:
                self.__dict_fillinig(__adv_link, __adv_name, __adv_price)
    
    def __dict_fillinig(self, __adv_link, __adv_name, __adv_price):
            __dictkeyname = __adv_name.text if __adv_name.text not in self.__dictofadverts else __adv_link
            self.__dictofadverts[__dictkeyname] = {}
            self.__dictofadverts[__dictkeyname]['Name'] = __adv_name.text
            self.__dictofadverts[__dictkeyname]['Price'] = str(__adv_price)+' грн.' if __adv_price != 0 else 'Договірна'
            self.__dictofadverts[__dictkeyname]['Link'] = __adv_link
    
    def __create_txt_file(self, __category):
        with open(f'C:/Users/Ilya/Desktop/{__category.text}.txt', 'w', encoding='utf-8') as x:
            count = 0
            for key, value in self.__dictofadverts.items():
                count += 1
                x.write(f"{count}"+":\n")
                x.write(f'Name: {value['Name']}\n')
                x.write(f"Price: {value['Price']}\n")
                x.write(f"Url: {value['Link']}\n")
                x.write("\n")    
        os.startfile(f"C:/Users/Ilya/Desktop/{__category.text}.txt")

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
    parcingexamp = GetInf(url, value)
button_start = tk.Button(root, text='Start parsing olx',command = start_parcing, bg='white', width=800, height=2, font=16)
button_start.pack(side='bottom', padx=10, pady=10)
root.mainloop()