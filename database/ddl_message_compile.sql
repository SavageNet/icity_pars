create or replace view dm.message_compile as 
select 
	model_name,
	string_agg(model_feature, ', ') as model_features,
	string_agg(price::text, ', ') as prices
from source.appler_price
group by 
	model_name
order by 
	lower(source.clear(model_name))
;