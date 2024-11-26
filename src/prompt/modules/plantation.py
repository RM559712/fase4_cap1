import datetime
import os
import pprint
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
import prompt.modules.crop as ModuleCrop
from custom.helper import Helper
from models.f3_c1_plantation import F3C1Plantation
from models.f3_c1_plantation_config_irrigation import F3C1PlantationConfigIrrigation
from models.f3_c1_plantation_config_location import F3C1PlantationConfigLocation

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Plantações =-')
    print('')


"""
Método responsável por verificar se existem plantações cadastradas
"""
def validate_exists_data():

    object_f3c1_plantation = F3C1Plantation()
    bool_exists_data = object_f3c1_plantation.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem plantações cadastradas.')


"""
Método responsável por recarregar o módulo "Plantações"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Plantações"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Plantações"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar cadastros',
            'action': action_list
        },{
            'code': 2,
            'title': 'Cadastrar',
            'action': action_insert
        },{
            'code': 3,
            'title': 'Editar',
            'action': action_update
        },{
            'code': 4,
            'title': 'Excluir',
            'action': action_delete
        },{
            'code': 5,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Plantações"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Plantações"

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
Método responsável pela formatação de visualização do ID do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['PLN_ID']}' if 'PLN_ID' in dict_data and type(dict_data['PLN_ID']) != None and Helper.is_int(dict_data['PLN_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da plantação: ')

    while True:

        try:

            if int_return.strip() == '':
                raise Exception('Deve ser informado um ID válido.')

            if Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return)


"""
Método responsável pela formatação de visualização do nome do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_name(dict_data: dict = {}) -> str:

    str_return = 'Nome da plantação: '
    str_return += f'{dict_data['PLN_NAME'].strip()}' if 'PLN_NAME' in dict_data and type(dict_data['PLN_NAME']) != None and type(dict_data['PLN_NAME']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Nome"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_name(dict_data: dict = {}) -> str:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter o nome atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o nome da plantação: '
    str_return = input(f'{str_label}')

    object_f3c1_plantation = F3C1Plantation()

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um nome válido.')

            if bool_is_update == False and type(str_return) != str: 
                raise Exception('O conteúdo informado deve ser texto.')

            if str_return.strip() != '':

                list_params_validate = [

                    {'str_column': 'LOWER(PLN_NAME)', 'str_type_where': '=', 'value': str_return.lower().strip()},
                    F3C1Plantation.get_params_to_active_data()

                ]

                if bool_is_update == True:

                    list_params_validate.append({'str_column': 'PLN_ID', 'str_type_where': '!=', 'value': dict_data['PLN_ID']})

                dict_plantation = object_f3c1_plantation.set_where(list_params_validate).get_one()

                if type(dict_plantation) == dict:
                    raise Exception(f'Já existe um registro cadastrado com o nome "{str_return.strip()}".')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela validação do parâmetro "Cultura"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_crop_id(dict_data: dict = {}) -> int:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter a cultura atual ( abaixo ), basta ignorar o preenchimento.\n{ModuleCrop.format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a cultura: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informada uma cultura válida.')

            if int_return.strip() != '' and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if Helper.is_int(int_return) == True:

                get_data_crop_by_id(int_return)

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return str(int_return.strip())


"""
Método responsável pela formatação de visualização da temperatura do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_temp(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_TEMP_MIN' in dict_data and type(dict_data['PCI_TEMP_MIN']) != None and Helper.is_float(dict_data['PCI_TEMP_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_TEMP_MIN']}°C')

    if 'PCI_TEMP_MAX' in dict_data and type(dict_data['PCI_TEMP_MAX']) != None and Helper.is_float(dict_data['PCI_TEMP_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_TEMP_MAX']}°C')

    str_return = 'Temperatura ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "temperatura mínima" e "temperatura máxima"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_temp(dict_data: dict = {}) -> dict:

    dict_return = {'pci_temp_min': None, 'pci_temp_max': None}

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    print('> Temperatura')
    print('A temperatura será exibida no formato [valor]°C ( ex.: 12°C, 21°C, etc. )')
    print('')

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_temp(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_temp_min = input(f'Caso exista, informe a temperatura mínima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_temp_min.strip() != '' and pci_temp_min.strip().lower() != 'none':

                if ',' in pci_temp_min:
                    pci_temp_min = pci_temp_min.replace(',', '.')

                if Helper.is_float(pci_temp_min) == False and Helper.is_int(pci_temp_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_temp_min = input()

    if pci_temp_min.strip() != '':
        dict_return['pci_temp_min'] = float(pci_temp_min) if pci_temp_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_temp_max = input(f'Caso exista, informe a temperatura máxima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_temp_max.strip() != '' and pci_temp_max.strip().lower() != 'none':

                if ',' in pci_temp_max:
                    pci_temp_max = pci_temp_max.replace(',', '.')

                if Helper.is_float(pci_temp_max) == False and Helper.is_int(pci_temp_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_temp_min']) != type(None) and Helper.is_float(dict_return['pci_temp_min']) == True:

                    if float(pci_temp_max) <= dict_return['pci_temp_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_temp_max = input()

    if pci_temp_max.strip() != '':
        dict_return['pci_temp_max'] = float(pci_temp_max) if pci_temp_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização da umidade do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_humidity(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_HUMIDITY_MIN' in dict_data and type(dict_data['PCI_HUMIDITY_MIN']) != None and Helper.is_float(dict_data['PCI_HUMIDITY_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_HUMIDITY_MIN']}%')

    if 'PCI_HUMIDITY_MAX' in dict_data and type(dict_data['PCI_HUMIDITY_MAX']) != None and Helper.is_float(dict_data['PCI_HUMIDITY_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_HUMIDITY_MAX']}%')

    str_return = 'Umidade ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "umidade mínima" e "umidade máxima"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_humidity(dict_data: dict = {}) -> dict:

    dict_return = {'pci_humidity_min': None, 'pci_humidity_max': None}

    print('> Umidade')
    print('A umidade será exibida no formato [valor]% ( ex.: 12%, 21%, etc. )')
    print('')

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_humidity(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_humidity_min = input(f'Caso exista, informe a umidade mínima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_humidity_min.strip() != '' and pci_humidity_min.strip().lower() != 'none':

                if ',' in pci_humidity_min:
                    pci_humidity_min = pci_humidity_min.replace(',', '.')

                if Helper.is_float(pci_humidity_min) == False and Helper.is_int(pci_humidity_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_humidity_min = input()

    if pci_humidity_min.strip() != '':
        dict_return['pci_humidity_min'] = float(pci_humidity_min) if pci_humidity_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_humidity_max = input(f'Caso exista, informe a umidade máxima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_humidity_max.strip() != '' and pci_humidity_max.strip().lower() != 'none':

                if ',' in pci_humidity_max:
                    pci_humidity_max = pci_humidity_max.replace(',', '.')

                if Helper.is_float(pci_humidity_max) == False and Helper.is_int(pci_humidity_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_humidity_min']) != type(None) and Helper.is_float(dict_return['pci_humidity_min']) == True:

                    if float(pci_humidity_max) <= dict_return['pci_humidity_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_humidity_max = input()

    if pci_humidity_max.strip() != '':
        dict_return['pci_humidity_max'] = float(pci_humidity_max) if pci_humidity_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização da luminosidade do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_light(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_LIGHT_MIN' in dict_data and type(dict_data['PCI_LIGHT_MIN']) != None and Helper.is_float(dict_data['PCI_LIGHT_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_LIGHT_MIN']} lux')

    if 'PCI_LIGHT_MAX' in dict_data and type(dict_data['PCI_LIGHT_MAX']) != None and Helper.is_float(dict_data['PCI_LIGHT_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_LIGHT_MAX']} lux')

    str_return = 'Luminosidade ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "luminosidade mínima" e "luminosidade máxima"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_light(dict_data: dict = {}) -> dict:

    dict_return = {'pci_light_min': None, 'pci_light_max': None}

    print('> Luminosidade')
    print('A luminosidade será exibida no formato [valor] lux ( ex.: 12 lux, 21 lux, etc. )')
    print('')

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_light(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_light_min = input(f'Caso exista, informe a luminosidade mínima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_light_min.strip() != '' and pci_light_min.strip().lower() != 'none':

                if ',' in pci_light_min:
                    pci_light_min = pci_light_min.replace(',', '.')

                if Helper.is_float(pci_light_min) == False and Helper.is_int(pci_light_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_light_min = input()

    if pci_light_min.strip() != '':
        dict_return['pci_light_min'] = float(pci_light_min) if pci_light_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_light_max = input(f'Caso exista, informe a luminosidade máxima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_light_max.strip() != '' and pci_light_max.strip().lower() != 'none':

                if ',' in pci_light_max:
                    pci_light_max = pci_light_max.replace(',', '.')

                if Helper.is_float(pci_light_max) == False and Helper.is_int(pci_light_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_light_min']) != type(None) and Helper.is_float(dict_return['pci_light_min']) == True:

                    if float(pci_light_max) <= dict_return['pci_light_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_light_max = input()

    if pci_light_max.strip() != '':
        dict_return['pci_light_max'] = float(pci_light_max) if pci_light_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização da radiação solar do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_radiation(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_RADIATION_MIN' in dict_data and type(dict_data['PCI_RADIATION_MIN']) != None and Helper.is_float(dict_data['PCI_RADIATION_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_RADIATION_MIN']} W/m²')

    if 'PCI_RADIATION_MAX' in dict_data and type(dict_data['PCI_RADIATION_MAX']) != None and Helper.is_float(dict_data['PCI_RADIATION_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_RADIATION_MAX']} W/m²')

    str_return = 'Radiação solar ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "radiação solar mínima" e "radiação solar máxima"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_radiation(dict_data: dict = {}) -> dict:

    dict_return = {'pci_radiation_min': None, 'pci_radiation_max': None}

    print('> Radiação solar')
    print('A radiação solar será exibida no formato [valor] W/m² ( ex.: 12 W/m², 21 W/m², etc. )')
    print('')

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_radiation(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_radiation_min = input(f'Caso exista, informe a radiação solar mínima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_radiation_min.strip() != '' and pci_radiation_min.strip().lower() != 'none':

                if ',' in pci_radiation_min:
                    pci_radiation_min = pci_radiation_min.replace(',', '.')

                if Helper.is_float(pci_radiation_min) == False and Helper.is_int(pci_radiation_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_radiation_min = input()

    if pci_radiation_min.strip() != '':
        dict_return['pci_radiation_min'] = float(pci_radiation_min) if pci_radiation_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_radiation_max = input(f'Caso exista, informe a radiação solar máxima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_radiation_max.strip() != '' and pci_radiation_max.strip().lower() != 'none':

                if ',' in pci_radiation_max:
                    pci_radiation_max = pci_radiation_max.replace(',', '.')

                if Helper.is_float(pci_radiation_max) == False and Helper.is_int(pci_radiation_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_radiation_min']) != type(None) and Helper.is_float(dict_return['pci_radiation_min']) == True:

                    if float(pci_radiation_max) <= dict_return['pci_radiation_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_radiation_max = input()

    if pci_radiation_max.strip() != '':
        dict_return['pci_radiation_max'] = float(pci_radiation_max) if pci_radiation_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização da salinidade do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_salinity(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_SALINITY_MIN' in dict_data and type(dict_data['PCI_SALINITY_MIN']) != None and Helper.is_float(dict_data['PCI_SALINITY_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_SALINITY_MIN']} dS/m')

    if 'PCI_SALINITY_MAX' in dict_data and type(dict_data['PCI_SALINITY_MAX']) != None and Helper.is_float(dict_data['PCI_SALINITY_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_SALINITY_MAX']} dS/m')

    str_return = 'Salinidade ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "salinidade mínima" e "salinidade máxima"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_salinity(dict_data: dict = {}) -> dict:

    dict_return = {'pci_salinity_min': None, 'pci_salinity_max': None}

    print('> Salinidade')
    print('A salinidade será exibida no formato [valor] dS/m ( ex.: 12 dS/m, 21 dS/m, etc. )')
    print('')

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_salinity(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_salinity_min = input(f'Caso exista, informe a salinidade mínima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_salinity_min.strip() != '' and pci_salinity_min.strip().lower() != 'none':

                if ',' in pci_salinity_min:
                    pci_salinity_min = pci_salinity_min.replace(',', '.')

                if Helper.is_float(pci_salinity_min) == False and Helper.is_int(pci_salinity_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_salinity_min = input()

    if pci_salinity_min.strip() != '':
        dict_return['pci_salinity_min'] = float(pci_salinity_min) if pci_salinity_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_salinity_max = input(f'Caso exista, informe a salinidade máxima para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_salinity_max.strip() != '' and pci_salinity_max.strip().lower() != 'none':

                if ',' in pci_salinity_max:
                    pci_salinity_max = pci_salinity_max.replace(',', '.')

                if Helper.is_float(pci_salinity_max) == False and Helper.is_int(pci_salinity_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_salinity_min']) != type(None) and Helper.is_float(dict_return['pci_salinity_min']) == True:

                    if float(pci_salinity_max) <= dict_return['pci_salinity_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_salinity_max = input()

    if pci_salinity_max.strip() != '':
        dict_return['pci_salinity_max'] = float(pci_salinity_max) if pci_salinity_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização do pH do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_ph(dict_data: dict = {}) -> str:

    str_return = None
    list_labels = []

    if 'PCI_PH_MIN' in dict_data and type(dict_data['PCI_PH_MIN']) != None and Helper.is_float(dict_data['PCI_PH_MIN']) == True:
        list_labels.append(f'Mínimo de {dict_data['PCI_PH_MIN']}')

    if 'PCI_PH_MAX' in dict_data and type(dict_data['PCI_PH_MAX']) != None and Helper.is_float(dict_data['PCI_PH_MAX']) == True:
        list_labels.append(f'Máximo de {dict_data['PCI_PH_MAX']}')

    str_return = 'pH ideal: '
    str_return += f'{' | ' . join(list_labels)}' if len(list_labels) > 0 else 'N/I'

    return str_return


"""
Método responsável pela validação dos parâmetros "pH mínimo" e "pH máximo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_ph(dict_data: dict = {}) -> dict:

    dict_return = {'pci_ph_min': None, 'pci_ph_max': None}

    print('> pH')
    print('O pH será exibido no formato [valor] ( ex.: 12, 21, etc. )')
    print('')

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos. Caso queira apagar o valor, digite "none".\n{format_data_view_ph(dict_data)}\n')

    # ----------------
    # Parâmetro mínimo
    # ----------------

    pci_ph_min = input(f'Caso exista, informe o pH mínimo para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_ph_min.strip() != '' and pci_ph_min.strip().lower() != 'none':

                if ',' in pci_ph_min:
                    pci_ph_min = pci_ph_min.replace(',', '.')

                if Helper.is_float(pci_ph_min) == False and Helper.is_int(pci_ph_min) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_ph_min = input()

    if pci_ph_min.strip() != '':
        dict_return['pci_ph_min'] = float(pci_ph_min) if pci_ph_min.strip().lower() != 'none' else ''

    # ----------------
    # Parâmetro máximo
    # ----------------

    print('')

    pci_ph_max = input(f'Caso exista, informe o pH máximo para plantio em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if pci_ph_max.strip() != '' and pci_ph_max.strip().lower() != 'none':

                if ',' in pci_ph_max:
                    pci_ph_max = pci_ph_max.replace(',', '.')

                if Helper.is_float(pci_ph_max) == False and Helper.is_int(pci_ph_max) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

                if type(dict_return['pci_ph_min']) != type(None) and Helper.is_float(dict_return['pci_ph_min']) == True:

                    if float(pci_ph_max) <= dict_return['pci_ph_min']:
                        raise Exception(f'O valor máximo deve ser maior que o valor mínimo.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            pci_ph_max = input()

    if pci_ph_max.strip() != '':
        dict_return['pci_ph_max'] = float(pci_ph_max) if pci_ph_max.strip().lower() != 'none' else ''

    return dict_return


"""
Método responsável pela formatação de visualização da latitude do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_latitude(dict_data: dict = {}) -> str:

    str_return = 'Latitude: '
    str_return += f'{dict_data['PCL_LATITUDE']}' if 'PCL_LATITUDE' in dict_data and type(dict_data['PCL_LATITUDE']) != None and Helper.is_float(dict_data['PCL_LATITUDE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Latitude"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_latitude(dict_data: dict = {}) -> float:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter a latitude atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_latitude(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a latitude da plantação em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da longitude do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_longitude(dict_data: dict = {}) -> str:

    str_return = 'Longitude: '
    str_return += f'{dict_data['PCL_LONGITUDE']}' if 'PCL_LONGITUDE' in dict_data and type(dict_data['PCL_LONGITUDE']) != None and Helper.is_float(dict_data['PCL_LONGITUDE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Longitude"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_longitude(dict_data: dict = {}) -> float:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter a longitude atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_longitude(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a longitude da plantação em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da quantidade de horas para verificação de chuva do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_next_hours_validate_rain(dict_data: dict = {}) -> str:

    str_return = 'Quantidade de horas para verificação de chuva: '
    str_return += f'{dict_data['PCL_NEXT_HOURS_VALIDATE_RAIN']}h' if 'PCL_NEXT_HOURS_VALIDATE_RAIN' in dict_data and type(dict_data['PCL_NEXT_HOURS_VALIDATE_RAIN']) != None and Helper.is_int(dict_data['PCL_NEXT_HOURS_VALIDATE_RAIN']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Quantidade de horas para verificação de chuva"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_next_hours_validate_rain(dict_data: dict = {}) -> int:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter a quantidade de horas para verificação de chuva atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_next_hours_validate_rain(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a quantidade de horas para verificação de chuva em formato numérico ( ex.: 123 ): '
    int_return = input(f'{str_label}')

    while True:

        try:

            if int_return.strip() != '' and int_return.strip().lower() != 'none':

                if Helper.is_int(int_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    int_value = None
    if int_return.strip() != '':
        int_value = float(int_return) if int_return.strip().lower() != 'none' else ''

    return int_value


"""
Método responsável pela formatação de visualização da quantidade média máxima de chuva do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_max_average_rain_volume(dict_data: dict = {}) -> str:

    str_return = 'Quantidade média máxima de chuva: '
    str_return += f'{dict_data['PCL_MAX_AVERAGE_RAIN_VOLUME']} mm' if 'PCL_MAX_AVERAGE_RAIN_VOLUME' in dict_data and type(dict_data['PCL_MAX_AVERAGE_RAIN_VOLUME']) != None and Helper.is_int(dict_data['PCL_MAX_AVERAGE_RAIN_VOLUME']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Quantidade média máxima de chuva"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_max_average_rain_volume(dict_data: dict = {}) -> float:

    bool_is_update = ('PLN_ID' in dict_data and type(dict_data['PLN_ID']) == int)

    str_label = f'Importante: Caso deseje manter a quantidade média máxima de chuva atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_max_average_rain_volume(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a quantidade média máxima de chuva da plantação em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['PLN_INSERT_DATE'])}' if 'PLN_INSERT_DATE' in dict_data and type(dict_data['PLN_INSERT_DATE']) != None and type(dict_data['PLN_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['PLN_UPDATE_DATE'])}' if 'PLN_UPDATE_DATE' in dict_data and type(dict_data['PLN_UPDATE_DATE']) != None and type(dict_data['PLN_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )
- bool_show_id: Status informando se o parâmetro "ID" deverá ser exibido ( bool )
- bool_show_insert_date: Status informando se o parâmetro "Data de cadastro" deverá ser exibido ( bool )
- bool_show_update_date Status informando se o parâmetro "Data de atualização" deverá ser exibido ( bool )

Return: str
"""
def format_data_view(dict_data: dict = {}, bool_show_id: bool = True, bool_show_insert_date: bool = True, bool_show_update_date: bool = True) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_id(dict_data)} \n' if bool_show_id == True else ''
        str_return += f'- {format_data_view_name(dict_data)} \n'
        str_return += f'- {ModuleCrop.format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_temp(dict_data)} \n'
        str_return += f'- {format_data_view_humidity(dict_data)} \n'
        str_return += f'- {format_data_view_light(dict_data)} \n'
        str_return += f'- {format_data_view_radiation(dict_data)} \n'
        str_return += f'- {format_data_view_salinity(dict_data)} \n'
        str_return += f'- {format_data_view_ph(dict_data)} \n'
        str_return += f'- {format_data_view_latitude(dict_data)} \n'
        str_return += f'- {format_data_view_longitude(dict_data)} \n'
        str_return += f'- {format_data_view_next_hours_validate_rain(dict_data)} \n'
        str_return += f'- {format_data_view_max_average_rain_volume(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Plantações"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f3c1_plantation = F3C1Plantation()

    object_f3c1_plantation.set_select(['PLN.*', 'CRP.CRP_NAME', 'PCI.*', 'PCL.*'])
    object_f3c1_plantation.set_table('F3_C1_PLANTATION PLN')
    object_f3c1_plantation.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F3_C1_CROP CRP', 'str_where': 'CRP.CRP_ID = PLN.PLN_CRP_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F3_C1_PLANTATION_CONFIG_IRRIGATION PCI', 'str_where': 'PCI.PCI_PLN_ID = PLN.PLN_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F3_C1_PLANTATION_CONFIG_LOCATION PCL', 'str_where': 'PCL.PCL_PLN_ID = PLN.PLN_ID'}
    ])
    object_f3c1_plantation.set_where([F3C1Plantation.get_params_to_active_data()])
    object_f3c1_plantation.set_order([{'str_column': 'PLN.PLN_ID', 'str_type_order': 'ASC'}])
    list_data = object_f3c1_plantation.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada plantação
"""
def get_data_by_id(int_pln_id: int = 0) -> dict:

    object_f3c1_plantation = F3C1Plantation()

    object_f3c1_plantation.set_select(['PLN.*', 'CRP.CRP_NAME', 'PCI.*', 'PCL.*'])
    object_f3c1_plantation.set_table('F3_C1_PLANTATION PLN')
    object_f3c1_plantation.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F3_C1_CROP CRP', 'str_where': 'CRP.CRP_ID = PLN.PLN_CRP_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F3_C1_PLANTATION_CONFIG_IRRIGATION PCI', 'str_where': 'PCI.PCI_PLN_ID = PLN.PLN_ID'},
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F3_C1_PLANTATION_CONFIG_LOCATION PCL', 'str_where': 'PCL.PCL_PLN_ID = PLN.PLN_ID'}
    ])
    object_f3c1_plantation.set_where([

        {'str_column': 'PLN.PLN_ID', 'str_type_where': '=', 'value': int_pln_id},
        F3C1Plantation.get_params_to_active_data()

    ])

    dict_data = object_f3c1_plantation.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_pln_id}.')

    return object_f3c1_plantation


"""
Método responsável por executar a ação de retorno de dados de configurações de irrigação uma determinada plantação
"""
def get_data_config_irrigation_by_id(int_pln_id: int = 0) -> dict:

    object_f3c1_plantation_config_irrigation = F3C1PlantationConfigIrrigation()

    object_f3c1_plantation_config_irrigation.set_where([

        {'str_column': 'PCI_PLN_ID', 'str_type_where': '=', 'value': int_pln_id},
        F3C1PlantationConfigIrrigation.get_params_to_active_data()

    ])

    dict_data = object_f3c1_plantation_config_irrigation.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro de configuração de irrigação foi localizado com o ID {int_pln_id}.')

    return object_f3c1_plantation_config_irrigation


"""
Método responsável por executar a ação de retorno de dados de localização uma determinada plantação
"""
def get_data_config_location_by_id(int_pln_id: int = 0) -> dict:

    object_f3c1_plantation_config_location = F3C1PlantationConfigLocation()

    object_f3c1_plantation_config_location.set_where([

        {'str_column': 'PCL_PLN_ID', 'str_type_where': '=', 'value': int_pln_id},
        F3C1PlantationConfigLocation.get_params_to_active_data()

    ])

    dict_data = object_f3c1_plantation_config_location.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro de configuração de localização foi localizado com o ID {int_pln_id}.')

    return object_f3c1_plantation_config_location


"""
Método responsável por executar a ação de retorno de dados de uma determinada cultura
"""
def get_data_crop_by_id(crp_id: int = 0) -> dict:

    object_f3c1_crop = ModuleCrop.get_data_by_id(crp_id)
    dict_data = object_f3c1_crop.get_one()

    return dict_data


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Plantações"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da plantação.')
    print('')

    str_pln_name = validate_name()

    print('')

    int_pln_crp_id = validate_crop_id()

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da configuração para que o sistema automático de irrigação seja executado. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    dict_temp = validate_temp()

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_humidity = validate_humidity()

    # -------
    # Etapa 5
    # -------

    Main.init_step()

    show_head_module()

    dict_light = validate_light()

    # -------
    # Etapa 6
    # -------

    Main.init_step()

    show_head_module()

    dict_radiation = validate_radiation()

    # -------
    # Etapa 7
    # -------

    Main.init_step()

    show_head_module()

    dict_salinity = validate_salinity()

    # -------
    # Etapa 8
    # -------

    Main.init_step()

    show_head_module()

    dict_ph = validate_ph()

    # -------
    # Etapa 9
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da localização geográfica da plantação. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # --------
    # Etapa 10
    # --------

    Main.init_step()

    show_head_module()

    float_pcl_latitude = validate_latitude()

    print('')

    float_pcl_longitude = validate_longitude()

    print('')

    int_pcl_next_hours_validate_rain = validate_next_hours_validate_rain()

    print('')

    float_pcl_max_average_rain_volume = validate_max_average_rain_volume()

    Main.loading('Salvando dados, por favor aguarde...')

    # --------
    # Etapa 11
    # --------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['PLN_NAME'] = str_pln_name
    dict_data['PLN_CRP_ID'] = int_pln_crp_id

    object_f3c1_plantation = F3C1Plantation()
    object_f3c1_plantation.insert(dict_data)

    int_pln_id = object_f3c1_plantation.get_last_id()

    # ----------------------------------------------------------------
    # Processo de cadastro dos parâmetros de configuração de irrigação
    # ----------------------------------------------------------------

    dict_data_config_irrigation = {}

    dict_data_config_irrigation['PCI_PLN_ID'] = int_pln_id

    if 'pci_temp_min' in dict_temp and type(dict_temp['pci_temp_min']) != type(None):
        dict_data_config_irrigation['PCI_TEMP_MIN'] = dict_temp['pci_temp_min']

    if 'pci_temp_max' in dict_temp and type(dict_temp['pci_temp_max']) != type(None):
        dict_data_config_irrigation['PCI_TEMP_MAX'] = dict_temp['pci_temp_max']

    if 'pci_humidity_min' in dict_humidity and type(dict_humidity['pci_humidity_min']) != type(None):
        dict_data_config_irrigation['PCI_HUMIDITY_MIN'] = dict_humidity['pci_humidity_min']

    if 'pci_humidity_max' in dict_humidity and type(dict_humidity['pci_humidity_max']) != type(None):
        dict_data_config_irrigation['PCI_HUMIDITY_MAX'] = dict_humidity['pci_humidity_max']

    if 'pci_light_min' in dict_light and type(dict_light['pci_light_min']) != type(None):
        dict_data_config_irrigation['PCI_LIGHT_MIN'] = dict_light['pci_light_min']

    if 'pci_light_max' in dict_light and type(dict_light['pci_light_max']) != type(None):
        dict_data_config_irrigation['PCI_LIGHT_MAX'] = dict_light['pci_light_max']

    if 'pci_radiation_min' in dict_radiation and type(dict_radiation['pci_radiation_min']) != type(None):
        dict_data_config_irrigation['PCI_RADIATION_MIN'] = dict_radiation['pci_radiation_min']

    if 'pci_radiation_max' in dict_radiation and type(dict_radiation['pci_radiation_max']) != type(None):
        dict_data_config_irrigation['PCI_RADIATION_MAX'] = dict_radiation['pci_radiation_max']

    if 'pci_salinity_min' in dict_salinity and type(dict_salinity['pci_salinity_min']) != type(None):
        dict_data_config_irrigation['PCI_SALINITY_MIN'] = dict_salinity['pci_salinity_min']

    if 'pci_salinity_max' in dict_salinity and type(dict_salinity['pci_salinity_max']) != type(None):
        dict_data_config_irrigation['PCI_SALINITY_MAX'] = dict_salinity['pci_salinity_max']

    if 'pci_ph_min' in dict_ph and type(dict_ph['pci_ph_min']) != type(None):
        dict_data_config_irrigation['PCI_PH_MIN'] = dict_ph['pci_ph_min']

    if 'pci_ph_max' in dict_ph and type(dict_ph['pci_ph_max']) != type(None):
        dict_data_config_irrigation['PCI_PH_MAX'] = dict_ph['pci_ph_max']

    object_f3c1_plantation_config_irrigation = F3C1PlantationConfigIrrigation()
    object_f3c1_plantation_config_irrigation.insert(dict_data_config_irrigation)

    # --------------------------------------------------
    # Processo de cadastro dos parâmetros de localização
    # --------------------------------------------------

    dict_data_config_location = {}

    dict_data_config_location['PCL_PLN_ID'] = int_pln_id
    dict_data_config_location['PCL_LATITUDE'] = float_pcl_latitude
    dict_data_config_location['PCL_LONGITUDE'] = float_pcl_longitude
    dict_data_config_location['PCL_NEXT_HOURS_VALIDATE_RAIN'] = int_pcl_next_hours_validate_rain
    dict_data_config_location['PCL_MAX_AVERAGE_RAIN_VOLUME'] = float_pcl_max_average_rain_volume

    object_f3c1_plantation_config_location = F3C1PlantationConfigLocation()
    object_f3c1_plantation_config_location.insert(dict_data_config_location)

    # Retorno de dados após o cadastro
    object_f3c1_plantation = get_data_by_id(int_pln_id)
    dict_data = object_f3c1_plantation.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Plantações"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_pln_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f3c1_plantation = get_data_by_id(int_pln_id)
    dict_data = object_f3c1_plantation.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da plantação.')
    print('')

    str_pln_name = validate_name(dict_data)

    print('')

    int_pln_crp_id = validate_crop_id(dict_data)

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da configuração para que o sistema automático de irrigação seja executado. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 5
    # -------

    Main.init_step()

    show_head_module()

    dict_temp = validate_temp(dict_data)

    # -------
    # Etapa 6
    # -------

    Main.init_step()

    show_head_module()

    dict_humidity = validate_humidity(dict_data)

    # -------
    # Etapa 7
    # -------

    Main.init_step()

    show_head_module()

    dict_light = validate_light(dict_data)

    # -------
    # Etapa 8
    # -------

    Main.init_step()

    show_head_module()

    dict_radiation = validate_radiation(dict_data)

    # -------
    # Etapa 9
    # -------

    Main.init_step()

    show_head_module()

    dict_salinity = validate_salinity(dict_data)

    # --------
    # Etapa 10
    # --------

    Main.init_step()

    show_head_module()

    dict_ph = validate_ph(dict_data)

    # --------
    # Etapa 11
    # --------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da localização geográfica da plantação. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # --------
    # Etapa 12
    # --------

    Main.init_step()

    show_head_module()

    float_pcl_latitude = validate_latitude(dict_data)

    print('')

    float_pcl_longitude = validate_longitude(dict_data)

    print('')

    int_pcl_next_hours_validate_rain = validate_next_hours_validate_rain(dict_data)

    print('')

    float_pcl_max_average_rain_volume = validate_max_average_rain_volume(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # --------
    # Etapa 13
    # --------

    Main.init_step()

    show_head_module()

    if str_pln_name.strip() != '':
        dict_data['PLN_NAME'] = str_pln_name

    if int_pln_crp_id.strip() != '':
        dict_data['PLN_CRP_ID'] = int_pln_crp_id

    object_f3c1_plantation.update(dict_data)

    # -------------------------------------------------------------------
    # Processo de atualização dos parâmetros de configuração de irrigação
    # -------------------------------------------------------------------

    object_f3c1_plantation_config_irrigation = get_data_config_irrigation_by_id(int_pln_id)
    dict_data_config_irrigation = object_f3c1_plantation_config_irrigation.get_one()

    if 'pci_temp_min' in dict_temp and type(dict_temp['pci_temp_min']) != type(None):
        dict_data_config_irrigation['PCI_TEMP_MIN'] = dict_temp['pci_temp_min']

    if 'pci_temp_max' in dict_temp and type(dict_temp['pci_temp_max']) != type(None):
        dict_data_config_irrigation['PCI_TEMP_MAX'] = dict_temp['pci_temp_max']

    if 'pci_humidity_min' in dict_humidity and type(dict_humidity['pci_humidity_min']) != type(None):
        dict_data_config_irrigation['PCI_HUMIDITY_MIN'] = dict_humidity['pci_humidity_min']

    if 'pci_humidity_max' in dict_humidity and type(dict_humidity['pci_humidity_max']) != type(None):
        dict_data_config_irrigation['PCI_HUMIDITY_MAX'] = dict_humidity['pci_humidity_max']

    if 'pci_light_min' in dict_light and type(dict_light['pci_light_min']) != type(None):
        dict_data_config_irrigation['PCI_LIGHT_MIN'] = dict_light['pci_light_min']

    if 'pci_light_max' in dict_light and type(dict_light['pci_light_max']) != type(None):
        dict_data_config_irrigation['PCI_LIGHT_MAX'] = dict_light['pci_light_max']

    if 'pci_radiation_min' in dict_radiation and type(dict_radiation['pci_radiation_min']) != type(None):
        dict_data_config_irrigation['PCI_RADIATION_MIN'] = dict_radiation['pci_radiation_min']

    if 'pci_radiation_max' in dict_radiation and type(dict_radiation['pci_radiation_max']) != type(None):
        dict_data_config_irrigation['PCI_RADIATION_MAX'] = dict_radiation['pci_radiation_max']

    if 'pci_salinity_min' in dict_salinity and type(dict_salinity['pci_salinity_min']) != type(None):
        dict_data_config_irrigation['PCI_SALINITY_MIN'] = dict_salinity['pci_salinity_min']

    if 'pci_salinity_max' in dict_salinity and type(dict_salinity['pci_salinity_max']) != type(None):
        dict_data_config_irrigation['PCI_SALINITY_MAX'] = dict_salinity['pci_salinity_max']

    if 'pci_ph_min' in dict_ph and type(dict_ph['pci_ph_min']) != type(None):
        dict_data_config_irrigation['PCI_PH_MIN'] = dict_ph['pci_ph_min']

    if 'pci_ph_max' in dict_ph and type(dict_ph['pci_ph_max']) != type(None):
        dict_data_config_irrigation['PCI_PH_MAX'] = dict_ph['pci_ph_max']

    object_f3c1_plantation_config_irrigation.update(dict_data_config_irrigation)

    # -----------------------------------------------------
    # Processo de atualização dos parâmetros de localização
    # -----------------------------------------------------

    object_f3c1_plantation_config_location = get_data_config_location_by_id(int_pln_id)
    dict_data_config_location = object_f3c1_plantation_config_location.get_one()

    if type(float_pcl_latitude) != type(None):
        dict_data_config_location['PCL_LATITUDE'] = float_pcl_latitude

    if type(float_pcl_longitude) != type(None):
        dict_data_config_location['PCL_LONGITUDE'] = float_pcl_longitude

    if type(int_pcl_next_hours_validate_rain) != type(None):
        dict_data_config_location['PCL_NEXT_HOURS_VALIDATE_RAIN'] = int_pcl_next_hours_validate_rain

    if type(float_pcl_max_average_rain_volume) != type(None):
        dict_data_config_location['PCL_MAX_AVERAGE_RAIN_VOLUME'] = float_pcl_max_average_rain_volume

    if type(dict_data_config_location) != type(None):
        object_f3c1_plantation_config_location.update(dict_data_config_location)

    # Retorno de dados após as atualizações
    object_f3c1_plantation = get_data_by_id(int_pln_id)
    dict_data = object_f3c1_plantation.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Plantações"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_pln_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f3c1_plantation = get_data_by_id(int_pln_id)
    dict_data = object_f3c1_plantation.get_one()

    dict_data['PLN_STATUS'] = F3C1Plantation.STATUS_DELETED

    object_f3c1_plantation.update(dict_data)

    # ----------------------------------------------------------------
    # Processo de exclusão dos parâmetros de configuração de irrigação
    # ----------------------------------------------------------------

    object_f3c1_plantation_config_irrigation = get_data_config_irrigation_by_id(int_pln_id)
    dict_data_config_irrigation = object_f3c1_plantation_config_irrigation.get_one()

    dict_data_config_irrigation['PCI_STATUS'] = F3C1PlantationConfigIrrigation.STATUS_DELETED

    object_f3c1_plantation_config_irrigation.update(dict_data_config_irrigation)

    # --------------------------------------------------
    # Processo de exclusão dos parâmetros de localização
    # --------------------------------------------------

    object_f3c1_plantation_config_location = get_data_config_location_by_id(int_pln_id)
    dict_data_config_location = object_f3c1_plantation_config_location.get_one()

    dict_data_config_location['PCL_STATUS'] = F3C1PlantationConfigLocation.STATUS_DELETED

    object_f3c1_plantation_config_location.update(dict_data_config_location)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Plantações"
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