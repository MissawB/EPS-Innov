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
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class DuelScreen(Screen):
    def __init__(self, **kwargs):
        super(DuelScreen, self).__init__(**kwargs)

        # Initialisation des données des joueurs
        self.players_data = {
            'Joueur 1': {'observables': {}, 'num_observables': 3},
            'Joueur 2': {'observables': {}, 'num_observables': 3}
        }
        self.timer_event = None
        self.start_time = 0
        self.chrono_duration = 0  # Durée du chrono en secondes
        self.is_timer_mode = True  # Variable pour suivre le mode actuel (Timer/Chrono)
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        # Layout principal pour tout l'écran
        main_layout = BoxLayout(orientation='vertical')

        # Partie du haut avec le bouton retour et le timer
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0))
        self.back_button = Button(text='Retour', size_hint_x=0.2, height=50)
        self.back_button.bind(on_release=self.go_back)
        top_layout.add_widget(self.back_button)

        self.timer_label = Label(text="Timer: 00:00", font_size=24, size_hint=(0.6, 1))
        top_layout.add_widget(self.timer_label)

        # Bouton pour basculer entre Timer et Chrono
        self.mode_button = Button(text="Chrono", size_hint=(0.2, 1))
        self.mode_button.bind(on_release=self.switch_mode)
        top_layout.add_widget(self.mode_button)

        # Ajouter le top_layout au layout principal
        main_layout.add_widget(top_layout)

        # Layout pour les deux joueurs
        players_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, 0.8))

        # Créer les sections pour chaque joueur avec cadre et couleur pour distinction
        for player, color in zip(self.players_data.keys(), [(0.8, 0.3, 0.3, 1), (0.3, 0.3, 0.8, 1)]):
            player_layout = self.create_player_section(player, color)
            players_layout.add_widget(player_layout)

        # Ajouter les sections des joueurs au layout principal
        main_layout.add_widget(players_layout)

        buttons_layout = BoxLayout(orientation='horizontal', spacing=1, padding=1, size_hint_y=None, height=50)

        # Bouton pour démarrer le timer
        self.start_timer_button = Button(text="Démarrer le Timer", size_hint=(0.5, 1))
        self.start_timer_button.bind(on_release=self.start_timer)
        buttons_layout.add_widget(self.start_timer_button)

        # Bouton pour archiver les données
        archive_button = Button(text="Archiver les Données", size_hint=(0.5, 1))
        archive_button.bind(on_release=self.archive_data)
        buttons_layout.add_widget(archive_button)

        # Ajouter les boutons côte à côte dans le layout principal
        main_layout.add_widget(buttons_layout)

        self.add_widget(main_layout)

    def create_player_section(self, player, color):
        # Création de la section pour chaque joueur avec un fond coloré
        player_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_x=0.5)

        # Fond coloré pour chaque section de joueur
        with player_layout.canvas.before:
            Color(*color)  # Couleur de fond pour chaque section de joueur
            player_layout.rect = Rectangle(size=player_layout.size, pos=player_layout.pos)
            player_layout.bind(size=lambda _, val: setattr(player_layout.rect, 'size', val),
                               pos=lambda _, val: setattr(player_layout.rect, 'pos', val))

        # Nom du joueur
        name_input = TextInput(text=player, font_size=18, size_hint_y=None, height=40)
        player_layout.add_widget(name_input)

        # Spinner pour le nombre de variables
        spinner_layout = BoxLayout(size_hint_y=None, height=40)
        spinner_label = Label(text="Nombre de \n variables:", font_size=16, size_hint_x=0.6)
        spinner = Spinner(text="3", values=["1", "2", "3", "4", "5"], size_hint_x=0.4)
        spinner.bind(text=lambda instance, val, p=player: self.set_num_observables(p, int(val)))
        spinner_layout.add_widget(spinner_label)
        spinner_layout.add_widget(spinner)
        player_layout.add_widget(spinner_layout)

        # ScrollView pour gérer un grand nombre de variables avec une taille ajustée
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width / 2, Window.height * 0.6))
        observables_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=(10, 10), spacing=10)
        observables_layout.bind(minimum_height=observables_layout.setter('height'))

        self.players_data[player]['layout'] = observables_layout
        scroll_view.add_widget(observables_layout)
        player_layout.add_widget(scroll_view)

        # Initialisation des observables par défaut
        self.update_observables_layout(player)
        return player_layout

    def set_num_observables(self, player, num_observables):
        self.players_data[player]['num_observables'] = num_observables
        self.update_observables_layout(player)

    def update_observables_layout(self, player):
        layout = self.players_data[player]['layout']
        layout.clear_widgets()

        for i in range(self.players_data[player]['num_observables']):
            obs_name = f'Var {i + 1}'
            if obs_name not in self.players_data[player]['observables']:
                self.players_data[player]['observables'][obs_name] = {'score': 0,
                                                                      'name_input': TextInput(text=obs_name)}

            name_input = self.players_data[player]['observables'][obs_name]['name_input']
            name_input.font_size = 16
            name_input.size_hint_y = None
            name_input.height = 30

            # Création d'un layout vertical pour chaque observable avec un espacement réduit
            observable_box = BoxLayout(orientation='vertical', spacing=1, size_hint=(1, None), height=100)

            # Ajout du nom de la variable en haut
            observable_box.add_widget(name_input)

            # Label pour le score au milieu
            score_label = Label(text=str(self.players_data[player]['observables'][obs_name]['score']), font_size=14,
                                size_hint_y=None, height=25)
            observable_box.add_widget(score_label)

            # Layout horizontal pour les boutons d'augmentation et de diminution en bas
            button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)

            btn_increase = Button(text="+", size_hint=(0.5, 1))
            btn_increase.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, 1))

            btn_decrease = Button(text="-", size_hint=(0.5, 1))
            btn_decrease.bind(on_press=lambda x, p=player, o=obs_name: self.update_score(p, o, -1))

            button_box.add_widget(btn_decrease)
            button_box.add_widget(btn_increase)

            observable_box.add_widget(button_box)

            # Réduire la hauteur de l'espace visuel
            spacer = Widget(size_hint_y=None, height=2)
            observable_box.add_widget(spacer)

            layout.add_widget(observable_box)
            setattr(self, f"{player}_{obs_name}_score_label", score_label)

    def update_score(self, player, observable, increment):
        self.players_data[player]['observables'][observable]['score'] += increment
        score_label = getattr(self, f"{player}_{observable}_score_label")
        score_label.text = str(self.players_data[player]['observables'][observable]['score'])

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

    def save_archive(self, custom_name, popup):
        archive_dir = "archives"
        os.makedirs(archive_dir, exist_ok=True)

        # Si aucun nom n'est saisi, utilise le nom par défaut
        if not custom_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{archive_dir}/archive_Duel_{timestamp}.txt"
        else:
            filename = f"{archive_dir}/{custom_name}.txt"

        # Obtenir la date et l'heure actuelles
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sauvegarde des données dans le fichier
        with open(filename, 'w') as f:
            # Écrire "Duel" pour indiquer le mode et ajouter la date et l'heure
            f.write(" Duel\n")
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

    def go_back(self, instance):
        self.stop_timer()
        self.manager.current = 'home'
