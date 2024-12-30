from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
from kivy.utils import platform

################################ Écran d'accueil ##################################################
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text="iSport", font_size=32)
        layout.add_widget(title)

        btn_layout = GridLayout(cols=1, spacing=10, size_hint=(1, 0.6))

        btn_selection = Button(text="Multiscores", font_size=24)
        btn_selection.bind(on_release=self.go_to_selection)
        btn_layout.add_widget(btn_selection)

        btn_archives = Button(text="Archives", font_size=24)
        btn_archives.bind(on_release=self.go_to_archives)
        btn_layout.add_widget(btn_archives)

        btn_credits = Button(text="Crédits", font_size=24)
        btn_credits.bind(on_release=self.go_to_credits)
        btn_layout.add_widget(btn_credits)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def build(self):
        # Demander les permissions avant toute action
        self.ask_permissions()
        return Label(text="iSport")

    def ask_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

    def go_to_selection(self, instance):
        self.manager.current = 'selection'

    def go_to_archives(self, instance):
        self.manager.current = 'archives'

    def go_to_credits(self, instance):
        self.manager.current = 'credits'
