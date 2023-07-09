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


def format_timestamp(data, time="0000"):

    if not (time == "" or time == None or time == "null" or time == "None"):
        h = int(time[0:2])
        m = int(time[2:])
    else:
        h = '00'
        m = '00'
    # data = data + datetime.timedelta(hours=hours, minutes=minutes)
    return '{0} {1}:{2}:00'.format(data, str(h).zfill(2), str(m).zfill(2))


def format_date(date):
    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None

    d = date[0:2]
    m = date[2:4]
    y = date[4:]

    return '{0}-{1}-{2}'.format(y, m, d)


def format_enum(opcoes, cod):
    if cod == "":
        return 'IGNORADO'
    try:
        opcao = opcoes[int(cod)]
    except Exception:
        try:
            opcao = opcoes[cod]
        except Exception:
            opcao = cod

    return opcao


def format_linha(linha):
    if linha:
        return linha.replace('*', '')
    return None


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        jc = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.

        d = []
        id_obito = jc['CONTADOR']
        cids = jc['ATESTADO'].replace('/', ', ')
        for cid in cids:
            d.append({
                'idObito': id_obito,
                'codCid': cid
            })

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
