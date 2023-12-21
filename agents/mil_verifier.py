import json
from tkinter import *


accepted_texts = set()
rejected_texts = set()
text = str()
main = None


def __process_texts(english_text: str, clif_text: str):
    global text
    text = english_text
    
    global main
    main = Tk()
    main.title(english_text)
    w = 1500
    h = 750
    ws = main.winfo_screenwidth()
    hs = main.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    main.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    clif_text_box = Text(main, height=5, width=52)
    clif_text_box.insert(chars=clif_text, index=INSERT)
    clif_text_box.pack(expand=True, fill=BOTH)
    
    accept_button = Button(main, text="Accept CLIF", command=__accept_button_action)
    reject_button = Button(main, text="Reject CLIF", command=__reject_button_action)
    accept_button.pack(side=LEFT)
    reject_button.pack(side=RIGHT)
    main.mainloop()


def __accept_button_action():
    accepted_texts.add(text)
    main.destroy()
    
    
def __reject_button_action():
    rejected_texts.add(text)
    main.destroy()


def semantically_verify_consistent_translations(
        clif_syntactically_verified_texts_file_path: str,
        tptp_consistent_texts_file_path: str,
        clif_semantically_accepted_texts_file_path: str,
        clif_semantically_rejected_texts_file_path: str):
    with open(file=clif_syntactically_verified_texts_file_path) as clif_syntactically_verified_texts_file:
        clif_syntactically_verified_texts = json.load(fp=clif_syntactically_verified_texts_file)
    with open(file=tptp_consistent_texts_file_path) as tptp_consistent_texts_file:
        tptp_consistent_texts = json.load(fp=tptp_consistent_texts_file)
        
    for english_text, clif_text in clif_syntactically_verified_texts.items():
        if english_text in tptp_consistent_texts:
            __process_texts(english_text=english_text, clif_text=clif_text)
    clif_semantically_accepted_texts = dict()
    for accepted_text in accepted_texts:
        clif_semantically_accepted_texts[accepted_text] = clif_syntactically_verified_texts[accepted_text]
    clif_semantically_rejected_texts = dict()
    for rejected_text in rejected_texts:
        clif_semantically_rejected_texts[rejected_text] = clif_syntactically_verified_texts[rejected_text]
        
    with open(file=clif_semantically_accepted_texts_file_path, mode='w') as clif_semantically_accepted_texts_file:
        json.dump(obj=clif_semantically_accepted_texts, fp=clif_semantically_accepted_texts_file, indent=4)
    with open(file=clif_semantically_rejected_texts_file_path, mode='w') as clif_semantically_rejected_texts_file:
        json.dump(obj=clif_semantically_rejected_texts, fp=clif_semantically_rejected_texts_file, indent=4)
            