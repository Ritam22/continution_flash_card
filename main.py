from tkinter import *
import random
import mysql.connector
# import pandas
# from gtts import gTTS
import os
# from playsound import playsound

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data_dict = {}
data_tuple = ()
primary_key = 0
# SQL.

spanish_english_database = mysql.connector.connect(host="localhost",
                                                   user="root",
                                                   password="",
                                                   database=""
                                                   )

cursor = spanish_english_database.cursor(buffered=True)

# data = pandas.read_csv("data/EngSyn - Sheet1.csv")
# df = pandas.DataFrame(data, columns=["English", "Synonyms"])
# print(df)
# # cursor.execute('CREATE TABLE engsyn (id INT AUTO_INCREMENT PRIMARY KEY, English varchar(60), Synonyms varchar(255), FOREIGN KEY (id) REFERENCES espeng (id))')
# sql = "INSERT INTO engsyn (English, Synonyms) VALUES (%s,%s)"
# list_data = []
# for row in df.itertuples():
#     tuple_data = (row.English, row.Synonyms)
#     list_data.append(tuple_data)
# cursor.executemany(sql, list_data)
# spanish_english_database.commit()


# Data Cleaning
def purify(card):
    card_list = card.split(" ")
    guessed_number_could_be = card_list[0]
    guessed_number_could_be.encode('ascii', 'ignore')
    or_guessed_number_could_be = card_list[-1]
    or_guessed_number_could_be.encode('ascii', 'ignore')
    if "," in guessed_number_could_be:
        guessed_number_could_be = guessed_number_could_be.replace(",", "")
    elif ";" in guessed_number_could_be:
        guessed_number_could_be = guessed_number_could_be.replace(";", "")
    elif "," in or_guessed_number_could_be:
        or_guessed_number_could_be = or_guessed_number_could_be.replace(",", "")
    elif ";" in or_guessed_number_could_be:
        or_guessed_number_could_be = or_guessed_number_could_be.replace(";", "")
    else:
        pass
    try:
        number = int(guessed_number_could_be)
        word_list = [x for x in card_list if x != card_list[0]]
        word = " ".join(word_list)
    except ValueError:
        number = int(or_guessed_number_could_be)
        word_list = [x for x in card_list if x != card_list[-1]]
        word = " ".join(word_list)
    return number, word


# Functionality
# sql_yet_to_learn = "SELECT * from yet_to_learn"
# check = "SELECT * from yet_to_learn limit 1"
# results = cursor.execute(check)
# if results is None:
#     copy_to_yet_to_learn = "insert into yet_to_learn select * from spanishenglishoriginal"
#     cursor.execute(copy_to_yet_to_learn)
#     cursor.execute(sql_yet_to_learn)
#     data_tuple = cursor.fetchall()
# else:
#     cursor.execute(sql_yet_to_learn)
#     data_tuple = cursor.fetchall()

sql_esp_eng = "SELECT * from espeng"
cursor.execute(sql_esp_eng)
spanish_data_tuple = cursor.fetchall()

sql_eng_syn = "SELECT * from engsyn"
cursor.execute(sql_eng_syn)
english_data_tuple = cursor.fetchall()


def next_card():
    global current_card, flip_flash_card, primary_key
    window.after_cancel(flip_flash_card)
    current_card = random.choice(spanish_data_tuple)
    # print(current_card)
    spanish = purify(current_card[1])[1]
    frequency = purify(current_card[1])[0]
    primary_key = current_card[0]
    canvas.itemconfig(flash_card_title, text="Spanish", fill="black")
    # speech = gTTS(text=spanish, lang="es", slow=False)
    # speech.save("spanish.mp3")
    canvas.itemconfig(flash_card_word, text=spanish, fill="black")
    # playsound("spanish.mp3")
    # os.remove("spanish.mp3")
    canvas.itemconfig(word_frequency, text=f"Frequency = {frequency}", fill="black")
    canvas.itemconfig(flash_card_bg, image=card_front_img)
    flip_flash_card = flip_flash_card = window.after(4000, func=flip_card, )


def flip_card():
    global current_card, primary_key
    primary_key = int(primary_key)
    sql_primary_key = f"select * from engsyn where id= {primary_key}"
    # print(sql_primary_key)
    cursor.execute(sql_primary_key)
    current_card_eng = cursor.fetchall()
    # print(current_card_eng)
    english = purify(current_card_eng[0][1])[1]
    frequency = purify(current_card_eng[0][1])[0]
    syn = current_card_eng[0][2]
    canvas.itemconfig(flash_card_title, text="English", fill="white")
    canvas.itemconfig(canvas_synonyms, text=f"Synonyms: {syn}", fill="white")
    # speech = gTTS(text=english, lang="en", slow=False)
    # speech.save("english.mp3")
    canvas.itemconfig(flash_card_word, text=english, fill="white")
    # playsound("english.mp3")
    # os.remove("english.mp3")
    canvas.itemconfig(word_frequency, text=f"Frequency = {frequency}", fill="white")
    canvas.itemconfig(flash_card_bg, image=card_back_img)


# def words_already_learned():
#     sql_quary_delete = "DELETE FROM yet_to_learn WHERE Spanish = %s"
#     esp = (current_card[0],)
#     cursor.execute(sql_quary_delete, esp)
#     spanish_english_database.commit()
#     next_card()


# UI
window = Tk()
window.title("Flash Spanish")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_flash_card = window.after(4000, func=flip_card, )

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
flash_card_bg = canvas.create_image(400, 263, image=card_front_img)
flash_card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
flash_card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
word_frequency = canvas.create_text(630, 450, text="Frequency", font=("Ariel", 10))
canvas_synonyms = canvas.create_text(180, 350, text="", font=("Ariel", 10))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image)
cross_button.config(highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image)
check_button.config(highlightthickness=0, command=next_card)
check_button.grid(row=1, column=1)

next_card()

window.mainloop()
