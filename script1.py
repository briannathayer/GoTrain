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

#This connects to the SSMS database where everything is stored
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=BRILAPTOP\SQLEXPRESS;"
                      "Database=Capstone;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
query = "SELECT [UserName], [Password], [UserID] FROM dbo.Users;"

df = pd.read_sql(query, cnxn)


#Pop up window widget
class PopupWindow(Widget):
    def btn(self):
        popFun()


#Has the window float
class P(FloatLayout):
    pass

#Reusable Code
#This is the popup function that tells you that the info you input is invalid
def popFun():
    show = P()
    window = Popup(title="Error", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()

#Login class
class loginWindow(Screen):
    #vairables for the inputs from the kivy file
    user = ObjectProperty(None)
    pwd = ObjectProperty(None)

    #Validation for the user, checks username and password
    def validate(self):
        #pulls the user info from the SQL database
        df = pd.read_sql(query, cnxn)
        spec = df[df['UserName'] == self.user.text]
        #Puts data into dataframe
        df2 = pd.DataFrame(spec)
        #resets the index to make it easier
        df_reset = df2.reset_index()
        #If there is nothing in the dataframe, the error popup triggers
        if df2.empty:
            popFun()

        else:
            passw = df_reset._get_value(0, 'Password')
            # If the password matches the username, logs the user into their profile
            if passw == self.pwd.text:
                #The variable userid will be used elsewhere, would this count as resuable code?
                global userid
                userid2 = df_reset._get_value(0, 'UserID')
                userid = int(userid2)
                sm.current = 'mainprofile'

                #Resets the log in input to empty
                self.user.text = ""
                self.pwd.text = ""
            #If it doesn't match, it will trigger the invalid entry popup
            else:
                popFun()

#The functions performed in the main welcome page
class mainProfileWindow(Screen):
    #Grabs the stat for how many workouts have been completed
    def stat(self):
        #Pulls the work out plans from the database
        query = "SELECT * FROM dbo.[Workouts];"

        df = pd.read_sql(query, cnxn)
        #Filters the list to the specific userid
        df1 = df[df['User_ID'] == userid]
        #Filters to get the completed workouts
        df2 = df1[df1['Completed'] == False]
        #Makes sure that the wokrouts are sorted by workout ID
        df3 = df2.sort_values('Workout_ID')
        df4 = df3.reset_index()
        #Gets the total count of workouts completed
        val = df2.shape
        global val2
        val2 = val[0]
        #Opens up the stats page
        sm.current = 'stats'

#Class for the sign up window
class signupWindow(Screen):
    #variables that hold the input of this page
    name1 = ObjectProperty(None)
    name2 = ObjectProperty(None)
    user = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):
        #Checks whether the username is empty - Validation
        if self.user.text != "":
            #Checks if user name is taken. If not taken
            if self.user.text not in df['UserName']:
                #Sets varibles to input text
                firstn = self.name1.text
                lastn = self.name2.text
                usern = self.user.text
                passw = self.pwd.text

                #adds the input into SQL
                cursor.execute('INSERT INTO dbo.Users(FirstName,LastName,UserName,Password) VALUES (?,?,?,?)',
                                (firstn, lastn, usern, passw))
                cnxn.commit()
                #Sends user back to login page
                sm.current = 'login'
                #Resets input boxes
                self.name1.text = ""
                self.name2.text = ""
                self.user.text = ""
                self.pwd.text = ""
            #If username taken
            else:
                popFun()
        #If user name empty
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

    #Takes you to the new workout window
    def newWO(self):
        sm.current = 'newwo'

    #Gets the current workout for the user
    def planday(self):

        #Grabs the workout table from SQL
        query = "SELECT * FROM dbo.[Workouts];"

        df = pd.read_sql(query, cnxn)
        #Turns table into dataframe
        df = pd.DataFrame(df)
        #filters dataframe by userid
        df1 = df[df['User_ID'] == userid]
        #Filters by workouts not completed yet
        df2 = df1[df1['Completed'] == False]
        #sorts by workout id
        df3 = df2.sort_values('Workout_ID')
        #resets the index
        df4 = df3.reset_index()
        #grabs the first workout plan
        current = df4.loc[0, 'WorkoutInfo']

        #global variable for workout id to be used later
        global woid2
        woid = df4.loc[0, 'Workout_ID']
        woid2 = int(woid)

        #global id that turns the current workout into a list
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

        weeks1 = self.length.text
        days1 = self.freq.text
        sports1 = self.sport.text


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



        def exer(z):
            ex = z[0]
            df1 = df[df["Muscle1"].str.contains(ex, case=False, na=False) | df["Muscle2"].str.contains(ex, case=False, na=False) | df["Muscle3"].str.contains(ex, case=False, na=False)]
            mdf = pd.DataFrame(df1)
            mdf2 = mdf.reset_index()
            size = mdf2.index.size
            num = np.random.randint(1, size)
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

    #Displays the workout of the day for the user
    def plan(self):
        self.workout = Label(text='')
        self.add_widget(self.workout)
        self.workout.text = f'{cwo[0]}\n{cwo[1]}\n{cwo[2]}\n{cwo[3]}\n{cwo[4]}\n{cwo[5]}\n{cwo[6]}\n{cwo[7]}\n'

    #Once workout is complete, updates the workout completeness in SQL and slears the workout page
    def comp(self):
        self.workout.text = ""
        result = 1
        update = "UPDATE dbo.[Workouts] SET Completed = (?) WHERE Workout_ID = (?);"
        try:
            cursor.execute(update, result, woid2)
            cnxn.commit()
        except pyodbc.ProgrammingError as ex:
            sql = ex.args[1]
        #Returns user to workout page
        sm.current = 'workout'



#brings in the kivy file
kv = Builder.load_file('login.kv')
#variable for window manager
sm = windowManager()


users = pd.read_csv('login.csv')

#the pages via the window builder
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


#Runs the program
if __name__ == "__main__":
    loginMain().run()


