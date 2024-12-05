import datetime
import os
import pprint
import subprocess
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as Pandas
import matplotlib.pyplot as Pyplot
import numpy as Numpy
import seaborn as Seaborn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score

import prompt.main as Main
import prompt.modules.plantation as ModulePlantation
from custom.helper import Helper
from models.f4_c1_irrigation import F4C1Irrigation

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Gráficos =-')
    print('')


"""
Método responsável por recarregar o módulo "Gráficos"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Gráficos"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Gráficos"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar gráfico de irrigação',
            'action': action_graphic_irrigation
        },{
            'code': 2,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Gráficos"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Gráficos"

Return: str
"""
def validate_menu_option() -> str:

    str_return = input(f'Digite uma opção: ')

    while True:

        try:

            if str_return.strip() == '':
                raise Exception('Deve ser definida uma opção válida.')

            if Helper.is_int(str_return) == False: 
                raise Exception('A opção informada deve ser numérica.')

            if int(str_return) not in get_menu_options_codes(): 
                raise Exception('A opção informada deve representar um dos menus disponíveis.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str_return


"""
Método responsável por solicitar a opção do sistema que deverá ser executada
"""
def require_menu_option():

    str_option = validate_menu_option()

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        if dict_menu_option['code'] == int(str_option):
            dict_menu_option['action']()


"""
Método responsável pela exibição de gráfico de irrigação do módulo "Gráficos"
"""
def action_graphic_irrigation():

    Main.init_step()

    show_head_module()

    pln_id = ModulePlantation.validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4c1_crop = ModulePlantation.get_data_by_id(pln_id)
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

    x = object_dataframe[['IRG_HOUR_INI', 'IRG_WEEK_DAY', 'IRG_DURATION', 'IRG_ORIGIN']]
    y = object_dataframe['IRG_WATER_LITER']

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)

    object_random_forest_regressor = RandomForestRegressor()
    object_random_forest_regressor.fit(X_train, y_train)

    y_pred = object_random_forest_regressor.predict(X_test)
    float_accuracy = object_random_forest_regressor.score(X_test, y_test)

    float_mse = mean_squared_error(y_test, y_pred)
    float_rmse = Numpy.sqrt(float_mse)
    float_mae = mean_absolute_error(y_test, y_pred)
    float_mape = mean_absolute_percentage_error(y_test, y_pred)
    float_r2 = r2_score(y_test, y_pred)

    # Gráfico de dispersão
    Pyplot.figure(figsize = (8, 6))
    Seaborn.scatterplot(x = y_test, y = y_pred)
    Pyplot.plot([y.min(), y.max()], [y.min(), y.max()], '--r', label = 'Ideal')
    Pyplot.xlabel('Valores reais (em litros)')
    Pyplot.ylabel('Valores previstos (em litros)')
    Pyplot.title(f'Valores reais x Valores previstos - {dict_data_plantation['PLN_NAME']}')
    Pyplot.legend()

    Main.init_step()

    show_head_module()

    print(f'Erro Quadrático Médio: {float_mse:.2f}')
    print(f'Raiz do Erro Quadrático Médio: {float_rmse:.2f}')
    print(f'Acurácia com Random Forest Regressor: {float_accuracy:.2f}')
    print(f'Média do Erro Absoluto: {float_mae:.2f}')
    print(f'Erro Percentual Médio Absoluto: {float_mape:.2f}')
    print(f'Coeficiente de Determinação: {float_r2:.2f}')

    print('')

    print('Visualizando gráfico...')

    Pyplot.show()

    Main.init_step()

    show_head_module()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Gráficos"
"""
def action_main():

    try:

        Main.init_step()

        Main.test_connection_by_database()

        show_head_module()

        list_menu_options = get_menu_options()

        for dict_menu_option in list_menu_options:
            print(f'{dict_menu_option['code']}. {dict_menu_option['title']}')

        print('')

        require_menu_option()

    except Exception as error:

        print(f'> Ocorreu o seguinte erro: {error}')
        require_reload()