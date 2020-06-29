import pandas as pd
import numpy as np

from pulp import *
pd.set_option('display.max_columns', None)

food_list = df['Foods'].tolist()
food_cost = {}
food_calories = {}
food_cholestrol = {}
food_fat = {}
food_sodium = {}
food_carbohydrates = {}
food_fiber = {}
food_protein = {}
food_vit_a = {}
food_vit_c = {}
food_calcium = {}
food_iron = {}

for food in food_list:
    food_cost[food] = float(df[df['Foods'] == food]['Price/ Serving'].values)
    food_calories[food] = float(df[df['Foods'] == food]['Calories'].values)
    food_cholestrol[food] = float(df[df['Foods'] == food]['Cholesterol mg'].values)
    food_fat[food] = float(df[df['Foods'] == food]['Total_Fat g'].values)
    food_sodium[food] = float(df[df['Foods'] == food]['Sodium mg'].values)
    food_carbohydrates[food] = float(df[df['Foods'] == food]['Carbohydrates g'].values)
    food_fiber[food] = float(df[df['Foods'] == food]['Dietary_Fiber g'].values)
    food_protein[food] = float(df[df['Foods'] == food]['Protein g'].values)
    food_vit_a[food] = float(df[df['Foods'] == food]['Vit_A IU'].values)
    food_vit_c[food] = float(df[df['Foods'] == food]['Vit_C IU'].values)
    food_calcium[food] = float(df[df['Foods'] == food]['Calcium mg'].values)
    food_iron[food] = float(df[df['Foods'] == food]['Iron mg'].values)


prob = LpProblem("The_Diet_Problem", LpMinimize)

# Food variables, continous, more than 0
food_vars = LpVariable.dicts("Foods",food_list,0)
# Define Objective Function
prob += lpSum([food_cost[i]*food_vars[i] for i in food_list]), "total diet cost"

# Define nutrition Constraints
prob += lpSum([food_calories[i]*food_vars[i] for i in food_list]) >= 1500, "min calorie intake"
prob += lpSum([food_calories[i]*food_vars[i] for i in food_list]) <= 2500, "max calorie intake"

prob += lpSum([food_cholestrol[i]*food_vars[i] for i in food_list]) >= 30, "min cholestrol intake"
prob += lpSum([food_cholestrol[i]*food_vars[i] for i in food_list]) <= 240, "max cholestrol intake"

prob += lpSum([food_fat[i]*food_vars[i] for i in food_list]) >= 20, "min fat intake"
prob += lpSum([food_fat[i]*food_vars[i] for i in food_list]) <= 70, "max fat intake"

prob += lpSum([food_sodium[i]*food_vars[i] for i in food_list]) >= 800, "min sodium intake"
prob += lpSum([food_sodium[i]*food_vars[i] for i in food_list]) <= 2000, "max sodium intake"

prob += lpSum([food_carbohydrates[i]*food_vars[i] for i in food_list]) >= 130, "min carbohydrate intake"
prob += lpSum([food_carbohydrates[i]*food_vars[i] for i in food_list]) <= 450, "max carbohydrate intake"

prob += lpSum([food_fiber[i]*food_vars[i] for i in food_list]) >= 125, "min fiber intake"
prob += lpSum([food_fiber[i]*food_vars[i] for i in food_list]) <= 250, "max fiber intake"

prob += lpSum([food_protein[i]*food_vars[i] for i in food_list]) >= 60, "min protein intake"
prob += lpSum([food_protein[i]*food_vars[i] for i in food_list]) <= 100, "max protein intake"

prob += lpSum([food_vit_a[i]*food_vars[i] for i in food_list]) >= 1000, "min vit_a intake"
prob += lpSum([food_vit_a[i]*food_vars[i] for i in food_list]) <= 10000, "max vit_a intake"

prob += lpSum([food_vit_c[i]*food_vars[i] for i in food_list]) >= 400, "min vit_c intake"
prob += lpSum([food_vit_c[i]*food_vars[i] for i in food_list]) <= 5000, "max vit_c intake"

prob += lpSum([food_calcium[i]*food_vars[i] for i in food_list]) >= 700, "min calcium intake"
prob += lpSum([food_calcium[i]*food_vars[i] for i in food_list]) <= 1500, "max calcium intake"

prob += lpSum([food_iron[i]*food_vars[i] for i in food_list]) >= 10, "min iron intake"
prob += lpSum([food_iron[i]*food_vars[i] for i in food_list]) <= 40, "max iron intake"

prob.writeLP("dietmodel.lp")
prob.solve()
print("Status:", LpStatus[prob.status])

for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
        
print("Total cost of cheapest diet = $", round(value(prob.objective),2))