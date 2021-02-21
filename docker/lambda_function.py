from pulp import *
import json

def lambda_handler(event, context):
    Ingredients = event['Ingredients']
    costs = event['cost']
    proteinPercent = event['proteinPercent']
    fatPercent = event['fatPercent']
    fibrePercent = event['fibrePercent']
    saltPercent = event['saltPercent']

    modelo, modelo_dict_result, modelo_status, modelo_objective = exec_otm(Ingredients, costs, proteinPercent, fatPercent, fibrePercent, saltPercent)
    
    return {
        'statusCode':200,
        'modelo': modelo,
        'modelo_dict_result': modelo_dict_result,
        'modelo_status': modelo_status,
        'modelo_objective': modelo_objective
    }


def exec_otm(Ingredients:list, costs:dict, proteinPercent:dict, fatPercent:dict, fibrePercent:dict, saltPercent:dict):
    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("The Blendind Problem", LpMinimize)

    # A dictionary called 'ingredient_vars' is created to contain the referenced Variables
    ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)

    # The objective function is added to 'prob' first
    prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]), "Total Cost of Ingredients per can"

    # The five constraints are added to 'prob'
    prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
    prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
    prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
    prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
    prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    #print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    dict_result={}
    for v in prob.variables():
        dict_result[v.name] = v.varValue

    # The optimised objective function value is printed to the screen    
    #print("Total Cost of Ingredients per can = ", value(prob.objective))

    return str(prob), dict_result, LpStatus[prob.status], value(prob.objective)