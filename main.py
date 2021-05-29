import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Create data table for question 1
con = sqlite3.connect(":memory:")
cur = con.cursor()

#create SQL tables
cur.execute("""CREATE TABLE name_table (StudentID text, Name text);""")
cur.execute("""CREATE TABLE mark_table (StudentID text, Total_marks integer);""")

#fill tables with data
cur.execute("""INSERT INTO name_table VALUES ('V001', 'Abe'), ('V002', 'Abhay'), ('V003', 'Acelin'), ('V004', 'Adelphos');""")
cur.execute("""INSERT INTO mark_table VALUES ('V001', 95), ('V002', 80), ('V003', 74), ('V004', 81);""")
con.commit()

#create Pandas dataframes
name_df = pd.DataFrame({"StudentID": ["V001", "V002", "V003", "V004"], "Name": ["Abe", "Abhay", "Acelin", "Adelphos"]})
mark_df = pd.DataFrame({"StudentID": ["V001", "V002", "V003", "V004"], "Total_marks": [95, 80, 74, 81]})


#Question 1a
print("\nQuestion 1a:\n")
print("StudentID\tName\n==========================")
for row in cur.execute("SELECT name_table.StudentID, Name, Total_marks FROM name_table, mark_table WHERE name_table.StudentID = mark_table.StudentID AND mark_table.Total_marks > (SELECT Total_marks FROM mark_table WHERE StudentID = 'V002');"):
    print(f"{row[0]}\t\t{row[1]}")

#Question 1b
print("\nQuestion 1b:\n")
def capitalize_E(df):
    #apply to dataframe col of names
    def proc_name(name):
        if 'e' in name or 'E' in name:
            return name.upper()
        else:
            return name.lower()

    df["Name"] = df["Name"].apply(proc_name)

    return df

name_df = capitalize_E(name_df)
print(name_df)

#Question 1c
print("\nQuestion 1c:\n")

def case_marks(name_df, mark_df):
    #merge dfs for easier work
    df = name_df.merge(mark_df, on="StudentID")

    #find all upper/lower case names
    upper = df.loc[lambda df: df["Name"].str.isupper(), :]
    lower = df.loc[lambda df: df["Name"].str.islower(), :]

    #create df with all summary stats
    summary_df = pd.DataFrame({"Uppercase": upper.describe().values[:,0], "Lowercase": lower.describe().values[:,0]}, index=upper.describe().index.values)
    return summary_df

summary_df = case_marks(name_df, mark_df)
print(summary_df)

#Question 2:
print("\nQuestion 2:\n")
#load df
wh_df = pd.read_csv("2017.csv")
print(f"Dataframe Shape: {wh_df.shape}\n")

#count & drop NA
print("N/A Values\n==========")
print(wh_df.isna().sum())
#print(wh_df.loc[wh_df.isna()==True,:])
print("\nN/A Rows:\n==========")
print(wh_df[wh_df.isna().any(axis=1)])

#fix rows with bad position title
wh_df.iloc[250,4] = wh_df.iloc[250,3][10:]
wh_df.iloc[250,3] = "Per Annum"
wh_df.iloc[350,4] = wh_df.iloc[350,3][10:]
wh_df.iloc[350,3] = "Per Annum"

print("\nN/A Values After Fix:\n=====================")
print(wh_df.isna().sum())
print()

#convert salary to float
print("\nSalary information:\n===================")
wh_df["SALARY"] = wh_df["SALARY"].apply(lambda s: float(s[1:].replace(",","")))
print(wh_df["SALARY"].describe())

#investigate rows with $0 salary
print("\nIndividuals with $0 Salary:\n===========================")
print(wh_df.loc[lambda df: df["SALARY"] == 0])

#Get summary of status
print("\nStatus:\n============")
title, count = np.unique(wh_df["STATUS"], return_counts=True)
for row in range(len(title)):
    print(f"{title[row]}: {count[row]}")

#display salaries by status
grouped = wh_df[["SALARY", "STATUS"]].groupby(["STATUS"])
labels = grouped.mean().index.values
vals = grouped.mean().values
stds = grouped.std().values / grouped.count().values

plt.bar(labels, vals[:,0])
plt.errorbar(labels, vals[:,0], yerr=stds[:,0], color="red", fmt='none')
plt.title("Mean Salary by Employment Status")
plt.xlabel("Employment Status")
plt.ylabel("Mean Salary (USD)")
plt.show()


#Get summary of positions
'''print("\nPosition:\n============")
position, count = np.unique(wh_df["POSITION TITLE"], return_counts=True)
for row in range(len(position)):
    print(f"{position[row]}: {count[row]}")'''

#condense positions to smaller categories
print("\nPosition by Group:\n============")
def group_pos(pos):
    if "DEPUTY ASSISTANT" in pos:
        return "DEPUTY ASSISTANT"
    elif "SPECIAL ASSISTANT" in pos:
        return "SPECIAL ASSISTANT"
    elif "ASSISTANT" in pos:
        return "ASSISTANT"
    elif "DEPUTY DIRECTOR" in pos:
        return "DEPUTY DIRECTOR"
    elif "DIRECTOR" in pos:
        return "DIRECTOR"
    elif "SUPERVISOR" in pos:
        return "SUPERVISOR"
    else:
        return "MISC"

wh_df["POSITION_GROUPED"] = wh_df["POSITION TITLE"].apply(group_pos)
position, count = np.unique(wh_df["POSITION_GROUPED"], return_counts=True)
for row in range(len(position)):
    print(f"{position[row]}: {count[row]}")


#display salaries
salary, count = np.unique(wh_df["SALARY"], return_counts=True)
plt.hist(salary)
plt.title("Histogram of Salaries")
plt.xlabel("Salary (USD)")
plt.ylabel("Number of Employees")
plt.show()


#display salaries by group
grouped = wh_df[["SALARY", "POSITION_GROUPED"]].groupby(["POSITION_GROUPED"])
labels = grouped.mean().index.values
vals = grouped.mean().values
stds = grouped.std().values / grouped.count().values

plt.bar(labels, vals[:,0])
plt.errorbar(labels, vals[:,0], yerr=stds[:,0], color="red", fmt='none')
plt.title("Mean Salary by Position Category")
plt.xlabel("Position Category")
plt.ylabel("Mean Salary (USD)")
plt.show()


#Question (?) - Between Question 2 and 3, unlabelled:
print("\nQuestion 3:\n\nSummary Stats:\n================")
df_3 = pd.read_csv("data.csv", index_col=0, header=None)
print(df_3.describe())
plt.hist(df_3.values)
plt.title("Unnamed Data Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
