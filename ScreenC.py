from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


################################ Écran des crédits ################################################
class CreditsScreen(Screen):
    def __init__(self, **kwargs):
        super(CreditsScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Layout pour le bouton de retour
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Ajoutez le bouton de retour qui reste fixe en haut
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        main_layout.add_widget(top_layout)

        # Créer un label pour le titre
        title_label = Label(text="Crédits", font_size=28, size_hint_y=None, height=40)
        main_layout.add_widget(title_label)

        # Créer le message des crédits
        credits_message = (
            "Développé par : \n Wassim BAHMANI \n El-Yamin ATTOUMANI \n Moussa DIARRASSOUBA \n Yanis GHAZI \n"
            "Élèves FISE 2027 de l'IMT Nord Europe\n\n"
            "Application développée dans le cadre du projet ouvert EPS'Innov\n\n"
            "Merci d'avoir utilisé notre application !"
        )

        # Créer un label pour le message des crédits et configurez-le pour le défilement
        credits_label = Label(
            text=credits_message,
            font_size=18,
            size_hint_y=None,
            text_size=(Window.width - 40, None),  # La largeur de texte est la largeur de la fenêtre moins les marges
            halign='center',
            valign='top'
        )
        credits_label.bind(texture_size=self._update_text_size)

        # Créer un ScrollView pour le label des crédits
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(credits_label)

        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'home'

    def _update_text_size(self, instance, value):
        instance.size = instance.texture_size
        instance.height = instance.texture_size[1]
        instance.text_size = (instance.width, None)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager


    class MyApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(CreditsScreen(name='credits'))
            return sm


    MyApp().run()
