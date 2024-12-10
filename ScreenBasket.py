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
from kivy.storage.jsonstore import JsonStore


################################ Écran des fonctionnalités pour le basket ################################################
class BasketScreen(Screen):
    def __init__(self, **kwargs):
        super(BasketScreen, self).__init__(**kwargs)

        # Initialisation des variables
        self.players_data = {}
        self.timer_event = None
        self.start_time = 0
        self.chrono_duration = 0  # Durée du chrono en secondes
        self.is_timer_mode = True  # Variable pour suivre le mode actuel (Timer/Chrono)
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        # Layout principal
        main_layout = BoxLayout(orientation='vertical')

        # Layout pour le bouton de retour et le timer
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Ajoutez le bouton de retour qui reste fixe en haut
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        # Label de Timer/Chrono en haut de la page
        self.timer_label = Label(text="Timer: 00:00", font_size=24, size_hint=(0.4, 1))
        top_layout.add_widget(self.timer_label)

        # Bouton pour basculer entre Timer et Chrono
        self.mode_button = Button(text="Mode Chrono", size_hint_x=0.2, height=50)
        self.mode_button.bind(on_release=self.switch_mode)
        top_layout.add_widget(self.mode_button)

        main_layout.add_widget(top_layout)
        # Créer un ScrollView pour le contenu
        main_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 50))
        main_scroll_content = BoxLayout(orientation='vertical', size_hint_y=None)
        main_scroll_content.bind(minimum_height=main_scroll_content.setter('height'))

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

        self.update_num_players(None, "5")  # Initialisation à 5 joueurs

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

    def update_num_players(self, instance, num_players_text):
        try:
            num_players = int(num_players_text)
        except (ValueError, IndexError):
            num_players = 5  # Valeur par défaut en cas de problème

        if num_players > 5:
            num_players = 5  # Limiter le nombre de joueurs à 5

        self.players_data = {f'Joueur {i + 1}': {'observables': {}, 'num_observables': 3} for i in range(num_players)}
        self.players_layout.clear_widgets()  # Clear existing player widgets

        for player in self.players_data.keys():
            player_layout = BoxLayout(orientation='vertical', padding=(0, 10), size_hint_y=None)
            player_layout.bind(minimum_height=player_layout.setter('height'))  # Assurer le redimensionnement

            name_input = TextInput(text=player, font_size=18, size_hint_y=None, height=40)  # Taille
            name_input.bind(text=self.on_name_change)
            player_layout.add_widget(name_input)

            spinner_layout = BoxLayout(size_hint_y=None, height=40)  # Taille
            spinner_label = Label(text="Nombre de variables:", font_size=16, size_hint_x=0.6)
            spinner = Spinner(text="3", values=["1", "2", "3"], size_hint_x=0.4)
            spinner.bind(text=lambda instance, val, p=player: self.set_num_observables(p, int(val)))
            spinner_layout.add_widget(spinner_label)
            spinner_layout.add_widget(spinner)
            player_layout.add_widget(spinner_layout)

            self.players_data[player]['layout'] = GridLayout(cols=4, size_hint_y=None, height=150)
            player_layout.add_widget(self.players_data[player]['layout'])
            self.update_observables_layout(player)

            self.players_layout.add_widget(player_layout)

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

        default_observables = ['Point', 'Passe', 'Rebond']

        for i in range(self.players_data[player]['num_observables']):
            obs_name = default_observables[i] if i < 3 else f'Var {i + 1}'
            if obs_name not in self.players_data[player]['observables']:
                self.players_data[player]['observables'][obs_name] = {
                    'score': 0,
                    'name_input': TextInput(text=obs_name)
                }

            name_input = self.players_data[player]['observables'][obs_name]['name_input']
            name_input.font_size = 16  # La taille de la police
            name_input.size_hint_x = 0.3  # La largeur relative de la zone de texte
            name_input.height = 40  # La hauteur de la zone de texte

            score_label = Label(text=str(self.players_data[player]['observables'][obs_name]['score']), font_size=14,
                                size_hint_x=0.2, height=30)  # La taille et la hauteur du label

            btn_increase = Button(text="+", size_hint=(0.2, 0.5), height=30)  # Ajuste la taille du bouton
            btn_increase.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, 1))

            btn_decrease = Button(text="-", size_hint=(0.2, 0.5), height=30)  # Ajuste la taille du bouton
            btn_decrease.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, -1))

            layout.add_widget(name_input)
            layout.add_widget(score_label)
            layout.add_widget(btn_increase)
            layout.add_widget(btn_decrease)

            setattr(self, f"{player}_{obs_name}_score_label", score_label)

    def update_score(self, player, observable, increment):
        self.players_data[player]['observables'][observable]['score'] += increment
        score_label = getattr(self, f"{player}_{observable}_score_label")
        score_label.text = str(self.players_data[player]['observables'][observable]['score'])

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
            archive_name = f"archive_Basket_{timestamp}"
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
                # Écrire "Basket" pour indiquer le mode et la date
                f.write(" Basket\n")
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