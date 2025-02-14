from ttkbootstrap import Window, Frame, DateEntry, Label, Button, Entry, OUTLINE, INFO, DARK, StringVar
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from tkinter import PhotoImage
from ttkbootstrap.tooltip import ToolTip

global current_date

window = Window(title="Date Convertor", themename="darkly")

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

selected_date = JalaliDateTime.now()

miladi_label = Label(window, text="Miladi")
miladi_label.grid(row=0, column=0, pady=10, padx=10)

miladi_date_entry = DateEntry(window, dateformat="%Y-%m-%d")
miladi_date_entry.grid(row=1, rowspan=2, column=0, pady=(0, 10), padx=10, sticky="ew")


def miladi_to_jalali():
    miladi = miladi_date_entry.entry.get()
    year = int(miladi.split("-")[0])
    month = int(miladi.split("-")[1])
    day = int(miladi.split("-")[2])
    jalali = JalaliDate.to_jalali(year, month, day)

    jalali_date.set(jalali)


miladi_to_jalali_button = Button(window, text="Miladi to Jalali", command=miladi_to_jalali)
miladi_to_jalali_button.grid(row=1, column=1, pady=(0, 10), padx=10, sticky="ew")


def jalali_to_miladi():
    jalali = jalali_date.get()
    year = int(jalali.split("-")[0])
    month = int(jalali.split("-")[1])
    day = int(jalali.split("-")[2])
    jalali_date_object = JalaliDate(year, month, day)
    miladi = jalali_date_object.to_gregorian()

    miladi_date_entry.entry.delete(0, "end")
    miladi_date_entry.entry.insert(0, miladi)


jalali_to_miladi_button = Button(window, text="Jalali to Miladi", bootstyle=OUTLINE + INFO, command=jalali_to_miladi)
jalali_to_miladi_button.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="ew")

jalali_label = Label(window, text="Jalali")
jalali_label.grid(row=0, column=2, pady=10, padx=10)

jalali_date = StringVar()
jalali_entry = Entry(window, textvariable=jalali_date)
jalali_entry.grid(row=1, rowspan=2, column=2, pady=(0, 10), padx=(10, 0), sticky="ew")


def on_button_clicked():
    global current_date

    jalali = jalali_date.get()
    year = int(jalali.split("-")[0])
    month = int(jalali.split("-")[1])
    day = int(jalali.split("-")[2])
    current_date = JalaliDate(year, month, day)

    window = Window(title="Persian Calendar", resizable=(0, 0), themename="darkly")

    header_frame = Frame(window)
    header_frame.grid(row=0, column=0, columnspan=7)

    def select_date(day):
        global current_date
        selected_date = JalaliDate(current_date.year, current_date.month, day)
        window.destroy()
        jalali_date.set(selected_date)

    def update_calendar():
        global current_date
        year_month_label.config(text=JalaliDate(current_date).strftime("%B %Y", "fa"))

        days_frame = Frame(window, width=30)
        days_frame.grid(row=2, column=0, columnspan=7, rowspan=6, sticky="ns")

        days_in_month = current_date.days_in_month(current_date.month, current_date.year)
        first_day_of_month = JalaliDate(current_date.year, current_date.month, 1).weekday()

        days = [""] * first_day_of_month + [str(day) for day in range(1, days_in_month + 1)]
        for i, day in enumerate(days):
            if day:
                day_btn = Button(days_frame, text=day, width=4,
                                 command=lambda d=day: select_date(int(d)))
                day_btn.grid(row=1 + i // 7, column=i % 7, padx=2, pady=2)
                if day == str(current_date.day):
                    day_btn.configure(state="disabled")

    def previous_button_clicked():
        global current_date
        if current_date.month == 1:
            current_date = JalaliDate(current_date.year - 1, 12, 1)
        else:
            current_date = JalaliDate(current_date.year, current_date.month - 1, 1)
        update_calendar()

    previous_button = Button(header_frame, text="««", width=2, command=previous_button_clicked)
    previous_button.grid(row=0, column=0, sticky="ew")
    ToolTip(previous_button, text="previous", bootstyle=DARK)

    year_month_label = Label(header_frame, width=30, font=("calibri", 10, "bold"), anchor="center",
                             text=JalaliDate(current_date).strftime("%B %Y", "fa"))

    year_month_label.grid(row=0, column=1, sticky="ew")

    def next_button_clicked():
        global current_date
        if current_date.month == 12:
            current_date = JalaliDate(current_date.year + 1, 1, 1)
        else:
            current_date = JalaliDate(current_date.year, current_date.month + 1, 1)
        update_calendar()

    next_button = Button(header_frame, text="»»", width=2, command=next_button_clicked)
    next_button.grid(row=0, column=8, sticky="ew")
    ToolTip(next_button, text="next")

    weekdays_frame = Frame(window, width=30)
    weekdays_frame.grid(row=1, column=0, sticky="ew")

    weekdays = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
    for i, day in enumerate(weekdays):
        Label(weekdays_frame, text=day, width=4, font=("calibri", 10, "bold"), anchor="center").grid(row=0,
                                                                                                     column=i,
                                                                                                     padx=3,
                                                                                                     pady=3)
    update_calendar()
    window.mainloop()


jalali_icon = PhotoImage(file="icon.png")
jalali_button = Button(window, command=on_button_clicked)
jalali_button.grid(row=1, column=3, rowspan=2, pady=(0, 10), padx=(0, 20), sticky="e")
jalali_button.config(image=jalali_icon)

jalali_today = JalaliDate.today()
jalali_date.set(jalali_today)

window.mainloop()
