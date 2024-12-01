from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

################################ Écran d'accueil ##################################################
class SelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Layout pour le bouton de retour
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0))

        # Ajoutez le bouton de retour qui reste fixe en haut
        self.back_button = Button(text='Retour', size_hint=(0.6, 1), height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        layout.add_widget(top_layout)

        title = Label(text="Selection du sport à analyser", font_size=32)
        layout.add_widget(title)


        btn_layout = GridLayout(cols=1, spacing=10, size_hint=(1, 0.6))

        btn_basket = Button(text="Basket", font_size=24)
        btn_basket.bind(on_release=self.go_to_basket)
        btn_layout.add_widget(btn_basket)

        btn_futsal = Button(text="Futsal", font_size=24)
        btn_futsal.bind(on_release=self.go_to_futsal)
        btn_layout.add_widget(btn_futsal)

        btn_vs = Button(text="1 vs 1", font_size=24)
        btn_vs.bind(on_release=self.go_to_vs)
        btn_layout.add_widget(btn_vs)

        btn_features = Button(text="Personnalisé", font_size=24)
        btn_features.bind(on_release=self.go_to_features)
        btn_layout.add_widget(btn_features)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

    def go_to_basket(self, instance):
        self.manager.current = 'basket'

    def go_to_futsal(self, instance):
        self.manager.current = 'futsal'

    def go_to_vs(self, instance):
        self.manager.current = 'vs'

    def go_to_features(self, instance):
        self.manager.current = 'features'