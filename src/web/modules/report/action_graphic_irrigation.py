import os
import sys

import streamlit as Streamlit
import pandas as Pandas
import matplotlib.pyplot as Pyplot
import numpy as Numpy
import seaborn as Seaborn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from models.f4_c1_irrigation import F4C1Irrigation
from models.f4_c1_plantation import F4C1Plantation

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes à estrutura do sistema
# ---------------------------------------------------------------------------------------------------------------

def get_data_by_plantation(int_pln_id: int = 0) -> dict:

    object_f4c1_plantation = F4C1Plantation()

    object_f4c1_plantation.set_select(['PLN.*', 'CRP.CRP_NAME', 'PCI.*', 'PCL.*'])
    object_f4c1_plantation.set_table('F4_C1_PLANTATION PLN')
    object_f4c1_plantation.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_C1_CROP CRP', 'str_where': 'CRP.CRP_ID = PLN.PLN_CRP_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F4_C1_PLANTATION_CONFIG_IRRIGATION PCI', 'str_where': 'PCI.PCI_PLN_ID = PLN.PLN_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F4_C1_PLANTATION_CONFIG_LOCATION PCL', 'str_where': 'PCL.PCL_PLN_ID = PLN.PLN_ID'}
    ])
    object_f4c1_plantation.set_where([

        {'str_column': 'PLN.PLN_ID', 'str_type_where': '=', 'value': int_pln_id},
        F4C1Plantation.get_params_to_active_data()

    ])

    dict_data = object_f4c1_plantation.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhuma plantação foi localizada com o ID {int_pln_id}.')

    return object_f4c1_plantation

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes à exibição da página
# ---------------------------------------------------------------------------------------------------------------

Streamlit.title('Gráfico de irrigação')

try:

    pln_id = Streamlit.number_input('Informe o ID da plantação', value = None, min_value = 0, max_value = 99999)

    if pln_id is None:

        Streamlit.write('Para exibir o gráfico de dispersão, deve ser informado o ID de uma plantação.')
        Streamlit.write('Após o preenchimento, pressione <enter>.')

    else:

        object_f4c1_crop = get_data_by_plantation(pln_id)
        dict_data_plantation = object_f4c1_crop.get_one()

        object_f4c1_irrigation = F4C1Irrigation()

        dict_data_finished_execution = object_f4c1_irrigation.get_finished_execution_by_plantation(pln_id = pln_id)
        if dict_data_finished_execution['status'] == False:
            raise Exception(dict_data_finished_execution['message'])

        if dict_data_finished_execution['list_data'] == None:
            raise Exception('Não existem irrigações cadastradas para essa plantação.')

        object_dataframe = Pandas.DataFrame(dict_data_finished_execution['list_data'])

        del object_dataframe['IRG_ID']
        del object_dataframe['IRG_PLN_ID']
        del object_dataframe['IRG_INSERT_DATE']
        del object_dataframe['IRG_UPDATE_DATE']

        object_dataframe['IRG_INI_DATE'] = Pandas.to_datetime(object_dataframe['IRG_INI_DATE'])
        object_dataframe['IRG_END_DATE'] = Pandas.to_datetime(object_dataframe['IRG_END_DATE'])

        object_dataframe['IRG_DURATION'] = (object_dataframe['IRG_END_DATE'] - object_dataframe['IRG_INI_DATE']).dt.total_seconds() / 60
        object_dataframe['IRG_HOUR_INI'] = object_dataframe['IRG_INI_DATE'].dt.hour
        object_dataframe['IRG_WEEK_DAY'] = object_dataframe['IRG_INI_DATE'].dt.dayofweek
        object_dataframe['IRG_WATER_LITER'] = object_dataframe['IRG_WATER'] / 1000

        Streamlit.subheader("Dados Processados")
        Streamlit.dataframe(object_dataframe)

        list_x = object_dataframe[['IRG_HOUR_INI', 'IRG_WEEK_DAY', 'IRG_DURATION', 'IRG_ORIGIN']]
        list_y = object_dataframe['IRG_WATER_LITER']

        X_train, X_test, y_train, y_test = train_test_split(list_x, list_y, test_size = 0.3, random_state = 42)

        object_random_forest_regressor = RandomForestRegressor()
        object_random_forest_regressor.fit(X_train, y_train)

        y_pred = object_random_forest_regressor.predict(X_test)
        float_accuracy = object_random_forest_regressor.score(X_test, y_test)

        float_mse = mean_squared_error(y_test, y_pred)
        float_rmse = Numpy.sqrt(float_mse)
        float_mae = mean_absolute_error(y_test, y_pred)
        float_mape = mean_absolute_percentage_error(y_test, y_pred)
        float_r2 = r2_score(y_test, y_pred)

        # Métricas
        Streamlit.subheader("Métricas do Modelo")
        Streamlit.write(f'Erro Quadrático Médio: {float_mse:.2f}')
        Streamlit.write(f'Raiz do Erro Quadrático Médio: {float_rmse:.2f}')
        Streamlit.write(f'Acurácia com Random Forest Regressor: {float_accuracy:.2f}')
        Streamlit.write(f'Média do Erro Absoluto: {float_mae:.2f}')
        Streamlit.write(f'Erro Percentual Médio Absoluto: {float_mape:.2f}')
        Streamlit.write(f'Coeficiente de Determinação: {float_r2:.2f}')

        # Gráfico de dispersão
        Streamlit.subheader("Gráfico: Valores Reais x Valores Previstos")
        object_figure, object_axes = Pyplot.subplots(figsize = (8, 6))
        Seaborn.scatterplot(x = y_test, y = y_pred, ax = object_axes)
        object_axes.plot([list_y.min(), list_y.max()], [list_y.min(), list_y.max()], '--r', label = 'Ideal')
        object_axes.set_xlabel('Valores reais (em litros)')
        object_axes.set_ylabel('Valores previstos (em litros)')
        object_axes.set_title(f"Valores Reais x Previstos - {dict_data_finished_execution['list_data'][0]['PLN_NAME']}")
        object_axes.legend()
        Streamlit.pyplot(object_figure)

except Exception as error:

    Streamlit.error(f'Ocorreu o seguinte erro: {error}')