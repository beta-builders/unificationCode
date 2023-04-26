"""Query para trazer o RawData
"""

#Query do projeto Handlers certifie
QUERY1 = """
select
	u."document" as CPF,
	u."name" as NOME,
	a.zip_code as CEP,
	a.street as LOGRADOURO,
	a."number" as NUMERO_LOGRADOURO,
	a.complement as COMPLEMENTO_LOGRADOURO,
	a.neighborhood as BAIRRO,
	a.city as CIDADE,
	a.state as UF,
	phone."data" as TELEFONE,
	email."data" as EMAIL,
	u.birthday as DATA_NASCIMENTO
from
	quota q
inner join "user" u on
	u.uuid = q.user_uuid
	and u.deleted_at is null
inner join address a on
	a.uuid = q.address_uuid
	and a.deleted_at is null
inner join contact phone on
	phone.user_uuid = u.uuid
	and phone."type" = 'PHONE'
	and phone.deleted_at is null
inner join contact email on
	email.user_uuid = u.uuid
	and email."type" = 'EMAIL'
	and email.deleted_at is null
where
	q.deleted_at is null
	and q."group" = '{}'
	and q."number" = '{}';
"""

#Query do projeto PDF generator
QUERY2 = """
select
	u."name" as NOME,
	u."document" as CPF,
	concat(a.street, ', ', a.number) as ENDERECO,
	a.complement as COMPLEMENTO,
	a.neighborhood as BARRO,
	a.city as CIDADE,
	a.state as UF,
	a.zip_code as CEP,
	c2."data" as TELEFONE,
	c."data" as EMAIL,
	q."group" as GRUPO,
	q."number" as COTA,
	replace((qai.data -> 'totalValue')::text, '.', ',') as CARTA_CREDITO_OBJETO_PLANO_VIGENTE,
	to_char(to_date(replace((qai.data -> 'acquisitionDate')::text, '"', ''), 'YYYY-MM-DD'), 'dd/mm/yyyy') as DATA_DA_AQUISICAO,
	to_char(to_date(replace((qaiah.data -> 'deletionDate')::text, '"', ''), 'YYYY-MM-DD'), 'dd/mm/yyyy') as DATA_DA_EXCLUSAO,
	replace((qai.data -> 'percCommonFundPaid')::text, '.', ',') as PERCENTUAL_PAGO_PELO_CLIENTE,
	qai.data -> 'proposedNumber' as CONTRATO_ADESAO,
	case
		when q.product_type = 'BUILDING_PROPERTY' then 'IMÓVEL'
		when q.product_type = 'LIGHT_VEHICLE' then 'VEÍCULO LEVE'
		when q.product_type = 'HEAVY_VEHICLE' then 'VEÍCULO PESADO'
		when q.product_type = 'MOTORCYCLE' then 'MOTOCICLETA'
		else '.'
	end as BEM_OBJETO,
	replace((qai.data -> 'totalUpdatedValue')::text, '.', ',') as CREDITO_ATUAL,
	replace((qai.data -> 'updatedDebitBalanceValue')::text, '.', ',') as SALDO_DEVEDOR,
	replace(q.offered_value::text, '.', ',') as PRECO_DE_AQUISICAO,
	b."name" as BANCO,
	ubi.account_branch as AGENCIA,
	concat(left(ubi.account_number, -1), '-', right(ubi.account_number, 1)) as CONTA_CORRENTE,
	s.uuid as SALE_UUID
from
	sale s
inner join quota q on
	q.uuid = s.quota_uuid
inner join "user" u on
	u.uuid = q.user_uuid
inner join address a on
	a.uuid = q.address_uuid
inner join contact c on
	c.user_uuid = u.uuid
	and c.deleted_at is null
	and c."type" = 'EMAIL'
	and c.main = true
inner join contact c2 on
	c2.user_uuid = u.uuid
	and c2.deleted_at is null
	and c2."type" = 'PHONE'
	and c2.main = true
inner join quota_adm_itau qai on
	qai.reference_id = q.integration_code
inner join quota_adm_itau_audit_history qaiah on
	qaiah.reference_id = qai.reference_id
inner join user_bank_info ubi on
	ubi.user_uuid = u.uuid
	and ubi.deleted_at is null
inner join bank b on
	b.uuid = ubi.bank_uuid
	and ubi.deleted_at is null
where
	q."group" = '{}'
	and q."number" = '{}';
 """
 
 
 #Query concatena o nome e o arquivo.rem, do CNAB pelo Grupo e Cota  e retorna o path e o nome do arquivo
QUERY3 = """
select
	concat('{}-msc-cnab-files') as cnab_full_path,
	concat(cf."name", '.rem') as name
from
	cnab_file cf
inner join quota q on
	q.uuid = cf.quota_uuid
where
	q."group" = '{}'
	and q."number" = '{}';
"""