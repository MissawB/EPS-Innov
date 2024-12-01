import os
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from datetime import datetime

class ArchivesScreen(Screen):
    def __init__(self, **kwargs):
        super(ArchivesScreen, self).__init__(**kwargs)

        # Structure pour stocker les données de manière détaillée
        self.sorted_data = {"Sport": {}, "Joueur": {}}

        # Layout principal
        main_layout = BoxLayout(orientation='vertical')

        # Layout pour les options de filtre et tri
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Bouton de retour
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        # Spinner pour sélectionner le filtre par sport
        self.filter_spinner = Spinner(
            text='Tout',
            values=['Tout', 'Futsal', 'Duel', 'Basket', 'Personnalisé'],
            size_hint_x=0.3
        )
        self.filter_spinner.bind(text=self.load_archives)
        top_layout.add_widget(self.filter_spinner)

        # Spinner pour le critère de tri
        self.sort_spinner = Spinner(
            text='Trier par',
            values=['Sport', 'Joueur', 'Variable', 'Nom d\'archive', 'Date'],
            size_hint_x=0.3
        )
        self.sort_spinner.bind(text=self.update_archive_display)
        top_layout.add_widget(self.sort_spinner)

        main_layout.add_widget(top_layout)

        # Layout pour afficher les archives avec scroll
        self.archive_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        self.archive_layout.bind(minimum_height=self.archive_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.archive_layout)

        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

        # Charger toutes les archives dès le début
        self.load_archives()

    #Lecture du contenu des fichiers
    def read_file_content(self, file_path):
        encodings = ['iso-8859-1', 'utf-8', 'latin-1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.readlines()
            except UnicodeDecodeError:
                print(f"Erreur de décodage avec l'encodage {enc} pour le fichier {file_path}")
        return None

    def extract_sport_type(self, content):
        for line in content:
            if "personnalisé" in line.lower():
                return "Personnalisé"
            if "futsal" in line.lower():
                return "Futsal"
            if "duel" in line.lower():
                return "Duel"
            if "basket" in line.lower():
                return "Basket"
        return "Inconnu"

    def extract_date(self, content):
        try:
            # Vérifier si la ligne existe
            if len(content) > 1:
                date_line = content[1]
                # Chercher le premier ':' et extraire tout ce qui suit
                if ":" in date_line:
                    date_str = date_line.split(":", 1)[1].strip()  # Séparer uniquement à la première occurrence de ":"
                    # Vérifier si la date est bien dans le bon format
                    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                else:
                    print("Format de la ligne de date invalide : pas de ':' trouvé.")
            else:
                print("La ligne de date est manquante dans le contenu.")
        except Exception as e:
            print(f"Erreur lors de l'extraction de la date : {e}")
        return None

    def load_archives(self, *args):
        self.archive_layout.clear_widgets()
        archive_dir = "archives"
        self.sorted_data = {"Sport": {}, "Joueur": {}}

        if not os.path.exists(archive_dir):
            print("Le dossier des archives n'existe pas.")
            return

        selected_sport = self.filter_spinner.text.lower()

        archives_with_dates = []
        for filename in sorted(os.listdir(archive_dir), reverse=True):
            file_path = os.path.join(archive_dir, filename)
            content = self.read_file_content(file_path)

            if content is None:
                continue

            sport_type = self.extract_sport_type(content)

            if selected_sport != 'tout' and selected_sport != sport_type:
                continue

            archive_date = self.extract_date(content)
            if archive_date:
                archives_with_dates.append((filename, file_path, content, sport_type, archive_date))

            self.organize_data(filename, content, sport_type)

        sorted_archives_by_date = sorted(archives_with_dates, key=lambda x: x[4], reverse=True)
        for _, file_path, content, sport_type, _ in sorted_archives_by_date:
            self.add_archive_to_layout(_, content, file_path, sport_type)

        self.update_archive_display()

    def organize_data(self, filename, content, sport_type):
        player_data = {}
        variable_data = {}  # Nouvelle structure pour organiser les données par variable
        current_player = None
        for line in content:
            line = line.strip()
            if line.startswith("¤"):
                current_player = line[1:]
                if current_player not in player_data:
                    player_data[current_player] = {'variables': []}
            elif line.startswith("£") and current_player:
                parts = line.split(":")
                variable = parts[0].strip(" £")
                score = int(parts[1].strip())
                player_data[current_player]['variables'].append((variable, score))

                # Ajouter la variable aux données globales
                if variable not in variable_data:
                    variable_data[variable] = []
                variable_data[variable].append((current_player, score))

        for player, data in player_data.items():
            if sport_type not in self.sorted_data["Sport"]:
                self.sorted_data["Sport"][sport_type] = []
            self.sorted_data["Sport"][sport_type].append((player, data))

            if player not in self.sorted_data["Joueur"]:
                self.sorted_data["Joueur"][player] = {}
            self.sorted_data["Joueur"][player][sport_type] = data

        # Ajouter les données triées par variable dans le dictionnaire global
        self.sorted_data["Variable"] = variable_data

    def update_archive_display(self, *args):
        self.archive_layout.clear_widgets()
        sort_by = self.sort_spinner.text

        if sort_by == "Trier par":
            self.display_default_order()
        elif sort_by == "Nom d'archive":
            self.display_sorted_by_filename()
        elif sort_by == "Date":
            self.display_sorted_by_date()
        elif sort_by == "Variable":
            self.display_sorted_by_variable()
        else:
            self.display_sorted_data(sort_by)

    def add_archive_to_layout(self, filename, content, file_path, sport_type):
        # Vérifier si l'archive doit être affichée sous forme de tableau
        selected_sport = self.filter_spinner.text.lower()

        if selected_sport == 'tout' or selected_sport == sport_type:
            title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            archive_label = Label(text=f"Archive: {filename} - Sport: {sport_type.capitalize()}", font_size=18,
                                  bold=True)
            title_layout.add_widget(archive_label)

            delete_button = Button(text="Effacer", size_hint_x=0.2)
            delete_button.bind(on_release=lambda instance: self.delete_archive(file_path, title_layout))
            title_layout.add_widget(delete_button)

            self.archive_layout.add_widget(title_layout)

            # Créer le tableau pour afficher les données de l'archive
            table_layout = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5)
            table_layout.bind(minimum_height=table_layout.setter('height'))
            table_layout.add_widget(Label(text="Joueur", bold=True, size_hint_y=None, height=30))
            table_layout.add_widget(Label(text="Variable", bold=True, size_hint_y=None, height=30))
            table_layout.add_widget(Label(text="Score", bold=True, size_hint_y=None, height=30))

            # Extraction des données de chaque joueur et variable
            player_data = {}
            current_player = None

            for line in content:
                line = line.strip()
                if line.startswith("¤"):
                    current_player = line[1:]
                    player_data[current_player] = {'variables': []}
                elif line.startswith("£") and current_player:
                    parts = line.split(":")
                    variable = parts[0].strip(" £")
                    score = int(parts[1].strip())
                    player_data[current_player]['variables'].append((variable, score))

            # Ajout de toutes les variables pour chaque joueur
            for player, data in player_data.items():
                for variable, score in data['variables']:
                    table_layout.add_widget(Label(text=player, size_hint_y=None, height=30))
                    table_layout.add_widget(Label(text=variable, size_hint_y=None, height=30))
                    table_layout.add_widget(Label(text=str(score), size_hint_y=None, height=30))

            self.archive_layout.add_widget(table_layout)

    def display_default_order(self):
        # Afficher les archives sans tri (ordre par défaut)
        archive_dir = "archives"
        for filename in sorted(os.listdir(archive_dir), reverse=True):
            file_path = os.path.join(archive_dir, filename)
            content = self.read_file_content(file_path)
            if content:
                sport_type = self.extract_sport_type(content)
                self.add_archive_to_layout(filename, content, file_path, sport_type)

    def display_sorted_by_filename(self):
        # Trier les archives par nom d'archive (alphabétique)
        archive_dir = "archives"
        sorted_files = sorted(os.listdir(archive_dir))  # Tri alphabétique
        for filename in sorted_files:
            file_path = os.path.join(archive_dir, filename)
            content = self.read_file_content(file_path)
            if content:
                sport_type = self.extract_sport_type(content)
                self.add_archive_to_layout(filename, content, file_path, sport_type)

    def display_sorted_by_date(self):
        # Trier les archives par date
        archive_dir = "archives"
        archives_with_dates = []

        for filename in sorted(os.listdir(archive_dir), reverse=True):
            file_path = os.path.join(archive_dir, filename)
            content = self.read_file_content(file_path)

            if content:
                sport_type = self.extract_sport_type(content)
                archive_date = self.extract_date(content)
                if archive_date:
                    archives_with_dates.append((filename, file_path, content, sport_type, archive_date))

        # Trier les archives par date (du plus récent au plus ancien)
        sorted_archives_by_date = sorted(archives_with_dates, key=lambda x: x[4], reverse=True)

        for _, file_path, content, sport_type, _ in sorted_archives_by_date:
            self.add_archive_to_layout(_, content, file_path, sport_type)

    def display_sorted_by_variable(self):
        # Créer un dictionnaire pour stocker les variables avec leurs scores respectifs pour chaque joueur
        variable_data = {}

        # Parcourir toutes les archives pour extraire les variables et les scores
        for sport, records in self.sorted_data["Sport"].items():
            for player, data in records:
                for variable, score in data['variables']:
                    # Si la variable n'existe pas dans le dictionnaire, l'ajouter
                    if variable not in variable_data:
                        variable_data[variable] = []
                    # Ajouter le score du joueur à la variable correspondante
                    variable_data[variable].append((player, sport, score))

        # Trier les variables par nom (ordre alphabétique)
        sorted_variables = sorted(variable_data.keys())

        # Afficher les variables triées
        for variable in sorted_variables:
            title_label = Label(text=f"Variable: {variable}", font_size=18, bold=True, size_hint_y=None, height=30)
            self.archive_layout.add_widget(title_label)

            table_layout = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5)
            table_layout.bind(minimum_height=table_layout.setter('height'))
            table_layout.add_widget(Label(text="Joueur", bold=True, size_hint_y=None, height=30))
            table_layout.add_widget(Label(text="Sport", bold=True, size_hint_y=None, height=30))
            table_layout.add_widget(Label(text="Score", bold=True, size_hint_y=None, height=30))

            # Afficher les scores des joueurs pour cette variable
            for player, sport, score in variable_data[variable]:
                table_layout.add_widget(Label(text=player, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text=sport.capitalize(), size_hint_y=None, height=30))
                table_layout.add_widget(Label(text=str(score), size_hint_y=None, height=30))

            self.archive_layout.add_widget(table_layout)

    def display_sorted_data(self, sort_by):
        if sort_by == "Joueur":
            for player, sports in self.sorted_data["Joueur"].items():
                title_label = Label(text=f"Joueur: {player}", font_size=18, bold=True, size_hint_y=None, height=30)
                self.archive_layout.add_widget(title_label)

                table_layout = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5)
                table_layout.bind(minimum_height=table_layout.setter('height'))
                table_layout.add_widget(Label(text="Sport", bold=True, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text="Variable", bold=True, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text="Score", bold=True, size_hint_y=None, height=30))

                for sport, data in sports.items():
                    for variable, score in data['variables']:
                        table_layout.add_widget(Label(text=sport.capitalize(), size_hint_y=None, height=30))
                        table_layout.add_widget(Label(text=variable, size_hint_y=None, height=30))
                        table_layout.add_widget(Label(text=str(score), size_hint_y=None, height=30))

                self.archive_layout.add_widget(table_layout)

        elif sort_by == "Sport":
            for sport, records in self.sorted_data["Sport"].items():
                title_label = Label(text=f"Sport: {sport}", font_size=18, bold=True, size_hint_y=None, height=30)
                self.archive_layout.add_widget(title_label)

                table_layout = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5)
                table_layout.bind(minimum_height=table_layout.setter('height'))
                table_layout.add_widget(Label(text="Joueur", bold=True, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text="Variable", bold=True, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text="Score", bold=True, size_hint_y=None, height=30))

                for player, data in records:
                    for variable, score in data['variables']:
                        table_layout.add_widget(Label(text=player, size_hint_y=None, height=30))
                        table_layout.add_widget(Label(text=variable, size_hint_y=None, height=30))
                        table_layout.add_widget(Label(text=str(score), size_hint_y=None, height=30))

                self.archive_layout.add_widget(table_layout)
        else:
            # Autres critères de tri (par exemple Variable)
            for key, records in self.sorted_data["Joueur"].items():
                title_label = Label(text=f"{sort_by}: {key}", font_size=18, bold=True, size_hint_y=None, height=30)
                self.archive_layout.add_widget(title_label)

                table_layout = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5)
                table_layout.bind(minimum_height=table_layout.setter('height'))
                table_layout.add_widget(
                    Label(text="Sport", bold=True, size_hint_y=None, height=30))  # Remplacer "Joueur" par "Sport"
                table_layout.add_widget(Label(text="Variable", bold=True, size_hint_y=None, height=30))
                table_layout.add_widget(Label(text="Score", bold=True, size_hint_y=None, height=30))

                # Affichage des données triées par Sport, Variable, etc.
                for player, data in records:
                    for variable, score in data['variables']:
                        # Afficher le sport de l'archive
                        sport_type = self.get_sport_for_player(player)  # Récupérer le sport associé à l'archive
                        table_layout.add_widget(
                            Label(text=sport_type.capitalize(), size_hint_y=None, height=30))  # Afficher le sport
                        table_layout.add_widget(Label(text=variable, size_hint_y=None, height=30))
                        table_layout.add_widget(Label(text=str(score), size_hint_y=None, height=30))

                self.archive_layout.add_widget(table_layout)

    def get_sport_for_player(self, player_name):
        """ Trouver le sport pour un joueur donné """
        for sport, players in self.sorted_data["Sport"].items():
            for player, _ in players:
                if player == player_name:
                    return sport
        return "Inconnu"

    def open_archive(self, file_path):
        # Ouvrir le fichier d'archive (afficher son contenu)
        content = self.read_file_content(file_path)
        if content:
            print("\n".join(content))

    #Bouton effacer
    def delete_archive(self, file_path, title_layout):
        try:
            os.remove(file_path)
            print(f"Archive supprimée: {file_path}")
            self.archive_layout.remove_widget(title_layout)
            next_widget = self.archive_layout.children[-1] if self.archive_layout.children else None
            if isinstance(next_widget, GridLayout):
                self.archive_layout.remove_widget(next_widget)
            self.load_archives()
        except Exception as e:
            print(f"Erreur lors de la suppression de l'archive {file_path}: {e}")

    #Bouton retour
    def go_back(self, instance):
        self.manager.current = 'home'