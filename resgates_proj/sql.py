SQL_RESGATES = """
DECLARE @data_ref AS date = '{{data_ref}}';

with cte_resgates as (

	SELECT 
		try_cast(mov.DT_LIQUIDACAO_FINANCEIRA as date)  as DT
		,dbops.isin_cota
		,dbops.nome_fundo
		,try_cast(mov.[VL_CORRIGIDO] as float(100)) as VL_CORRIGIDO
		,mov.CD_TIPO
	FROM [AUG_UPLOAD].[jcot].[movimentacoes] as mov
	left join [Operacoes].dbo.fundosaugme as dbops
		on dbops.codigo_no_adm=mov.CD_FUNDO
	where mov.[CD_TIPO]<>'A' and mov.DT_LIQUIDACAO_FINANCEIRA>@data_ref and mov.DT_LIQUIDACAO_FINANCEIRA is not null

)



, cte_resgates_D as (

select 
	cte_resgates.nome_fundo
	,cte_resgates.isin_cota
	,(select sum(D1.VL_CORRIGIDO) from cte_resgates as D1 where D1.dt<=dateadd(day,1,@data_ref) and D1.nome_fundo=cte_resgates.nome_fundo	group by D1.nome_fundo)  as Ate_d1
	,(select sum(d7.VL_CORRIGIDO) from cte_resgates as d7 where d7.dt<=dateadd(day,7,@data_ref) and d7.nome_fundo=cte_resgates.nome_fundo	group by d7.nome_fundo)  as Ate_d7
	,(select sum(d30.VL_CORRIGIDO) from cte_resgates as d30 where d30.dt<=dateadd(day,30,@data_ref) and d30.nome_fundo=cte_resgates.nome_fundo	group by d30.nome_fundo)  as Ate_d30
	,(select sum(d60.VL_CORRIGIDO) from cte_resgates as d60 where d60.dt<=dateadd(day,60,@data_ref) and d60.nome_fundo=cte_resgates.nome_fundo	group by d60.nome_fundo)  as Ate_d60
	,(select sum(d90.VL_CORRIGIDO) from cte_resgates as d90 where d90.dt<=dateadd(day,90,@data_ref) and d90.nome_fundo=cte_resgates.nome_fundo	group by d90.nome_fundo)  as Ate_d90
	,(select sum(d120.VL_CORRIGIDO) from cte_resgates as d120 where d120.dt<=dateadd(day,120,@data_ref) and d120.nome_fundo=cte_resgates.nome_fundo	group by d120.nome_fundo)  as Ate_d120
	,(select sum(d150.VL_CORRIGIDO) from cte_resgates as d150 where d150.dt<=dateadd(day,150,@data_ref) and d150.nome_fundo=cte_resgates.nome_fundo	group by d150.nome_fundo)  as Ate_d150
	,(select sum(d180.VL_CORRIGIDO) from cte_resgates as d180 where d180.dt<=dateadd(day,180,@data_ref) and d180.nome_fundo=cte_resgates.nome_fundo	group by d180.nome_fundo)  as Ate_d180
	

from cte_resgates

group by cte_resgates.nome_fundo,cte_resgates.isin_cota

)

select cte_resgates_D.nome_fundo
	,try_cast(cte_resgates_D.Ate_d1/PL.patliq as decimal(10,6)) as AteD1
	,try_cast(cte_resgates_D.Ate_d7/PL.patliq as decimal(10,6)) as AteD7
	,try_cast(cte_resgates_D.Ate_d30/PL.patliq as decimal(10,6)) as AteD30
	,try_cast(cte_resgates_D.Ate_d60/PL.patliq as decimal(10,6)) as AteD60
	,try_cast(cte_resgates_D.Ate_d90/PL.patliq as decimal(10,6)) as AteD90
	,try_cast(cte_resgates_D.Ate_d120/PL.patliq as decimal(10,6)) as AteD120
	,try_cast(cte_resgates_D.Ate_d150/PL.patliq as decimal(10,6)) as AteD150
	,try_cast(cte_resgates_D.Ate_d180/PL.patliq as decimal(10,6)) as AteD180


from cte_resgates_D
left join carteiras.dbo.header as PL
	on PL.isin=cte_resgates_D.isin_cota and PL.DataPosicao=@data_ref
	--select *from [Operacoes].[ops].[fundos_augme] 
"""


