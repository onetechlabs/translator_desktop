try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
from functools import partial
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import requests
from PIL import ImageTk, Image

root = tk.Tk()

langs = tk.StringVar(root)
lang2s = tk.StringVar(root)
langchoices=[]
langValChoices=[]
orLangValue=""
toLangValue=""
TextOrLang = tk.Text()
TextTdLang = tk.Text()
TextResult = ""

    
def main():
    app = MainFrame(root)
    app.mainloop()

class MainFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.master.title("Translator")
        self.master.resizable(0,0)
        self.master.geometry("420x500")
        self.master['bg']='#7979d2'
        self.setup_icon()
        self.formPenerjemah()
    
    def formPenerjemah(self):
        tk.Label(root,text ="Origin Language",bg="#7979d2",font=(None, 12)).grid(sticky='w', row = 0,column = 0,padx = (10,0),pady = (10,5))
        tk.Label(root,text ="To Language",bg="#7979d2",font=(None, 12)).grid(sticky='e', row = 0,column = 1,padx = (30,0),pady = (10,5))
        
        r = requests.post('http://localhost:8000/dropdown-language-lists', json={})
        rj = r.json()
        for i in rj['data']['records']:
            langchoices.append( i['language_name'] )
            langValChoices.append( i['id'] )
        
        langs.set(langchoices[0])
        orLangs = tk.OptionMenu(root, langs, *langchoices)
        orLangs['bg']='#7979d2'
        orLangs.config(width=20)
        orLangs.grid(row = 1,column = 0,padx = (10,0),pady = (10,5))
        lang2s.set(langchoices[int(rj['data']['total_data'])-1])
        toLangs = tk.OptionMenu(root, lang2s, *langchoices)
        toLangs.config(width=20)
        toLangs['bg']='#7979d2'
        toLangs.grid(row = 1,column = 1,padx = (10,0),pady = (10,5))
        tk.Label(root,bg="#7979d2",text ="Text to Translate",font=(None, 12)).grid(sticky='w', row = 2,column = 0,padx = (10,0),pady = (10,5))
        TextOrLang.config(width=27, height=20,highlightbackground = "grey", highlightcolor= "grey",highlightthickness=1)
        TextOrLang.grid(sticky='w', row = 3,column = 0,padx = (10,0),pady = (10,5))
        tk.Label(root,bg="#7979d2",text ="Translated Text",font=(None, 12)).grid(sticky='e', row = 2,column = 1,padx = (10,0),pady = (10,5))
        
        TextTdLang.config(width=27, height=20,highlightbackground = "grey", highlightcolor= "grey",highlightthickness=1)
        TextTdLang.grid(sticky='w', row = 3,column = 1,padx = (10,0),pady = (10,5))
        submitT = tk.Button(root,highlightbackground = "#7979d2", highlightcolor= "grey", text="Translate It !", command=Action.do_translate)
        submitT.config(width=15)
        submitT.grid(column=0,row=4, padx = (0,0),pady = (5,5), columnspan=2)

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "logo.png")
        if os.path.exists(icon_path):
            icon = ImageTk.PhotoImage(Image.open(icon_path))
            root.iconphoto(False, icon)
class Action():
    def do_translate():
        textT=str(TextOrLang.get("1.0",END)).replace("\n","")
        print(textT)
        readFinalData = requests.post('http://localhost:8000/translate', json={
            "lang_id_origin":str(langValChoices[langchoices.index(langs.get())]),
            "lang_id_translated":str(langValChoices[langchoices.index(lang2s.get())]),
            "text": textT
        })
        readFinalDataJson = readFinalData.json()
        print(readFinalDataJson)
        
        TextTdLang.delete(1.0, END)
        TextTdLang.insert(END, readFinalDataJson["data"]["text_before_after"])

if __name__ == '__main__':
    main()