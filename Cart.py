from tkinter import *

def cart(product_list):
    windows = Tk()
    windows.wm_title("Your Cart")
    windows.geometry("500x350")

    products = Label(windows, text="Your products here").place(x=0, y=0)
    product_name = Label(windows, text="Product Name").place(x=0,  y=20)
    quantity = Label(windows, text="Quantity").place(x=200, y=20)
    prices = {'beer':2, "soda":2 , "coca":1, "coffee":2}

    unique_item = set(product_list)
    total_price = 0
    for index, value in enumerate(unique_item):
        item_name = Label(windows, text=value).place(x=0, y=55 + (index * 35))
        num_of_item_name = product_list.count(value)
        item_quantity = Entry(windows)
        item_quantity.place(x=200, y=55 + (index * 35))
        item_quantity.insert(END, num_of_item_name)
        total_price += prices[value] * num_of_item_name

    total_label = Label(windows, text='Total Price: $').place(x=400, y=20)
    total_money = Label(windows, text=total_price).place(x=480, y=20)
    windows.mainloop()