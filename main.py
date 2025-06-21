import tkinter as tk
from tkinter import IntVar
import requests
from PIL import Image, ImageTk


from io import BytesIO

# Initialize root window
root = tk.Tk()
root.title("Weather Forecast")
root.geometry("400x400")
root.resizable(0, 0)

# Colors and fonts
sky_color = "#76c3ef"
grass_color = "#aad207"
output_color = "#dcf0fb"
input_color = "#ecf2ae"
large_font = ('SimSun', 14)
small_font = ('SimSun', 11)

def get_weather():
    city_name = response['name']
    city_lat = str(response['coord']['lat'])
    city_lon = str(response['coord']['lon'])

    main_weather = response['weather'][0]['main']
    desc = response['weather'][0]['description']

    temp = str(response['main']['temp'])
    feels_like = str(response['main']['feels_like'])
    temp_min = str(response['main']['temp_min'])
    temp_max = str(response['main']['temp_max'])
    humidity = str(response['main']['humidity'])

    # Update output labels
    city_l.config(text=f"{city_name} ({city_lat}, {city_lon})", font=large_font, bg=output_color)
    weather_l.config(text=f"Weather: {main_weather}, {desc}", font=small_font, bg=output_color)
    temp_l.config(text=f"Temperature: {temp} °C", font=small_font, bg=output_color)
    feels_l.config(text=f"Feels Like: {feels_like} °C", font=small_font, bg=output_color)
    tempmax_l.config(text=f"Temp Max: {temp_max} °C", font=small_font, bg=output_color)
    tempmin_l.config(text=f"Temp Min: {temp_min} °C", font=small_font, bg=output_color)
    humidity_l.config(text=f"Humidity: {humidity}%", font=small_font, bg=output_color)

def search():
    global response
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = '5713131624d4c551043718f4793607b7'

    if search_method.get() == 1:
        query = {'q': city_entry.get(), 'appid': api_key, 'units': 'metric'}
    elif search_method.get() == 2:
        query = {'zip': city_entry.get(), 'appid': api_key, 'units': 'metric'}
    else:
        return

    res = requests.get(url, params=query)
    response = res.json()

    # Debug print to see what the API returned
    print(response)

    if res.status_code == 200:
        get_weather()
        get_icon()
    else:
        # Handle errors
        city_l.config(text=f"Error: {response.get('message', 'Unknown error')}", font=large_font, bg=output_color)
        weather_l.config(text="", bg=output_color)
        temp_l.config(text="", bg=output_color)
        feels_l.config(text="", bg=output_color)
        tempmax_l.config(text="", bg=output_color)
        tempmin_l.config(text="", bg=output_color)
        humidity_l.config(text="", bg=output_color)
        photolabel_l.config(image="")


def get_icon():
    global img
    icon_id = response['weather'][0]['icon']
    url = f'https://openweathermap.org/img/wn/{icon_id}@2x.png'
    icon_response = requests.get(url, stream=True)
    img_data = icon_response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    photolabel_l.config(image=img)

# Frames
sky_frame = tk.Frame(root, bg=sky_color, height=230)
sky_frame.pack(fill="both", expand=True)

grass_frame = tk.Frame(root, bg=grass_color)
grass_frame.pack(fill="both", expand=True)

output_frame = tk.LabelFrame(sky_frame, bg=output_color, height=225, width=325)
output_frame.pack(pady=30)
output_frame.pack_propagate(0)

input_frame = tk.LabelFrame(grass_frame, bg=input_color, width=325)
input_frame.pack(pady=15)
input_frame.pack_propagate(0)

# Output Widgets
city_l = tk.Label(output_frame, bg=output_color)
weather_l = tk.Label(output_frame, bg=output_color)
temp_l = tk.Label(output_frame, bg=output_color)
feels_l = tk.Label(output_frame, bg=output_color)
tempmax_l = tk.Label(output_frame, bg=output_color)
tempmin_l = tk.Label(output_frame, bg=output_color)
humidity_l = tk.Label(output_frame, bg=output_color)
photolabel_l = tk.Label(output_frame, bg=output_color)

city_l.pack()
weather_l.pack()
temp_l.pack()
feels_l.pack()
tempmax_l.pack()
tempmin_l.pack()
humidity_l.pack()
photolabel_l.pack()

# Input Widgets
city_entry = tk.Entry(input_frame, width=25, font=small_font)
city_entry.grid(row=0, column=0, padx=10, pady=10)

submit_but = tk.Button(input_frame, font=large_font, text='Submit', command=search)
submit_but.grid(row=0, column=1, padx=2, pady=10)

search_method = IntVar()
search_method.set(1)

r1 = tk.Radiobutton(input_frame, font=small_font, text='Search by city name', variable=search_method, value=1)
r2 = tk.Radiobutton(input_frame, font=small_font, text='Search by zipcode', variable=search_method, value=2)

r1.grid(row=1, column=0, padx=5, pady=(2, 10))
r2.grid(row=1, column=1, padx=0, pady=(2, 10))

# Run app
root.mainloop()
