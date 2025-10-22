from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
import pyodbc
#ADD VALIDATION


cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=BRILAPTOP\SQLEXPRESS;"
                      "Database=Capstone;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
query = "SELECT [UserName], [Password] FROM dbo.Users;"

df = pd.read_sql(query, cnxn)
#ADD VALIDATION



class PopupWindow(Widget):
    def btn(self):
        popFun()



class P(FloatLayout):
    pass


def popFun():
    show = P()
    window = Popup(title="Error", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()

def popIn():
    show = P()
    window = Popup(title="Logged In", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):


        spec = df[df['UserName'] == self.email.text]
        df2 = pd.DataFrame(spec)
        df_reset = df2.reset_index()
        if df2.empty:
            popFun()
        else:
            passw = df_reset._get_value(0, 'Password')
            if passw == self.pwd.text:

                sm.current = 'mainprofile'


                self.email.text = ""
                self.pwd.text = ""
            else:
                popFun()

class mainProfileWindow(Screen):
    pass


class signupWindow(Screen):
    name1 = ObjectProperty(None)
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        if self.email.text != "":
            if self.email.text not in df['UserName']:
                firstn = self.name1.text
                lastn = self.name2.text
                usern = self.email.text
                passw = self.pwd.text


                cursor.execute('INSERT INTO dbo.Users(FirstName,LastName,UserName,Password) VALUES (?,?,?,?)',
                                (firstn, lastn, usern, passw))
                cnxn.commit()
                sm.current = 'login'
                self.name1.text = ""
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
            else:
                popFun()
        else:

            popFun()



class logDataWindow(Screen):
    pass



class windowManager(ScreenManager):
    pass

class workoutWindow(Screen):
    pass

class profileWindow(Screen):
    pass

class socialWindow(Screen):
    pass

class settingsWindow(Screen):
    pass

class statsWindow(Screen):
    pass


kv = Builder.load_file('login.kv')
sm = windowManager()


users = pd.read_csv('login.csv')


sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(mainProfileWindow(name='mainprofile'))
sm.add_widget(workoutWindow(name='workout'))
sm.add_widget(profileWindow(name='profile'))
sm.add_widget(socialWindow(name='social'))
sm.add_widget(settingsWindow(name='settings'))
sm.add_widget(statsWindow(name='stats'))


class loginMain(App):
    def build(self):
        return sm



if __name__ == "__main__":
    loginMain().run()


