from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json

# Essa classe herda a classe StreamCallback, do apache/nifi.

# Função para converter o código armazenado no sistema para
# um ENUM correspondente.


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def formatorigem(self, cod):

        origens = {
            1: 'ORACLE',
            2: 'BANCO ESTADUAL',
            3: 'BANCO SEADE',
            9: 'IGNORADO'
        }

        if cod == "":
            return 'IGNORADO'
        try:
            origem = origens[int(cod)]
        except Exception as e:
            origem = cod
            print(e)

        return origem

    def process(self, inputStream, outputStream):
        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        json_content = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.
        metadados = {}
        metadados['idObito'] = json_content['CONTADOR']
        metadados['origemDados'] = self.formatorigem(json_content['ORIGEM'])
        metadados['formCodificado'] = (json_content['CODIFICADO'] == 'S')
        metadados['versaoSistema'] = json_content['VERSAOSIST']
        # O conteúdo é serializado para JSON.
        content = json.dumps(metadados)

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
