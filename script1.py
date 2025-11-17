from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
import pandas as pd
import pyodbc
import numpy as np
from perfmon import ObjectType

#ADD VALIDATION

#This connects to the SSMS database where everything is stored
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=BRILAPTOP\SQLEXPRESS;"
                      "Database=Capstone;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
query = "SELECT [UserName], [Password], [UserID] FROM dbo.Users;"

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

#Login class
class loginWindow(Screen):
    user = ObjectProperty(None)
    pwd = ObjectProperty(None)

    #Validation for the user, checks username and password
    def validate(self):

        df = pd.read_sql(query, cnxn)
        spec = df[df['UserName'] == self.user.text]
        df2 = pd.DataFrame(spec)
        df_reset = df2.reset_index()
        if df2.empty:
            popFun()
        else:
            passw = df_reset._get_value(0, 'Password')
            if passw == self.pwd.text:

                global userid
                userid2 = df_reset._get_value(0, 'UserID')
                userid = int(userid2)
                print(type(userid))
                sm.current = 'mainprofile'


                self.user.text = ""
                self.pwd.text = ""
            else:
                popFun()

#The functions performed in the main welcome page
class mainProfileWindow(Screen):
    #Grabs the stat for how many workouts have been completed
    def stat(self):
        query = "SELECT * FROM dbo.[Workouts];"

        df = pd.read_sql(query, cnxn)

        print(df)

        df1 = df[df['User_ID'] == userid]

        print(df1)
        df2 = df1[df1['Completed'] == False]
        df3 = df2.sort_values('Workout_ID')
        df4 = df3.reset_index()
        val = df2.shape
        global val2
        val2 = val[0]

        print(val2)

        sm.current = 'stats'

#Class for the sign up window
class signupWindow(Screen):
    name1 = ObjectProperty(None)
    name2 = ObjectProperty(None)
    user = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        if self.user.text != "":
            if self.user.text not in df['UserName']:
                firstn = self.name1.text
                lastn = self.name2.text
                usern = self.user.text
                passw = self.pwd.text


                cursor.execute('INSERT INTO dbo.Users(FirstName,LastName,UserName,Password) VALUES (?,?,?,?)',
                                (firstn, lastn, usern, passw))
                cnxn.commit()
                sm.current = 'login'
                self.name1.text = ""
                self.name2.text = ""
                self.user.text = ""
                self.pwd.text = ""
            else:
                popFun()
        else:

            popFun()
#Class for the stats
class statsWindow(Screen):
    #Displays the number of workouts completed
    def stats(self):
        self.woleft = Label(text='')
        self.add_widget(self.woleft)
        self.woleft.text = f'{val2} Workouts Completed'



class logDataWindow(Screen):
    pass


#Screen Manager
class windowManager(ScreenManager):
    pass
#Class that holds the functions for the making a new workout
class workoutWindow(Screen):

    def newWO(self):
        sm.current = 'newwo'

    def planday(self):

        query = "SELECT * FROM dbo.[Workouts];"

        df = pd.read_sql(query, cnxn)
        print("df")
        print(df)
        print(userid)
        df = pd.DataFrame(df)
        df1 = df[df['User_ID'] == userid]
        print('df1')
        print(df1)
        df2 = df1[df1['Completed'] == False]
        print('df2')
        print(df2)
        df3 = df2.sort_values('Workout_ID')
        print('df3')
        print(df3)
        df4 = df3.reset_index()
        print('df4')
        print(df4)
        current = df4.loc[0, 'WorkoutInfo']

        global woid2
        woid = df4.loc[0, 'Workout_ID']
        woid2 = int(woid)

        global cwo
        cwo = current.split(', ')
        sm.current = 'plan'
        return cwo

#Class for actually making the new workout
class newWorkout(Screen):
    length = ObjectProperty(None)
    freq = ObjectProperty(None)
    sport = ObjectProperty(None)



    def buildwo(self):
        query2 = "SELECT * FROM dbo.[Exercise DataBase];"

        df = pd.read_sql(query2, cnxn)

        num1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        num2 = [1,2,3,4,5]
        num3 = [1,2,3]

        weeks1 = self.length.text
        days1 = self.freq.text
        sports1 = self.sport.text


        if weeks1 not in num1:
            print("failed at weeks")
            sm.current = 'mainprofile'
        elif days1 not in num2:
            print("failed at days")
            sm.current = 'mainprofile'
        elif sports1 not in num3:
            print("failed at sport")
            sm.current = 'mainprofile'
        else:
            weeks = int(weeks1)
            days = int(days1)
            sports = int(sports1)
            day = list()

            match sports:
                case 1:  # snowboarding
                    upper = ['core', 'biceps', 'triceps', 'back', 'shoulder']
                    lower = ['calves', 'hamstrings', 'glutes', 'quads']
                case 2:  # rock climbing
                    upper = ['forearms', 'biceps', 'back', 'core', 'triceps']
                    lower = ['calves', 'hamstrings', 'glutes', 'quads']
                case 3:  # dance
                    upper = ['chest', 'back', 'shoulders', 'biceps', 'triceps', 'core']
                    lower = ['ankles', 'feet', 'calves', 'hamstrings', 'glutes', 'quads', 'hip flexors']

            match days:
                case 1:
                    result = [[upper, upper, upper, upper, lower, lower, lower, lower]]
                case 2:
                    result = [[upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower]]
                case 3:
                    result = [[upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower],
                            [upper, upper, upper, upper, lower, lower, lower, lower]]
                case 4:
                    result = [[upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower],
                            [upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower]]
                case 5:
                    result = [[upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower],
                            [upper, upper, upper, upper, lower, lower, lower, lower],
                            [upper, upper, upper, upper, upper, upper, upper, upper],
                            [lower, lower, lower, lower, lower, lower, lower, lower]]


        # NEED TO MAKE A VALIDATION THING IN ORDER TO MAKE SURE THAT THE SAME THING HASN'T BEEN SELECTED TWICE IN ONE WORKOUT.
            def exer(z):
                ex = z[0]
                df1 = df[df["Muscle1"].str.contains(ex, case=False, na=False) | df["Muscle2"].str.contains(ex, case=False,
                                                                                                       na=False) | df[
                            "Muscle3"].str.contains(ex, case=False, na=False)]
                mdf = pd.DataFrame(df1)
                mdf2 = mdf.reset_index()
                size = mdf2.index.size
                num = np.random.randint(0, size - 1)
                wo = mdf2.Exercise_Name[num]
                return wo

            def daily(x):
                for y in x:
                    for z in y:
                        this = exer(z)
                        day.append(this)
                        val = z.pop(0)
                        z.append(val)

            def week():
                daily(result)
                a = [day[i:i + n] for i in range(0, len(day), n)]
                day.clear()
                return a

            def full(length):
                for x in range(length):
                    c = week()
                    for x in c:
                        d = ', '.join(x)
                        print(userid)
                        cursor.execute('INSERT INTO dbo.Workouts(User_ID,WorkoutInfo,Completed) VALUES (?,?,?)',
                                   (userid, d, 0))
                        cnxn.commit()

            full(weeks)
            sm.current = 'newwo'

#Class that shows the workout
class planWindow(Screen):

    def plan(self):
        self.workout = Label(text='')
        self.add_widget(self.workout)
        self.workout.text = f'{cwo[0]}\n{cwo[1]}\n{cwo[2]}\n{cwo[3]}\n{cwo[4]}\n{cwo[5]}\n{cwo[6]}\n{cwo[7]}\n'

    def comp(self):
        self.workout.text = ""
        result = 1
        update = "UPDATE dbo.[Workouts] SET Completed = (?) WHERE Workout_ID = (?);"
        try:
            cursor.execute(update, result, woid2)
            cnxn.commit()
        except pyodbc.ProgrammingError as ex:
            sql = ex.args[1]
            print(sql)
        sm.current = 'workout'




kv = Builder.load_file('login.kv')
sm = windowManager()


users = pd.read_csv('login.csv')


sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(mainProfileWindow(name='mainprofile'))
sm.add_widget(workoutWindow(name='workout'))
sm.add_widget(statsWindow(name='stats'))
sm.add_widget(newWorkout(name='newwo'))
sm.add_widget(planWindow(name='plan'))


#Builds the program
class loginMain(App):
    def build(self):
        return sm


#Actually builds the program
if __name__ == "__main__":
    loginMain().run()


