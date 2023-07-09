from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json

# Essa classe herda a classe StreamCallback, do apache/nifi.


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

        # Um objeto cid é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.

        cid = {}

        # Valida os tamanhos das strings.
        if len(jc['CAT']) <= 10 and len(jc['DESCRICAO']) <= 100:
            cid['codigo'] = jc['CAT']
            cid['descricao'] = jc['DESCRICAO']

        # O conteúdo é serializado para JSON.
        content = json.dumps(cid)

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
