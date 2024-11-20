import requests
import json
from tkinter import*
from tkinter import messagebox as mb
from tkinter import ttk


def update_b_label(event): #функция для обновления метки (которая отображает полную информацию по названию валюты)
    code = b_combobox.get()#код получим из комбобокса
    name= cur[code] #имя валюты получим из списка cur
    b_label.config(text=name)


def update_t_label(event): #функция для обновления метки (которая отображает полную информацию по названию валюты)
    code = t_combobox.get()#код получим из комбобокса
    name= cur[code] #имя валюты получим из списка cur
    t_label.config(text=name)


def exchange():
    t_code=t_combobox.get() # код валюты получаем из поля ввода информации
    b_code=b_combobox.get()

    if t_code and b_code: #делаем проверку, если код введен, то работаем и делаем обработку исключений
        try:
            response=requests.get(f"https://open.er-api.com/v6/latest/{b_code}")# ответ получим из вопроса с сайта
            response.raise_for_status() #проверяем на ошибки, если ответ 200, то все хорошо, если нет отрабатываем исключения
            data=response.json() #ответ от json
            if t_code in data["rates"]: #если внутри rates есть код валют, то можно обрабатывать
                exchange_rate=data["rates"][t_code]# курс обмена из словаря (date rates) выбираем значение по ключу
                t_name=cur[t_code]
                b_name=cur[b_code]
                mb.showinfo("курс обмена", f"курс: {exchange_rate:.2f}{t_name} за 1 {b_name}")# выводим окно. .2f означает количество символов после запятой, чтобы отражались лишь сотые (f-это формат)
            else:
                mb.showerror("ошибка", f"валюта {t_code} не найдена")
        except Exception as e: # обрабатываем исключения
            mb.showerror("ошибка", f"произошла ошибка: {e}")
    else: # если поле ввода пустое
        mb.showwarning("внимание",f"введите код валюты")


cur = {
    "RUB": "российский рубль",
    "EUR": "евро",
    "GBP": "британский фунт стерлингов",
    "JPY": "японская йена",
    "CNY": "китайский юань",
    "KZT": "казахский тенге",
    "UZS": "узбекский сум",
    "CHF": "швейцарский франк",
    "AED": "дирхам ОАЭ",
    "CAD": "канадский доллар",
    "USD": "Американский доллар"
} # скобки фигурные, т.к. теперь будет списком отображаться


window=Tk()
window.title("курс обмена валют")
window.geometry("360x300")

Label(text="базовая валюта").pack(padx=10, pady=10)
b_combobox=ttk.Combobox(values=list(cur.keys()))
b_combobox.pack(padx=10, pady=10)
b_combobox.bind("<<comboboxSelected>>", update_b_label)

b_label=ttk.Label()#метка для отображения полной информации по названию валюты
b_label.pack(padx=10, pady=10)

Label(text="целевая валюта").pack(padx=10, pady=10)
t_combobox=ttk.Combobox(values=list(cur.keys())) # присваиваем комбобоксу значение cur(список), а чтобы из списка сделать словарь присваеваем значение list
t_combobox.pack(padx=10, pady=10)
t_combobox.bind("<<comboboxSelected>>", update_t_label)

t_label=ttk.Label()#метка для отображения полной информации по названию валюты
t_label.pack(padx=10, pady=10)

Button(text="получить курс обмена",command=exchange).pack(padx=10, pady=10)# кнопка с функцией обмена

window.mainloop()
