import pandas as pd
import pyodbc


cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=BRILAPTOP\SQLEXPRESS;"
                      "Database=Capstone;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
query = "SELECT [UserName], [Password] FROM dbo.Users;"

df = pd.read_sql(query, cnxn)


weeks = int(input("How often "))
days = int(input("How often  "))
sport = int(input("Sport "))
day = list()
n = 8

match sport:
    case 1: #snowboarding
        upper = ['core', 'biceps', 'triceps', 'back', 'shoulder']
        lower = ['calves', 'hamstrings', 'glutes', 'quads']
    case 2: #rock climbing
        upper = ['forearms', 'biceps', 'back', 'core', 'triceps']
        lower = ['calves', 'hamstrings', 'glutes', 'quads']
    case 3: #dance
        upper = ['chest', 'back', 'shoulders', 'biceps', 'triceps', 'core']
        lower = ['ankles', 'feet', 'calves', 'hamstrings', 'glutes', 'quads', 'hip flexors']

match days:
    case 1:
        result = [[upper, upper, upper, upper, lower, lower, lower, lower]]
    case 2:
        result = [[upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower]]
    case 3:
        result = [[upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower], [upper, upper, upper, upper, lower, lower, lower, lower]]
    case 4:
        result = [[upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower], [upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower]]
    case 5:
        result = [[upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower], [upper, upper, upper, upper, lower, lower, lower, lower], [upper, upper, upper, upper, upper, upper, upper, upper], [lower, lower, lower, lower, lower, lower, lower, lower]]


#print(result)  # Output: two

def daily(x):
    for y in x:
        for z in y:
            ex = z[0]
            day.append(ex)
            val = z.pop(0)
            z.append(val)



def week():
    daily(result)
    a = [day[i:i + n] for i in range(0, len(day), n)]
    print(a)
    day.clear()


def full(y):
    for x in range(y):
        week()



full(weeks)
