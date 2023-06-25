# Apache Nifi

## Construindo e Rodando

Para construir a imagem personalizada do apache nifi, com driver para conexão jdbc com o MySQL e usuário:

```shell
docker compose up -d
```

## Construindo o Fluxo

Os dados utilizados no exemplo vêm de duas fontes:

- [Arquivo de dados sobre os CIDs](./data/CID-10-GRUPOS.CSV) [1], disponível na pasta [data](./data/)
- [Dados sobre a mortalidade, em 2020](https://diaad.s3.sa-east-1.amazonaws.com/sim/Mortalidade_Geral_2020.csv) [2]

### Fluxo para os dados de CID

#### Extract

Para o arquivo, utilizamos o processador **GetFile** do Apache Nifi, com a seguinte configuração:

![](assets/cid10-getfile.png)

- O Input Directory contém o caminho relativo a pasta `/opt/nifi/nifi-current/data-in` do container, observe que a
  pasta `data-in`  está em um _bind_ com a pasta local: [data](./data), por meio da configuração
  no [docker-compose](docker-compose.yaml):

```yaml
volumes:
  - "./data:/opt/nifi/nifi-current/data-in" 
```

> O filtro por nome foi inserido para que o processador não recupere outros arquivos da pasta. Durante o período de testes recomenda-se utilizar a propriedade "Keep Source File" como `true`, para que o arquivo original não seja deletado após o processamento.

O processador GetFile tem uma saída possível, presente na aba "Relationships", e ficará no estado inválido até que as
saídas sejam tratadas.

![](assets/cid10-getfile-proc.png)

Como a saída desse processador será o arquivo `CSV` lido, o próximo processador será responsável por fazer a leitura
desse arquivo CSV e separá-lo em arquivos contendo apenas um registro, já no formato `JSON`. Para isso, o processador *
*SplitRecord** será utilizado, para ligar os dois processadores basta passar o mouse por cima do primeiro e quando a
seta representada na figura abaixo aparecer, arrastar o mouse até o segundo processador.

![](assets/cid10-ligacao-split.png)

A seguir, será solicitada a configuração da conexão, onde a saída em caso de `sucess` do primeiro processador
(**GetFile**) será direcionada para o processador **SplitRecord**.

![](assets/cid10-lig-config.png)

Nesse momento será criada uma fila (_queue_) entre os processadores, onde será possível acompanhar o estado do fluxo de
dados.

![](assets/cid10-getfile-queue.png)

> Observe que o processador **GetFile** agora está no estado válido, mas ainda não foi iniciado, e o processador *
*SplitRecord** está no estado inválido.

Para verificar o funcionamento do processador GetFile ele será executado apenas uma vez, para isso clique com o botão
direito do mouse sobre o processador e selecione a opção **Run Once**:

![](assets/getfile-runonce.png)

Após a execução, o arquivo lido (1 arquivo de 26.42 KB) entrará para a fila, aguardando a entrada no próximo
processador:

![](assets/getfile-queued.png)

É possível verificar os arquivos na fila selecionando a opção **List Queue** da fila:

![](assets/listqueue.png)

![](assets/listqueue-2.png)

#### Transform

O processador **SplitRecord** contém a primeira etapa da transformação dos dados, a transformação de `CSV` para `JSON`,
para isso ele utilizará dois serviços, um de leitura CSV e outro de escrita JSON. Esses serviços devem ser configurados
de forma global para o fluxo, para isso clique em um espaço vazio do fluxo e selecione a opção **Configure**.

![](./assets/5036.png)

Na aba **controller services** selecione a opção para adicionar um novo serviço, e busque por **CSVReader**.

![](./assets/5230.png)

Clique no ícone de engrenagem para configurar o leitor e nas propriedades altere as seguintes configurações:

| Configuração               | Valor                          | Descrição                                                    |
| -------------------------- | ------------------------------ | ------------------------------------------------------------ |
| Schema Access Strategy     | Use Strings Fields From Header | Determina como os nomes das propriedades serão determinados. |
| Value Separator            | ;                              | Separador de registros, no caso do arquivo usado é ';'.      |
| Treat First Line as Header | true                           | Auto explicativo.                                            |

Para ativar o serviço, clique no ícone de raio e no botão "Enable" da tela que aparecer.

Repita os passos anteriores para adicionar os serviços de leitura e escrita em JSON: **JsonRecordSetWriter** e **JsonTreeReader**. Não é necessário alterar nenhuma configuração, mas caso deseje uma saída mais bonita, habilite a configuração "Pretty Print JSON" no JsonRecordSetWriter.

Agora que os serviços de leitura e escrita estão criados e habilitados, é possível inseri-los na configuração do **SplitRecord**.

![](./assets/0001.png)

O processador SplitRecord tem 3 saídas possíveis, e é necessário direcioná-las ou configurá-las como finais, na aba relationships.

![](./assets/0100.png)

A saída splits será direcionada para o próximo processador.

Como esse processador realizará um grande número de tarefas, é possível criar threads para realizar o trabalho de forma concorrente. No exemplo serão utilizadas 5 threads.

![](./assets/0336.png)

## Referências

[1] Arquivos em Formato CSV - CID-10, disponível em <http://www2.datasus.gov.br/cid10/V2008/descrcsv.htm>. Acesso em 12
de junho de 2023.

[2] Sistema de Informação sobre Mortalidade – SIM, disponível em  <https://opendatasus.saude.gov.br/dataset/sim>. Acesso
em 12 de junho de 2023.

[3] Exemplo de Script Jython, disponível em <https://gist.github.com/ijokarumawak/1df6d34cd1b2861eb6b7432ee7245ccd>

[4] <https://www.youtube.com/watch?v=cHElJ8M5g0Y&ab_channel=InsightByte>
