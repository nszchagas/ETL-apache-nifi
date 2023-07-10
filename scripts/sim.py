from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json
import datetime
from datetime import datetime
from json import JSONEncoder

# Essa classe herda a classe StreamCallback, do apache/nifi.

# Função para converter o código armazenado no sistema para
# um ENUM correspondente.


def format_enum(opcoes, cod):
    if cod == "" or cod == "null" or cod == None:
        return 'IGNORADO'
    try:
        opcao = opcoes[int(cod)]
    except Exception:
        try:
            opcao = opcoes[cod]
        except Exception:
            opcao = None

    return opcao


def format_linha(linha):
    if linha:
        return linha.replace('*', '')
    return None


def format_date(date):
    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None

    d = int(date[0:2])
    m = int(date[2:4])
    y = int(date[4:])
    data = datetime(y, m, d)

    return data.strftime("%Y-%m-%d %H:%M:%S.000")


def format_timestamp(date, time="0000"):

    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None

    d = int(date[0:2])
    m = int(date[2:4])
    y = int(date[4:])

    if not (time == "" or time == None or time == "null" or time == "None"):
        h = int(time[0:2])
        mins = int(time[2:])
    else:
        h = 0
        mins = 0
    s = 0
    data = datetime(y, m, d, h, mins, s)

    return data.strftime("%Y-%m-%d %H:%M:%S.000")
    # return int(data.timestamp())


def format_escolaridade(dados):
    escolaridade = 'IGNORADO'

    # A escolaridade pode estar em um dos três campos: ESC, ESC2010 e ESCFALAGR1.
    esc = {1: 'NENHUMA', 2: 'FUND_I_INC', 3: 'FUND_II_INC',
           4: 'MEDIO_INC', 5: 'MEDIO_COMP', 9: 'IGNORADO'}
    esc2010 = {0: 'NENHUMA', 1: 'FUND_I_COMP', 2: 'FUND_II_COMP',
               3: 'MEDIO_COMP', 4: 'SUPERIOR_INC', 5: 'SUPERIOR_COMP', 9: 'IGNORADO'}
    escfalagr1 = {0: 'NENHUMA', 1: 'FUND_I_INC', 2: 'FUND_I_COMP', 3: 'FUND_II_INC', 4: 'FUND_II_COMP', 5: 'MEDIO_INC',
                  6: 'MEDIO_COMP', 7: 'SUPERIOR_INC', 8: 'SUPERIOR_COMP', 9: 'IGNORADO', 10: 'IGNORADO', 11: 'IGNORADO', 12: 'IGNORADO'}
    if dados['ESC']:
        return format_enum(esc, dados['ESC'])
    if dados['ESC2010']:
        return format_enum(esc2010, dados['ESC2010'])
    if dados['ESCFALAGR1']:
        return format_enum(escfalagr1, dados['ESCFALAGR1'])

    return escolaridade


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        # Opções para os enums
        circunstancia = {1: 'ACIDENTE', 2: 'SUICIDIO',
                         3: 'HOMICIO', 4: 'OUTROS', 9: 'IGNORADO'}

        opcoes_parto = {1: 'ANTES', 2: 'DURANTE', 3: 'DEPOIS', 9: 'IGNORADO'}

        tipo_resgate_opcoes = {1: 'NAO_ACRESCENTOU',
                               2: 'SIM_NOVAS_INFORMACOES', 3: 'SIM_CORRECAO_CAUSAS'}
        # ENUMS
        fonte_investigacao = {1: 'CMMI', 2: 'ENTREVISTA_FAMILIA', 3: 'PRONTUARIO',
                              4: 'BANCOS_DE_DADOS', 5: 'SVO', 6: 'IML', 7: 'OUTRA', 8: 'MULTIPLAS_FONTES', 9: 'IGNORADO'}

        tipo_resgate_informacao = {
            1: 'NAO_ACRESCENTOU', 2: 'SIM_NOVAS_INFOS', 3: 'SIM_CORRECAO'}

        nivel_investigador = {'E': 'ESTADUAL',
                              'R': 'REGIONAL', 'M': 'MUNICIPAL'}

        sexo = {'M': 'M', 'F': 'F', 'I': 'IGNORADO'}

        etnia = {1: 'BRANCA', 2: 'PRETA',
                 3: 'AMARELA', 4: 'PARDA', 5: 'INDIGENA'}

        estado_civil = {1: 'SOLTEIRO', 2: 'CASADO', 3: 'VIUVO',
                        4: 'SEPARADO', 5: 'UNIAO_CONSENSUAL', 9: 'IGNORADO'}

        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        jc = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.

        d = {}

        # Óbito
        d['idObito'] = jc['contador']
        d['dataHora'] = format_timestamp(
            jc['DTOBITO'], jc['HORAOBITO'])
        d['circunstancia'] = format_enum(circunstancia, jc['CIRCOBITO'])
        d['isObitoFetal'] = (jc['TIPOBITO'] == 1)
        d['houveAlteracaoCausa'] = (jc['ALTCAUSA'] == 1)
        d['obitoEmRelacaoAoParto'] = format_enum(
            opcoes_parto, jc['OBITOPARTO'])
        d['crmAtestante'] = jc['ATESTANTE']
        d['causaBasica'] = jc['CAUSABAS']

        date_keys = ['DTNASC', 'DTATESTADO',
                     'DTINVESTIG', 'DTCADINV', 'DTCONINV']

        for dk in date_keys:
            jc[dk] = format_date(jc[dk])

        # Pessoa falecida
        d['naturalidade'] = jc['NATURAL']
        d['codMunResidencia'] = jc['CODMUNRES']
        d['codMunNaturalidade'] = jc['CODMUNNATU']
        d['dtNascimento'] = jc['DTNASC']
        d['dtFalecimento'] = jc['DTATESTADO']
        d['sexo'] = jc['SEXO']
        d['etnia'] = format_enum(etnia, jc['RACACOR'])
        d['estadoCivil'] = format_enum(estado_civil, jc['ESTCIV'])
        d['escolaridade'] = format_escolaridade(jc)

        # Diagnóstico
        d['linhaA'] = format_linha(jc['LINHAA'])
        d['linhaB'] = format_linha(jc['LINHAB'])
        d['linhaC'] = format_linha(jc['LINHAC'])
        d['linhaD'] = format_linha(jc['LINHAD'])
        d['linhaII'] = format_linha(jc['LINHAII'])

        # Investigação
        d['fonteInvestigacao'] = format_enum(
            fonte_investigacao, jc['FONTEINV'])
        d['tipoResgateInformacao'] = format_enum(
            tipo_resgate_informacao, jc['TPRESGINFO'])
        d['dtInicio'] = jc['DTINVESTIG']
        d['dtCadastro'] = jc['DTCADINV']
        d['dtConclusao'] = jc['DTCONINV']
        d['nivelInvestigador'] = format_enum(
            nivel_investigador, jc['TPNIVELINV'])

        # O conteúdo é serializado para JSON.
        content = json.dumps(d)

        # E por fim, o conteúdo é escrito novamente no arquivo,
        # fazendo a sobrescrita.
        outputStream.write(bytearray(content.encode('utf-8')))


flowFile = session.get()
if (flowFile != None):
    # Se houver flowFile, faz a escrita nela, utilizando a classe criada
    # anteriormente como CallBack dessa função.
    flowFile = session.write(flowFile, PyStreamCallback())

# O arquivo é transferido para a próxima etapa, com o status de sucesso.
session.transfer(flowFile, REL_SUCCESS)
