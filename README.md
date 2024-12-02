# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/images/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro-DOS - Automatização de irrigações

## 👨‍👩 Grupo

Grupo de número <b>55</b> formado pelos integrantes mencionados abaixo.

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/cirohenrique/">Ciro Henrique</a> ( <i>RM559040</i> )
- <a href="javascript:void(0)">Enyd Bentivoglio</a> ( <i>RM560234</i> )
- <a href="https://www.linkedin.com/in/marcofranzoi/">Marco Franzoi</a> ( <i>RM559468</i> )
- <a href="https://www.linkedin.com/in/rodrigo-mazuco-16749b37/">Rodrigo Mazuco</a> ( <i>RM559712</i> )

## 👩‍🏫 Professores:

### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

## 📜 Descrição

<b>Referência</b>: https://on.fiap.com.br/mod/assign/view.php?id=445529&c=12139

Essa versão possui funcionalidades que visam automatizar a execução de irrigações de plantações a partir de medições de sensores e alertas meteorológicos de acordo com a região das plantações.

Algumas informações sobre os módulos dessa versão:

- <strong>Módulo "Culturas"</strong>: Permite que sejam cadastradas diferentes culturas.
- <strong>Módulo "Plantações"</strong>: Permite que sejam cadastradas diferentes plantações, podendo associá-las à culturas utilizando como parâmetro o ID conforme cadastro no módulo "Culturas". Além disso, caso necessário, é possível configurar a plantação com os parâmetros "Temperatura" ( <i>mínimo e máximo - formato °C</i> ), "Umidade" ( <i>mínimo e máximo - formato %</i> ), "Luminosidade" ( <i>mínimo e máximo - formato lux</i> ), "Radiação" ( <i>mínimo e máximo - formato W/m²</i> ), "Salinidade" ( <i>mínimo e máximo - formato dS/m</i> ) e "pH" ( <i>mínimo e máximo - formato inteiro</i> ) para o contexto de culturas, com os parâmetros "Latitude" e "Longitude" para o contexto de localização e "Quantidade de horas para verificação de chuva" e "Quantidade média máxima de chuva" para o contexto de validação de chuva. Esses parâmetros são utilizados, por exemplo, para que a irrigação automática possa ser verificada e executada a partir das medições armazenadas no sistema conforme veremos mais a frente.
- <strong>Módulo "Sensores"</strong>: Permite que sejam cadastrados diferentes sensores com seus códigos de série e associados aos possíveis tipos "Sensor de Temperatura do solo", "Sensor de Umidade do solo", "Sensor de luminosidade", "Sensor de radiação", "Sensor de salinidade do solo" ou "Sensor de pH do solo".
- <strong>Módulo "Irrigações"</strong>: Permite que irrigações sejam iniciadas ou finalizadas manualmente utilizando como parâmetro o ID da plantação desejada conforme cadastro no módulo "Plantações". Ao finalizar uma irrigação, é possível informar a quantidade de água utilizada em formato ml.
- <strong>Módulo "Medições"</strong>: Permite que medições sejam cadastradas utilizando como parâmetro o ID da plantação na qual a medição foi efetuada conforme cadastro no módulo "Plantações", o ID do sensor utilizado na medição conforme cadastro no módulo "Sensores" e o valor da medição. Ao final do cadastro, caso a plantação não esteja com uma irrigação em execução, é possível que a irrigação seja iniciada de forma automática caso o valor da medição atenda às possíveis regras:
    - <strong>Sensor de Temperatura do solo</strong>: Caso a temperatura do solo esteja maior do que o limite máximo configurado. A temperatura influencia a taxa de evaporação. Com temperaturas altas, o solo seca mais rápido, o que pode demandar mais irrigação.
    - <strong>Sensor de Umidade do solo</strong>: Caso a umidade do solo esteja menor do que o limite mínimo configurado. Um nível de umidade abaixo de um limite determinado indica que o solo está seco e precisa de irrigação.
    - <strong>Sensor de luminosidade</strong>: Caso a luminosidade do local da plantação esteja maior do que o limite máximo configurado. A taxa de evaporação é maior quando a luminosidade do local é muito alta, o que pode demandar mais irrigação.
    - <strong>Sensor de radiação</strong>: Caso a radiação do local da plantação esteja maior do que o limite máximo configurado. ocorrerem perdas. A taxa de evaporação é maior quando a taxa de radiação do local é muito alta, o que pode demandar mais irrigação.
    - <strong>Verificação de chuva</strong>: Caso as verificações acima sejam sejam atendidas, será verificado se a região da plantação está sendo afetada com chuvas utilizando como parâmetro a latitude, a longitude e a quantidade de horas entre o horário da medição e as próximas horas. Por fim, caso positivo, será verificado se a quantidade média de chuva no período configurado é inferior à quantidade média máxima de chuva. Mesmo que uma plantação esteja sendo afetada com chuvas, pode ser que o nível de umidade continue abaixo de um limite determinado.
- <strong>Execução dos sensores</strong>: Permite que os sensores sejam simulados, de modo que suas respectivas medições sejam exibidas.
    - <strong>Sensor de Temperatura do solo</strong>: Exemplo desenvolvido de forma simples para simular um sensor de temperatura de solo. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284258762268673. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";
    - <strong>Sensor de Umidade do solo</strong>: Exemplo desenvolvido de forma simples para simular um sensor de umidade de solo. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284346299505665. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";
    - <strong>Sensor de luminosidade</strong>: Exemplo desenvolvido de forma simples para simular um sensor de luminosidade. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284365617425409. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";
    - <strong>Sensor de radiação</strong>: Exemplo desenvolvido de forma simples para simular um sensor de radiação. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284387471852545. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";
    - <strong>Sensor de salinidade do solo</strong>: Exemplo desenvolvido de forma simples para simular um sensor de salinidade de solo. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284404628657153. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";
    - <strong>Sensor de pH do solo</strong>: Exemplo desenvolvido de forma simples para simular um sensor de pH de solo. Pode ser visualizado e testado no seguinte endereço da plataforma Wokwi: https://wokwi.com/projects/414284423030119425. Exemplos de utilização do <i>Serial Plotter</i> estão disponíveis em "";

- <PENDENTE> <Módulos com as bibliotecas "Scikit-learn" e "Streamlit">

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

1. <b>assets</b>: Diretório para armazenamento de arquivos complementares da estrutura do sistema.
    - Diretório "images": Diretório para armazenamento de imagens.

2. <b>config</b>: Diretório para armazenamento de arquivos em formato <i>json</i> contendo configurações.
    - Arquivo "db.json": Configurações destinadadas à conexão com banco de dados.
    - Arquivo "params.json": Configurações do sistema em geral.

3. <b>document</b>: Diretório para armazenamento de documentos relacionados ao sistema.
    - Diretório "sensors": Diretório para armazenamento dos conteúdos relacionados aos sensores do sistema conforme exemplificado na plataforma Wokwi.

4. <b>scripts</b>: Diretório para armazenamento de scripts.
    - Diretório "oracle": Diretório para armazenamento de scripts do banco de dados Oracle.

5. <b>src</b>: Diretório para armazenamento de código fonte do sistema em Python.
    - Diretório "custom": Diretório para armazenamento <i>classes/componentes</i> auxiliares do sistema.
    - Diretório "models": Diretório para armazenamento <i>classes/componentes</i> relacionados ao banco de dados.
    - Diretório "prompt": Diretório para armazenamento arquivos de inicialização do sistema em formato <i>prompt</i>.

6. <b>README.md</b>: Documentação do sistema em formato markdown.

## 🔧 Como executar o código

Como se trata de uma versão em formato <i>prompt</i>, para execução das funcionalidades, os seguintes passos devem ser seguidos:

1. Utilizando algum editor de código compatível com a linguagem de programação Python (<i>VsCode, PyCharm, etc.</i>), acesse o diretório "./src/prompt".
2. Neste diretório, basta abrir o arquivo "main.py" e executá-lo.

Para essa versão não são solicitados parâmetros para acesso como por exemplo <i>username</i>, <i>password</i>, <i>token access</i>, etc.

## 🗃 Histórico de lançamentos

* 1.1.0 - 06/12/2024
* 1.0.0 - 13/11/2024

## 📋 Licença

Desenvolvido pelo Grupo 55 para o projeto da fase 4 (<i>Cap 1 - Automação e inteligência na FarmTech Solutions</i>) da <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a>. Está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>