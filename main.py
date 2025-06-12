from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
import os

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        self.inner = GridLayout(cols=1, size_hint_y=None, padding=30)
        self.inner.bind(minimum_height=self.inner.setter('height'))

        self.label = Label(
            text="Tap the button for a quote",
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            text_size=(700, None),
        )
        self.label.bind(texture_size=self.label.setter('size'))
        self.inner.add_widget(self.label)

        scroll = ScrollView(do_scroll_y=True, do_scroll_x=False, size_hint=(1, 0.6))
        scroll.add_widget(self.inner)

        quote_btn = Button(text="Get Quote", size_hint=(1, 0.13))
        quote_btn.bind(on_press=self.get_quote)

        save_btn = Button(text="Save to Favorites", size_hint=(1, 0.13))
        save_btn.bind(on_press=self.save_quote)

        view_btn = Button(text="View Favorites", size_hint=(1, 0.14))
        view_btn.bind(on_press=self.view_favorites)

        layout.add_widget(scroll)
        layout.add_widget(quote_btn)
        layout.add_widget(save_btn)
        layout.add_widget(view_btn)

        self.add_widget(layout)
        self.current_quote = ""

    def get_quote(self, instance):
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=5, verify=False)
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            self.current_quote = f'"{quote}"\n\n— {author}'
            self.label.text = self.current_quote
        except:
            self.label.text = "Error fetching quote."
            self.current_quote = ""

    def save_quote(self, instance):
        try:
            if self.current_quote:
                with open("/storage/emulated/0/Download/FavoriteQuotes.txt", "a") as file:
                    file.write(self.current_quote + "\n\n")
                self.label.text = "💾 Quote saved!"
            else:
                self.label.text = "No quote to save."
        except:
            self.label.text = "❌ Save failed."

    def view_favorites(self, instance):
        self.manager.current = "favorites"


class FavoritesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.quote_area = Label(
            text="Loading...",
            font_size='18sp',
            halign='center',
            valign='top',
            size_hint_y=None,
            text_size=(700, None)
        )
        self.quote_area.bind(texture_size=self.quote_area.setter('size'))

        scroll = ScrollView(do_scroll_y=True)
        scroll.add_widget(self.quote_area)

        back_btn = Button(text="← Back", size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(scroll)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_pre_enter(self):
        try:
            path = "/storage/emulated/0/Download/FavoriteQuotes.txt"
            if os.path.exists(path):
                with open(path, "r") as file:
                    content = file.read().strip()
                    self.quote_area.text = content if content else "No saved quotes yet."
            else:
                self.quote_area.text = "No favorites.txt file found."
        except:
            self.quote_area.text = "Error reading favorites."

    def go_back(self, instance):
        self.manager.current = "main"


class QuoteApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(FavoritesScreen(name="favorites"))
        return sm

QuoteApp().run()
