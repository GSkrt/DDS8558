/*use date trunc for public */ 

drop materialized view public.monthly_energy ; 
create materialized view if not exists public.monthly_energy as 
select month_date , max(value)- min(value) as w_month_kwh
from 
(
select
	date(date_trunc('month',t)) as month_date,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
month_date 


drop materialized view public.daily_energy ;

create materialized view if not exists public.daily_energy as 
select day , max(value)- min(value) as w_day_kwh
from 
(
select
	date(t) as day,
	--txtid,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
day



refresh materialized view public.monthly_energy 
select * from public.monthly_energy me 

select * from public.daily_energy de 



--limit 100

 /******************************************
  * 
  *  	Hourly energy time 
  * 
  *****************************************/

create materialized view if not exists public.hourly_energy as 
select datetime_hour , max(value)- min(value) as w_hour_kwh
from 
(
select
	date_trunc('hour',t) as datetime_hour,
	--txtid,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
datetime_hour



create materialized view if not exists public.hourly_energy as 
select datetime_hour , max(value)- min(value) as w_hour_kwh
from 
(
select
	date_trunc('hour',t) as datetime_hour,
	--txtid,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
datetime_hour

 
refresh materialized view public.monthly_energy ; 
refresh materialized view public.daily_energy ;
refresh materialized view public.hourly_energy ;
refresh materialized view public.fifteenm_energy ; 



select * from public.hourly_energy he 




create materialized view if not exists public.fifteenm_energy as 
select
	tabela.datetime_hour,
	max(tabela.value)-min(tabela.value) as W_15min 
from
	(
	select
		--t,
		date_trunc('hour', t) + date_part('minute', t)::int / 15 * interval '15 min' as datetime_hour,
		value
	from
		public.measurements_serial ms
	where
		txtid like '%energy_kWh%'
	 ) as tabela
group by
	tabela.datetime_hour

	

select
	datetime_hour as t,
	w_15min as w15
from
	public.fifteenm_energy fe
	
	
select
	datetime_hour as t,
	w_hour_kwh as w
from
	public.hourly_energy he 


