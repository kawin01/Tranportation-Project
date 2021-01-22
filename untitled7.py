# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:31:04 2021

@author: 70037165
"""
from pulp import *
import pandas as pd

#LpProblem, LpMinimize, LpVariable, lpSum

# Assign spreadsheet filename: file
file = r'C:\Users\70037165\Desktop\SKU Rationalization\SSC for Python.xlsx'

cost_df = pd.read_excel(file, sheet_name = 'Distance', header = 0)
cost_df = cost_df.set_index(['Sending plant', 'Receiving plant'])
costs = cost_df.to_dict()

df = pd.read_excel(file, sheet_name= 'Data', header = 0)
plant = list(set(df['Plant']))
code = list(set(df['Code']))

df = df.set_index(['Code', 'Plant'])
df.sort_index

#sending_plants = []
#receiving_plants = []



for inx, data in df.groupby(level = 0):
    sending_plants = []
    receiving_plants = []
    sending_amount = []
    for inx1, data1 in data.iterrows():
        if data1['Batch'] > (data1['Monthly sales'] * 1.5):
            inx1_list = list(inx1)
            #print(inx1_list[0])
            sending_plants.append(inx1_list[1])
            sending_amount.append((inx1[1], data1['Batch'] - (data1['Monthly sales'] * 1.5)))
        else:
            inx1_list = list(inx1)
            receiving_plants.append(inx1_list[1])

        print('SKU: ' + str(inx1[0]))
        print('sending is: ' + str(sending_plants))
        print('receiving is: ' + str(receiving_plants))
        
        if not sending_plants:
            print('No sending plant\n')
        elif not receiving_plants:
            print('Have sending - but no receiving\n')
        else:
            #sending_amount.append(data1['Batch'] - (data1['Monthly sales'] * 1.5))
            print(sending_amount)
            sending_amount_dict = dict(sending_amount)

#print(costs)


# Initialize Model
            model = LpProblem("Minimize Transportation Costs", LpMinimize)
    
            # Define decision variables
            key = [(s, r) for s in sending_plants for r in receiving_plants]
            var_dict = LpVariable.dicts('sending product amount', 
                                        key, 
                                        lowBound = 0, cat='Float')
            
            
            # Use the LpVariable dictionary variable to define objective
            model += lpSum([costs[(s, r)] * var_dict[(s, r)] 
                            for s in sending_plants for r in receiving_plants])
            
            # Define Constraints
            # For each overproduction plant, sum plant shipment set equal to over quantity
            for s in sending_plants:
                model += lpSum([var_dict[(s, r)] for r in receiving_plants]) == sending_amount_dict[s]
            
            # Solve Model
            model.solve(COIN_CMD(msg=1))
            print("The moving amount is".format(var_dict))


'''
          
print('receiving is: ' + str(receiving_plant))
print('sending is: ' + str(sending_plant))
          




sending_plants s
receing_plants r
sending_amount = [s, sa]

costs [s, r]
from pulp import *
# Initialize Model
model = LpProblem("Minimize Transportation Costs", LpMinimize)

# Define decision variables
key = [(s, r) for s in sending_plants for r in receiving_plants]
var_dict = LpVariable.dicts('moving amount', 
                            key, 
                            lowBound=0, cat='Integer')


# Use the LpVariable dictionary variable to define objective
model += lpSum([costs[(s, r)] * var_dict[(s,r)] 
                for s in sending_plants for r in receiving_plants])

# Define Constraints
# For each overproduction plant, sum plant shipment set equal to over quantity
for s in sending_plants:
    model += lpSum([var_dict[(s, r] for r in receving_plants]) == moving_amount[s]

# Solve Model
model.solve()
print("The moving amount is".format(var_dict))'''
