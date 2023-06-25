## Apache Nifi

### Docker Compose

```yaml title="docker-compose.yaml" linenums="1"
--8<--
docker-compose.yaml
--8<--
```

### Dockerfile

```Dockerfile title="Dockerfile" linenums="1"
--8<--
Dockerfile
--8<--
```

### Rodando

Para rodar a imagem personalizada do apache nifi, com driver para conexão jdbc com o MySQL e usuário:

```shell
docker compose up -d
```

## Banco de Dados

### Docker Compose

```yaml title="docker-compose.yaml" linenums="1"
version: "3.3"
services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    restart: always
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ALLOW_EMPTY_PASSWORD=1
    volumes:
      - mysql:/var/lib/mysql
    networks:
      - mysql

volumes:
  mysql:
    external: true

networks:
  mysql:
    external: true
```

### Scripts Iniciais

```sql title="fisico.sql" linenums="1"
--8<--
fisico.sql
--8<--
```

```sql title="controle.sql" linenums="1"
--8<--
controle.sql
--8<--
```

Para limpar a base após os testes, basta executar o script:

```sql title="apaga.sql" linenums="1"
--8<--
apaga.sql
--8<--
```
