import streamlit as st
import json
import requests
import pandas as pd
import numpy as np
from PIL import Image



def exec_otm(Ingredients:list, costs:dict, proteinPercent:dict, fatPercent:dict, fibrePercent:dict, saltPercent:dict):
    # Build data dict
    u = 'https://9m9k32x7tj.execute-api.us-east-1.amazonaws.com/test/otm-blending'

    d = {
        'Ingredients':Ingredients,
        'cost':costs,
        'proteinPercent':proteinPercent,
        'fatPercent':fatPercent,
        'fibrePercent':fibrePercent,
        'saltPercent':saltPercent

        }

    # Send request
    res = requests.post(url=u, data=json.dumps(d))


    # Convert data
    content = json.loads(res.content)
    return content['modelo'], content['modelo_dict_result'], content['modelo_status'], content['modelo_objective']

# composicao dos produtos

# A dictionary of the protein percent in each of the Ingredients is created
proteinPercent = {'Frango': 0.100, 
                  'Carne Bovina': 0.200, 
                  'Carneiro': 0.150, 
                  'Arroz': 0.000, 
                  'Trigo': 0.040, 
                  'Gel': 0.000}

# A dictionary of the fat percent in each of the Ingredients is created
fatPercent = {'Frango': 0.080, 
              'Carne Bovina': 0.100, 
              'Carneiro': 0.110, 
              'Arroz': 0.010, 
              'Trigo': 0.010, 
              'Gel': 0.000}

# A dictionary of the fibre percent in each of the Ingredients is created
fibrePercent = {'Frango': 0.001, 
                'Carne Bovina': 0.005, 
                'Carneiro': 0.003, 
                'Arroz': 0.100, 
                'Trigo': 0.150, 
                'Gel': 0.000}

# A dictionary of the salt percent in each of the Ingredients is created
saltPercent = {'Frango': 0.002, 
               'Carne Bovina': 0.005, 
               'Carneiro': 0.007, 
               'Arroz': 0.002, 
               'Trigo': 0.008, 
               'Gel': 0.000}

st.sidebar.title('Entre com o custos e com os produtos para a otimização')
# input para o modelo
# Add a selectbox to the sidebar:
produtos_considerados = st.sidebar.multiselect(
    'Quais produtos considerar?',
    ('Frango', 'Carne Bovina', 'Carneiro', 'Arroz','Trigo','Gel'), ('Frango', 'Carne Bovina', 'Carneiro', 'Arroz','Trigo','Gel')
)

custo_padrao ={'Frango': 0.013, 
         'Carne Bovina': 0.008, 
         'Carneiro': 0.010, 
         'Arroz': 0.002, 
         'Trigo': 0.005, 
         'Gel': 0.001}

produtos_custo={}
# custos
for i in produtos_considerados:
    produtos_custo[i] = st.sidebar.number_input("Custo "+i, custo_padrao[i], format='%f')

#left_column, right_column = st.beta_columns(2)

# MAIN
st.markdown("<h1 style='text-align: center; color: red;'>Otimização: Problema da Mistura</h1>", unsafe_allow_html=True)


image = Image.open('figures/figura_principal.png')

st.image(image, caption='Problema da Mistura', use_column_width=True)

if st.sidebar.button('Otimizar'):
    proteinPercent_new = { your_key: proteinPercent[your_key] for your_key in produtos_custo.keys() }
    fatPercent_new = { your_key: fatPercent[your_key] for your_key in produtos_custo.keys() }
    fibrePercent_new = { your_key: fibrePercent[your_key] for your_key in produtos_custo.keys() }
    saltPercent_new = { your_key: saltPercent[your_key] for your_key in produtos_custo.keys() }

    modelo, modelo_dict_result, modelo_status, modelo_objective = exec_otm(list(produtos_custo.keys()), produtos_custo, proteinPercent_new, fatPercent_new, fibrePercent_new, saltPercent_new)
    #left_column.write(modelo)
    st.write('Status da Solução: ' + str(modelo_status))
    st.write('Custo total da solução: US$ ' + str(modelo_objective) )
    #st.write(modelo_dict_result)
    st.write('Quantidade (gramas) a ser comprada de cada produto:')
    st.write(pd.DataFrame(np.reshape(list(modelo_dict_result.values()), (-1, len(produtos_custo.keys()))), columns=list(produtos_custo.keys())))



