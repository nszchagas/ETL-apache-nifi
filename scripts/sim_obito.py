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
            opcao = cod

    return opcao


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


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        # Opções para os enums

        # CIRCOBITO = CIRCUNSTANCIA
        circunstancia = {1: 'ACIDENTE', 2: 'SUICIDIO',
                         3: 'HOMICIO', 4: 'OUTROS', 9: 'IGNORADO'}

        opcoes_parto = {1: 'ANTES', 2: 'DURANTE', 3: 'DEPOIS', 9: 'IGNORADO'}

        tipo_resgate_opcoes = {1: 'NAO_ACRESCENTOU',
                               2: 'SIM_NOVAS_INFORMACOES', 3: 'SIM_CORRECAO_CAUSAS'}
        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        jc = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.

        d = {}

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

        # Não nulos sem default: idObito, causaBasica, dataHora

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
