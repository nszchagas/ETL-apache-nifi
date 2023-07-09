from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json
import datetime
from datetime import datetime
from json import JSONEncoder


# Função para converter o código armazenado no sistema para
# um ENUM correspondente.
def format_enum(opcoes, cod):
    if cod == "":
        return 'IGNORADO'
    try:
        opcao = opcoes[int(cod)]
    except Exception as e:
        opcao = cod
    return opcao

# Formata datas para o formato aceito no mysql.


def format_date(date):
    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None

    d = date[0:2]
    m = date[2:4]
    y = date[4:]

    return '{0}-{1}-{2}'.format(y, m, d)


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

# É valido se ao menos uma das chaves não for nula.


def is_objeto_valido(objeto, chaves):
    for c in chaves:
        if (object[c] is not None):
            return True
    return False


# Essa classe herda a classe StreamCallback, do apache/nifi.


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        # Opções para os enums

        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        jc = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.

        # ENUMS
        fonte_investigacao = {
            1: 'CMMI',
            2: 'ENTREVISTA_FAMILIA',
            3: 'PRONTUARIO',
            4: 'BANCOS_DE_DADOS',
            5: 'SVO',
            6: 'IML',
            7: 'OUTRA',
            8: 'MULTIPLAS_FONTES',
            9: 'IGNORADO'
        }

        tipo_resgate_informacao = {
            1: 'NAO_ACRESCENTOU',
            2: 'SIM_NOVAS_INFOS',
            3: 'SIM_CORRECAO'
        }

        nivel_investigador = {
            'E': 'ESTADUAL',
            'R': 'REGIONAL',
            'M': 'MUNICIPAL'
        }

        # Dados formatados
        d = {}

        d['idObito'] = jc['CONTADOR']
        d['fonteInvestigacao'] = format_enum(
            fonte_investigacao, jc['FONTEINV'])
        d['tipoResgateInformacao'] = format_enum(
            tipo_resgate_informacao, jc['TPRESGINFO'])
        d['dtInicio'] = format_date(jc['DTINVESTIG'])
        d['dtCadastro'] = format_date(jc['DTCADINV'])
        d['dtConclusao'] = format_date(jc['DTCONINV'])
        d['nivelInvestigador'] = format_enum(
            nivel_investigador, jc['TPNIVELINV'])

        # Verifica se algum dos campos não é nulo.
        chaves = ['idInvestigacao', 'fonteInvestigacao', 'tipoResgateInformacao',
                  'dtInicio', 'dtcadastro', 'dtConclusao', 'nivelInvestigador']

        is_objeto_valido(d, chaves)

        # O conteúdo é serializado para JSON.
        content = json.dumps(d, cls=DateTimeEncoder)

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
