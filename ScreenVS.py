from datetime import datetime
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore


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

        # Layout principal
        main_layout = BoxLayout(orientation='vertical')

        # Layout supérieur (bouton retour et timer)
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0))
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        self.timer_label = Label(text="Timer: 00:00", font_size=24, size_hint=(0.6, 1))
        top_layout.add_widget(self.timer_label)

        self.mode_button = Button(text="Chrono", size_hint=(0.2, 1))
        self.mode_button.bind(on_release=self.switch_mode)
        top_layout.add_widget(self.mode_button)

        main_layout.add_widget(top_layout)

        # Layout des joueurs
        self.players_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, 0.8))
        for player, color in zip(self.players_data.keys(), [(0.8, 0.3, 0.3, 1), (0.3, 0.3, 0.8, 1)]):
            player_layout = self.create_player_section(player, color)
            self.players_layout.add_widget(player_layout)

        main_layout.add_widget(self.players_layout)

        # Layout des boutons (démarrer le timer, archiver les données)
        buttons_layout = BoxLayout(orientation='horizontal', spacing=1, padding=1, size_hint_y=None, height=50)

        self.start_timer_button = Button(text="Démarrer le Timer", size_hint=(0.5, 1))
        self.start_timer_button.bind(on_release=self.start_timer)
        buttons_layout.add_widget(self.start_timer_button)

        archive_button = Button(text="Archiver les Données", size_hint=(0.5, 1))
        archive_button.bind(on_release=self.archive_data)
        buttons_layout.add_widget(archive_button)

        main_layout.add_widget(buttons_layout)
        self.add_widget(main_layout)

    def on_enter(self):
        """ S'exécute lorsque l'utilisateur entre sur l'écran """
        self.show_player_setup_popup()

    def show_player_setup_popup(self):
        """ Affiche une popup pour configurer les noms des joueurs """
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))
        popup_layout.add_widget(Label(text="Choisissez le nom des joueurs", font_size=18, size_hint_y=None, height=40))

        self.player_inputs = {}
        for player in self.players_data.keys():
            player_label = Label(text=f"Nom du {player} :", size_hint_y=None, height=30)
            popup_layout.add_widget(player_label)
            player_input = TextInput(text=player, size_hint_y=None, height=40)
            self.player_inputs[player] = player_input
            popup_layout.add_widget(player_input)

        confirm_button = Button(text="Valider", size_hint_y=None, height=40)
        confirm_button.bind(on_release=self.on_player_setup_confirm)
        popup_layout.add_widget(confirm_button)

        self.popup = Popup(title="Configuration des Joueurs", content=popup_layout, size_hint=(0.8, 0.8))
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
        """ Affiche une popup pour configurer le nombre et les noms des variables """
        self.use_same_variables = True  # Par défaut, les mêmes noms sont utilisés pour tous les joueurs

        # Layout principal de la popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Titre
        layout.add_widget(Label(text="Configuration des Variables", size_hint_y=None, height=40, font_size=18))

        # Bouton pour basculer entre les modes
        self.mode_button = Button(text="Utiliser des noms identiques pour tous les joueurs",
                                  size_hint_y=None, height=40)
        self.mode_button.bind(on_release=self.toggle_variable_mode)
        layout.add_widget(self.mode_button)

        # Section pour modifier le nombre de variables
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

        # ScrollView pour les champs de saisie
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=10)

        # Layout contenant les inputs des variables
        self.variables_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        self.variables_layout.bind(minimum_height=self.variables_layout.setter('height'))
        scroll_view.add_widget(self.variables_layout)
        layout.add_widget(scroll_view)

        # Ajout initial des inputs des variables
        self.update_variable_inputs()

        # Bouton pour valider
        confirm_button = Button(text="Valider", size_hint_y=None, height=40)
        confirm_button.bind(on_release=self.on_variable_setup_confirm)
        layout.add_widget(confirm_button)

        self.popup = Popup(title="Configuration des Variables", content=layout, size_hint=(0.8, 0.8))
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
        variable_names = set()  # Pour vérifier les doublons
        invalid_names = []  # Pour suivre les noms invalides

        if self.use_same_variables:
            # Utilise les mêmes noms pour tous les joueurs
            for i in range(self.players_data[next(iter(self.players_data))]['num_observables']):
                var_name = self.variable_inputs[f'Var_{i + 1}'].text.strip()
                if not var_name or var_name in variable_names:
                    invalid_names.append(var_name)
                else:
                    variable_names.add(var_name)

            if invalid_names:
                self.show_error_popup(f"Noms de variables invalides ou dupliqués : {', '.join(invalid_names)}")
                return

            for player in self.players_data.keys():
                self.players_data[player]['observables'] = {name: {'score': 0} for name in variable_names}
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
        """ Met à jour l'affichage des sections des joueurs avec les variables et leurs scores """
        for player, data in self.players_data.items():
            if player not in self.observable_widgets:
                print(f"Le joueur '{player}' n'a pas de layout dans observable_widgets.")
                self.observable_widgets[player] = BoxLayout(orientation='vertical', size_hint_y=None)

            player_vars_layout = self.observable_widgets[player]
            player_vars_layout.clear_widgets()  # Réinitialise les widgets des variables

            for var_name, var_data in data['observables'].items():
                var_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)

                var_label = Label(text=f"{var_name}:", size_hint_x=0.6, size_hint_y=None, height=50)
                var_score = Label(text=str(var_data['score']), size_hint_x=0.2, size_hint_y=None, height=50)

                var_layout.add_widget(var_label)
                var_layout.add_widget(var_score)

                player_vars_layout.add_widget(var_layout)

    def create_player_section(self, player, color):
        """ Crée une section pour un joueur avec une ScrollView pour les variables """
        # Layout principal pour chaque joueur
        player_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_x=0.5)

        with player_layout.canvas.before:
            Color(*color)
            player_layout.rect = Rectangle(size=player_layout.size, pos=player_layout.pos)
            player_layout.bind(
                size=lambda _, val: setattr(player_layout.rect, 'size', val),
                pos=lambda _, val: setattr(player_layout.rect, 'pos', val),
            )

        # Layout horizontal pour le nom du joueur et le bouton de configuration
        name_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # TextInput pour afficher et modifier le nom du joueur
        name_input = Label(text=player, font_size=22, size_hint_y=None, height=40)
        self.player_name_widgets[player] = name_input  # Lien entre le joueur et son widget
        name_button_layout.add_widget(name_input)

        # Bouton pour ouvrir la configuration dans une popup
        config_button = Button(
            background_normal="./image/bouton_parametre.png",
            background_down="./image/bouton_parametre.png",
            size_hint_x=0.12,
            size_hint_y=None,
            height=50,
            border=(0, 0, 0, 0),
            size=(name_input.height, name_input.height)  # La même hauteur que le champ de texte
        )
        config_button.bind(on_release=lambda instance, p=player: self.show_player_var_popup(p))
        name_button_layout.add_widget(config_button)

        player_layout.add_widget(name_button_layout)

        # Layout pour les variables
        player_vars_layout = BoxLayout(orientation='vertical', spacing=1, padding=1, size_hint_y=0.2, height=40)
        player_vars_layout.bind(minimum_height=player_vars_layout.setter('height'))

        # ScrollView pour les variables
        vars_scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        vars_scroll.add_widget(player_vars_layout)

        player_layout.add_widget(vars_scroll)

        # Stockage des widgets pour les observables
        self.observable_widgets[player] = player_vars_layout

        return player_layout

    def show_player_var_popup(self, player):
        """ Affiche une popup pour configurer les variables et les scores du joueur. """
        # Si une popup est déjà ouverte, la fermer avant d'en créer une nouvelle
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
            self.popup = None

        # Nettoyer le layout existant dans players_data pour éviter les conflits
        if 'layout' in self.players_data[player]:
            old_layout = self.players_data[player].pop('layout', None)
            if old_layout:
                old_layout.clear_widgets()

        # Conteneur principal de la popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))

        # Conteneur principal pour le joueur
        main_player_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        main_player_layout.bind(minimum_height=main_player_layout.setter('height'))

        # Ligne d'informations avec le TextInput, le Spinner et le bouton d'image
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        # Champ de texte pour le nom
        name_input = TextInput(
            text=player,
            font_size=16,
            size_hint_x=0.5,
            multiline=False,
            hint_text="Nom du joueur"
        )
        name_input.bind(text=self.on_name_change)
        info_layout.add_widget(name_input)

        # Spinner pour le nombre d'observables
        spinner = Spinner(
            text=str(self.players_data[player].get('num_observables', 3)),  # Par défaut, 3 observables
            values=[str(i) for i in range(1, 6)],
            size_hint_x=0.2,
            size_hint_y=None,
            height=50
        )
        spinner.bind(
            text=lambda instance, val, p=player: self.set_num_observables(p, int(val))
            # Mise à jour du nombre d'observables
        )
        info_layout.add_widget(spinner)

        # Bouton d'image pour la configuration
        config_button = Button(
            background_normal="./image/bouton_parametre.png",
            background_down="./image/bouton_parametre.png",
            size_hint_x=0.09,
            size_hint_y=None,
            height=50,
            border=(0, 0, 0, 0)
        )
        config_button.bind(on_release=lambda instance, p=player: self.show_player_config_popup(p))
        info_layout.add_widget(config_button)

        # Ajouter le layout des informations au layout principal
        main_player_layout.add_widget(info_layout)

        # Conteneur vertical pour les variables du joueur
        variables_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
        )
        self.players_data[player]['layout'] = variables_layout

        # Mettre à jour les observables et les afficher dans la popup
        self.update_observables_layout(player)

        # Ajouter le layout des variables au layout principal
        main_player_layout.add_widget(variables_layout)

        # Ajouter un ScrollView pour gérer le défilement si nécessaire
        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(main_player_layout)
        content.add_widget(scroll_view)

        # Bouton pour fermer la popup
        close_button = Button(
            text="Fermer",
            size_hint_y=None,
            height=50
        )
        close_button.bind(on_release=self.close_popup)
        content.add_widget(close_button)

        # Créer et afficher la popup
        self.popup = Popup(
            title=f"Paramètres de {player}",
            content=content,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        self.popup.bind(on_dismiss=self.cleanup_popup)
        self.popup.open()

    def show_player_config_popup(self, player):
        """
        Affiche un popup permettant de configurer les variables d'un joueur, notamment leur valeur initiale,
        leur coefficient, et leurs dépendances.
        """
        # Création du layout principal du popup
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Spinner pour sélectionner une variable à configurer
        variable_spinner = Spinner(
            text="Sélectionnez une variable",
            values=list(self.players_data[player]['observables'].keys()),
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(variable_spinner)

        # Champs pour configurer la valeur initiale et le coefficient
        initial_value_label = Label(text="Valeur initiale", size_hint=(1, None), height=30)
        initial_value_input = TextInput(multiline=False, size_hint=(1, None), height=50, input_filter="int")
        coefficient_label = Label(text="Coefficient", size_hint=(1, None), height=30)
        coefficient_input = TextInput(multiline=False, size_hint=(1, None), height=50, input_filter="int")
        layout.add_widget(initial_value_label)
        layout.add_widget(initial_value_input)
        layout.add_widget(coefficient_label)
        layout.add_widget(coefficient_input)

        # Bouton pour configurer les dépendances
        dependency_button = Button(text="Configurer dépendances", size_hint=(1, None), height=40)
        dependency_button.bind(on_release=lambda instance: self.show_dependency_config_popup(player))
        layout.add_widget(dependency_button)

        # Bouton pour appliquer les modifications
        apply_button = Button(text="Appliquer", size_hint=(1, None), height=40)
        layout.add_widget(apply_button)

        # Création du popup
        popup = Popup(title=f"Configuration du joueur {player}", content=layout, size_hint=(0.8, 0.9))

        def update_fields(spinner, text):
            """Mise à jour des champs lorsque l'utilisateur change de variable."""
            if text and text in self.players_data[player]['observables']:
                observable_data = self.players_data[player]['observables'][text]
                initial_value_input.text = str(observable_data.get('initial', 0))
                coefficient_input.text = str(observable_data.get('coefficient', 1))
                apply_button.disabled = False
            else:
                initial_value_input.text = ""
                coefficient_input.text = ""
                apply_button.disabled = True

        def apply_changes(instance):
            """Applique les modifications saisies dans les champs."""
            selected_variable = variable_spinner.text
            if selected_variable in self.players_data[player]['observables']:
                try:
                    # Conversion des entrées
                    initial_value = int(initial_value_input.text)
                    coefficient = int(coefficient_input.text)

                    # Mise à jour des données de la variable
                    observable_data = self.players_data[player]['observables'][selected_variable]
                    observable_data['initial'] = initial_value
                    observable_data['coefficient'] = coefficient
                    observable_data['score'] = initial_value  # Réinitialise le score

                    # Met à jour l'affichage des variables
                    self.update_observables_layout(player)

                    # Ferme le popup après validation
                    popup.dismiss()
                except ValueError:
                    self.show_warning("Veuillez entrer des valeurs valides pour la configuration.")

        # Liaison des événements
        variable_spinner.bind(text=update_fields)
        apply_button.bind(on_release=apply_changes)

        # Désactiver le bouton Appliquer par défaut
        apply_button.disabled = True

        # Affichage du popup
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

            # Mise à jour de l'affichage du score avec la valeur initiale
            var_score.text = str(observable_data['score'])

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

    def show_dependency_config_popup(self, player):
        """
        Affiche un popup permettant de configurer les dépendances entre les variables
        observables d'un joueur sous forme de tableau avec des indications sur les axes.
        """
        try:
            # Récupérer les variables observables du joueur
            variables = list(self.players_data[player]['observables'].keys())

            # Layout principal du popup
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

            # Ajouter un titre pour les axes
            axes_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            axes_layout.add_widget(Label(text="Variables dépendantes (lignes)", size_hint_x=None, width=150))
            layout.add_widget(axes_layout)

            # Layout pour le tableau des dépendances
            table_layout = GridLayout(cols=len(variables) + 1, size_hint_y=None)
            table_layout.height = 40 * (len(variables) + 1)  # Une ligne pour les noms + chaque variable
            table_layout.spacing = 5

            # Ajouter la première ligne avec les noms des colonnes
            table_layout.add_widget(Label(text=" ", size_hint_x=None, width=150))  # Coin vide
            for var in variables:
                table_layout.add_widget(Label(text=f"{var} (Base)", size_hint_x=None, width=100))

            # Ajouter une ligne pour chaque variable
            dependency_spinners = {}  # Dictionnaire pour garder une trace des spinners
            for base_var in variables:
                # Ajouter l'étiquette de la ligne
                table_layout.add_widget(Label(text=f"{base_var} (Dépendante)", size_hint_x=None, width=150))

                for dependent_var in variables:
                    if base_var == dependent_var:
                        # Ajouter une cellule vide si la variable est la même
                        table_layout.add_widget(Label(text="-", size_hint_x=None, width=100))
                    else:
                        # Déterminer le mode actuel de la dépendance
                        dependencies = self.players_data[player]['observables'][base_var].get('dependent_on', [])
                        current_mode = "Aucune"
                        for dep in dependencies:
                            if dep['var'] == dependent_var:
                                current_mode = dep.get('mode', "Aucune")
                                break

                        # Ajouter un spinner pour configurer la dépendance
                        spinner = Spinner(
                            text=current_mode,
                            values=["Aucune", "Somme", "Produit", "Pourcentage"],
                            size_hint_x=None,
                            width=100
                        )
                        table_layout.add_widget(spinner)
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
                    if mode == "Aucune":
                        # Supprimer la dépendance si le mode est "Aucune"
                        self.players_data[player]['observables'][base_var]['dependent_on'] = [
                            dep for dep in self.players_data[player]['observables'][base_var].get('dependent_on', [])
                            if dep['var'] != dependent_var
                        ]
                    else:
                        # Ajouter ou mettre à jour la dépendance
                        dependencies = self.players_data[player]['observables'][base_var].setdefault('dependent_on', [])
                        for dep in dependencies:
                            if dep['var'] == dependent_var:
                                dep['mode'] = mode  # Mettre à jour le mode existant
                                break
                        else:
                            # Ajouter une nouvelle dépendance si elle n'existe pas
                            dependencies.append({'var': dependent_var, 'mode': mode})

                        print(
                            f"Added/Updated dependency: {dependent_var} depends on {base_var} with mode {mode}")  # Log

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

            # Mettre à jour les points
            points = obs_data.get('points', 0) + change
            obs_data['points'] = points
            print(f"New points calculated: {points}")

            # Calculer le nouveau score
            initial_value = obs_data.get('initial', 0)
            coefficient = obs_data.get('coefficient', 1)
            new_score = points * coefficient + initial_value
            obs_data['score'] = new_score
            print(f"New score calculated: {new_score}")

            # Recalculer les dépendances
            self.recalculate_dependent_variables(player, observable)

            # Mise à jour visuelle
            obs_data['score_label'].text = str(int(new_score))

        except Exception as e:
            self.show_warning(f"Erreur lors de la mise à jour du score : {e}")

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
        # Création du layout du popup
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Layout pour les heures, minutes, secondes
        time_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        time_layout.bind(minimum_height=time_layout.setter('height'))

        # Heures
        hour_layout = BoxLayout(orientation='vertical')
        hour_label = Label(text=f"Heures: {self.hours}", size_hint_y=None, height=40)
        increase_hour = Button(text="+", size_hint_y=None, height=40)
        decrease_hour = Button(text="-", size_hint_y=None, height=40)
        increase_hour.bind(on_release=lambda x: self.change_time('hours', 1, hour_label))
        decrease_hour.bind(on_release=lambda x: self.change_time('hours', -1, hour_label))
        hour_layout.add_widget(increase_hour)
        hour_layout.add_widget(hour_label)
        hour_layout.add_widget(decrease_hour)

        # Minutes
        minute_layout = BoxLayout(orientation='vertical')
        minute_label = Label(text=f"Minutes: {self.minutes}", size_hint_y=None, height=40)
        increase_minute = Button(text="+", size_hint_y=None, height=40)
        decrease_minute = Button(text="-", size_hint_y=None, height=40)
        increase_minute.bind(on_release=lambda x: self.change_time('minutes', 1, minute_label))
        decrease_minute.bind(on_release=lambda x: self.change_time('minutes', -1, minute_label))
        minute_layout.add_widget(increase_minute)
        minute_layout.add_widget(minute_label)
        minute_layout.add_widget(decrease_minute)

        # Secondes
        second_layout = BoxLayout(orientation='vertical')
        second_label = Label(text=f"Secondes: {self.seconds}", size_hint_y=None, height=40)
        increase_second = Button(text="+", size_hint_y=None, height=40)
        decrease_second = Button(text="-", size_hint_y=None, height=40)
        increase_second.bind(on_release=lambda x: self.change_time('seconds', 1, second_label))
        decrease_second.bind(on_release=lambda x: self.change_time('seconds', -1, second_label))
        second_layout.add_widget(increase_second)
        second_layout.add_widget(second_label)
        second_layout.add_widget(decrease_second)

        # Ajout des sections au layout principal
        time_layout.add_widget(hour_layout)
        time_layout.add_widget(minute_layout)
        time_layout.add_widget(second_layout)
        layout.add_widget(time_layout)

        # Bouton pour fermer le popup
        close_button = Button(text="Fermer", size_hint_y=None, height=40)
        close_button.bind(on_release=lambda x: popup.dismiss())
        layout.add_widget(close_button)

        # Création et ouverture du popup
        popup = Popup(title="Réglage de la durée du Chrono", content=layout, size_hint=(0.8, 0.8))
        popup.open()

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

    def archive_data(self, instance):
        """Affiche un popup pour saisir le nom de l'archive."""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label de titre
        label = Label(text="Entrez le nom de l'archive :", size_hint_y=None, height=40)
        layout.add_widget(label)

        # Champ de saisie du nom de l'archive
        archive_name_input = TextInput(text="", font_size=16, size_hint_y=None, height=40)
        layout.add_widget(archive_name_input)

        # Bouton pour archiver
        confirm_button = Button(text="Archiver", size_hint_y=None, height=50)
        confirm_button.bind(on_release=lambda x: self.save_archive(archive_name_input.text, popup))
        layout.add_widget(confirm_button)

        # Popup pour saisir le nom
        popup = Popup(title="Choisir un nom d'archive", content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def save_archive(self, custom_name, popup):
        """Crée et enregistre une archive au même endroit que précédemment, dans un répertoire 'archives'."""
        archive_dir = 'archives'

        # 🗂️ Initialisation du fichier de stockage JSON pour garantir la persistance
        store = JsonStore(f'{archive_dir}/temp.json')

        # 🗂️ Si l'utilisateur n'a pas défini de nom, on génère un nom par défaut avec la date/heure
        if not custom_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"archive_Duel_{timestamp}"
        else:
            archive_name = custom_name

        # 📅 Obtenir la date et l'heure actuelles
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 📁 Créer le chemin complet de l'archive
        archive_path = f'{archive_dir}/{archive_name}.txt'

        # ⚙️ Formater les données des joueurs
        cleaned_players_data = {}
        for player, data in self.players_data.items():
            cleaned_players_data[player] = {
                'observables': {obs_name: {'score': obs_data['score']} for obs_name, obs_data in
                                data['observables'].items()}
            }

        # 📝 Sauvegarder les données dans le fichier au format texte
        try:
            # Écrire les données au format texte dans le fichier
            with open(archive_path, 'w', encoding='utf-8') as f:
                # Écrire "Duel" pour indiquer le mode et la date
                f.write("Duel\n")
                f.write(f"Date et heure : {date_heure}\n\n")

                # Écrire les données des joueurs
                for player, data in cleaned_players_data.items():
                    f.write(f"¤{player}\n")
                    for obs_name, obs_data in data['observables'].items():
                        f.write(f"  £{obs_name}£: {obs_data['score']}\n")
                    f.write(f"\n")

            print(f"✅ Données archivées dans : {archive_path}")
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'archive : {e}")

        # Fermer le popup après l'archivage
        popup.dismiss()

    def go_back(self, instance):
        self.stop_timer()
        self.manager.current = 'home'
