import datetime
import os
import pprint
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
import prompt.modules.crop as ModuleCrop
import prompt.modules.plantation as ModulePlantation
from custom.helper import Helper
from models.f4_c1_irrigation import F4C1Irrigation

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Irrigações =-')
    print('')


"""
Método responsável por verificar se existem irrigações cadastradas
"""
def validate_exists_data():

    object_f4c1_irrigation = F4C1Irrigation()
    bool_exists_data = object_f4c1_irrigation.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem irrigações cadastradas.')


"""
Método responsável por recarregar o módulo "Irrigações"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Irrigações"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Irrigações"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar execuções',
            'action': action_list
        },{
            'code': 2,
            'title': 'Iniciar irrigação por plantação',
            'action': action_ini
        },{
            'code': 3,
            'title': 'Finalizar irrigação por plantação',
            'action': action_end
        },{
            'code': 4,
            'title': 'Visualizar informações de irrigação ativa por plantação',
            'action': action_view_status
        },{
            'code': 5,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Irrigações"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Irrigações"

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
Método responsável pela formatação de visualização do ID do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['IRG_ID']}' if 'IRG_ID' in dict_data and type(dict_data['IRG_ID']) != None and Helper.is_int(dict_data['IRG_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da irrigação: ')

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
Método responsável pela formatação de visualização da origem da execução da irrigação do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_origin(dict_data: dict = {}) -> str:

    object_f4c1_irrigation = F4C1Irrigation()

    str_return = 'Origem: '
    str_return += f'{object_f4c1_irrigation.get_label_origin(dict_data['IRG_ORIGIN'])}' if 'IRG_ORIGIN' in dict_data and type(dict_data['IRG_ORIGIN']) != None and Helper.is_int(dict_data['IRG_ORIGIN']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de início da irrigação do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_ini_date(dict_data: dict = {}) -> str:

    str_return = 'Data de início: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['IRG_INI_DATE'])}' if 'IRG_INI_DATE' in dict_data and type(dict_data['IRG_INI_DATE']) != None and type(dict_data['IRG_INI_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de finalização da irrigação do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_end_date(dict_data: dict = {}) -> str:

    str_return = 'Data de finalização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['IRG_END_DATE'])}' if 'IRG_END_DATE' in dict_data and type(dict_data['IRG_END_DATE']) != None and type(dict_data['IRG_END_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetros "Quantidade de água"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: dict
"""
def validate_water(dict_data: dict = {}) -> float:

    bool_is_update = ('IRG_ID' in dict_data and type(dict_data['IRG_ID']) == int)

    print('> Quantidade de água')
    print('A quantidade de água será exibida no formato [valor] ml ( ex.: 12 ml, 21 ml, etc. )')
    print('')

    if bool_is_update == True:
        print(f'Importante: Caso deseje manter os valores atuais ( abaixo ), basta ignorar os preenchimentos.\n{format_data_view_water(dict_data)}\n')

    int_return = input(f'Informe a quantidade de água utilizada na irrigação em formato numérico ( ex.: 123, 123.45 ou 123,45 ): ')

    while True:

        try:

            if ',' in int_return:
                int_return = int_return.replace(',', '.')

            if Helper.is_float(int_return) == False and Helper.is_int(int_return) == False:
                raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int_return


"""
Método responsável pela formatação de visualização da quantidade de água do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_water(dict_data: dict = {}) -> str:

    str_return = 'Quantidade de água: '
    str_return += f'{dict_data['IRG_WATER']} ml' if 'IRG_WATER' in dict_data and type(dict_data['IRG_WATER']) != None and Helper.is_float(dict_data['IRG_WATER']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do status de execução execução da irrigação do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_status_execution(dict_data: dict = {}) -> str:

    object_f4c1_irrigation = F4C1Irrigation()

    str_return = 'Status de execução: '
    str_return += f'{object_f4c1_irrigation.get_label_status_execution(dict_data['IRG_STATUS_EXECUTION'])}' if 'IRG_STATUS_EXECUTION' in dict_data and type(dict_data['IRG_STATUS_EXECUTION']) != None and Helper.is_int(dict_data['IRG_STATUS_EXECUTION']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['IRG_INSERT_DATE'])}' if 'IRG_INSERT_DATE' in dict_data and type(dict_data['IRG_INSERT_DATE']) != None and type(dict_data['IRG_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Irrigações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['IRG_UPDATE_DATE'])}' if 'IRG_UPDATE_DATE' in dict_data and type(dict_data['IRG_UPDATE_DATE']) != None and type(dict_data['IRG_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Irrigações"

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
        str_return += f'- {ModulePlantation.format_data_view_name(dict_data)} \n'
        str_return += f'- {ModuleCrop.format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_origin(dict_data)} \n'
        str_return += f'- {format_data_view_ini_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_end_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_water(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_status_execution(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Irrigações"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4c1_irrigation = F4C1Irrigation()

    object_f4c1_irrigation.set_select(['IRG.*', 'PLN.PLN_NAME', 'CRP.CRP_NAME'])
    object_f4c1_irrigation.set_table('F4_C1_IRRIGATION IRG')
    object_f4c1_irrigation.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_C1_PLANTATION PLN', 'str_where': 'PLN.PLN_ID = IRG.IRG_PLN_ID'},
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_C1_CROP CRP', 'str_where': 'CRP.CRP_ID = PLN.PLN_CRP_ID'}
    ])
    object_f4c1_irrigation.set_where([F4C1Irrigation.get_params_to_active_data()])
    object_f4c1_irrigation.set_order([{'str_column': 'IRG_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4c1_irrigation.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada irrigação
"""
def get_data_by_id(int_irg_id: int = 0) -> dict:

    object_f4c1_irrigation = F4C1Irrigation()

    object_f4c1_irrigation.set_where([

        {'str_column': 'IRG_ID', 'str_type_where': '=', 'value': int_irg_id},
        F4C1Irrigation.get_params_to_active_data()

    ])

    dict_data = object_f4c1_irrigation.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_irg_id}.')

    return object_f4c1_irrigation


"""
Método responsável por executar a ação de retorno de dados de uma determinada plantação
"""
def get_data_plantation_by_id(pln_id: int = 0) -> dict:

    object_f4c1_plantation = ModulePlantation.get_data_by_id(pln_id)
    dict_data = object_f4c1_plantation.get_one()

    return dict_data


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de inicialização de irrigação do módulo "Irrigações"
"""
def action_ini():

    Main.init_step()

    show_head_module()

    pln_id = ModulePlantation.validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    dict_data_plantation = get_data_plantation_by_id(pln_id)

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(ModulePlantation.format_data_view(dict_data_plantation))

    input(f'Pressione <enter> para iniciar a irrigação para a plantação informada...')

    # -------
    # Etapa 3
    # -------

    Main.loading('Iniciando irrigação, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4c1_irrigation = F4C1Irrigation()

    dict_begin_execution = object_f4c1_irrigation.begin_execution_by_plantation({'pln_id': dict_data_plantation['PLN_ID'], 'irg_origin': F4C1Irrigation.ORIGIN_MANUAL})
    if dict_begin_execution['status'] == False:
        raise Exception(dict_begin_execution['message'])

    print('Irrigação iniciada com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de finalização de irrigação do módulo "Irrigações"
"""
def action_end():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    pln_id = ModulePlantation.validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    get_data_plantation_by_id(pln_id)

    object_f4c1_irrigation = F4C1Irrigation()

    dict_active_irrigation = object_f4c1_irrigation.get_active_execution_by_plantation(pln_id)
    if dict_active_irrigation['status'] == False:
        raise Exception(dict_active_irrigation['message'])

    print('Os dados abaixo representam a irrigação atual ativa do registro informado.')
    print('')

    print(format_data_view(dict_active_irrigation['dict_data']))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    irg_water = validate_water()

    Main.loading('Finalizando irrigação, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_finish_execution = object_f4c1_irrigation.finish_execution_by_plantation({

        'pln_id': pln_id,
        'irg_water': irg_water

    })

    if dict_finish_execution['status'] == False:
        raise Exception(dict_finish_execution['message'])

    print('Irrigação finalizada com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de visualização de status de irrigação do módulo "Irrigações"
"""
def action_view_status():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    pln_id = ModulePlantation.validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    get_data_plantation_by_id(pln_id)

    object_f4c1_irrigation = F4C1Irrigation()

    dict_active_irrigation = object_f4c1_irrigation.get_active_execution_by_plantation(pln_id)
    if dict_active_irrigation['status'] == False:
        raise Exception(dict_active_irrigation['message'])

    print('Os dados abaixo representam a irrigação atual ativa do registro informado.')
    print('')

    print(format_data_view(dict_active_irrigation['dict_data']))

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Irrigações"
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