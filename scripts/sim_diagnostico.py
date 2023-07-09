from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json
import datetime
from datetime import datetime
from json import JSONEncoder


def format_linha(linha):
    if linha:
        return linha.replace('*', '')
    return None


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

        d = {}

        d['idObito'] = jc['contador']
        d['linhaA'] = format_linha(jc['LINHAA'])
        d['linhaB'] = format_linha(jc['LINHAB'])
        d['linhaC'] = format_linha(jc['LINHAC'])
        d['linhaD'] = format_linha(jc['LINHAD'])
        d['linhaII'] = format_linha(jc['LINHAII'])

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
