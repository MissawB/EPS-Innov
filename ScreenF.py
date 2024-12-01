import os
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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import logging
logging.basicConfig(level=logging.DEBUG)

################################ Écran des fonctionnalités ################################################
class FeaturesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.players_data = {}
        self.timer_event = None
        self.start_time = 0
        self.chrono_duration = 0
        self.is_timer_mode = True
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        main_layout = BoxLayout(orientation='vertical')
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Bouton de retour
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        # Label de Timer/Chrono
        self.timer_label = Label(text="Timer: 00:00", font_size=24, size_hint=(0.4, 1))
        top_layout.add_widget(self.timer_label)

        # Bouton de mode
        self.mode_button = Button(text="Mode Chrono", size_hint_x=0.2, height=50)
        self.mode_button.bind(on_release=self.switch_mode)
        top_layout.add_widget(self.mode_button)

        main_layout.add_widget(top_layout)

        # ScrollView pour le contenu
        main_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 50))
        main_scroll_content = BoxLayout(orientation='vertical', size_hint_y=None)
        main_scroll_content.bind(minimum_height=main_scroll_content.setter('height'))

        # Spinner pour le nombre de joueurs
        self.num_players_spinner = Spinner(text="3", values=["1", "2", "3", "4", "5"], size_hint=(1, None), height=50)
        self.num_players_spinner.bind(text=self.update_num_players)
        main_scroll_content.add_widget(self.num_players_spinner)

        self.players_layout = GridLayout(cols=1, padding=20, spacing=10, size_hint_y=None)
        self.players_layout.bind(minimum_height=self.players_layout.setter('height'))
        main_scroll_content.add_widget(self.players_layout)

        self.start_timer_button = Button(text="Démarrer le Timer", size_hint=(1, None), height=50)
        self.start_timer_button.bind(on_release=self.start_timer)
        main_scroll_content.add_widget(self.start_timer_button)

        archive_button = Button(text="Archiver les Données", size_hint=(1, None), height=50)
        archive_button.bind(on_release=self.archive_data)
        main_scroll_content.add_widget(archive_button)

        main_scroll_view.add_widget(main_scroll_content)
        main_layout.add_widget(main_scroll_view)

        self.add_widget(main_layout)
        self.update_num_players(None, "3")

    from kivy.uix.button import Button

    def update_num_players(self, instance, num_players_text):
        try:
            num_players = int(num_players_text)
        except (ValueError, IndexError):
            num_players = 3

        self.players_data = {
            f'Joueur {i + 1}': {
                'observables': {},
                'num_observables': 3,
                'dependencies': {}
            }
            for i in range(num_players)
        }
        self.players_layout.clear_widgets()

        for player in self.players_data.keys():
            main_player_layout = BoxLayout(orientation='vertical', padding=(0, 5), size_hint_y=None)
            main_player_layout.bind(minimum_height=main_player_layout.setter('height'))
            info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)

            name_input = TextInput(text=player, font_size=16, size_hint_x=0.4)
            name_input.bind(text=self.on_name_change)
            info_layout.add_widget(name_input)

            spinner = Spinner(text="3", values=[str(i) for i in range(1,8)], size_hint_x=0.1)
            spinner.bind(text=lambda instance, val, p=player: self.set_num_observables(p, int(val)))
            info_layout.add_widget(spinner)

            # Bouton avec une image au lieu du texte "Configurer"
            config_button = Button(
                background_normal="/Users/bahma/.spyder-py3/EPS'Innov/image/bouton_parametre.png",  # Chemin de l'image
                size_hint_x=0.1,
                background_down="/Users/bahma/.spyder-py3/EPS'Innov/image/bouton_parametre.png",  # Optionnel : même image lors du clic
                border=(0, 0, 0, 0)  # Supprime les bordures
            )
            config_button.bind(on_release=lambda instance, p=player: self.show_player_config_popup(p))
            info_layout.add_widget(config_button)

            main_player_layout.add_widget(info_layout)
            variables_layout = GridLayout(cols=4, size_hint_y=None, padding=5, spacing=2)
            self.players_data[player]['layout'] = variables_layout
            main_player_layout.add_widget(variables_layout)
            self.update_observables_layout(player)
            self.players_layout.add_widget(main_player_layout)

    def on_name_change(self, instance, value):
        for player in list(self.players_data.keys()):
            if instance in self.players_data[player]['layout'].children:
                self.players_data[value] = self.players_data.pop(player)
                break

    def set_num_observables(self, player, num_observables):
        self.players_data[player]['num_observables'] = num_observables
        self.update_observables_layout(player)

    def update_observables_layout(self, player):
        layout = self.players_data[player]['layout']
        layout.clear_widgets()

        for i in range(self.players_data[player]['num_observables']):
            obs_name = f'Var {i + 1}'
            if obs_name not in self.players_data[player]['observables']:
                self.players_data[player]['observables'][obs_name] = {
                    'score': 0,
                    'initial': 0,  # Valeur initiale par défaut
                    'coefficient': 1,  # Coefficient par défaut
                    'point': 0,
                    'name_input': TextInput(text=obs_name, font_size=14, size_hint_x=0.5, height=30),
                    'score_label': Label(text="0", font_size=14, size_hint_x=0.2, height=30),
                }

            observable_data = self.players_data[player]['observables'][obs_name]
            name_input = observable_data['name_input']
            score_label = observable_data['score_label']

            # Stockage des dépendances
            self.players_data[player]['dependencies'] = {}  # Réinitialiser les dépendances
            self.players_data[player]['observables'][obs_name]['dependencies'] = {}

            # Mise à jour de l'affichage du score avec la valeur initiale
            score_label.text = str(observable_data['score'])

            btn_increase = Button(text="+", size_hint=(0.1, 0.5), height=30)
            btn_increase.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, 1))

            btn_decrease = Button(text="-", size_hint=(0.1, 0.5), height=30)
            btn_decrease.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, -1))

            layout.add_widget(name_input)
            layout.add_widget(score_label)
            layout.add_widget(btn_increase)
            layout.add_widget(btn_decrease)

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

        #Rapport minute/seconde

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

        #Arrêter le temps lorsque nécessaire

    def stop_timer(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            self.start_timer_button.text = "Démarrer le Timer" if self.is_timer_mode else "Démarrer le Chrono"

        # Gérer le temps

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

        # Timer/Chrono
    def switch_mode(self, instance):
            self.is_timer_mode = not self.is_timer_mode
            if self.is_timer_mode:
                self.mode_button.text = "Mode Chrono"
                self.timer_label.text = "Timer: 00:00"
                self.start_timer_button.text = "Démarrer le Timer"
            else:
                self.mode_button.text = "Mode Timer"
                self.timer_label.text = "Chrono: 00:00"
                self.start_timer_button.text = "Démarrer le Chrono"
                self.show_chrono_popup()

            self.stop_timer()

        #Visuel du Chrono
    def show_chrono_popup(self):
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            time_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
            time_layout.bind(minimum_height=time_layout.setter('height'))

            def create_time_section(label_text, increment_fn, decrement_fn):
                time_section = BoxLayout(orientation='vertical')
                label = Label(text=label_text, size_hint_y=None, height=40)
                increase_btn = Button(text="+", size_hint_y=None, height=40)
                decrease_btn = Button(text="-", size_hint_y=None, height=40)
                increase_btn.bind(on_release=increment_fn)
                decrease_btn.bind(on_release=decrement_fn)
                time_section.add_widget(increase_btn)
                time_section.add_widget(label)
                time_section.add_widget(decrease_btn)
                return time_section, label

            hours_section, self.hour_label = create_time_section(
                f"Heures: {self.hours}",
                lambda x: self.change_time('hours', 1, self.hour_label),
                lambda x: self.change_time('hours', -1, self.hour_label)
            )

            minutes_section, self.minute_label = create_time_section(
                f"Minutes: {self.minutes}",
                lambda x: self.change_time('minutes', 1, self.minute_label),
                lambda x: self.change_time('minutes', -1, self.minute_label)
            )

            seconds_section, self.second_label = create_time_section(
                f"Secondes: {self.seconds}",
                lambda x: self.change_time('seconds', 1, self.second_label),
                lambda x: self.change_time('seconds', -1, self.second_label)
            )

            time_layout.add_widget(hours_section)
            time_layout.add_widget(minutes_section)
            time_layout.add_widget(seconds_section)

            layout.add_widget(time_layout)
            close_button = Button(text="Fermer", size_hint_y=None, height=40)
            layout.add_widget(close_button)

            popup = Popup(title="Réglage de la durée du Chrono", content=layout, size_hint=(0.8, 0.8))
            close_button.bind(on_release=popup.dismiss)
            popup.open()

        #Changer nom de l'archive
    def archive_data(self, instance):
        # Création du popup pour entrer le nom du fichier
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label pour le titre
        label = Label(text="Entrez le nom de l'archive :",
                      size_hint_y=None, height=40)
        layout.add_widget(label)

        # Champ de saisie pour le nom de l'archive
        archive_name_input = TextInput(text="", font_size=16, size_hint_y=None, height=40)
        layout.add_widget(archive_name_input)

        # Bouton pour confirmer et créer l'archive
        confirm_button = Button(text="Archiver", size_hint_y=None, height=50)
        confirm_button.bind(on_release=lambda x: self.save_archive(archive_name_input.text, popup))
        layout.add_widget(confirm_button)

        # Création et ouverture du popup
        popup = Popup(title="Choisir un nom d'archive", content=layout, size_hint=(0.8, 0.5))
        popup.open()

        #Sauvegarde d'archives

    def save_archive(self, custom_name, popup):
        archive_dir = "archives"
        os.makedirs(archive_dir, exist_ok=True)

        # Si aucun nom n'est saisi, utilise le nom par défaut
        if not custom_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{archive_dir}/archive_Personnalisé_{timestamp}.txt"
        else:
            filename = f"{archive_dir}/{custom_name}.txt"

        # Obtenir la date et l'heure actuelles
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sauvegarde des données dans le fichier
        with open(filename, 'w') as f:
            # Écrire "Personnalisé" pour indiquer le mode et ajouter la date et l'heure
            f.write(" Personnalisé\n")
            f.write(f"Date et heure : {date_heure}\n\n")

            # Écrire les données des joueurs
            for player, data in self.players_data.items():
                f.write(f"¤{player}\n")
                for obs_name, obs_data in data['observables'].items():
                    f.write(f"  £{obs_name}£: {obs_data['score']}\n")
                f.write(f"\n")

        print(f"Data archived to {filename}")

        # Fermer le popup après avoir archivé
        popup.dismiss()

        #Retourner sur la page principale

    def go_back(self, instance):
        self.stop_timer()
        self.manager.current = 'home'