import json
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

class Timetable(App):
    def build(self):
        self.custom_timetable = self.load_timetable()
        self.layout = BoxLayout(orientation="vertical",padding=30,spacing=20)
        self.title_label = Label(text="My school Timetable",font_size=30)
        self.day_spinner = Spinner(text="Select Day",values=("mon","tue","wed","thu","fri","sat"),font_size=22,size_hint_y=None,size=(400,60))
        self.show_button = Button(text="SHOW TIMETABLE",font_size=22)
        self.show_button.bind(on_press=self.show_timetable)
        self.set_button = Button(text="SET / EDIT TIMETABLE",font_size=22)
        self.result = Label(text="Enter day and press SHOW TIMETABLE",font_size=20)
        self.scroll = ScrollView(size_hint=(1, None),size=(self.layout.width,300))
        self.set_button.bind(on_press=self.open_editor)
        self.set_button.bind(on_press=self.show_timetable)
        self.layout.add_widget(self.title_label)
        self.scroll.add_widget(self.result)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.day_spinner)
        self.layout.add_widget(self.show_button)
        self.layout.add_widget(self.set_button)
        return self.layout
    def show_timetable(self,instance):
        selected_day = self.day_spinner.text
        if selected_day == "Select Day":
            self.result.text = "Please select a day!"
            return
        timetable = self.custom_timetable[selected_day]
        text = f"{selected_day}\n\n"
        for number,subjects in enumerate(timetable,start=1):
            text += f"{number}. {subjects}\n"
        self.result.text = text
    def load_timetable(self):
        if os.path.exists("My_timetable.json"):
            try:
                with open("my_timetable.json","r",encoding="utf-8") as file:
                    data = json.load(file)
                    return data
            except Exception:
                pass
        return {
                "mon" : ["","","","","","","",""],
                "tue" : ["","","","","","","",""],
                "wed" : ["","","","","","","",""],
                "thu" : ["","","","","","","",""],
                "fri" : ["","","","","","","",""],
                "sat" : ["","","","","","","",""]
                }
    def open_editor(self,instance):
        selected_day = self.day_spinner.text
        if selected_day == "Selected Day":
            self.result.text = "Please select a day first"
            return
        editor = BoxLayout(orientation="vertical",spacing=10,padding=20)
        inputs = []
        for i in range(8):
            row = BoxLayout(spacing=10)
            label = Label(text=f"Period {i + 1}")
            box = TextInput(text=self.custom_timetable[selected_day][i],multiline=False)
            inputs.append(box)
            row.add_widget(label)
            row.add_widget(box)
            editor.add_widget(row)
        save_button = Button(text="SAVE",font_size=20,height=60)
        editor.add_widget(save_button)
        popup = Popup(title=f"Set {selected_day} Timetable",content=editor,size_hint=(0.9,0.9))
        def save(instance):
            self.custom_timetable[selected_day]=[box.text for box in inputs]
            with open("my_timetable.json","w",encoding="utf-8") as file:
                json.dump(self.custom_timetable,file,indent=4)
            popup.dismiss()
            self.result.text = (f"{selected_day} timetable saved!")
        save_button.bind(on_release=save)
        popup.open()
Timetable().run()