import os
os.environ["KIVY_METRICS_DENSITY"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_PY2_LOGGING"] = "1"
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ScreenF import FeaturesScreen
from ScreenC import CreditsScreen
from ScreenA import ArchivesScreen
from ScreenS import SelectionScreen
from MainScreen import HomeScreen
from ScreenBasket import BasketScreen
from ScreenFutsal import FutsalScreen
from ScreenVS import DuelScreen

################################ Gestionnaire d'écran ################################################
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(HomeScreen(name='home'))
        self.add_widget(FeaturesScreen(name='features'))
        self.add_widget(SelectionScreen(name='selection'))
        self.add_widget(ArchivesScreen(name='archives'))
        self.add_widget(CreditsScreen(name='credits'))
        self.add_widget(BasketScreen(name='basket'))
        self.add_widget(FutsalScreen(name='futsal'))
        self.add_widget(DuelScreen(name='vs'))

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        return sm

if __name__ == '__main__':
    MyApp().run()