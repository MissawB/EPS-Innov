from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.metrics import sp,dp
from kivy.utils import get_color_from_hex
import random
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color as KivyColor, Rectangle as KivyRectangle
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle, RoundedRectangle
from functools import partial
from kivy.properties import NumericProperty, StringProperty
import time

# Gestionnaire d'écrans
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(HomeScreen(name='home'))
        self.add_widget(SelectionScreen(name='selection'))
        self.add_widget(CreditsScreen(name='credits'))
        self.add_widget(DuelScreen(name='vs'))
        self.add_widget(FeaturesScreen(name='features'))
        self.add_widget(ArchivesScreen(name='archives'))

# Écran d'accueil
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Ajouter le titre en haut
        title = Label(text="iSport", font_size=sp(Window.width * 0.06),size_hint=(1, 0.7), height=Window.height * 0.1)
        layout.add_widget(title)


        btn_layout = GridLayout(cols=1, spacing=10,size_hint=(1, 0.3))

        btn_selection = Button(text="Multiscores", size_hint=(1, None), height=Window.height * 0.1, font_size=sp(Window.width * 0.03))
        btn_selection.bind(on_release=self.go_to_selection)
        btn_layout.add_widget(btn_selection)

        btn_archives = Button(text="Archives", size_hint=(1, None), height=Window.height * 0.1, font_size=sp(Window.width * 0.03))
        btn_archives.bind(on_release=self.go_to_archives)
        btn_layout.add_widget(btn_archives)

        btn_credits = Button(text="Crédits", size_hint=(1, None), height=Window.height * 0.1, font_size=sp(Window.width * 0.03))
        btn_credits.bind(on_release=self.go_to_credits)
        btn_layout.add_widget(btn_credits)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def go_to_selection(self, instance):
        self.manager.current = 'selection'

    def go_to_archives(self, instance):
        self.manager.current = 'archives'

    def go_to_credits(self, instance):
        self.manager.current = 'credits'

# Écran de sélection
class SelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Layout pour le bouton de retour
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=Window.height * 0.08, padding=(10, 0))

        # Ajoutez le bouton de retour qui reste fixe en haut
        self.back_button = Button(text='Retour', size_hint=(0.6, 1),height=Window.height * 0.05,font_size=sp(Window.width * 0.03))
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        layout.add_widget(top_layout)

        title = Label(text="Choix du mode", font_size=sp(Window.width * 0.04))
        layout.add_widget(title)


        btn_layout = GridLayout(cols=1, spacing=10, size_hint=(1, 0.6))

        btn_vs = Button(text="1 vs 1", font_size=sp(Window.width * 0.03))
        btn_vs.bind(on_release=self.go_to_vs)
        btn_layout.add_widget(btn_vs)

        btn_features = Button(text="Personnalisé", font_size=sp(Window.width * 0.03))
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

# Écran de crédits
class CreditsScreen(Screen):
    def __init__(self, **kwargs):
        super(CreditsScreen, self).__init__(**kwargs)

        # S'assurer que la disposition occupe tout l'écran
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))

        # Layout pour le bouton de retour
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=Window.height * 0.08)

        # Ajouter le bouton de retour avec une taille plus grande
        self.back_button = Button(text='Retour', size_hint=(1, 1), font_size=sp(Window.width * 0.03))
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        main_layout.add_widget(top_layout)

        # Créer un label pour le titre
        title_label = Label(text="Crédits", font_size=sp(Window.width * 0.04), size_hint_y=None, height=Window.height * 0.1)
        main_layout.add_widget(title_label)

        # Créer le message des crédits
        credits_message = (
            "Développé par : \n Wassim BAHMANI \n El-Yamin ATTOUMANI \n Moussa DIARRASSOUBA \n Yanis GHAZI \n Mathilde BARBE \n"
            "Élèves FISE 2027 de l'IMT Nord Europe\n\n"
            "Application développée dans le cadre du projet ouvert EPS'Innov\n\n"
            "Merci d'avoir utilisé notre application !"
        )

        # Créer un label pour le message des crédits et configurez-le pour le défilement
        credits_label = Label(
            text=credits_message,
            font_size=sp(Window.width *0.02),
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

# Écran de 1 vs 1
class DuelScreen(Screen):
    def __init__(self, **kwargs):
        super(DuelScreen, self).__init__(**kwargs)

        # Initialisation des données des joueurs
        self.players_data = {
            'Joueur 1': {'observables': {}, 'num_observables': 3},
            'Joueur 2': {'observables': {}, 'num_observables': 3}
        }

        self.player_name_widgets = {}  # Pour stocker les TextInput des sections des joueurs
        self.observable_widgets = {}  # Pour stocker les widgets liés aux scores des variables

        self.timer_event = None
        self.start_time = 0
        self.chrono_duration = 0  # Durée du chrono en secondes
        self.is_timer_mode = True  # Variable pour suivre le mode actuel (Timer/Chrono)
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        # Layout principal avec gestion d'espace améliorée
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(2),  # Réduction espacement
            padding=dp(2),  # Réduction marge
            size_hint=(1, 1))  # Remplissage complet

        # Layout supérieur compact
        top_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),  # Hauteur réduite
            padding=dp(0),
            spacing=dp(2))  # Espacement réduit

        self.back_button = Button(
            text='Retour',
            size_hint_x=0.2,
            height=dp(60),
            font_size=dp(18))
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        self.timer_label = Label(
            text="Timer: 00:00",
            font_size=dp(28),
            halign='center',
            size_hint=(0.6, 1))
        top_layout.add_widget(self.timer_label)

        self.mode_button = Button(
            text="Chrono",
            size_hint=(0.2, 1),
            font_size=dp(18))
        self.mode_button.bind(on_release=self.switch_mode)
        top_layout.add_widget(self.mode_button)

        main_layout.add_widget(top_layout)

        # Layout des joueurs
        self.players_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            padding=dp(10),
            size_hint=(1, 0.8))

        for player, color in zip(self.players_data.keys(), [(0.8, 0.3, 0.3, 1), (0.3, 0.3, 0.8, 1)]):
            player_layout = self.create_player_section(player, color)
            self.players_layout.add_widget(player_layout)

        main_layout.add_widget(self.players_layout)

        # Layout des boutons (démarrer le timer, archiver les données)
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            padding=dp(5),
            size_hint_y=None,
            height=dp(70))

        self.start_timer_button = Button(
            text="Démarrer",
            size_hint=(0.3, 1),
            font_size=dp(18))
        self.start_timer_button.bind(on_release=self.start_timer)
        buttons_layout.add_widget(self.start_timer_button)

        reset_scores_button = Button(
            text="Réinitialiser",
            size_hint=(0.3, 1),
            font_size=dp(18))
        reset_scores_button.bind(on_release=lambda instance: self.show_reset_scores_popup())
        buttons_layout.add_widget(reset_scores_button)

        main_layout.add_widget(buttons_layout)
        self.add_widget(main_layout)

    def on_enter(self):
        """ S'exécute lorsque l'utilisateur entre sur l'écran """
        self.show_player_setup_popup()

    def show_player_setup_popup(self):
        """Popup de configuration des joueurs - Version corrigée"""
        popup_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint=(1, 1))

        # En-tête
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=dp(10))

        title = Label(
            text="[b]MODIFICATION DES JOUEURS[/b]",
            markup=True,
            font_size=dp(24),
            halign='center')

        header.add_widget(title)
        popup_layout.add_widget(header)

        # Contenu défilant
        scroll_content = ScrollView(
            bar_width=dp(12),
            bar_inactive_color=[0.5, 0.5, 0.5, 0.5],
            size_hint=(1, 1))

        form_layout = GridLayout(
            cols=1,
            spacing=dp(20),
            size_hint_y=None,
            padding=(dp(10), dp(20)))
        form_layout.bind(minimum_height=form_layout.setter('height'))

        self.player_inputs = {}
        players = list(self.players_data.keys())  # Liste figée des joueurs initiaux

        for i, player in enumerate(players, 1):
            # Groupe joueur
            player_group = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100),
                spacing=dp(5))

            # Titre joueur
            player_group.add_widget(Label(
                text=f"JOUEUR {i}",
                font_size=dp(18),
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=dp(30)))

            # Champ de saisie
            player_input = TextInput(
                text=player,
                hint_text=f"Nom du joueur {i}...",
                font_size=dp(22),
                size_hint_y=None,
                height=dp(60),
                background_color=(1, 1, 1, 0.3))

            self.player_inputs[player] = player_input
            player_group.add_widget(player_input)
            form_layout.add_widget(player_group)

        scroll_content.add_widget(form_layout)
        popup_layout.add_widget(scroll_content)

        # Boutons de contrôle
        controls = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(80))

        cancel_btn = Button(
            text="Annuler",
            font_size=dp(20),
            background_color=(0.8, 0.3, 0.3, 1))
        cancel_btn.bind(on_release=lambda x: self.popup.dismiss())

        confirm_btn = Button(
            text="Valider",
            font_size=dp(20),
            background_color=(0.3, 0.7, 0.4, 1))
        confirm_btn.bind(on_release=self.on_player_setup_confirm)

        controls.add_widget(cancel_btn)
        controls.add_widget(confirm_btn)
        popup_layout.add_widget(controls)

        self.popup = Popup(
            title='',
            content=popup_layout,
            size_hint=(0.95, 0.95))
        self.popup.open()

    def on_player_setup_confirm(self, instance):
        """ Met à jour les noms des joueurs """
        new_players_data = {}
        new_observable_widgets = {}  # Pour mettre à jour les widgets des observables

        for player, player_input in self.player_inputs.items():
            new_name = player_input.text.strip()
            new_players_data[new_name] = self.players_data.pop(player)

            # Mettre à jour observable_widgets avec le nouveau nom
            if player in self.observable_widgets:
                new_observable_widgets[new_name] = self.observable_widgets.pop(player)

            # Mettre à jour le TextInput associé dans la section joueur
            if player in self.player_name_widgets:
                self.player_name_widgets[player].text = new_name

        self.players_data = new_players_data
        self.observable_widgets = new_observable_widgets  # Synchronise les widgets
        self.popup.dismiss()
        self.show_variable_setup_popup()

    def show_variable_setup_popup(self):
        """Popup de configuration des variables - Version mobile améliorée"""
        self.use_same_variables = True  # Par défaut, les mêmes noms sont utilisés pour tous les joueurs
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint=(1, 1))

        # En-tête
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=dp(10))

        title = Label(
            text="[b]CONFIGURATION DES VARIABLES[/b]",
            markup=True,
            font_size=dp(22),
            halign='center',
            color=get_color_from_hex('#2c3e50'),
            size_hint_x=0.8)

        close_btn = Button(
        text = '×',
        font_size = dp(36),
        size = (dp(60), dp(60)),
        background_color = get_color_from_hex('#e74c3c'),
        background_normal = '')
        close_btn.bind(on_release=lambda x: self.popup.dismiss())

        header.add_widget(title)
        header.add_widget(close_btn)
        layout.add_widget(header)

        # Contenu principal
        main_content = ScrollView(
        bar_width = dp(12),
        size_hint = (1, 1))

        form_layout = GridLayout(
        cols = 1,
        spacing = dp(20),
        size_hint_y = None,
        padding = (0, dp(10)))
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Mode de configuration
        self.mode_button = ToggleButton(
        text = "Noms identiques pour tous",
        font_size = dp(18),
        size_hint_y = None,
        height = dp(60),
        group = 'var_mode',
        background_normal = '',
        background_color = (0.2, 0.6, 0.8, 1) if self.use_same_variables else (0.8, 0.8, 0.8, 1))
        self.mode_button.bind(on_release=self.toggle_variable_mode)
        layout.add_widget(self.mode_button)

        # Contrôle nombre de variables
        var_control = GridLayout(
        cols = 3,
        spacing = dp(10),
        size_hint_y = None,
        height = dp(80))

        decrease_btn = Button(
            text="-",
            font_size=dp(40),
            size_hint=(0.2, 1),
            background_color=get_color_from_hex('#c0392b'))

        self.num_variables_label = Label(
            text=f"Variables: {self.players_data[next(iter(self.players_data))]['num_observables']}",
            font_size=dp(22),
            halign='center',
            bold=True)

        increase_btn = Button(
            text="+",
            font_size=dp(40),
            size_hint=(0.2, 1),
            background_color=get_color_from_hex('#27ae60'))

        var_control.add_widget(decrease_btn)
        var_control.add_widget(self.num_variables_label)
        var_control.add_widget(increase_btn)
        form_layout.add_widget(var_control)

        # Liste des variables
        var_scroll = ScrollView(
            size_hint=(1, None),
            height=dp(300),
            bar_width=dp(10))

        self.variables_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            size_hint_y=None,
            row_default_height=dp(70))

        self.update_variable_inputs()
        var_scroll.add_widget(self.variables_layout)
        form_layout.add_widget(var_scroll)

        main_content.add_widget(form_layout)
        layout.add_widget(main_content)

        # Bouton de validation
        confirm_btn = Button(
            text="VALIDER LA CONFIGURATION",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(70),
            background_color=get_color_from_hex('#f39c12'),
            background_normal='')
        confirm_btn.bind(on_release=self.on_variable_setup_confirm)
        layout.add_widget(confirm_btn)

        # Liaisons des boutons
        decrease_btn.bind(on_release=lambda x: self.change_num_variables(-1))
        increase_btn.bind(on_release=lambda x: self.change_num_variables(1))

        self.popup = Popup(
            title='',
            content=layout,
            size_hint=(0.95, 0.95),
            separator_height=0)
        self.popup.open()

    def change_num_variables(self, delta):
        """ Change le nombre de variables pour chaque joueur """
        current_num = self.players_data[next(iter(self.players_data))]['num_observables']
        new_num = max(1, current_num + delta)  # Le nombre minimum de variables est 1
        for player in self.players_data.keys():
            self.players_data[player]['num_observables'] = new_num
        self.num_variables_label.text = f"Nombre de variables : {new_num}"
        self.update_variable_inputs()

    def set_num_observables(self, player, num_observables):
        """ Met à jour le nombre d'observables pour le joueur et met à jour l'interface. """
        self.players_data[player]['num_observables'] = num_observables
        self.update_observables_layout(player)

    def toggle_variable_mode(self, instance):
        """ Bascule entre les modes 'identique' et 'différent' pour les variables """
        self.use_same_variables = not self.use_same_variables
        if self.use_same_variables:
            self.mode_button.text = "Utiliser des noms identiques pour tous les joueurs"
        else:
            self.mode_button.text = "Utiliser des noms différents pour chaque joueur"
        self.update_variable_inputs()

    def update_variable_inputs(self):
        """ Met à jour les champs de saisie des noms des variables en fonction du mode sélectionné """
        self.variables_layout.clear_widgets()  # Supprime les widgets existants
        self.variable_inputs = {}

        if self.use_same_variables:
            # Une seule série de noms pour tous les joueurs
            for i in range(1, max(player['num_observables'] for player in self.players_data.values()) + 1):
                var_input = TextInput(text=f"Var {i}", size_hint_y=None, height=40)
                self.variable_inputs[f'Var_{i}'] = var_input
                self.variables_layout.add_widget(var_input)
        else:
            # Une série de noms distincte pour chaque joueur
            for player in self.players_data.keys():
                player_label = Label(text=f"Variables pour {player}:", size_hint_y=None, height=30)
                self.variables_layout.add_widget(player_label)

                for i in range(1, self.players_data[player]['num_observables'] + 1):
                    var_input = TextInput(text=f"Var {i}", size_hint_y=None, height=40)
                    self.variable_inputs[f'{player}_Var_{i}'] = var_input
                    self.variables_layout.add_widget(var_input)

    def on_variable_setup_confirm(self, instance):
        """ Met à jour les noms des variables """
        variable_names = []  # Utiliser une liste pour préserver l'ordre
        invalid_names = []  # Pour suivre les noms invalides

        if self.use_same_variables:
            # Utilise les mêmes noms pour tous les joueurs
            for i in range(self.players_data[next(iter(self.players_data))]['num_observables']):
                var_name = self.variable_inputs[f'Var_{i + 1}'].text.strip()
                if not var_name:
                    invalid_names.append(var_name)
                elif var_name in variable_names:  # Vérifier les doublons
                    invalid_names.append(var_name)
                else:
                    variable_names.append(var_name)  # Ajouter dans l'ordre

            if invalid_names:
                self.show_error_popup(f"Noms de variables invalides ou dupliqués : {', '.join(invalid_names)}")
                return

            for player in self.players_data.keys():
                # Créer un dictionnaire ordonné dans l'ordre des variable_names
                self.players_data[player]['observables'] = {
                    name: {'score': 0} for name in variable_names
                }
        else:
            # Utilise des noms distincts pour chaque joueur
            for player in self.players_data.keys():
                for i in range(self.players_data[player]['num_observables']):
                    var_name = self.variable_inputs[f'{player}_Var_{i + 1}'].text.strip()
                    if not var_name or var_name in variable_names:
                        invalid_names.append(f"{player} - {var_name}")
                    else:
                        variable_names.add(var_name)
                        self.players_data[player]['observables'][var_name] = {'score': 0}

            if invalid_names:
                self.show_error_popup(f"Noms de variables invalides ou dupliqués : {', '.join(invalid_names)}")
                return

        # Réinitialisez ou mettez à jour les widgets des observables
        for player in self.players_data.keys():
            if player not in self.observable_widgets:
                self.observable_widgets[player] = BoxLayout(orientation='vertical', size_hint_y=None)
            self.update_observables_layout(player)

        self.popup.dismiss()
        self.update_player_sections()

    def show_error_popup(self, error_message):
        """ Affiche une popup d'erreur """
        error_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))
        error_layout.add_widget(Label(text=error_message, font_size=16, size_hint_y=None, height=40))

        close_button = Button(text="Fermer", size_hint_y=None, height=40)
        close_button.bind(on_release=lambda instance: self.popup.dismiss())
        error_layout.add_widget(close_button)

        self.popup = Popup(title="Erreur", content=error_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def update_player_sections(self):
        """ Met à jour l'affichage des sections des joueurs """
        for player, data in self.players_data.items():
            if player not in self.observable_widgets:
                self.observable_widgets[player] = BoxLayout(orientation='vertical', size_hint_y=None)

            player_vars_layout = self.observable_widgets[player]
            player_vars_layout.clear_widgets()

            for var_name, var_data in data['observables'].items():
                # Création du layout pour une variable
                var_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(40),
                    spacing=dp(5))

                # Label du nom
                var_label = Label(
                    text=f"{var_name}:",
                    size_hint_x=0.7,
                    halign='left',
                    font_size=dp(16))

                # Label du score lié aux données
                var_score = ScoreLabel(
                    text=str(var_data['score']),
                    size_hint_x=0.3,
                    font_size=dp(16),
                    bold=True)

                # Lien direct avec les données
                var_data['main_score_label'] = var_score

                var_layout.add_widget(var_label)
                var_layout.add_widget(var_score)
                player_vars_layout.add_widget(var_layout)

                # Ajustement hauteur
                player_vars_layout.height = len(data['observables']) * dp(40)

    def create_player_section(self, player, color):
        """ Crée une section pour un joueur avec une ScrollView pour les variables """
        # Layout principal pour chaque joueur
        player_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(450))

        with player_layout.canvas.before:
            Color(*color)
            player_layout.rect = Rectangle(size=player_layout.size, pos=player_layout.pos)
            player_layout.bind(
                size=lambda _, val: setattr(player_layout.rect, 'size', val),
                pos=lambda _, val: setattr(player_layout.rect, 'pos', val),
            )

        # Layout horizontal pour le nom du joueur et le bouton de configuration
        name_button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(5))

        # TextInput pour afficher et modifier le nom du joueur
        name_input = Label(
            text=player,
            font_size=dp(24),  # Taille de police augmentée
            size_hint_y=None,
            height=dp(60))
        self.player_name_widgets[player] = name_input  # Lien entre le joueur et son widget
        name_button_layout.add_widget(name_input)

        # Bouton pour ouvrir la configuration dans une popup
        config_button = Button(
            text='Var',
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(60),
            border=(0, 0, 0, 0),
            size=(name_input.height, name_input.height)  # La même hauteur que le champ de texte
        )
        config_button.bind(on_release=lambda instance, p=player: self.show_player_var_popup(p))
        name_button_layout.add_widget(config_button)

        player_layout.add_widget(name_button_layout)

        # Layout pour les variables
        player_vars_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(5),
            row_default_height=dp(50))
        player_vars_layout.bind(minimum_height=player_vars_layout.setter('height'))

        # ScrollView pour les variables
        vars_scroll = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(15))
        vars_scroll.add_widget(player_vars_layout)

        player_layout.add_widget(vars_scroll)

        # Stockage des widgets pour les observables
        self.observable_widgets[player] = player_vars_layout

        return player_layout

    def show_player_var_popup(self, player):
        """Popup de configuration du joueur avec toutes les fonctionnalités"""
        try:
            if player not in self.players_data:
                return

            # Création du layout principal
            content = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                padding=dp(15),
                size_hint=(1, 1))

            # ================= EN-TÊTE =================
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                spacing=dp(10))

            # Titre dynamique
            title = Label(
                text=f"[b]Configuration de {player}[/b]",
                markup=True,
                font_size=dp(22),
                halign='left',
                size_hint_x=0.8)

            # Bouton fermeture fonctionnel
            close_btn = Button(
                text='×',
                font_size=dp(36),
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                background_color=(0.9, 0.2, 0.2, 1),
                background_normal='')
            close_btn.bind(on_release=lambda x: self.popup.dismiss())

            header.add_widget(title)
            header.add_widget(close_btn)
            content.add_widget(header)

            # ================= CORPS DE LA POPUP =================
            main_scroll = ScrollView(
                size_hint=(1, 1),
                bar_width=dp(10))

            main_layout = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=(dp(5), dp(10)))
            main_layout.bind(minimum_height=main_layout.setter('height'))

            # Section édition du nom
            name_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            name_input = TextInput(
                text=player,
                hint_text="Nouveau nom...",
                font_size=dp(20),
                size_hint_x=0.7)
            name_input.bind(text=lambda i, v: self.update_player_name(player, v))

            name_box.add_widget(Label(text="Nom:", size_hint_x=0.3))
            name_box.add_widget(name_input)
            main_layout.add_widget(name_box)

            # Section variables avec boutons +/-
            variables_header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(40))
            variables_header.add_widget(Label(text="Variables", size_hint_x=0.6))
            variables_header.add_widget(Label(text="Score", size_hint_x=0.2))
            variables_header.add_widget(Widget(size_hint_x=0.2))  # Espacement
            main_layout.add_widget(variables_header)

            for obs_name, obs_data in self.players_data[player]['observables'].items():
                var_row = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(60),
                    spacing=dp(5))

                lbl_name = Label(
                    text=obs_name,
                    size_hint_x=0.6,
                    font_size=dp(18),
                    halign='left')

                # Création du label lié dynamiquement
                lbl_score = ScoreLabel(
                    score_value=obs_data['score'],
                    prefix="Score: ",
                    size_hint_x=0.2,
                    font_size=dp(20),
                    halign='center')

                # Stockage des références
                obs_data['score_widget'] = lbl_score
                obs_data['row_widget'] = var_row

                btn_group = BoxLayout(
                    orientation='horizontal',
                    size_hint_x=0.2,
                    spacing=dp(2))

                # Boutons avec liaison améliorée
                btn_minus = Button(text="-", font_size=dp(20))
                btn_minus.bind(
                    on_press=lambda instance, p=player, o=obs_name: self.update_score(p, o, -1)
                )

                btn_plus = Button(text="+", font_size=dp(20))
                btn_plus.bind(
                    on_press=lambda instance, p=player, o=obs_name: self.update_score(p, o, 1)
                )

                btn_group.add_widget(btn_minus)
                btn_group.add_widget(btn_plus)

                var_row.add_widget(lbl_name)
                var_row.add_widget(lbl_score)
                var_row.add_widget(btn_group)
                main_layout.add_widget(var_row)

            # ================= BOUTONS ACTION =================
            action_buttons = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            # Bouton Options Avancées
            btn_advanced = Button(
                text="Options Avancées",
                background_color=(0.2, 0.6, 0.9, 1),
                on_release=lambda x: self.show_advanced_options(player))

            # Bouton Réinitialiser
            btn_reset = Button(
                text="Réinitialiser Scores",
                background_color=(0.9, 0.3, 0.3, 1),
                on_release=lambda x: self.reset_player_scores(player))

            btn_deps = Button(
                text="Dépendances",
                background_color=(0.4, 0.2, 0.8, 1),
                on_release=lambda x: self.show_dependency_matrix(player))

            action_buttons.add_widget(btn_deps)  # Ajouter à la BoxLayout existante

            action_buttons.add_widget(btn_advanced)
            action_buttons.add_widget(btn_reset)
            main_layout.add_widget(action_buttons)

            main_scroll.add_widget(main_layout)
            content.add_widget(main_scroll)

            # ================= GESTION POPUP =================
            self.popup = Popup(
                title='',
                content=content,
                size_hint=(0.9, 0.9),
                auto_dismiss=False)

            # Bouton de fermeture externe
            content.add_widget(Button(
                text="Fermer",
                size_hint_y=None,
                height=dp(50),
                on_release=lambda x: self.popup.dismiss()))

            self.popup.open()

        except Exception as e:
            print(f"Erreur show_player_var_popup: {str(e)}")
            self.show_warning("Erreur d'affichage des paramètres")

    def refresh_popup_scores(self, player):
        """Actualise dynamiquement tous les scores visibles dans la popup"""
        if hasattr(self, 'current_player_popup') and self.current_player_popup:
            observables = self.players_data[player]['observables']

            # Parcourir toute l'arborescence de widgets
            for widget in self.current_player_popup.content.walk():
                if isinstance(widget, ScoreLabel) and hasattr(widget, 'id'):
                    var_name = widget.id
                    if var_name in observables:
                        widget.text = f"Score: {observables[var_name]['score']}"

    def show_dependency_matrix(self, player):
        """Affiche une matrice de dépendances interactive et adaptative"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        header.add_widget(Label(text="[b]DÉPENDANCES → (Ligne dépend de la Colonne)[/b]", markup=True))
        close_btn = Button(text='×', size_hint_x=None, width=dp(40))
        close_btn.bind(on_release=lambda x: self.deps_popup.dismiss())
        header.add_widget(close_btn)
        content.add_widget(header)

        # Calcul de la taille adaptative
        variables = list(self.players_data[player]['observables'].keys())
        num_vars = len(variables)
        col_width = max(Window.width / (num_vars + 2), dp(100))  # Largeur minimum 100dp

        # Grille principale avec scroll
        scroll = ScrollView(size_hint=(1, 1), bar_width=dp(15))
        grid = GridLayout(
            cols=num_vars + 1,
            size_hint=(None, None),
            spacing=dp(2),
            row_default_height=col_width * 0.3,
            col_default_width=col_width
        )
        grid.bind(minimum_size=grid.setter('size'))

        # En-têtes de colonnes (variables cibles)
        grid.add_widget(Label(text="→", bold=True))  # Coin supérieur gauche
        for var in variables:
            grid.add_widget(Label(
                text=var,
                bold=True,
                color=(0, 0, 1, 1),
                font_size=dp(14),
                text_size=(col_width, None),
                halign='center'
            ))

        # Lignes (variables sources)
        for source_var in variables:
            # En-tête de ligne
            grid.add_widget(Label(
                text=source_var,
                bold=True,
                color=(1, 0, 0, 1),
                font_size=dp(14),
                text_size=(col_width, None),
                halign='center'
            ))

            # Cellules
            for target_var in variables:
                if source_var == target_var:
                    grid.add_widget(Label(text="---"))  # Diagonale
                else:
                    # Récupération dépendance existante
                    deps = self.players_data[player]['observables'][source_var].get('dependent_on', [])
                    dep = next((d for d in deps if d['var'] == target_var), None)

                    # Création bouton avec style conditionnel
                    btn = Button(
                        text=dep['mode'] if dep else "+",
                        font_size=dp(12),
                        background_color=self.get_dep_color(dep['mode'] if dep else None),
                        background_normal=''
                    )
                    btn.bind(on_release=partial(self.edit_dependency, player, source_var, target_var))
                    grid.add_widget(btn)

        scroll.add_widget(grid)
        content.add_widget(scroll)

        # Légende interactive
        legend = GridLayout(cols=4, size_hint_y=None, height=dp(50), spacing=dp(5))
        legend.add_widget(Label(text="[b]Légende:[/b]", markup=True))
        for mode, color in [('Somme', (0, 1, 0, 0.3)), ('Produit', (1, 0, 0, 0.3)), ('%', (0, 0, 1, 0.3))]:
            legend.add_widget(Button(
                text=mode,
                background_color=color,
                on_release=partial(self.show_help_popup, mode)
            ))
        content.add_widget(legend)

        self.deps_popup = Popup(
            title=f"Dépendances de {player}",
            content=content,
            size_hint=(0.98, 0.95),
            auto_dismiss=False
        )
        self.deps_popup.open()

    def get_dep_color(self, mode):
        """Retourne la couleur correspondant au type de dépendance"""
        return {
            'Somme': (0, 1, 0, 0.4),  # Vert
            'Produit': (1, 0, 0, 0.4),  # Rouge
            'Pourcentage': (0, 0, 1, 0.4),  # Bleu
            None: (0.9, 0.9, 0.9, 1)  # Gris
        }.get(mode, (0.8, 0.8, 0.8, 1))

    def show_help_popup(self, mode, instance):
        """Affiche l'aide contextuelle pour un type de dépendance"""
        help_text = {
            'Somme': "Score = Source + Cible",
            'Produit': "Score = Source × Cible",
            '%': "Score = (Source / Cible) × 100"
        }.get(mode, "Ajoute une relation entre les variables")

        Popup(
            title=f"Aide - {mode}",
            content=Label(text=help_text, padding=dp(20)),
            size_hint=(0.6, 0.4)
        ).open()

    def edit_dependency(self, player, source_var, target_var, instance):
        """Menu contextuel pour modifier une dépendance"""
        menu = GridLayout(cols=1, spacing=dp(5), padding=dp(10))

        options = [
            ('× Supprimer', 'Aucune', (0.9, 0.3, 0.3, 1)),
            ('+ Somme', 'Somme', (0, 0.8, 0, 1)),
            ('× Produit', 'Produit', (0.8, 0, 0, 1)),
            ('% Pourcentage', 'Pourcentage', (0, 0, 0.8, 1))
        ]

        # Création du popup AVANT la boucle
        edit_popup = Popup(
            title=f"{source_var} → {target_var}",
            content=menu,
            size_hint=(None, None),
            size=(dp(250), dp(300)))

        for text, mode, color in options:
            btn = Button(
                text=text,
                background_color=color,
                background_normal='',
                size_hint_y=None,
                height=dp(50))

            # Liaison CORRECTE avec l'ordre : instance arrive en premier automatiquement
            btn.bind(on_release=lambda _, m=mode: self.update_dependency(
                player,
                source_var,
                target_var,
                m,
                edit_popup))

            menu.add_widget(btn)

        edit_popup.open()

    def update_dependency(self, player, base_var, target_var, mode, edit_popup):
        try:
            observables = self.players_data[player]['observables']

            # Initialisation garantie des dépendances
            if 'dependent_on' not in observables[base_var]:
                observables[base_var]['dependent_on'] = []

            deps = observables[base_var]['dependent_on']

            # Suppression des anciennes dépendances pour cette cible
            deps[:] = [d for d in deps if d['var'] != target_var]

            if mode != 'Aucune':
                # Ajout avec structure claire
                deps.append({
                    'var': target_var,
                    'mode': mode,
                    'coefficient': 1.0  # Ajout optionnel pour calculs futurs
                })

                print(f"Dépendance enregistrée : {deps[-1]}")  # Debug

            # FORCER le recalcul complet
            self.recalculate_dependent_variables(player, base_var)

            # Mise à jour visuelle IMMÉDIATE
            self.deps_popup.dismiss()
            Clock.schedule_once(lambda dt: self.show_dependency_matrix(player), 0.1)

        except Exception as e:
            print(f"Erreur critique: {str(e)}")
            self.show_warning(f"Erreur: {str(e)}")

        finally:
            edit_popup.dismiss()

    def show_advanced_options(self, player):
        """Popup de configuration avancée des variables (coefficients/dépendances)"""
        try:
            # Création du layout principal
            content = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                padding=dp(15),
                size_hint=(1, 1))

            # ================= EN-TÊTE =================
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                spacing=dp(10))

            title = Label(
                text=f"[b]Options avancées - {player}[/b]",
                markup=True,
                font_size=dp(22),
                halign='left')

            close_btn = Button(
                text='×',
                font_size=dp(36),
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                background_color=(0.9, 0.2, 0.2, 1))
            close_btn.bind(on_release=lambda x: self.advanced_popup.dismiss())

            header.add_widget(title)
            header.add_widget(close_btn)
            content.add_widget(header)

            # ================= CORPS DE LA POPUP =================
            main_scroll = ScrollView(size_hint=(1, 1))

            main_layout = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=dp(10))
            main_layout.bind(minimum_height=main_layout.setter('height'))

            # Sélection de la variable
            var_spinner = Spinner(
                text='Choisir une variable',
                values=list(self.players_data[player]['observables'].keys()),
                size_hint_y=None,
                height=dp(50),
                font_size=dp(18))

            # Champs de configuration
            input_grid = GridLayout(
                cols=2,
                spacing=dp(10),
                size_hint_y=None,
                height=dp(100))

            initial_input = TextInput(
                hint_text="Valeur initiale",
                input_filter='int',
                font_size=dp(18))

            coeff_input = TextInput(
                hint_text="Coefficient",
                input_filter='int',
                font_size=dp(18))

            input_grid.add_widget(Label(text="Valeur initiale:"))
            input_grid.add_widget(initial_input)
            input_grid.add_widget(Label(text="Multiplicateur:"))
            input_grid.add_widget(coeff_input)


            # Mise à jour dynamique des champs
            def update_fields(instance, value):
                """Remplit les champs avec les valeurs existantes"""
                if value in self.players_data[player]['observables']:
                    data = self.players_data[player]['observables'][value]
                    initial_input.text = str(data.get('initial', 0))
                    coeff_input.text = str(data.get('coefficient', 1))


            var_spinner.bind(text=update_fields)

            # ================= BOUTONS ACTION =================
            btn_group = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            btn_apply = Button(
                text='Appliquer',
                background_color=(0.3, 0.7, 0.4, 1),
                on_release=lambda x: self.apply_advanced_settings(
                    player,
                    var_spinner.text,
                    initial_input.text,
                    coeff_input.text))

            btn_cancel = Button(
                text='Annuler',
                background_color=(0.9, 0.3, 0.3, 1),
                on_release=lambda x: self.advanced_popup.dismiss())

            btn_group.add_widget(btn_apply)
            btn_group.add_widget(btn_cancel)

            # Assemblage final
            main_layout.add_widget(var_spinner)
            main_layout.add_widget(input_grid)
            main_layout.add_widget(btn_group)
            main_scroll.add_widget(main_layout)
            content.add_widget(main_scroll)

            # Création de la popup
            self.advanced_popup = Popup(
                title='',
                content=content,
                size_hint=(0.85, 0.85),
                auto_dismiss=False)
            self.advanced_popup.open()

        except Exception as e:
            print(f"Erreur show_advanced_options: {str(e)}")
            self.show_warning("Erreur de configuration avancée")

    def apply_advanced_settings(self, player, var_name, initial, coeff):
        """Applique les paramètres avancés"""
        try:
            if not var_name or var_name not in self.players_data[player]['observables']:
                return

            # Conversion des valeurs
            initial = int(initial) if initial else 0
            coeff = int(coeff) if coeff else 1

            # Mise à jour des paramètres de base
            obs_data = self.players_data[player]['observables'][var_name]
            obs_data.update({
                'initial': initial,
                'coefficient': coeff,
                'score': initial + (obs_data.get('points', 0) * coeff)
            })

            # Rafraîchissement de l'interface
            if self.popup:
                self.popup.dismiss()
                self.show_player_var_popup(player)

            self.advanced_popup.dismiss()

        except ValueError:
            self.show_warning("Valeurs numériques invalides!")
        except Exception as e:
            print(f"Erreur apply_advanced_settings: {str(e)}")
            self.show_warning("Erreur d'application des paramètres")

    def show_player_config_popup(self, player):
        """Popup de configuration des variables - Version mobile améliorée"""
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(25))

        # Header stylisé
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70))

        title = Label(
            text="[b]Configuration[/b]",
            markup=True,
            font_size=dp(24),
            halign='center')

        close_btn = Button(
            text='×',
            font_size=dp(36),
            size=(dp(60), dp(60)),
            background_color=(0.9, 0.1, 0.1, 1))
        close_btn.bind(on_release=lambda x: popup.dismiss())

        header.add_widget(title)
        header.add_widget(close_btn)
        layout.add_widget(header)

        # Contenu défilant
        main_content = ScrollView(
            bar_width=dp(10))

        form = GridLayout(
            cols=1,
            spacing=dp(20),
            size_hint_y=None,
            row_default_height=dp(70))
        form.bind(minimum_height=form.setter('height'))

        # Fonction de mise à jour des champs
        def update_fields(spinner, text):
            if text in self.players_data[player]['observables']:
                obs = self.players_data[player]['observables'][text]
                initial_input.text = str(obs.get('initial', 0))
                coeff_input.text = str(obs.get('coefficient', 1))

        # Fonction d'application des changements
        def apply_changes(instance):
            selected = var_spinner.text
            if selected in self.players_data[player]['observables']:
                try:
                    self.players_data[player]['observables'][selected]['initial'] = int(initial_input.text)
                    self.players_data[player]['observables'][selected]['coefficient'] = int(coeff_input.text)
                    self.update_observables_layout(player)
                    popup.dismiss()
                except ValueError:
                    self.show_warning("Valeurs invalides!")

        # Sélection variable
        var_spinner = Spinner(
            text="Choisir une variable",
            values=list(self.players_data[player]['observables'].keys()),
            font_size=dp(22),
            size_hint_y=None,
            height=dp(70))
        form.add_widget(var_spinner)
        # Ajouter les liaisons manquantes
        var_spinner.bind(text=update_fields)

        # Champs de configuration
        input_group = GridLayout(
            cols=2,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(150))

        initial_input = TextInput(
            hint_text="Valeur initiale",
            input_filter="int",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(70))

        coeff_input = TextInput(
            hint_text="Coefficient",
            input_filter="int",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(70))

        input_group.add_widget(Label(text="Valeur de départ:", font_size=dp(20)))
        input_group.add_widget(initial_input)
        input_group.add_widget(Label(text="Multiplicateur:", font_size=dp(20)))
        input_group.add_widget(coeff_input)
        form.add_widget(input_group)

        # Boutons d'actions
        action_group = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(80))

        dep_btn = Button(
            text="Dépendances",
            font_size=dp(20),
            background_color=(0.3, 0.5, 0.8, 1))

        apply_btn = Button(
            text="Sauvegarder",
            font_size=dp(20),
            background_color=(0.2, 0.7, 0.3, 1))

        dep_btn.bind(on_release=lambda x: self.show_dependency_config_popup(player))
        apply_btn.bind(on_release=apply_changes)

        action_group.add_widget(dep_btn)
        action_group.add_widget(apply_btn)
        form.add_widget(action_group)

        main_content.add_widget(form)
        layout.add_widget(main_content)

        popup = Popup(
            title='',
            content=layout,
            size_hint=(0.9, 0.85))
        popup.open()

    def update_observables_layout(self, player):
        """ Met à jour la disposition des variables observables pour un joueur. """
        if player not in self.players_data:
            raise ValueError(f"Les données pour le joueur {player} sont introuvables.")

        # Initialiser le layout si nécessaire
        if 'layout' not in self.players_data[player]:
            self.players_data[player]['layout'] = BoxLayout(orientation='vertical', size_hint_y=None)
        layout = self.players_data[player]['layout']

        layout.clear_widgets()  # Réinitialise les widgets des variables

        # Initialiser la structure des observables si elle n'existe pas
        if 'observables' not in self.players_data[player] or not self.players_data[player]['observables']:
            self.players_data[player]['observables'] = {
                f"Observable {i + 1}": {'score': 0} for i in range(self.players_data[player].get('num_observables', 3))
            }
        observables = self.players_data[player]['observables']
        layout.height = len(observables) * 50  # Ajuste la hauteur en fonction du nombre d'observables

        for obs_name, observable_data in observables.items():
            if 'score' not in observable_data:
                observable_data['score'] = 0

            var_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            var_label = Label(text=f"{obs_name}:", size_hint_x=0.6, size_hint_y=None, height=40)
            var_score = Label(text=str(observable_data['score']), size_hint_x=0.2, size_hint_y=None, height=40)

            # Ajouter la référence du Label au dictionnaire de l'observable
            observable_data['score_label'] = var_score  # <-- Ligne ajoutée

            btn_increase = Button(text="+", size_hint=(0.1, None), height=40)
            btn_increase.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, 1))

            btn_decrease = Button(text="-", size_hint=(0.1, None), height=40)
            btn_decrease.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, -1))

            var_layout.add_widget(var_label)
            var_layout.add_widget(var_score)
            var_layout.add_widget(btn_increase)
            var_layout.add_widget(btn_decrease)

            layout.add_widget(var_layout)

    def initialize_observable(self, player, observable, initial_value=0, coefficient=1, dependency=None,
                              dependency_mode="Somme"):
        self.players_data[player]['observables'][observable] = {
            'initial': initial_value,
            'coefficient': coefficient,
            'score': initial_value,
            'score_label': Label(text=str(initial_value)),
            'dependent_on': [],
            'dependency_mode': dependency_mode,
        }

    def on_name_change(self, instance, value):
        # Met à jour le nom du joueur dans players_data
        for player in list(self.players_data.keys()):
            if instance.text != player:
                if instance.text.strip() not in self.players_data:
                    self.players_data[instance.text.strip()] = self.players_data.pop(player)
                break

    def close_popup(self, instance):
        """Ferme la popup."""
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def cleanup_popup(self, instance):
        """Nettoie après fermeture."""
        self.popup = None

    def on_player_var_setup_confirm(self, player):
        """ Valide et met à jour les variables pour un joueur spécifique """
        variable_names = set()  # Pour vérifier les doublons
        invalid_names = []  # Pour suivre les noms invalides
        updated_variables = {}

        # Validation des noms des variables
        for key, input_widget in self.player_variable_inputs.items():
            var_name = input_widget.text.strip()
            if not var_name or var_name in variable_names:
                invalid_names.append(var_name)
            else:
                variable_names.add(var_name)
                updated_variables[var_name] = self.players_data[player]['observables'].get(var_name, {'score': 0})

        if invalid_names:
            self.show_error_popup(f"Noms de variables invalides ou dupliqués : {', '.join(invalid_names)}")
            return

        # Mise à jour des variables pour le joueur
        self.players_data[player]['observables'] = updated_variables
        self.popup.dismiss()
        self.update_player_sections()

    def on_combine_variable_change(self, spinner, variable_spinner, new_value):
        # Vérifier si la variable sélectionnée est la même que celle de base
        base_variable = variable_spinner.text
        if new_value == base_variable:
            spinner.text = ""  # Réinitialiser le choix de la variable dépendante
            # Afficher un message d'erreur ou un avertissement si nécessaire
            self.show_warning("Vous ne pouvez pas sélectionner la même variable.")

    def recalculate_dependent_variables(self, player, source_var):
        """Recalcule les scores des variables dépendantes avec la nouvelle valeur"""
        try:
            observables = self.players_data[player]['observables']
            current_score = observables[source_var]['score']

            if 'calculating' in observables[source_var]:
                return

            observables[source_var]['calculating'] = True

            for var_name, data in observables.items():
                dependencies = data.get('dependent_on', [])
                for dep in dependencies:
                    if dep['var'] == source_var:
                        mode = dep['mode']
                        base = data.get('score', 0)

                        if mode == "Somme":
                            data['score'] = base + current_score
                        elif mode == "Produit":
                            data['score'] = base * current_score
                        elif mode == "Pourcentage" and current_score != 0:
                            data['score'] = (base / current_score) * 100

                        # CORRECTION : Utiliser 'main_score_label' au lieu de 'score_label'
                        if 'main_score_label' in data:
                            data['main_score_label'].text = str(int(data['score']))

                        # Propagation récursive
                        self.recalculate_dependent_variables(player, var_name)

            observables[source_var].pop('calculating', None)

        except Exception as e:
            print(f"Erreur dans recalculate_dependent_variables: {e}")
            observables[source_var].pop('calculating', None)

    def decalculate_dependent_variables(self, player, source_var, old_score):
        """Retire la contribution de l'ancien score sur les variables dépendantes"""
        try:
            observables = self.players_data[player]['observables']

            if 'calculating' in observables.get(source_var, {}):
                return

            observables[source_var]['calculating'] = True

            for var_name, data in observables.items():
                dependencies = data.get('dependent_on', [])
                for dep in dependencies:
                    if dep['var'] == source_var:
                        mode = dep['mode']
                        current_score = data.get('score', 0)

                        # Calculer la contribution basée sur l'ancien score
                        if mode == "Somme":
                            contribution = old_score
                        elif mode == "Produit":
                            contribution = current_score / old_score if old_score != 0 else 0
                        elif mode == "Pourcentage":
                            contribution = (current_score * old_score) / 100 if old_score != 0 else 0
                        else:
                            contribution = 0

                        # Retirer la contribution
                        new_score = current_score - contribution
                        data['score'] = new_score
                        if 'score_label' in data:
                            data['score_label'].text = str(int(new_score))

            # Nettoyer l'indicateur de calcul
            observables[source_var].pop('calculating', None)

        except Exception as e:
            print(f"Erreur dans decalculate_dependent_variables: {e}")
            observables[source_var].pop('calculating', None)

    def detect_cycle(self, player, start_var, target_var):
        observables = self.players_data[player]['observables']
        visited = set()

        while target_var in observables:
            if target_var in visited:
                return True  # Cycle détecté
            visited.add(target_var)
            target_var = observables[target_var].get('dependent_on')

        return False

    def update_variable_value(self, player, var_name, new_value):
            # Mettez à jour la valeur de la variable dans les données du joueur
            if var_name in self.players_data[player]['observables']:
                self.players_data[player]['observables'][var_name]['value'] = new_value

    def update_player_name(self, old_name, new_name):
        if new_name.strip() and new_name != old_name:
            # Mettre à jour toutes les références
            self.players_data[new_name] = self.players_data.pop(old_name)
            if old_name in self.player_name_widgets:
                self.player_name_widgets[new_name] = self.player_name_widgets.pop(old_name)
            # Fermer toute popup ouverte avec l'ancien nom
            if hasattr(self, 'popup'):
                self.popup.dismiss()
        #Modification des variables

    def apply_variable_config(self, player, observable, initial, coefficient, popup):
        if observable in self.players_data[player]['observables']:
            # Conversion des valeurs en int avec des valeurs par défaut
            initial_value = int(initial) if initial else 0
            coefficient_value = int(coefficient) if coefficient else 1

            # Mise à jour des données de l'observable
            self.players_data[player]['observables'][observable]['initial'] = initial_value
            self.players_data[player]['observables'][observable]['coefficient'] = coefficient_value

            # Mise à jour du score actuel en fonction de la valeur initiale
            self.players_data[player]['observables'][observable]['score'] = initial_value

        # Mise à jour de l'affichage des variables du joueur
        self.update_observables_layout(player)

        # Fermeture du Popup
        popup.dismiss()

    def apply_sum_dependency(self, player, var_name, combine_var):
        observables = self.players_data[player]['observables']

        # Vérifiez si la dépendance a déjà été appliquée
        if observables[var_name].get('dependent_on') == combine_var:
            return

        # Calcul de la nouvelle valeur
        dependent_score = observables[combine_var]['score']
        base_score = observables[var_name]['score']
        new_score = base_score + dependent_score

        # Mettre à jour les données
        observables[var_name]['score'] = new_score
        observables[var_name]['score_label'].text = str(int(new_score))

        # Enregistrez la dépendance
        observables[var_name]['dependent_on'] = combine_var

        # Propager les dépendances
        self.recalculate_dependent_variables(player, var_name)

    def apply_product_dependency(self, player, var_name, combine_var):
        dependent_score = self.players_data[player]['observables'][combine_var]['score']
        base_score = self.players_data[player]['observables'][var_name]['score']
        self.players_data[player]['observables'][var_name]['score'] = base_score * dependent_score
        self.update_observables_layout(player)

    def apply_percentage_dependency(self, player, var_name, combine_var):
        dependent_score = self.players_data[player]['observables'][combine_var]['score']
        base_score = self.players_data[player]['observables'][var_name]['score']
        self.players_data[player]['observables'][var_name]['score'] = (base_score / dependent_score) * 100
        self.update_observables_layout(player)

    def update_variable(self, player, var_name):
        observables = self.players_data[player]['observables']
        dependencies = self.players_data[player].get('dependencies', {})

        if var_name in dependencies:
            dependent_var = dependencies[var_name]
            if dependent_var in observables:
                base_score = observables[var_name]['score']
                dependent_score = observables[dependent_var]['score']
                mode = observables[var_name].get('dependency_mode', 'Somme')

                # Calcul du nouveau score en fonction du mode
                if mode == "Somme":
                    base_score = dependent_score + base_score
                elif mode == "Produit":
                    base_score = dependent_score * base_score
                elif mode == "Pourcentage":
                    if dependent_score != 0:
                        base_score = (base_score / dependent_score) * 100
                    else:
                        self.show_warning("Division par zéro lors du calcul de la dépendance.")
                        return

                # Mise à jour du score
                observables[var_name]['score'] = base_score
                observables[var_name]['score_label'].text = str(int(base_score))

        # Propager la mise à jour aux dépendances secondaires
        for dep_var, dep_on in dependencies.items():
            if dep_on == var_name:
                self.update_variable(player, dep_var)

    def update_score(self, player, observable, change):
        """Met à jour le score depuis la popup"""
        try:
            obs_data = self.players_data[player]['observables'][observable]

            coeff = obs_data.get('coefficient', 1)

            # Capturer l'ancien score avant modification
            old_score = obs_data.get('score', 0)

            # Calculer le nouveau score
            new_score = old_score + coeff * change

            # 1. Retirer l'ancienne contribution des dépendances
            self.decalculate_dependent_variables(player, observable, old_score)

            # 2. Mettre à jour le score actuel
            obs_data['score'] = new_score

            # 3. Appliquer la nouvelle contribution aux dépendances
            self.recalculate_dependent_variables(player, observable)

            # Ajouter cette ligne pour rafraîchir toute l'interface
            self.update_all_ui_labels(player)

            # Mise à jour de la variable modifiée
            if 'main_score_label' in obs_data:
                obs_data['main_score_label'].text = str(new_score)
            if 'score_widget' in obs_data:
                obs_data['score_widget'].text = str(new_score)

        except KeyError as e:
            print(f"Erreur update_score: Variable {observable} non trouvée")

    def update_all_ui_labels(self, player):
        """Met à jour tous les labels du joueur"""
        for var_name, data in self.players_data[player]['observables'].items():
            if 'main_score_label' in data:
                data['main_score_label'].text = str(int(data['score']))

    def process_dependencies(self, player, source_var):
        """Gère toutes les mises à jour de dépendances"""
        # 1. Suppression de l'ancienne valeur
        self.decalculate_dependent_variables(player, source_var)  # Nom corrigé

        # 2. Application nouvelle valeur
        self.recalculate_dependent_variables(player, source_var)  # Nom corrigé

        # 3. Mise à jour de l'UI pour toutes les variables impactées
        for var_name, data in self.players_data[player]['observables'].items():
            if 'main_score_label' in data:
                data['main_score_label'].text = str(data['score'])
            if 'score_widget' in data:
                data['score_widget'].text = str(data['score'])

    def get_variable_value(self, player, variable_name):
        # Cette fonction récupère la valeur d'une variable pour un joueur donné
        return self.players_data[player]['observables'][variable_name]['value']

    def store_result(self, player, result, dep_mode):
        # Cette fonction stocke le résultat du calcul dans une variable
        self.players_data[player]['observables'][f"result_{dep_mode}"] = result

        #Débuter le temps lorsque nécessaire

    def show_warning(self, message):
        """
        Affiche un avertissement via un popup.
        """
        popup = Popup(title="Attention", content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def switch_mode(self, instance):
        # Change le mode entre Timer et Chrono
        self.is_timer_mode = not self.is_timer_mode
        if self.is_timer_mode:
            self.mode_button.text = "Mode Chrono"
            self.timer_label.text = "Timer: 00:00"
            self.start_timer_button.text = "Démarrer le Timer"
        else:
            self.mode_button.text = "Mode Timer"
            self.timer_label.text = "Chrono: 00:00"
            self.start_timer_button.text = "Démarrer le Chrono"
            self.show_chrono_popup()  # Affiche le popup pour configurer le chrono

        # Arrête le timer/chrono si actif
        self.stop_timer()

    def show_chrono_popup(self):
        # Configuration des couleurs
        primary_color = get_color_from_hex('#2c3e50')  # Bleu foncé
        secondary_color = get_color_from_hex('#3498db')  # Bleu vif
        background_color = (1, 1, 1, 0.95)  # Blanc semi-transparent

        from kivy.metrics import dp
        # Layout principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(25),
            size_hint=(0.9, 0.7))

        # En-tête personnalisé
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10))

        title = Label(
            text="[b]DURÉE DU CHRONO[/b]",
            markup=True,
            font_size=dp(22),
            color=primary_color,
            bold=True,
            size_hint_x=0.8)

        close_btn = Button(
        text = '×',
        font_size = dp(32),
        size_hint = (None, None),
        size = (dp(50), dp(50)),
        background_color = secondary_color,
        background_normal = '')
        close_btn.bind(on_release=lambda x: popup.dismiss())

        header.add_widget(title)
        header.add_widget(close_btn)
        layout.add_widget(header)

        # Conteneur des temps
        time_container = GridLayout(
        cols = 3,
        spacing = dp(20),
        size_hint_y = 0.7)

        # Style commun pour les contrôles
        time_style = {
            'button': {
                'size_hint': (1, 0.3),
                'font_size': dp(28),
                'background_normal': '',
                'background_color': secondary_color
            },
            'label': {
                'font_size': dp(32),
                'bold': True,
                'color': primary_color
            }
        }

        # Heures
        hour_box = BoxLayout(orientation='vertical', spacing=dp(5))
        hour_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('hours', 1, hour_label),
            **time_style['button']))
        hour_label = Label(text=f"{self.hours:02}", **time_style['label'])
        hour_box.add_widget(hour_label)
        hour_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('hours', -1, hour_label),
            **time_style['button']))

        # Minutes
        minute_box = BoxLayout(orientation='vertical', spacing=dp(5))
        minute_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('minutes', 1, minute_label),
            **time_style['button']))
        minute_label = Label(text=f"{self.minutes:02}", **time_style['label'])
        minute_box.add_widget(minute_label)
        minute_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('minutes', -1, minute_label),
            **time_style['button']))

        # Secondes
        second_box = BoxLayout(orientation='vertical', spacing=dp(5))
        second_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('seconds', 1, second_label),
            **time_style['button']))
        second_label = Label(text=f"{self.seconds:02}", **time_style['label'])
        second_box.add_widget(second_label)
        second_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('seconds', -1, second_label),
            **time_style['button']))

        time_container.add_widget(hour_box)
        time_container.add_widget(minute_box)
        time_container.add_widget(second_box)
        layout.add_widget(time_container)


        # Séparateur visuel
        layout.add_widget(Widget(size_hint_y=None, height=dp(1)))

        # Bouton de validation
        validate_btn = Button(
            text="Valider les paramètres",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60),
            background_color=secondary_color,
            background_normal='')
        validate_btn.bind(on_release=lambda x: popup.dismiss())
        layout.add_widget(validate_btn)

        # Création du popup
        popup = Popup(
            title='',
            content=layout,
            separator_height=0)
        popup.open()

    def change_time(self, unit, increment, label):
        if unit == 'hours':
            self.hours = max(0, self.hours + increment)
            label.text = f"{self.hours}"
        elif unit == 'minutes':
            self.minutes = max(0, min(59, self.minutes + increment))
            label.text = f"{self.minutes}"
        elif unit == 'seconds':
            self.seconds = max(0, min(59, self.seconds + increment))
            label.text = f"{self.seconds}"

        # Met à jour la durée totale du chrono en secondes
        self.chrono_duration = self.hours * 3600 + self.minutes * 60 + self.seconds

    def start_timer(self, instance):
        if not self.timer_event:
            self.start_time = self.chrono_duration if not self.is_timer_mode else 0
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            if self.is_timer_mode:
                self.start_timer_button.text = "Arrêter le Timer"
            else:
                self.start_timer_button.text = "Arrêter le Chrono"
        else:
            self.stop_timer()

    def stop_timer(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            self.start_timer_button.text = "Démarrer le Timer" if self.is_timer_mode else "Démarrer le Chrono"

    def update_timer(self, dt):
        if self.is_timer_mode:
            self.start_time += 1
        else:
            self.start_time -= 1
            if self.start_time <= 0:
                self.stop_timer()

        minutes, seconds = divmod(abs(self.start_time), 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.text = f"{'Timer' if self.is_timer_mode else 'Chrono'}: {hours:02}:{minutes:02}:{seconds:02}"

        # Changer nom de l'archive

    def reset_scores(self):
        """Réinitialise les scores avec mise à jour visuelle garantie"""
        try:
            for player, pdata in self.players_data.items():
                for var_name, obs in pdata['observables'].items():
                    # Réinitialisation des données
                    initial = obs.get('initial', 0)
                    obs.update({
                        'points': 0,
                        'score': initial
                    })

                    # Mise à jour directe de tous les labels connus
                    if 'main_score_label' in obs:  # <-- Clé corrigée
                        obs['main_score_label'].text = str(initial)
                    if 'score_label' in obs:
                        obs['score_label'].text = str(initial)

            # Rafraîchissement forcé de l'interface
            self.update_player_sections()  # <-- Appel explicite
            for player in self.players_data:
                if player in self.observable_widgets:
                    self.observable_widgets[player].clear_widgets()
                    self.update_player_sections()

        except Exception as e:
            self.show_warning(f"Erreur réinitialisation : {str(e)}")

    def reset_player_scores(self, player):
        """Réinitialisation ciblée avec double mise à jour"""
        try:
            for obs in self.players_data[player]['observables'].values():
                initial = obs.get('initial', 0)
                obs['score'] = initial

                # Mise à jour synchrone des deux labels
                if 'main_score_label' in obs:  # Label principal
                    obs['main_score_label'].text = str(initial)
                if 'score_label' in obs:  # Label dans la popup
                    obs['score_label'].text = str(initial)

            # Double rafraîchissement nécessaire
            self.update_observables_layout(player)
            self.update_player_sections()  # <-- Ajout crucial

        except KeyError as e:
            print(f"Joueur {player} introuvable : {str(e)}")

    def show_reset_scores_popup(self):
        """Affiche une popup demandant à l'utilisateur de confirmer la réinitialisation des scores."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(
            Label(text="Voulez-vous vraiment réinitialiser les scores de la partie en cours ?", size_hint_y=None,
                  height=40))

        # Boutons de validation/annulation
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        valider_button = Button(text="Valider")
        annuler_button = Button(text="Annuler")
        button_layout.add_widget(valider_button)
        button_layout.add_widget(annuler_button)

        content.add_widget(button_layout)

        popup = Popup(title="Confirmation", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)

        # Lorsque l'utilisateur clique sur "Valider", on réinitialise les scores et on ferme la popup
        def on_valider(instance):
            self.reset_scores()
            popup.dismiss()

        # Si l'utilisateur clique sur "Annuler", on ferme simplement la popup
        def on_annuler(instance):
            popup.dismiss()

        valider_button.bind(on_release=on_valider)
        annuler_button.bind(on_release=on_annuler)

        popup.open()

    def refresh_all_observables(self):
        for player in self.players_data:
            if 'layout' in self.players_data[player]:
                self.update_observables_layout(player)

    def go_back(self, instance):
        self.stop_timer()
        self.manager.current = 'home'

#Ecran personnalise
class FeaturesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialisation de la classe parente Screen

        # ---------------------------
        # CONFIGURATION DES COULEURS
        # ---------------------------
        self.BG_COLOR = (0.95, 0.95, 0.95, 1)  # Couleur de fond gris clair
        self.PRIMARY_COLOR = (0.13, 0.58, 0.95, 1)  # Bleu Material Design
        self.SECONDARY_COLOR = (0.2, 0.8, 0.4, 1)  # Vert Material Design
        self.TEXT_COLOR = (0.1, 0.1, 0.1, 1)  # Noir pour le texte

        # ---------------------------
        # CONFIGURATION MOBILE
        # ---------------------------
        self.spacing = dp(10)  # Espacement entre les éléments
        self.padding = dp(10)  # Marge intérieure
        self.button_height = dp(50)  # Hauteur standard des boutons
        self.font_size = dp(16)  # Taille de police de base

        # ---------------------------
        # INITIALISATION DES DONNÉES
        # ---------------------------
        self.players_data = {}  # Dictionnaire des données joueurs
        self.teams = {}  # Dictionnaire des équipes
        self.player_names = []  # Liste des noms de joueurs
        self.use_same_variables = True  # Mode variables partagées
        self.display_mode = "individual"  # Mode d'affichage initial
        self.TEAM_COLORS = {}  # Couleurs attribuées aux équipes
        self.timer_event = None  # Événement du timer
        self.hours = 0  # Heures pour le chrono
        self.minutes = 0  # Minutes pour le chrono
        self.seconds = 0  # Secondes pour le chrono
        self.is_timer_mode = True  # Mode timer/chrono

        # ---------------------------
        # BARRE SUPÉRIEURE
        # ---------------------------
        top_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[dp(15), dp(5)]
        )

        # Fond arrondi de la barre
        with top_layout.canvas.before:
            Color(*self.PRIMARY_COLOR)
            self.top_rect = RoundedRectangle(
                size=top_layout.size,
                pos=top_layout.pos,
                radius=[0, 0, dp(15), dp(15)]
            )
        top_layout.bind(pos=self.update_rect, size=self.update_rect)

        # Bouton retour
        self.back_button = Button(
            text='Retour',
            font_size=dp(16),
            size_hint_x=None,
            width=dp(50),
            background_color=(0.9, 0.9, 0.9, 1),
            color=self.TEXT_COLOR,
            border=(dp(8), dp(8), dp(8), dp(8)))
        # Configuration finale du bouton Retour
        self.back_button.bind(on_release=self.go_back)  # Liaison explicite
        top_layout.add_widget(self.back_button)

        # Affichage du timer
        self.timer_label = Label(
            text="00:00:00",
            font_size=dp(18),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_x=0.4
        )

        # Boutons de contrôle
        control_buttons = [
            ('Mode Chrono', self.switch_mode),
            ('Équipe', self.toggle_display_mode),
            ('Stats', self.toggle_team_stats)
        ]

        for text, callback in control_buttons:
            btn = Button(
                text=text,
                font_size=dp(14),
                size_hint_x=None,
                width=dp(80),
                height=self.button_height,
                background_color=self.SECONDARY_COLOR,
                color=(1, 1, 1, 1),
                border=(dp(6), dp(6), dp(6), dp(6))
            )
            if text == "Équipe":
                self.display_mode_button = btn  # Référence pour le toggle
            btn.bind(on_release=callback)
            top_layout.add_widget(btn)

            # ---------------------------
            # CONTENU PRINCIPAL SCROLLABLE
            # ---------------------------
            self.content_scroll = ScrollView(
                size_hint=(1, 1),
                bar_width=dp(6),
                bar_color=(0.5, 0.5, 0.5, 0.3),
                do_scroll_x=False  # Désactive le scroll horizontal
            )

            # Conteneur principal avec hauteur adaptative
            self.main_scroll_content = BoxLayout(
                orientation='vertical',
                spacing=self.spacing,
                size_hint_y=None,
                padding=[dp(15), dp(20), dp(15), dp(20)]
            )
            self.main_scroll_content.bind(minimum_height=self.main_scroll_content.setter('height'))

            # ---------------------------
            # INITIALISATION DES WIDGETS
            # ---------------------------
            # Layout joueurs
            self.players_layout = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=dp(10)
            )
            self.players_layout.bind(minimum_height=self.players_layout.setter('height'))

            # Layout équipes
            self.team_display_container = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=dp(10),
                height=0
            )
            self.team_display_container.bind(minimum_height=self.team_display_container.setter('height'))

            # Conteneur dynamique principal (joueurs OU équipes)
            self.dynamic_content = BoxLayout(orientation='vertical', size_hint_y=None)
            self.dynamic_content.add_widget(self.players_layout)

            # Ajout dans l'ordre correct
            self.main_scroll_content.add_widget(self.dynamic_content)  # Contenu dynamique en premier

            # ---------------------------
            # STATISTIQUES DES ÉQUIPES
            # ---------------------------
            # Conteneur principal des stats avec fond
            self.team_stats_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing=dp(2),
                padding=dp(5),
                height=dp(300)
            )

            # Configuration du fond
            with self.team_stats_container.canvas.before:
                Color(0.9, 0.9, 0.9, 1)  # Gris clair
                self.stats_bg = RoundedRectangle(
                    size=self.team_stats_container.size,
                    pos=self.team_stats_container.pos,
                    radius=[dp(10)]
                )
            self.team_stats_container.bind(
                pos=lambda inst, val: setattr(self.stats_bg, 'pos', val),
                size=lambda inst, val: setattr(self.stats_bg, 'size', val)
            )

            # En-têtes du tableau
            headers = GridLayout(
                cols=3,
                size_hint_y=None,
                height=dp(40),
                spacing=dp(2)
            )

            # Ajout des en-têtes
            for text in ["Équipe", "Total", "Moyenne"]:
                header = Label(
                    text=f"[b]{text}[/b]",
                    markup=True,
                    color=self.TEXT_COLOR,
                    font_size=dp(16),
                    bold=True)
                headers.add_widget(header)

            # ScrollView pour les données
            self.stats_scroll = ScrollView(
                size_hint=(1, 1),
                bar_width=dp(4)
            )

            self.team_stats_layout = GridLayout(
                cols=3,
                size_hint_y=None,
                spacing=dp(2),
                row_default_height=dp(300)
            )
            self.team_stats_layout.bind(minimum_height=self.team_stats_layout.setter('height'))

            self.stats_scroll.add_widget(self.team_stats_layout)

            # Assemblage final
            self.team_stats_container.add_widget(headers)
            self.team_stats_container.add_widget(self.stats_scroll)

            # Ajout au layout principal
            self.main_scroll_content.add_widget(self.team_stats_container)

            # Masquage initial
            self.team_stats_container.opacity = 0
            self.team_stats_container.disabled = True

        # ---------------------------
        # BOUTONS D'ACTION
        # ---------------------------
        action_buttons = [
            ('Démarrer le Timer', self.start_timer),
            ('Réinitialiser', lambda x: self.show_reset_scores_popup())
        ]

        for text, callback in action_buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=self.button_height,
                background_color=self.PRIMARY_COLOR,
                color=(1, 1, 1, 1),
                font_size=self.font_size,
                border=(dp(8), dp(8), dp(8), dp(8))
            )
            if text == "Démarrer le Timer":
                self.start_timer_button = btn  # Référence stockée
            btn.bind(on_release=callback)
            self.main_scroll_content.add_widget(btn)


        # ---------------------------
        # ASSEMBLAGE FINAL
        # ---------------------------
        top_layout.add_widget(self.timer_label)

        root_layout = BoxLayout(orientation='vertical', spacing=0)
        root_layout.add_widget(top_layout)
        root_layout.add_widget(self.content_scroll)

        self.content_scroll.add_widget(self.main_scroll_content)
        self.add_widget(root_layout)

        # Initialisation des joueurs
        self.update_num_players(None, "3")

    def update_rect(self, instance, value):
        """Mise à jour dynamique du fond arrondi"""
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size

    def _update_stats_bg(self, instance, value):
        self.stats_bg.pos = instance.pos
        self.stats_bg.size = instance.size

    def on_enter(self, *args):
        # Appelle la popup dès que l'utilisateur entre sur cet écran
        self.show_init_popup()

    def show_team_selection_popup(self):
        """
        Affiche une seule popup de configuration des équipes.
        L'utilisateur peut saisir un nom d'équipe, choisir les joueurs à assigner
        et visualiser la liste des équipes créées. En validant, la popup se ferme et
        la configuration des variables est lancée.
        """
        # Si self.teams n'existe pas, on l'initialise
        if not hasattr(self, 'teams'):
            self.teams = {}

        # Création du layout principal
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Titre de la popup
        layout.add_widget(Label(text="Configuration des équipes", size_hint_y=None, height=40))

        # Section de configuration d'une équipe
        team_config_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        team_config_layout.bind(minimum_height=team_config_layout.setter('height'))

        # Saisie du nom de l'équipe
        team_name_input = TextInput(hint_text="Nom de l'équipe", size_hint_y=None, height=40)
        team_config_layout.add_widget(team_name_input)

        # Instruction pour la sélection des joueurs
        team_config_layout.add_widget(
            Label(text="Sélectionnez les joueurs pour cette équipe :", size_hint_y=None, height=30))

        # Layout pour la liste des joueurs avec cases à cocher
        players_checkbox_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        players_checkbox_layout.bind(minimum_height=players_checkbox_layout.setter('height'))

        # Récupération de la liste des joueurs (préférer self.player_names s'ils existent)
        players_list = self.player_names if self.player_names else list(self.players_data.keys())
        player_checkboxes = {}
        for player in players_list:
            h_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            chk = CheckBox()
            lbl = Label(text=player, halign='left')
            h_layout.add_widget(chk)
            h_layout.add_widget(lbl)
            players_checkbox_layout.add_widget(h_layout)
            player_checkboxes[player] = chk

        # Intégrer le layout des cases à cocher dans un ScrollView
        scroll_view = ScrollView(size_hint=(1, None), height=150)
        scroll_view.add_widget(players_checkbox_layout)
        team_config_layout.add_widget(scroll_view)

        # Bouton pour ajouter l'équipe
        add_team_button = Button(text="Ajouter l'équipe", size_hint_y=None, height=40)
        team_config_layout.add_widget(add_team_button)

        layout.add_widget(team_config_layout)

        # Section d'affichage des équipes déjà créées
        created_teams_label = Label(text="Équipes créées :", size_hint_y=None, height=30)
        layout.add_widget(created_teams_label)

        created_teams_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        created_teams_layout.bind(minimum_height=created_teams_layout.setter('height'))
        teams_scroll = ScrollView(size_hint=(1, None), height=150)
        teams_scroll.add_widget(created_teams_layout)
        layout.add_widget(teams_scroll)

        # Boutons de validation ou d'annulation
        bottom_buttons = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        terminer_button = Button(text="Terminer")
        annuler_button = Button(text="Annuler")
        bottom_buttons.add_widget(terminer_button)
        bottom_buttons.add_widget(annuler_button)
        layout.add_widget(bottom_buttons)

        # Création de la popup
        popup = Popup(title="Configuration des équipes", content=layout, size_hint=(0.8, 0.8), auto_dismiss=False)

        # Callback pour ajouter une équipe
        def on_add_team(instance):
            team_name = team_name_input.text.strip()
            if not team_name:
                self.show_warning("Veuillez entrer un nom d'équipe.")
                return
            # Récupérer les joueurs sélectionnés
            selected_players = [player for player, chk in player_checkboxes.items() if chk.active]
            if not selected_players:
                self.show_warning("Veuillez sélectionner au moins un joueur.")
                return
            # Ajouter ou mettre à jour l'équipe
            self.teams[team_name] = selected_players
            # Mettre à jour l'affichage des équipes créées
            created_teams_layout.clear_widgets()
            for t_name, players in self.teams.items():
                team_label = Label(text=f"{t_name}: {', '.join(players)}", size_hint_y=None, height=30)
                created_teams_layout.add_widget(team_label)
            # Réinitialiser les champs
            team_name_input.text = ""
            for chk in player_checkboxes.values():
                chk.active = False

        add_team_button.bind(on_release=on_add_team)

        # Callback pour terminer la configuration des équipes
        def on_termine(instance):
            popup.dismiss()
            # Après configuration des équipes, on passe à la configuration des variables
            self.show_variable_setup_popup()

        # Callback pour annuler et passer directement à la configuration des variables
        def on_annuler(instance):
            popup.dismiss()
            self.show_variable_setup_popup()

        terminer_button.bind(on_release=on_termine)
        annuler_button.bind(on_release=on_annuler)

        popup.open()

    def show_more_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Voulez-vous créer une autre équipe ?", size_hint_y=None, height=40))
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        oui_button = Button(text="Oui")
        non_button = Button(text="Non")
        button_layout.add_widget(oui_button)
        button_layout.add_widget(non_button)
        content.add_widget(button_layout)
        popup = Popup(title="Nouvelle équipe", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)

        def on_oui(instance):
            popup.dismiss()
            self.show_team_config_popup()

        def on_non(instance):
            popup.dismiss()
            self.show_variable_setup_popup()

        oui_button.bind(on_release=on_oui)
        non_button.bind(on_release=on_non)
        popup.open()

    def update_teams_display(self):
        self.team_display_container.clear_widgets()
        if not self.teams:
            self.team_display_container.add_widget(Label(text="Aucune équipe créée.", size_hint_y=None, height=40))
            return

        for team, players in self.teams.items():
            # Création du conteneur principal de l'équipe
            team_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=50 + (40 * len(players)),  # Ajustement dynamique de la hauteur
                padding=5
            )

            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            team_container.bind(pos=update_rect, size=update_rect)

            # Style de l'équipe
            team_color = self.get_team_color(team)
            text_color = self.get_text_color(team_color)

            with team_container.canvas.before:
                Color(*team_color)
                team_container.rect = RoundedRectangle(
                    size=team_container.size,
                    pos=team_container.pos,
                    radius=[10]
                )

            # Titre de l'équipe aligné à gauche
            team_label = Label(
                text=f"[b]{team}[/b]",
                markup=True,
                halign='left',
                size_hint_x=1,
                size_hint_y=None,
                height=40,
                color=text_color
            )
            team_label.bind(size=team_label.setter('text_size'))
            team_container.add_widget(team_label)

            # Liste des joueurs avec boutons
            players_layout = GridLayout(
                cols=1,
                size_hint_y=None,
                height=40 * len(players),
                spacing=5
            )

            for player in players:
                # Ligne joueur + bouton
                player_row = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=40
                )

                # Nom du joueur
                player_label = Label(
                    text=f" • {player}",
                    halign='left',
                    size_hint_x=0.8,
                    color=text_color
                )
                player_label.bind(size=player_label.setter('text_size'))

                # Bouton de configuration
                config_btn = Button(
                    text="+",
                    size_hint_x=0.2,
                    background_normal='',
                    background_color=(0.9, 0.9, 0.9, 0.5),
                    color=text_color
                )
                config_btn.bind(
                    on_release=lambda instance, p=player: self.show_player_var_popup(p)
                )

                player_row.add_widget(player_label)
                player_row.add_widget(config_btn)
                players_layout.add_widget(player_row)

            self.team_display_container.height = sum([c.height for c in self.team_display_container.children])
            self.team_display_container.do_layout()

            team_container.add_widget(players_layout)
            self.team_display_container.add_widget(team_container)

    def update_team_stats_display(self):
        """
        Affiche un tableau récapitulant pour chaque équipe la somme et la moyenne
        des scores pour chaque variable.
        """
        self.team_stats_layout.clear_widgets()
        variables = self.get_variables_list()

        if not variables or not self.teams:
            no_data_label = Label(
                text="Aucune donnée disponible",
                color=self.TEXT_COLOR,
                size_hint_y=None,
                height=40
            )
            self.team_stats_layout.add_widget(no_data_label)
            return

        # Configuration des dimensions dynamiques
        HEADER_HEIGHT = dp(45)
        ROW_HEIGHT = dp(50)
        COL_WIDTH = dp(160)
        TABLE_PADDING = dp(15)

        # Calcul des dimensions
        num_rows = len(self.teams) + 1  # Ligne d'en-tête + équipes
        table_height = num_rows * ROW_HEIGHT + TABLE_PADDING * 2
        table_width = (len(variables) + 1) * COL_WIDTH + TABLE_PADDING * 2

        table = GridLayout(
            cols=len(variables) + 1,
            spacing=dp(2),
            size_hint=(None, None),
            row_default_height=ROW_HEIGHT,
            col_default_width=COL_WIDTH,
            height=table_height,
            width=table_width,
            padding=TABLE_PADDING
        )

        # Style amélioré
        HEADER_BG = (0.2, 0.4, 0.6, 1)
        ROW_EVEN = (0.97, 0.97, 0.97, 1)
        ROW_ODD = (0.92, 0.92, 0.92, 1)
        FONT_SIZE = dp(16)

        # En-tête
        header = ["Équipe"] + [f"Variable {i + 1}" for i in range(len(variables))]
        for col in header:
            lbl = Label(
                text=col.upper(),
                bold=True,
                color=(1, 1, 1, 1),
                font_size=FONT_SIZE,
                size_hint=(None, None),
                size=(COL_WIDTH, HEADER_HEIGHT)
            )
            with lbl.canvas.before:
                Color(*HEADER_BG)
                rect = Rectangle(size=lbl.size, pos=lbl.pos)
            lbl.bind(size=lambda inst, val: setattr(rect, 'size', val))
            table.add_widget(lbl)

        # Données
        for idx, team in enumerate(self.teams.keys()):
            bg_color = ROW_EVEN if idx % 2 == 0 else ROW_ODD

            # Cellule équipe
            team_lbl = Label(
                text=team,
                color=self.TEXT_COLOR,
                font_size=FONT_SIZE,
                size_hint=(None, None),
                size=(COL_WIDTH, ROW_HEIGHT)
            )
            self._add_bg_color(team_lbl, bg_color)
            table.add_widget(team_lbl)

            # Cellules statistiques
            for var in variables:
                stats = self.calculate_team_stats(team, var)
                stat_lbl = Label(
                    text=f"{stats['total']}\n{stats['moy']:.1f}",
                    color=self.TEXT_COLOR,
                    halign='right',
                    font_size=FONT_SIZE,
                    size_hint=(None, None),
                    size=(COL_WIDTH, ROW_HEIGHT)
                )
                self._add_bg_color(stat_lbl, bg_color)
                table.add_widget(stat_lbl)

        # ScrollView adaptatif
        self.stats_scrollview = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(8),
            do_scroll_x=True,
            do_scroll_y=True
        )
        self.stats_scrollview.add_widget(table)
        self.team_stats_layout.add_widget(self.stats_scrollview)

    def _add_bg_color(self, widget, color):
        """Helper pour ajouter un fond coloré"""
        with widget.canvas.before:
            Color(*color)
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
        widget.bind(
            size=lambda inst, val: setattr(inst.rect, 'size', val),
            pos=lambda inst, val: setattr(inst.rect, 'pos', val)
        )

    def toggle_team_stats(self, instance):
        """Active/désactive UNIQUEMENT le conteneur des stats"""
        if self.team_stats_container.opacity == 0:
            self.team_stats_container.opacity = 1
            self.team_stats_container.disabled = False
        else:
            self.team_stats_container.opacity = 0
            self.team_stats_container.disabled = True

    def get_team_color(self, team_name):
        if team_name not in self.TEAM_COLORS:
            self.TEAM_COLORS[team_name] = [random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1), 1]
        return self.TEAM_COLORS[team_name]

    def get_text_color(self, bg_color):
        luminance = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]
        return (0, 0, 0, 1) if luminance > 0.5 else (1, 1, 1, 1)

    def refresh_popup_scores(self, player):
        """Actualise dynamiquement tous les scores visibles dans la popup"""
        if hasattr(self, 'current_player_popup') and self.current_player_popup:
            observables = self.players_data[player]['observables']

            # Parcourir toute l'arborescence de widgets
            for widget in self.current_player_popup.content.walk():
                if isinstance(widget, ScoreLabel) and hasattr(widget, 'id'):
                    var_name = widget.id
                    if var_name in observables:
                        widget.text = f"Score: {observables[var_name]['score']}"

    def show_dependency_matrix(self, player):
        """Affiche une matrice de dépendances interactive et adaptative"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        header.add_widget(Label(text="[b]DÉPENDANCES → (Ligne dépend de la Colonne)[/b]", markup=True))
        close_btn = Button(text='×', size_hint_x=None, width=dp(40))
        close_btn.bind(on_release=lambda x: self.deps_popup.dismiss())
        header.add_widget(close_btn)
        content.add_widget(header)

        # Calcul de la taille adaptative
        variables = list(self.players_data[player]['observables'].keys())
        num_vars = len(variables)
        col_width = max(Window.width / (num_vars + 2), dp(100))  # Largeur minimum 100dp

        # Grille principale avec scroll
        scroll = ScrollView(size_hint=(1, 1), bar_width=dp(15))
        grid = GridLayout(
            cols=num_vars + 1,
            size_hint=(None, None),
            spacing=dp(2),
            row_default_height=col_width * 0.3,
            col_default_width=col_width
        )
        grid.bind(minimum_size=grid.setter('size'))

        # En-têtes de colonnes (variables cibles)
        grid.add_widget(Label(text="→", bold=True))  # Coin supérieur gauche
        for var in variables:
            grid.add_widget(Label(
                text=var,
                bold=True,
                color=(0, 0, 1, 1),
                font_size=dp(14),
                text_size=(col_width, None),
                halign='center'
            ))

        # Lignes (variables sources)
        for source_var in variables:
            # En-tête de ligne
            grid.add_widget(Label(
                text=source_var,
                bold=True,
                color=(1, 0, 0, 1),
                font_size=dp(14),
                text_size=(col_width, None),
                halign='center'
            ))

            # Cellules
            for target_var in variables:
                if source_var == target_var:
                    grid.add_widget(Label(text="---"))  # Diagonale
                else:
                    # Récupération dépendance existante
                    deps = self.players_data[player]['observables'][source_var].get('dependent_on', [])
                    dep = next((d for d in deps if d['var'] == target_var), None)

                    # Création bouton avec style conditionnel
                    btn = Button(
                        text=dep['mode'] if dep else "+",
                        font_size=dp(12),
                        background_color=self.get_dep_color(dep['mode'] if dep else None),
                        background_normal=''
                    )
                    btn.bind(on_release=partial(self.edit_dependency, player, source_var, target_var))
                    grid.add_widget(btn)

        scroll.add_widget(grid)
        content.add_widget(scroll)

        # Légende interactive
        legend = GridLayout(cols=4, size_hint_y=None, height=dp(50), spacing=dp(5))
        legend.add_widget(Label(text="[b]Légende:[/b]", markup=True))
        for mode, color in [('Somme', (0, 1, 0, 0.3)), ('Produit', (1, 0, 0, 0.3)), ('%', (0, 0, 1, 0.3))]:
            legend.add_widget(Button(
                text=mode,
                background_color=color,
                on_release=partial(self.show_help_popup, mode)
            ))
        content.add_widget(legend)

        self.deps_popup = Popup(
            title=f"Dépendances de {player}",
            content=content,
            size_hint=(0.98, 0.95),
            auto_dismiss=False
        )
        self.deps_popup.open()

    def get_dep_color(self, mode):
        """Retourne la couleur correspondant au type de dépendance"""
        return {
            'Somme': (0, 1, 0, 0.4),  # Vert
            'Produit': (1, 0, 0, 0.4),  # Rouge
            'Pourcentage': (0, 0, 1, 0.4),  # Bleu
            None: (0.9, 0.9, 0.9, 1)  # Gris
        }.get(mode, (0.8, 0.8, 0.8, 1))

    def show_help_popup(self, mode, instance):
        """Affiche l'aide contextuelle pour un type de dépendance"""
        help_text = {
            'Somme': "Score = Source + Cible",
            'Produit': "Score = Source × Cible",
            '%': "Score = (Source / Cible) × 100"
        }.get(mode, "Ajoute une relation entre les variables")

        Popup(
            title=f"Aide - {mode}",
            content=Label(text=help_text, padding=dp(20)),
            size_hint=(0.6, 0.4)
        ).open()

    def edit_dependency(self, player, source_var, target_var, instance):
        """Menu contextuel pour modifier une dépendance"""
        menu = GridLayout(cols=1, spacing=dp(5), padding=dp(10))

        options = [
            ('× Supprimer', 'Aucune', (0.9, 0.3, 0.3, 1)),
            ('+ Somme', 'Somme', (0, 0.8, 0, 1)),
            ('× Produit', 'Produit', (0.8, 0, 0, 1)),
            ('% Pourcentage', 'Pourcentage', (0, 0, 0.8, 1))
        ]

        # Création du popup AVANT la boucle
        edit_popup = Popup(
            title=f"{source_var} → {target_var}",
            content=menu,
            size_hint=(None, None),
            size=(dp(250), dp(300)))

        for text, mode, color in options:
            btn = Button(
                text=text,
                background_color=color,
                background_normal='',
                size_hint_y=None,
                height=dp(50))

            # Liaison CORRECTE avec l'ordre : instance arrive en premier automatiquement
            btn.bind(on_release=lambda _, m=mode: self.update_dependency(
                player,
                source_var,
                target_var,
                m,
                edit_popup))

            menu.add_widget(btn)

        edit_popup.open()

    def update_dependency(self, player, base_var, target_var, mode, edit_popup):
        try:
            observables = self.players_data[player]['observables']

            # Initialisation garantie des dépendances
            if 'dependent_on' not in observables[base_var]:
                observables[base_var]['dependent_on'] = []

            deps = observables[base_var]['dependent_on']

            # Suppression des anciennes dépendances pour cette cible
            deps[:] = [d for d in deps if d['var'] != target_var]

            if mode != 'Aucune':
                # Ajout avec structure claire
                deps.append({
                    'var': target_var,
                    'mode': mode,
                    'coefficient': 1.0  # Ajout optionnel pour calculs futurs
                })

                print(f"Dépendance enregistrée : {deps[-1]}")  # Debug

            # FORCER le recalcul complet
            self.recalculate_dependent_variables(player, base_var)

            # Mise à jour visuelle IMMÉDIATE
            self.deps_popup.dismiss()
            Clock.schedule_once(lambda dt: self.show_dependency_matrix(player), 0.1)

        except Exception as e:
            print(f"Erreur critique: {str(e)}")
            self.show_warning(f"Erreur: {str(e)}")

        finally:
            edit_popup.dismiss()

    def show_advanced_options(self, player):
        """Popup de configuration avancée des variables (coefficients/dépendances)"""
        try:
            # Création du layout principal
            content = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                padding=dp(15),
                size_hint=(1, 1))

            # ================= EN-TÊTE =================
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                spacing=dp(10))

            title = Label(
                text=f"[b]Options avancées - {player}[/b]",
                markup=True,
                font_size=dp(22),
                halign='left')

            close_btn = Button(
                text='×',
                font_size=dp(36),
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                background_color=(0.9, 0.2, 0.2, 1))
            close_btn.bind(on_release=lambda x: self.advanced_popup.dismiss())

            header.add_widget(title)
            header.add_widget(close_btn)
            content.add_widget(header)

            # ================= CORPS DE LA POPUP =================
            main_scroll = ScrollView(size_hint=(1, 1))

            main_layout = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=dp(10))
            main_layout.bind(minimum_height=main_layout.setter('height'))

            # Sélection de la variable
            var_spinner = Spinner(
                text='Choisir une variable',
                values=list(self.players_data[player]['observables'].keys()),
                size_hint_y=None,
                height=dp(50),
                font_size=dp(18))

            # Champs de configuration
            input_grid = GridLayout(
                cols=2,
                spacing=dp(10),
                size_hint_y=None,
                height=dp(100))

            initial_input = TextInput(
                hint_text="Valeur initiale",
                input_filter='int',
                font_size=dp(18))

            coeff_input = TextInput(
                hint_text="Coefficient",
                input_filter='int',
                font_size=dp(18))

            input_grid.add_widget(Label(text="Valeur initiale:"))
            input_grid.add_widget(initial_input)
            input_grid.add_widget(Label(text="Multiplicateur:"))
            input_grid.add_widget(coeff_input)


            # Mise à jour dynamique des champs
            def update_fields(instance, value):
                """Remplit les champs avec les valeurs existantes"""
                if value in self.players_data[player]['observables']:
                    data = self.players_data[player]['observables'][value]
                    initial_input.text = str(data.get('initial', 0))
                    coeff_input.text = str(data.get('coefficient', 1))


            var_spinner.bind(text=update_fields)

            # ================= BOUTONS ACTION =================
            btn_group = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            btn_apply = Button(
                text='Appliquer',
                background_color=(0.3, 0.7, 0.4, 1),
                on_release=lambda x: self.apply_advanced_settings(
                    player,
                    var_spinner.text,
                    initial_input.text,
                    coeff_input.text))

            btn_cancel = Button(
                text='Annuler',
                background_color=(0.9, 0.3, 0.3, 1),
                on_release=lambda x: self.advanced_popup.dismiss())

            btn_group.add_widget(btn_apply)
            btn_group.add_widget(btn_cancel)

            # Assemblage final
            main_layout.add_widget(var_spinner)
            main_layout.add_widget(input_grid)
            main_layout.add_widget(btn_group)
            main_scroll.add_widget(main_layout)
            content.add_widget(main_scroll)

            # Création de la popup
            self.advanced_popup = Popup(
                title='',
                content=content,
                size_hint=(0.85, 0.85),
                auto_dismiss=False)
            self.advanced_popup.open()

        except Exception as e:
            print(f"Erreur show_advanced_options: {str(e)}")
            self.show_warning("Erreur de configuration avancée")

    def apply_advanced_settings(self, player, var_name, initial, coeff):
        """Applique les paramètres avancés"""
        try:
            if not var_name or var_name not in self.players_data[player]['observables']:
                return

            # Conversion des valeurs
            initial = int(initial) if initial else 0
            coeff = int(coeff) if coeff else 1

            # Mise à jour des paramètres de base
            obs_data = self.players_data[player]['observables'][var_name]
            obs_data.update({
                'initial': initial,
                'coefficient': coeff,
                'score': initial + (obs_data.get('points', 0) * coeff)
            })

            # Rafraîchissement de l'interface
            if self.popup:
                self.popup.dismiss()
                self.show_player_var_popup(player)

            self.advanced_popup.dismiss()

        except ValueError:
            self.show_warning("Valeurs numériques invalides!")
        except Exception as e:
            print(f"Erreur apply_advanced_settings: {str(e)}")
            self.show_warning("Erreur d'application des paramètres")

    def get_variables_list(self):
        if not self.players_data:
            return []
        first_player = next(iter(self.players_data.values()))
        return [f"Var {i + 1}" for i in range(first_player.get('num_observables', 0))]

    def calculate_team_stats(self, team_name, var_name):
        total = 0
        count = 0
        if team_name in self.teams:
            for player in self.teams[team_name]:
                player_data = self.players_data.get(player)
                if player_data and var_name in player_data.get('observables', {}):
                    total += player_data['observables'][var_name].get('score', 0)
                    count += 1
        return {'total': total, 'moy': total / count if count > 0 else 0}

    def show_init_popup(self):
        # Popup de configuration initiale des joueurs
        def update_name_fields(num_players):
            players_layout.clear_widgets()
            name_inputs.clear()
            for i in range(num_players):
                name_input = TextInput(
                    hint_text=f"Nom du Joueur {i + 1}",
                    size_hint=(1, None),
                    height=50,
                    multiline=False
                )
                if i < len(self.player_names):
                    name_input.text = self.player_names[i]
                else:
                    name_input.text = f"Joueur {i + 1}"
                name_inputs.append(name_input)
                players_layout.add_widget(name_input)

        def change_num_players(change):
            nonlocal num_players
            num_players = max(1, min(20, num_players + change))
            num_players_label.text = f"Nombre de joueurs : {num_players}"
            update_name_fields(num_players)

        def on_confirm(instance):
            self.player_names = [name_inputs[i].text.strip() for i in range(num_players)]
            new_data = {}
            for i in range(num_players):
                if i < len(self.player_names):
                    player_name = self.player_names[i]
                else:
                    player_name = f'Joueur {i + 1}'
                if player_name in self.players_data:
                    new_data[player_name] = self.players_data[player_name]
                else:
                    new_data[player_name] = {'observables': {}, 'num_observables': 3}
            self.players_data = new_data
            self.update_num_players(None, str(num_players))
            popup.dismiss()
            Clock.schedule_once(lambda dt: self.show_optional_team_popup(), 0.2)

        num_players = 3
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))
        popup_layout.add_widget(Label(text="Choisissez le nombre de joueurs", font_size=18, size_hint_y=None, height=40))
        player_count_section = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        decrease_btn = Button(text="-", size_hint=(0.2, 1))
        decrease_btn.bind(on_release=lambda instance: change_num_players(-1))
        increase_btn = Button(text="+", size_hint=(0.2, 1))
        increase_btn.bind(on_release=lambda instance: change_num_players(1))
        num_players_label = Label(text=f"Nombre de joueurs : {num_players}", size_hint=(0.6, 1))
        player_count_section.add_widget(decrease_btn)
        player_count_section.add_widget(num_players_label)
        player_count_section.add_widget(increase_btn)
        popup_layout.add_widget(player_count_section)
        scroll_view = ScrollView(size_hint=(1, 0.7))
        players_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        players_layout.bind(minimum_height=players_layout.setter('height'))
        name_inputs = []
        update_name_fields(num_players)
        scroll_view.add_widget(players_layout)
        popup_layout.add_widget(scroll_view)
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        confirm_button = Button(text="Valider", size_hint=(0.5, 1))
        confirm_button.bind(on_release=on_confirm)
        button_layout.add_widget(confirm_button)
        cancel_button = Button(text="Annuler", size_hint=(0.5, 1))
        cancel_button.bind(on_release=lambda instance: popup.dismiss())
        button_layout.add_widget(cancel_button)
        popup_layout.add_widget(button_layout)
        popup = Popup(title="Configuration Initiale", content=popup_layout, size_hint=(0.8, 0.9), auto_dismiss=False)
        popup.open()

    def show_optional_team_popup(self):
        """Affiche une popup demandant si l'utilisateur souhaite créer des équipes."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Voulez-vous créer des équipes ?", size_hint_y=None, height=40))
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        oui_button = Button(text="Oui")
        non_button = Button(text="Non")
        button_layout.add_widget(oui_button)
        button_layout.add_widget(non_button)
        content.add_widget(button_layout)
        popup = Popup(title="Création d'équipes", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)
        def on_oui(instance):
            popup.dismiss()
            self.show_team_config_popup()  # Ouvre la popup de configuration des équipes
        def on_non(instance):
            popup.dismiss()
            self.show_variable_setup_popup()  # Passe directement à la configuration des variables
        oui_button.bind(on_release=on_oui)
        non_button.bind(on_release=on_non)
        popup.open()

    def show_team_config_popup(self):
        """Affiche une popup permettant de créer une équipe et d'y assigner des joueurs."""
        # Utilise self.player_names s'ils existent, sinon les clés de players_data
        players_list = self.player_names if self.player_names else list(self.players_data.keys())
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Configuration d'une équipe", size_hint_y=None, height=40))

        team_name_input = TextInput(hint_text="Nom de l'équipe", size_hint_y=None, height=40)
        layout.add_widget(team_name_input)

        layout.add_widget(Label(text="Sélectionnez les joueurs pour cette équipe :", size_hint_y=None, height=30))

        players_checkbox_layout = GridLayout(cols=1, size_hint_y=None)
        players_checkbox_layout.bind(minimum_height=players_checkbox_layout.setter('height'))
        player_checkboxes = {}
        for player in players_list:
            h_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            chk = CheckBox()
            lbl = Label(text=player)
            h_layout.add_widget(chk)
            h_layout.add_widget(lbl)
            players_checkbox_layout.add_widget(h_layout)
            player_checkboxes[player] = chk

        scroll_view = ScrollView(size_hint=(1, 0.5))
        scroll_view.add_widget(players_checkbox_layout)
        layout.add_widget(scroll_view)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        valider_button = Button(text="Valider")
        annuler_button = Button(text="Annuler")
        button_layout.add_widget(valider_button)
        button_layout.add_widget(annuler_button)
        layout.add_widget(button_layout)

        popup = Popup(title="Configuration des équipes", content=layout, size_hint=(0.8, 0.8), auto_dismiss=False)

        def on_valider(instance):
            team_name = team_name_input.text.strip()
            if not team_name:
                self.show_warning("Veuillez entrer un nom d'équipe.")
                return
            selected_players = [player for player, chk in player_checkboxes.items() if chk.active]
            if not selected_players:
                self.show_warning("Veuillez sélectionner au moins un joueur.")
                return
            if not hasattr(self, 'teams'):
                self.teams = {}
            # Crée la nouvelle équipe (si le nom existe déjà, il sera écrasé)
            self.teams[team_name] = selected_players
            popup.dismiss()
            self.show_warning(f"Équipe '{team_name}' créée avec : {', '.join(selected_players)}", warning_type="info")
            self.update_teams_display()
            self.update_team_stats_display()
            # Après la création de l'équipe, proposer de créer une autre équipe ou de passer à la configuration des variables.
            self.show_more_popup()

        def on_annuler(instance):
            popup.dismiss()
            self.show_variable_setup_popup()

        valider_button.bind(on_release=on_valider)
        annuler_button.bind(on_release=on_annuler)
        popup.open()

    def get_team_for_player(self, player):
        """Retourne le nom de l'équipe à laquelle appartient le joueur, ou None s'il n'en fait pas partie."""
        if hasattr(self, 'teams'):
            for team_name, players in self.teams.items():
                if player in players:
                    return team_name
        return None

    def update_num_players(self, instance, num_players_text):
        try:
            num_players = int(num_players_text)
        except (ValueError, TypeError):
            num_players = 3

        new_players_data = {}
        for i in range(num_players):
            player_name = self.player_names[i] if i < len(self.player_names) else f'Joueur {i + 1}'
            new_players_data[player_name] = self.players_data.get(
                player_name,
                {'observables': {}, 'num_observables': 3}
            )

        self.players_data = new_players_data
        self.players_layout.clear_widgets()

        # Correction : Récupération du spacing vertical seulement
        vertical_spacing = self.players_layout.spacing[1] if isinstance(self.players_layout.spacing,
                                                                        list) else self.players_layout.spacing

        player_card_height = dp(80)  # Hauteur fixe par carte
        total_height = (player_card_height + vertical_spacing) * num_players - vertical_spacing

        self.players_layout.height = total_height
        self.players_layout.minimum_height = total_height

        for player in self.players_data.keys():
            # Création de la carte joueur
            player_card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                padding=dp(15),
                spacing=dp(10)
            )

            # Création du rectangle comme attribut de la carte
            with player_card.canvas.before:
                Color(1, 1, 1, 1)
                player_card.rect = RoundedRectangle(  # Stocké dans l'instance de la carte
                    pos=player_card.pos,
                    size=player_card.size,
                    radius=[dp(8)]
                )

            # Fonction de mise à jour spécifique à chaque carte
            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            player_card.bind(pos=update_rect, size=update_rect)

            # Label du nom
            name_label = Label(
                text=player,
                font_size=dp(18),
                color=self.TEXT_COLOR,
                size_hint_x=0.7,
                halign='left'
            )

            # Bouton de configuration
            config_button = Button(
                text="+",
                font_size=dp(24),
                size_hint_x=0.3,
                background_color=(0.9, 0.9, 0.9, 1),
                color=self.TEXT_COLOR,
                border=(dp(8), dp(8), dp(8), dp(8))
            )
            config_button.bind(on_release=lambda instance, p=player: self.show_player_var_popup(p))

            player_card.add_widget(name_label)
            player_card.add_widget(config_button)
            self.players_layout.add_widget(player_card)

    def toggle_display_mode(self, instance):
        self.dynamic_content.clear_widgets()

        if self.display_mode == "individual":
            self.display_mode = "team"
            self.display_mode_button.text = "Afficher par individu"
            self.dynamic_content.add_widget(self.team_display_container)

            # Ajustements visuels
            self.team_display_container.opacity = 1
            self.team_display_container.disabled = False
            self.players_layout.opacity = 0
            self.players_layout.disabled = True

        else:
            self.display_mode = "individual"
            self.display_mode_button.text = "Afficher par équipe"
            self.dynamic_content.add_widget(self.players_layout)

            # Ajustements visuels
            self.team_display_container.opacity = 0
            self.team_display_container.disabled = True
            self.players_layout.opacity = 1
            self.players_layout.disabled = False

        # Force la mise à jour des hauteurs
        self.dynamic_content.height = self.dynamic_content.minimum_height
        self.main_scroll_content.height = self.main_scroll_content.minimum_height

    def show_variable_setup_popup(self):
        """Affiche une popup pour configurer le nombre et les noms des variables.
           Si des équipes ont été créées, les noms par défaut intègrent le nom de l'équipe du joueur.
           La création d'équipe est facultative.
        """
        # Initialiser les observables si nécessaire
        self.initialize_observables()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Configuration des Variables", size_hint_y=None, height=40, font_size=18))

        self.mode_button = Button(text="Utiliser des noms identiques pour tous les joueurs",
                                  size_hint_y=None, height=40)
        self.mode_button.bind(on_release=self.toggle_variable_mode)
        layout.add_widget(self.mode_button)

        var_count_section = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        decrease_btn = Button(text="-", size_hint=(0.2, 1))
        decrease_btn.bind(on_release=lambda instance: self.change_num_variables(-1))
        increase_btn = Button(text="+", size_hint=(0.2, 1))
        increase_btn.bind(on_release=lambda instance: self.change_num_variables(1))
        self.num_variables_label = Label(
            text=f"Nombre de variables : {self.players_data[next(iter(self.players_data))]['num_observables']}",
            size_hint=(0.6, 1))
        var_count_section.add_widget(decrease_btn)
        var_count_section.add_widget(self.num_variables_label)
        var_count_section.add_widget(increase_btn)
        layout.add_widget(var_count_section)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=10)
        self.variables_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        self.variables_layout.bind(minimum_height=self.variables_layout.setter('height'))
        scroll_view.add_widget(self.variables_layout)
        layout.add_widget(scroll_view)

        self.update_variable_inputs()

        confirm_button = Button(text="Valider", size_hint_y=None, height=40)
        confirm_button.bind(on_release=self.on_variable_setup_confirm)
        layout.add_widget(confirm_button)

        self.popup = Popup(title="Configuration des Variables", content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

        self.update_teams_display()
        self.update_team_stats_display()

    def on_variable_setup_confirm(self, instance):
        if self.use_same_variables:
            num_vars = max(player['num_observables'] for player in self.players_data.values())
            for j in range(1, num_vars + 1):
                var_input = self.variable_inputs[f'Var_{j}']
                var_name = var_input.text.strip()
                for player in self.players_data:
                    key = f'Var {j}'
                    if key in self.players_data[player]['observables']:
                        self.players_data[player]['observables'][key]['name'] = var_name or key
                        self.players_data[player]['observables'][key]['name_label'].text = var_name or key
        else:
            for player in self.players_data:
                for j in range(1, self.players_data[player]['num_observables'] + 1):
                    var_input = self.variable_inputs[f'{player}_Var_{j}']
                    var_name = var_input.text.strip()
                    key = f'Var {j}'
                    if key in self.players_data[player]['observables']:
                        self.players_data[player]['observables'][key]['name'] = var_name or key
                        self.players_data[player]['observables'][key]['name_label'].text = var_name or key

        self.refresh_all_observables()
        self.popup.dismiss()

    def refresh_all_observables(self):
        for player in self.players_data:
            if 'layout' in self.players_data[player]:
                self.update_observables_layout(player)

    def change_num_variables(self, delta):
        current_num = self.players_data[next(iter(self.players_data))]['num_observables']
        new_num = max(1, current_num + delta)
        for player in self.players_data.keys():
            self.players_data[player]['num_observables'] = new_num
            # Pour chaque variable, si elle n'existe pas, on la crée
            for j in range(1, new_num + 1):
                key = f'Var {j}'
                if key not in self.players_data[player]['observables']:
                    self.players_data[player]['observables'][key] = {
                        'score': 0,
                        'initial': 0,
                        'coefficient': 1,
                        'point': 0,
                        'name': key,  # Nom par défaut
                        'name_label': Label(text=key),
                        'score_label': Label(text="0")
                    }
            # On supprime les variables en trop, le cas échéant
            keys_to_remove = [k for k in self.players_data[player]['observables'] if int(k.split()[-1]) > new_num]
            for k in keys_to_remove:
                del self.players_data[player]['observables'][k]
        self.num_variables_label.text = f"Nombre de variables : {new_num}"
        self.update_variable_inputs()

    def toggle_variable_mode(self, instance):
        self.use_same_variables = not self.use_same_variables
        if self.use_same_variables:
            self.mode_button.text = "Utiliser des noms identiques pour tous les joueurs"
        else:
            self.mode_button.text = "Utiliser des noms différents pour chaque joueur"
        self.update_variable_inputs()

    def update_variable_inputs(self):
        """Met à jour les champs de saisie dans la popup de variables.
           Si des équipes existent, et en mode 'noms différents', le nom par défaut sera préfixé par le nom de l'équipe du joueur.
        """
        self.variables_layout.clear_widgets()
        self.variable_inputs = {}

        if self.use_same_variables:
            # Mode identique : utiliser le joueur de référence
            ref_player = next(iter(self.players_data))
            num_vars = self.players_data[ref_player]['num_observables']
            for i in range(1, num_vars + 1):
                key = f"Var {i}"
                current_name = self.players_data[ref_player]['observables'].get(key, {}).get("name", key)
                var_input = TextInput(text=current_name, size_hint_y=None, height=40)
                self.variable_inputs[f'Var_{i}'] = var_input
                self.variables_layout.add_widget(var_input)
        else:
            # Mode différent : pour chaque joueur, préfixer le nom par celui de l'équipe s'il existe
            for player in self.players_data:
                player_label = Label(text=f"Variables pour {player}:", size_hint_y=None, height=30)
                self.variables_layout.add_widget(player_label)
                num_vars = self.players_data[player]['num_observables']
                team = self.get_team_for_player(player)
                for i in range(1, num_vars + 1):
                    key = f"Var {i}"
                    default_name = f"{team} - Var {i}" if team else key
                    current_name = self.players_data[player]['observables'].get(key, {}).get("name", default_name)
                    var_input = TextInput(text=current_name, size_hint_y=None, height=40)
                    self.variable_inputs[f'{player}_Var_{i}'] = var_input
                    self.variables_layout.add_widget(var_input)

    def show_player_var_popup(self, player):
        """Popup de configuration du joueur avec toutes les fonctionnalités"""
        try:
            if player not in self.players_data:
                return

            # Création du layout principal
            content = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                padding=dp(15),
                size_hint=(1, 1))

            # ================= EN-TÊTE =================
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                spacing=dp(10))

            # Titre dynamique
            title = Label(
                text=f"[b]Configuration de {player}[/b]",
                markup=True,
                font_size=dp(22),
                halign='left',
                size_hint_x=0.8)

            # Bouton fermeture fonctionnel
            close_btn = Button(
                text='×',
                font_size=dp(36),
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                background_color=(0.9, 0.2, 0.2, 1),
                background_normal='')
            close_btn.bind(on_release=lambda x: self.popup.dismiss())

            header.add_widget(title)
            header.add_widget(close_btn)
            content.add_widget(header)

            # ================= CORPS DE LA POPUP =================
            main_scroll = ScrollView(
                size_hint=(1, 1),
                bar_width=dp(10))

            main_layout = GridLayout(
                cols=1,
                spacing=dp(15),
                size_hint_y=None,
                padding=(dp(5), dp(10)))
            main_layout.bind(minimum_height=main_layout.setter('height'))

            # Section édition du nom
            name_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            name_input = TextInput(
                text=player,
                hint_text="Nouveau nom...",
                font_size=dp(20),
                size_hint_x=0.7)
            name_input.bind(text=lambda i, v: self.update_player_name(player, v))

            name_box.add_widget(Label(text="Nom:", size_hint_x=0.3))
            name_box.add_widget(name_input)
            main_layout.add_widget(name_box)

            # Section variables avec boutons +/-
            variables_header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(40))
            variables_header.add_widget(Label(text="Variables", size_hint_x=0.6))
            variables_header.add_widget(Label(text="Score", size_hint_x=0.2))
            variables_header.add_widget(Widget(size_hint_x=0.2))  # Espacement
            main_layout.add_widget(variables_header)

            for obs_name, obs_data in self.players_data[player]['observables'].items():
                var_row = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(60),
                    spacing=dp(5))

                lbl_name = Label(
                    text=obs_name,
                    size_hint_x=0.6,
                    font_size=dp(18),
                    halign='left')

                # Création du label lié dynamiquement
                lbl_score = ScoreLabel(
                    score_value=obs_data['score'],
                    prefix="Score: ",
                    size_hint_x=0.2,
                    font_size=dp(20),
                    halign='center')

                # Stockage des références
                obs_data['score_widget'] = lbl_score
                obs_data['row_widget'] = var_row

                btn_group = BoxLayout(
                    orientation='horizontal',
                    size_hint_x=0.2,
                    spacing=dp(2))

                # Boutons avec liaison améliorée
                btn_minus = Button(text="-", font_size=dp(20))
                btn_minus.bind(
                    on_press=lambda instance, p=player, o=obs_name: self.update_score(p, o, -1)
                )

                btn_plus = Button(text="+", font_size=dp(20))
                btn_plus.bind(
                    on_press=lambda instance, p=player, o=obs_name: self.update_score(p, o, 1)
                )

                btn_group.add_widget(btn_minus)
                btn_group.add_widget(btn_plus)

                var_row.add_widget(lbl_name)
                var_row.add_widget(lbl_score)
                var_row.add_widget(btn_group)
                main_layout.add_widget(var_row)

            # ================= BOUTONS ACTION =================
            action_buttons = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                spacing=dp(10))

            # Bouton Options Avancées
            btn_advanced = Button(
                text="Options Avancées",
                background_color=(0.2, 0.6, 0.9, 1),
                on_release=lambda x: self.show_advanced_options(player))

            # Bouton Réinitialiser
            btn_reset = Button(
                text="Réinitialiser Scores",
                background_color=(0.9, 0.3, 0.3, 1),
                on_release=lambda x: self.reset_player_scores(player))

            btn_deps = Button(
                text="Dépendances",
                background_color=(0.4, 0.2, 0.8, 1),
                on_release=lambda x: self.show_dependency_matrix(player))

            action_buttons.add_widget(btn_deps)  # Ajouter à la BoxLayout existante

            action_buttons.add_widget(btn_advanced)
            action_buttons.add_widget(btn_reset)
            main_layout.add_widget(action_buttons)

            main_scroll.add_widget(main_layout)
            content.add_widget(main_scroll)

            # ================= GESTION POPUP =================
            self.popup = Popup(
                title='',
                content=content,
                size_hint=(0.9, 0.9),
                auto_dismiss=False)

            # Bouton de fermeture externe
            content.add_widget(Button(
                text="Fermer",
                size_hint_y=None,
                height=dp(50),
                on_release=lambda x: self.popup.dismiss()))

            self.popup.open()

        except Exception as e:
            print(f"Erreur show_player_var_popup: {str(e)}")
            self.show_warning("Erreur d'affichage des paramètres")

    def close_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def cleanup_popup(self, instance):
        self.popup = None

    def initialize_observables(self):
        for player in self.players_data:
            num_vars = self.players_data[player].get('num_observables', 3)
            for i in range(1, num_vars + 1):
                key = f"Var {i}"
                if key not in self.players_data[player]['observables']:
                    self.players_data[player]['observables'][key] = {
                        'score': 0,
                        'initial': 0,
                        'coefficient': 1,
                        'point': 0,
                        'name': key,  # Nom par défaut
                        'name_label': Label(text=key),
                        'score_label': Label(text="0")
                    }

    def update_observables_layout(self, player):
        layout = self.players_data[player]['layout']
        layout.clear_widgets()

        num_observables = self.players_data[player].get('num_observables', 3)
        layout.height = num_observables * 50

        for i in range(num_observables):
            key = f'Var {i + 1}'
            if key not in self.players_data[player]['observables']:
                self.players_data[player]['observables'][key] = {
                    'score': 0,
                    'initial': 0,
                    'coefficient': 1,
                    'point': 0,
                    'name': key,  # Nom par défaut
                    'name_label': Label(text=key),
                    'score_label': Label(text="0")
                }
            observable_data = self.players_data[player]['observables'][key]
            chosen_name = observable_data.get('name', key)
            observable_data['name_label'].text = chosen_name

            score_label = observable_data['score_label']
            score_label.text = str(observable_data['score'])

            btn_increase = Button(text="+", size_hint=(0.1, 0.5), height=30)
            btn_increase.bind(on_press=lambda x, p=player, o=key: self.update_score(p, o, 1))

            btn_decrease = Button(text="-", size_hint=(0.1, 0.5), height=30)
            btn_decrease.bind(on_press=lambda x, p=player, o=key: self.update_score(p, o, -1))

            layout.add_widget(observable_data['name_label'])
            layout.add_widget(score_label)
            layout.add_widget(btn_increase)
            layout.add_widget(btn_decrease)

    def set_num_observables(self, player, num_observables):
        self.players_data[player]['num_observables'] = num_observables
        self.update_observables_layout(player)

    def initialize_observable(self, player, observable, initial_value=0, coefficient=1, dependency=None,
                              dependency_mode="Somme"):
        self.players_data[player]['observables'][observable] = {
            'initial': initial_value,
            'coefficient': coefficient,
            'score': initial_value,
            'score_label': Label(text=str(initial_value)),
            'dependent_on': [],
            'dependency_mode': dependency_mode,
        }

    def show_player_config_popup(self, player):
        # Création d'un mapping pour utiliser les noms personnalisés dans le Spinner
        variable_mapping = {}
        for key, data in self.players_data[player]['observables'].items():
            variable_mapping[data.get('name', key)] = key

        spinner_values = list(variable_mapping.keys())

        # Création du layout du popup
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        variable_spinner = Spinner(
            text="Sélectionnez une variable",
            values=spinner_values,
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(variable_spinner)

        # Champs pour la valeur initiale et le coefficient
        initial_value_label = Label(text="Valeur initiale", size_hint=(1, None), height=30)
        initial_value_input = TextInput(multiline=False, size_hint=(1, None), height=50, input_filter="int")
        coefficient_label = Label(text="Coefficient", size_hint=(1, None), height=30)
        coefficient_input = TextInput(multiline=False, size_hint=(1, None), height=50, input_filter="int")
        layout.add_widget(initial_value_label)
        layout.add_widget(initial_value_input)
        layout.add_widget(coefficient_label)
        layout.add_widget(coefficient_input)

        dependency_button = Button(text="Configurer dépendances", size_hint=(1, None), height=40)
        dependency_button.bind(on_release=lambda instance: self.show_dependency_config_popup(player))
        layout.add_widget(dependency_button)

        def apply_changes(instance):
            selected_name = variable_spinner.text
            selected_key = variable_mapping.get(selected_name)
            if selected_key:
                try:
                    initial_value = int(initial_value_input.text.strip())
                except ValueError:
                    initial_value = 0
                try:
                    coefficient = int(coefficient_input.text.strip())
                except ValueError:
                    coefficient = 1

                obs = self.players_data[player]['observables'][selected_key]
                obs['initial'] = initial_value
                obs['coefficient'] = coefficient
                obs['score'] = initial_value  # Réinitialiser le score si nécessaire
                obs['score_label'].text = str(initial_value)
            popup.dismiss()

        apply_button = Button(text="Appliquer", size_hint=(1, None), height=40)
        apply_button.bind(on_release=apply_changes)
        layout.add_widget(apply_button)

        popup = Popup(title=f"Configuration du joueur {player}", content=layout, size_hint=(0.8, 0.9))
        popup.open()

    def show_dependency_config_popup(self, player):
        """
        Affiche un popup permettant de configurer les dépendances entre les variables
        observables d'un joueur sous forme de tableau avec des indications sur les axes.
        """
        try:
            # Construire un mapping : nom personnalisé -> clé d'observable
            variable_mapping = {}
            for key, obs in self.players_data[player]['observables'].items():
                # Utilise le nom enregistré (ou la clé par défaut)
                var_name = obs.get('name', key)
                variable_mapping[var_name] = key

            # Liste des noms personnalisés
            variable_names = list(variable_mapping.keys())

            # Layout principal du popup
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

            # Ajouter un titre pour les axes
            axes_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            axes_layout.add_widget(Label(text="Variables dépendantes (lignes)", size_hint_x=None, width=150))
            layout.add_widget(axes_layout)

            # Layout pour le tableau des dépendances
            num_vars = len(variable_names)
            table_layout = GridLayout(cols=num_vars + 1, size_hint_y=None)
            table_layout.height = 40 * (num_vars + 1)  # Une ligne pour les titres + une ligne par variable
            table_layout.spacing = 5

            # Première ligne : étiquette vide en première cellule
            table_layout.add_widget(Label(text=" ", size_hint_x=None, width=150))
            for var in variable_names:
                table_layout.add_widget(Label(text=f"{var} (Base)", size_hint_x=None, width=100))

            dependency_spinners = {}  # Pour garder une trace des spinners

            # Pour chaque variable en ligne (dépendante)
            for base_var in variable_names:
                # Première colonne : le nom de la variable dépendante
                table_layout.add_widget(Label(text=f"{base_var} (Dépendante)", size_hint_x=None, width=150))
                # Pour chaque variable en colonne (base)
                for dependent_var in variable_names:
                    if base_var == dependent_var:
                        table_layout.add_widget(Label(text="-", size_hint_x=None, width=100))
                    else:
                        # Récupérer le mode actuel de la dépendance depuis les données,
                        # en recherchant dans l'attribut 'dependent_on' de l'observable correspondant à base_var.
                        base_key = variable_mapping[base_var]
                        dependencies = self.players_data[player]['observables'][base_key].get('dependent_on', [])
                        current_mode = "Aucune"
                        for dep in dependencies:
                            # Comparaison sur les clés
                            if dep['var'] == variable_mapping[dependent_var]:
                                current_mode = dep.get('mode', "Aucune")
                                break

                        spinner = Spinner(
                            text=current_mode,
                            values=["Aucune", "Somme", "Produit", "Pourcentage"],
                            size_hint_x=None,
                            width=100
                        )
                        table_layout.add_widget(spinner)
                        # Enregistrer dans le dictionnaire avec la paire (base_var, dependent_var)
                        dependency_spinners[(base_var, dependent_var)] = spinner

            # Scroller pour gérer le tableau si trop grand
            scroll_view = ScrollView(size_hint=(1, 0.8))
            scroll_view.add_widget(table_layout)
            layout.add_widget(scroll_view)

            # Bouton pour appliquer les modifications
            apply_button = Button(text="Appliquer", size_hint=(1, None), height=40)

            def apply_dependencies(instance):
                """
                Applique les dépendances configurées dans le tableau.
                """
                for (base_var, dependent_var), spinner in dependency_spinners.items():
                    mode = spinner.text
                    # Récupérer les clés d'observable correspondantes
                    base_key = variable_mapping[base_var]
                    dependent_key = variable_mapping[dependent_var]
                    if mode == "Aucune":
                        # Supprimer la dépendance si le mode est "Aucune"
                        self.players_data[player]['observables'][base_key]['dependent_on'] = [
                            dep for dep in self.players_data[player]['observables'][base_key].get('dependent_on', [])
                            if dep['var'] != dependent_key
                        ]
                    else:
                        # Ajouter ou mettre à jour la dépendance
                        dependencies = self.players_data[player]['observables'][base_key].setdefault('dependent_on', [])
                        for dep in dependencies:
                            if dep['var'] == dependent_key:
                                dep['mode'] = mode  # Met à jour le mode existant
                                break
                        else:
                            # Ajouter une nouvelle dépendance
                            dependencies.append({'var': dependent_key, 'mode': mode})
                        print(f"Added/Updated dependency: {dependent_key} depends on {base_key} with mode {mode}")

                self.update_observables_layout(player)
                popup.dismiss()

            apply_button.bind(on_release=apply_dependencies)
            layout.add_widget(apply_button)

            # Création et affichage du popup
            popup = Popup(title=f"Configuration des dépendances pour {player}", content=layout, size_hint=(0.9, 0.9))
            popup.open()

        except Exception as e:
            print(f"Erreur dans show_dependency_config_popup: {e}")
            self.show_warning(f"Une erreur est survenue : {e}")

    def add_dependency(self, player, base_var, dependent_var, mode):
        """
        Ajoute une dépendance entre deux variables observables avec le mode spécifié.
        """
        if base_var == "Sélectionnez une variable de base" or dependent_var == "Sélectionnez une variable dépendante":
            self.show_warning("Veuillez sélectionner des variables valides.")
            return

        if base_var == dependent_var:
            self.show_warning("Une variable ne peut pas dépendre d'elle-même.")
            return

        if mode not in ["Somme", "Produit", "Pourcentage"]:
            self.show_warning("Mode de dépendance invalide.")
            return

        # Ajout de la dépendance
        observables = self.players_data[player]['observables']
        observables[base_var].setdefault('dependent_on', []).append({
            'var': dependent_var,
            'mode': mode
        })

        self.recalculate_dependent_variables(player, base_var)

    def on_combine_variable_change(self, spinner, variable_spinner, new_value):
        # Vérifier si la variable sélectionnée est la même que celle de base
        base_variable = variable_spinner.text
        if new_value == base_variable:
            spinner.text = ""  # Réinitialiser le choix de la variable dépendante
            # Afficher un message d'erreur ou un avertissement si nécessaire
            self.show_warning("Vous ne pouvez pas sélectionner la même variable.")

    def recalculate_dependent_variables(self, player, var_name):
        """Recalcule les scores pour toutes les variables dépendantes, y compris celles ayant plusieurs dépendances."""
        try:
            print(f"Recalculating dependencies for {var_name} (player: {player})")
            observables = self.players_data[player]['observables']

            # Empêche les boucles infinies si la variable est déjà en cours de calcul
            if 'calculating' in observables[var_name]:
                return

            # Marque la variable comme étant en cours de calcul
            observables[var_name]['calculating'] = True

            # Récupère les dépendances
            dependencies = observables[var_name].get('dependent_on', [])

            # Vérifier si des dépendances existent pour la variable
            if not dependencies:
                print(f"No dependencies found for {var_name}.")

            # Parcourt chaque dépendance
            for dependency in dependencies:
                dependent_var = dependency['var']
                mode = dependency['mode']  # Mode de la dépendance
                print(f"Processing dependency: {dependent_var} (mode: {mode})")

                if dependent_var in observables:
                    dependent_score = observables[dependent_var]['score']
                    base_score = observables[var_name]['score']

                    # Accès aux informations spécifiques de la variable dépendante
                    dependent_data = observables[var_name]  # Accède au dictionnaire de la variable dépendante
                    coefficient = dependent_data.get('coefficient', 1)
                    initial_value = dependent_data.get('initial', 0)
                    point = dependent_data.get('points', 0)

                    # Calcul de la valeur sans dépendance
                    score_without_var = point * coefficient + initial_value

                    # Affiche les scores avant calcul
                    print(f"Base score for {var_name}: {base_score}")
                    print(f"Dependent score for {dependent_var}: {dependent_score}")
                    print(f"Score without variable: {score_without_var}")

                    # Initialisation du score final pour la variable dépendante
                    new_score = dependent_score

                    # Si plusieurs dépendances, on applique chaque mode de manière appropriée
                    if mode == "Somme":
                        # Si le mode est "Somme", additionner les résultats de chaque dépendance
                        new_score += score_without_var
                    elif mode == "Produit":
                        # Si le mode est "Produit", multiplier les résultats de chaque dépendance
                        new_score *= score_without_var
                    elif mode == "Pourcentage" and score_without_var != 0:
                        # Si le mode est "Pourcentage", appliquer le pourcentage de la dépendance
                        new_score = (new_score / score_without_var) * 100
                    else:
                        new_score = new_score

                    # Mise à jour du score de la variable dépendante
                    observables[dependent_var]['score'] = new_score
                    observables[dependent_var]['score_label'].text = str(int(new_score))

                    # Affiche la mise à jour
                    print(f"Updating {dependent_var} (mode: {mode}, new_score: {new_score})")

                    # Appel récursif pour mettre à jour les dépendances de cette variable dépendante
                    self.recalculate_dependent_variables(player, dependent_var)

            # Nettoie l'indicateur de calcul
            observables[var_name].pop('calculating', None)

        except Exception as e:
            print(f"Error in recalculate_dependent_variables: {e}")

    def decalculate_dependent_variables(self, player, var_name):
        """Enlève la contribution actuelle des variables dépendantes sans recalcul immédiat."""
        try:
            print(f"Removing current contributions for dependencies of {var_name} (player: {player})")
            observables = self.players_data[player]['observables']

            # Empêche les boucles infinies si la variable est déjà en cours de calcul
            if 'calculating' in observables[var_name]:
                print(f"Skipping {var_name} to avoid infinite loop.")
                return

            # Marque la variable comme étant en cours de calcul
            observables[var_name]['calculating'] = True

            # Récupère les dépendances
            dependencies = observables[var_name].get('dependent_on', [])

            # Vérifie si des dépendances existent
            if not dependencies:
                print(f"No dependencies found for {var_name}.")
                observables[var_name].pop('calculating', None)
                return

            # Parcourt chaque dépendance
            for dependency in dependencies:
                dependent_var = dependency['var']
                mode = dependency['mode']  # Mode de la dépendance
                print(f"Processing dependency: {dependent_var} (mode: {mode})")

                if dependent_var not in observables:
                    print(f"Dependency {dependent_var} not found. Skipping.")
                    continue

                dependent_score = observables[dependent_var]['score']
                base_score = observables[var_name]['score']

                # Accès aux informations spécifiques de la variable dépendante
                dependent_data = observables[dependent_var]
                coefficient = dependent_data.get('coefficient', 1)
                initial_value = dependent_data.get('initial', 0)
                point = dependent_data.get('points', 0)

                # Calcul de la valeur actuelle de la contribution
                current_contribution = 0
                if mode == "Somme":
                    current_contribution = base_score
                elif mode == "Produit" and base_score != 0:
                    current_contribution = dependent_score / base_score
                elif mode == "Pourcentage" and base_score != 0:
                    current_contribution = (dependent_score * base_score) / 100

                # Enlève la contribution actuelle du score de la variable dépendante
                new_score = dependent_score - current_contribution
                observables[dependent_var]['score'] = max(0, new_score)  # Empêche les scores négatifs
                observables[dependent_var]['score_label'].text = str(int(new_score))
                print(f"Updated {dependent_var} (mode: {mode}, new_score: {new_score})")

                # Appel récursif pour traiter les dépendances en cascade
                self.decalculate_dependent_variables(player, dependent_var)

            # Nettoie l'indicateur de calcul
            observables[var_name].pop('calculating', None)

        except Exception as e:
            print(f"Error in decalculate_dependent_variables: {e}")
            observables[var_name].pop('calculating', None)

    def detect_cycle(self, player, start_var, target_var):
        observables = self.players_data[player]['observables']
        visited = set()

        while target_var in observables:
            if target_var in visited:
                return True  # Cycle détecté
            visited.add(target_var)
            target_var = observables[target_var].get('dependent_on')

        return False

    def update_variable_value(self, player, var_name, new_value):
            # Mettez à jour la valeur de la variable dans les données du joueur
            if var_name in self.players_data[player]['observables']:
                self.players_data[player]['observables'][var_name]['value'] = new_value

        #Modification des variables
    def apply_variable_config(self, player, observable, initial, coefficient, popup):
        if observable in self.players_data[player]['observables']:
            # Conversion des valeurs en int avec des valeurs par défaut
            initial_value = int(initial) if initial else 0
            coefficient_value = int(coefficient) if coefficient else 1

            # Mise à jour des données de l'observable
            self.players_data[player]['observables'][observable]['initial'] = initial_value
            self.players_data[player]['observables'][observable]['coefficient'] = coefficient_value

            # Mise à jour du score actuel en fonction de la valeur initiale
            self.players_data[player]['observables'][observable]['score'] = initial_value

        # Mise à jour de l'affichage des variables du joueur
        self.update_observables_layout(player)

        # Fermeture du Popup
        popup.dismiss()

    def apply_sum_dependency(self, player, var_name, combine_var):
        observables = self.players_data[player]['observables']

        # Vérifiez si la dépendance a déjà été appliquée
        if observables[var_name].get('dependent_on') == combine_var:
            return

        # Calcul de la nouvelle valeur
        dependent_score = observables[combine_var]['score']
        base_score = observables[var_name]['score']
        new_score = base_score + dependent_score

        # Mettre à jour les données
        observables[var_name]['score'] = new_score
        observables[var_name]['score_label'].text = str(int(new_score))

        # Enregistrez la dépendance
        observables[var_name]['dependent_on'] = combine_var

        # Propager les dépendances
        self.recalculate_dependent_variables(player, var_name)

    def apply_product_dependency(self, player, var_name, combine_var):
        dependent_score = self.players_data[player]['observables'][combine_var]['score']
        base_score = self.players_data[player]['observables'][var_name]['score']
        self.players_data[player]['observables'][var_name]['score'] = base_score * dependent_score
        self.update_observables_layout(player)

    def apply_percentage_dependency(self, player, var_name, combine_var):
        dependent_score = self.players_data[player]['observables'][combine_var]['score']
        base_score = self.players_data[player]['observables'][var_name]['score']
        self.players_data[player]['observables'][var_name]['score'] = (base_score / dependent_score) * 100
        self.update_observables_layout(player)

    def update_variable(self, player, var_name):
        observables = self.players_data[player]['observables']
        dependencies = self.players_data[player].get('dependencies', {})

        if var_name in dependencies:
            dependent_var = dependencies[var_name]
            if dependent_var in observables:
                base_score = observables[var_name]['score']
                dependent_score = observables[dependent_var]['score']
                mode = observables[var_name].get('dependency_mode', 'Somme')

                # Calcul du nouveau score en fonction du mode
                if mode == "Somme":
                    base_score = dependent_score + base_score
                elif mode == "Produit":
                    base_score = dependent_score * base_score
                elif mode == "Pourcentage":
                    if dependent_score != 0:
                        base_score = (base_score / dependent_score) * 100
                    else:
                        self.show_warning("Division par zéro lors du calcul de la dépendance.")
                        return

                # Mise à jour du score
                observables[var_name]['score'] = base_score
                observables[var_name]['score_label'].text = str(int(base_score))

        # Propager la mise à jour aux dépendances secondaires
        for dep_var, dep_on in dependencies.items():
            if dep_on == var_name:
                self.update_variable(player, dep_var)

    def update_score(self, player, observable, change):
        """Met à jour le score d'une observable et gère ses dépendances."""
        try:
            print(f"Updating score for {observable} (player: {player}) with change: {change}")
            obs_data = self.players_data[player]['observables'][observable]

            # Supprimer les contributions actuelles des dépendances
            self.decalculate_dependent_variables(player, observable)

            current_points = obs_data.get('points', 0)
            new_points = current_points + change
            obs_data['points'] = new_points
            print(f"New points: {new_points}")

            try:
                initial_value = float(obs_data.get('initial', 0))
            except:
                initial_value = 0
            try:
                coefficient = float(obs_data.get('coefficient', 1))
            except:
                coefficient = 1

            new_score = new_points * coefficient + initial_value
            obs_data['score'] = new_score
            print(f"New score: {new_score}")

            self.recalculate_dependent_variables(player, observable)
            obs_data['score_label'].text = str(int(new_score))

            self.update_teams_display()
            self.update_team_stats_display()
        except Exception as e:
            self.show_warning(f"Erreur lors de la mise à jour du score : {e}")

    def get_variable_value(self, player, variable_name):
        # Cette fonction récupère la valeur d'une variable pour un joueur donné
        return self.players_data[player]['observables'][variable_name]['value']

    def store_result(self, player, result, dep_mode):
        # Cette fonction stocke le résultat du calcul dans une variable
        self.players_data[player]['observables'][f"result_{dep_mode}"] = result

        #Débuter le temps lorsque nécessaire

    def show_warning(self, message, warning_type="warning"):
        # Ajoutez ici votre code pour afficher l'avertissement
        print(f"[{warning_type.upper()}] {message}")

    def switch_mode(self, instance):
        """Bascule entre les modes Timer et Chrono"""
        self.stop_timer()
        self.is_timer_mode = not self.is_timer_mode

        # Réinitialisation complète
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.timer_label.text = "00:00:00"

        # Mise à jour de l'interface
        if self.is_timer_mode:
            instance.text = "Mode Chrono"
            self.start_timer_button.text = "Démarrer le Timer"
        else:
            instance.text = "Mode Timer"
            self.start_timer_button.text = "Démarrer le Chrono"
            self.show_chrono_popup()

    def start_timer(self, instance):
        """Gère le démarrage/arrêt du timer"""
        if not self.timer_event:
            self.start_time = time.time()
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
            instance.text = "Arrêter"  # Utilise l'instance directe du bouton
        else:
            self.stop_timer()
            # Met à jour le texte selon le mode actuel
            instance.text = "Démarrer le Timer" if self.is_timer_mode else "Démarrer le Chrono"

    def show_chrono_popup(self):
        # Configuration des couleurs
        primary_color = get_color_from_hex('#2c3e50')  # Bleu foncé
        secondary_color = get_color_from_hex('#3498db')  # Bleu vif
        background_color = (1, 1, 1, 0.95)  # Blanc semi-transparent

        from kivy.metrics import dp
        # Layout principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(25),
            size_hint=(0.9, 0.7))

        # En-tête personnalisé
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10))

        title = Label(
            text="[b]DURÉE DU CHRONO[/b]",
            markup=True,
            font_size=dp(22),
            color=primary_color,
            bold=True,
            size_hint_x=0.8)

        close_btn = Button(
        text = '×',
        font_size = dp(32),
        size_hint = (None, None),
        size = (dp(50), dp(50)),
        background_color = secondary_color,
        background_normal = '')
        close_btn.bind(on_release=lambda x: popup.dismiss())

        header.add_widget(title)
        header.add_widget(close_btn)
        layout.add_widget(header)

        # Conteneur des temps
        time_container = GridLayout(
        cols = 3,
        spacing = dp(20),
        size_hint_y = 0.7)

        # Style commun pour les contrôles
        time_style = {
            'button': {
                'size_hint': (1, 0.3),
                'font_size': dp(28),
                'background_normal': '',
                'background_color': secondary_color
            },
            'label': {
                'font_size': dp(32),
                'bold': True,
                'color': primary_color
            }
        }

        # Heures
        hour_box = BoxLayout(orientation='vertical', spacing=dp(5))
        hour_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('hours', 1, hour_label),
            **time_style['button']))
        hour_label = Label(text=f"{self.hours:02}", **time_style['label'])
        hour_box.add_widget(hour_label)
        hour_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('hours', -1, hour_label),
            **time_style['button']))

        # Minutes
        minute_box = BoxLayout(orientation='vertical', spacing=dp(5))
        minute_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('minutes', 1, minute_label),
            **time_style['button']))
        minute_label = Label(text=f"{self.minutes:02}", **time_style['label'])
        minute_box.add_widget(minute_label)
        minute_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('minutes', -1, minute_label),
            **time_style['button']))

        # Secondes
        second_box = BoxLayout(orientation='vertical', spacing=dp(5))
        second_box.add_widget(Button(
            text="+",
            on_release=lambda x: self.change_time('seconds', 1, second_label),
            **time_style['button']))
        second_label = Label(text=f"{self.seconds:02}", **time_style['label'])
        second_box.add_widget(second_label)
        second_box.add_widget(Button(
            text="-",
            on_release=lambda x: self.change_time('seconds', -1, second_label),
            **time_style['button']))

        time_container.add_widget(hour_box)
        time_container.add_widget(minute_box)
        time_container.add_widget(second_box)
        layout.add_widget(time_container)


        # Séparateur visuel
        layout.add_widget(Widget(size_hint_y=None, height=dp(1)))

        # Bouton de validation
        validate_btn = Button(
            text="Valider les paramètres",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60),
            background_color=secondary_color,
            background_normal='')
        validate_btn.bind(on_release=lambda x: popup.dismiss())
        layout.add_widget(validate_btn)

        # Création du popup
        popup = Popup(
            title='',
            content=layout,
            separator_height=0)
        popup.open()

    def change_time(self, unit, increment, label):
        if unit == 'hours':
            self.hours = max(0, self.hours + increment)
            label.text = f"{self.hours}"
        elif unit == 'minutes':
            self.minutes = max(0, min(59, self.minutes + increment))
            label.text = f"{self.minutes}"
        elif unit == 'seconds':
            self.seconds = max(0, min(59, self.seconds + increment))
            label.text = f"{self.seconds}"

        # Met à jour la durée totale du chrono en secondes
        self.chrono_duration = self.hours * 3600 + self.minutes * 60 + self.seconds

    def stop_timer(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            self.start_timer_button.text = "Démarrer le Timer" if self.is_timer_mode else "Démarrer le Chrono"

    def update_timer(self, dt):
        """Met à jour l'affichage du timer/chrono"""
        if self.is_timer_mode:
            self.start_time += 1
        else:
            self.start_time -= 1
            if self.start_time <= 0:
                self.stop_timer()

        minutes, seconds = divmod(abs(self.start_time), 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.text = f"{'Timer' if self.is_timer_mode else 'Chrono'}: {hours:02}:{minutes:02}:{seconds:02}"

        # Changer nom de l'archive

    def change_time(self, unit, increment, label):
        if unit == 'hours':
            self.hours = max(0, self.hours + increment)
            label.text = f"Heures: {self.hours}"
        elif unit == 'minutes':
            self.minutes = max(0, min(59, self.minutes + increment))
            label.text = f"Minutes: {self.minutes}"
        elif unit == 'seconds':
            self.seconds = max(0, min(59, self.seconds + increment))
            label.text = f"Secondes: {self.seconds}"
        self.chrono_duration = self.hours * 3600 + self.minutes * 60 + self.seconds

    def reset_scores(self):
        """Réinitialise les scores de toutes les observables de tous les joueurs."""
        try:
            for player, pdata in self.players_data.items():
                for key, obs in pdata['observables'].items():
                    # Réinitialise les points à 0
                    obs['points'] = 0
                    # Le nouveau score est la valeur initiale + (0 * coefficient)
                    initial_value = obs.get('initial', 0)
                    obs['score'] = initial_value
                    # Mettre à jour le label affichant le score
                    obs['score_label'].text = str(initial_value)
            # Si des layouts de variables sont affichés, les mettre à jour
            self.refresh_all_observables()
        except Exception as e:
            self.show_warning(f"Erreur lors de la réinitialisation des scores : {e}")

        #Changer nom de l'archive

    def show_reset_scores_popup(self):
        """Affiche une popup demandant à l'utilisateur de confirmer la réinitialisation des scores."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(
            Label(text="Voulez-vous vraiment réinitialiser les scores de la partie en cours ?", size_hint_y=None,
                  height=40))

        # Boutons de validation/annulation
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        valider_button = Button(text="Valider")
        annuler_button = Button(text="Annuler")
        button_layout.add_widget(valider_button)
        button_layout.add_widget(annuler_button)

        content.add_widget(button_layout)

        popup = Popup(title="Confirmation", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)

        # Lorsque l'utilisateur clique sur "Valider", on réinitialise les scores et on ferme la popup
        def on_valider(instance):
            self.reset_scores()
            popup.dismiss()

        # Si l'utilisateur clique sur "Annuler", on ferme simplement la popup
        def on_annuler(instance):
            popup.dismiss()

        valider_button.bind(on_release=on_valider)
        annuler_button.bind(on_release=on_annuler)

        popup.open()

        #Retourner sur la page principale

    def go_back(self, instance):
        """Gestion correcte du retour à l'écran précédent"""
        self.stop_timer()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'

#Ecran d'archive
class ArchivesScreen(Screen):
    def __init__(self, **kwargs):
        super(ArchivesScreen, self).__init__(**kwargs)
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
            "Archives des parties précédentes\n"
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

#Pour la synchro
class ScoreLabel(Label):
    """Label spécial pour la mise à jour automatique des scores"""
    score_value = NumericProperty(0)
    prefix = StringProperty("")

    def on_score_value(self, instance, value):
        self.text = f"{self.prefix}{value}"

# Application principale
class MyApp(App):
    def build(self):
        return MyScreenManager()

# Point d'entrée
if __name__ == '__main__':
    MyApp().run()
