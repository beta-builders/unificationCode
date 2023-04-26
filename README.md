Unificação contrato de sessão + pdf generator
#Para que o código rode local são necessários realizar as seguintes configurações:

Incluir uma pasta nomeada como ".aws" e dentro dela salvar o arquivo "config" e "credentials" com suas configurações pessoais.
Dentro da pasta "dao" deverá conter um arquivo chamado "config.py" neste arquivo estarão todos as váriaveis utilizadas com seus respectivos valores, são elas: DBPASS, DBUSER, DBNAME = "msc", DBPORT, DBURL, STUSER, STPASS, AWSENV = "dev".
Criar na pasta raiz o arquivo ".gitignore", nele colocar todos os arquivos com senha, e os acrescentados nesse passo a passo.
Dentro da pasta "templates/yaml" deverá conter um arquivo chamado "config.yaml" ele será a base para gerar os outros arquivos yaml, segue a baixo modelo de uso:
""" contrato: nome_cedente: "" cpf_cedente: "" endereco_cedente: "M" comp_cedente: "" bairro_cedente: "" cidade_cedente: "" uf_cedente: "" cep_cedente: "" telefone_cedente: "" email_cedente: "" grupo: "" cota: "" carta_credito: "" data_aquisicao: "" data_exclusao: "" percentual_pago: "" contrato_adesao: "" bem_objeto: "" credito_atual: "" saldo_devedor: "" preco_aquisicao: "" preco_aquisicao_extenso: "" banco: "" agencia: "" conta_corrente: "" mes: "" ano: '' dia: ''

certificadora: baseUrl: cnpj: cpfUsuario: token:

"""

#Descrição das funcionalidades:

Na pasta ".devcontainer" é onde esta toda configuração para utilização do Docker, utilizamos ele para rodar local e para subir para a AWS.
Na pasta "API" é onde estão as funcionalidades que poderão ser chamadas e usadadas na "main.py". São elas:
caller_cadastro_cedentes: Realiza o cadastro do cedente. caller_cadastro_coleta_digital: Cadastro da Coleta Digital de Recebíveis. caller_cadastro_coleta_hibrida: Cadastro da Coleta hibrida de Recebíveis. caller_consulta_docs: Consulta os tipos de documentos. caller_consulta_props: Consulta os propósitos de assinatura. caller_consulta_status_coleta: Consulta o status da coleta.
Na pasta "dao" quando testar local será gerado automaticamente a pasta "pycache" incluir esse arquivo no ".gitignore". Deverá estar nessa pasta o arquivo "config.py" passado no passo a cima. O arquivo "queries.py" contem todas as queries usadas para geração do contrato de sessão, cnab e dowload do s3. O arquivo "querie_data.py" le as queries acima e geram um arquivo.csv na pasta data. O arquivo "update_data.py" le o csv dentro da pasta data e gera um arquivo.yaml, também na pasta data. O arquivo "update_s3.py" ele irá gerar o arquivo "arq_cnab.cvs" com o caminho e o nome do arquivo do cnab, dentro da pasta data.
Na pasta "data" estarão os documentos gerados acima.
Na pasta "templates" teremos algumas subpastas: "json": Nela estarão os arquivos usados na "main.py" para conversão do .json "pdf": Nela estará o modelo de template em branco do contrato de sessão, e após rodar a "main.py" será dentro dela que estará o contrato preenchido. Lembrar de colocar no "git.ignore" esse arquivo. "yaml": Nessa pastá estará o corpo base do "config.yaml" criado em passo lá em cima.
O documento "Dockerfile": conterá mais atualizações e configurações para uso do Docker.
O documento "fill_forms_pdfwr.ipynb": É o arquivo que foi usado inicialmente para geração do pdf.
Na "main.py" é onde está concentrada todas as chamadas. Vale ressaltra que não são todos grupos e quotas que geram arquivo de Cnab, o mesmo ele não é gerado em produção!
O arquivo "msc-pdf-generator.code-workspace:
No arquivo "requiremenrs.txt": Estara todas bibliotecas que precisam ser instaladas para rodar local o código.
