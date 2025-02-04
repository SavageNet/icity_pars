truncate table stg.custom_delta; 
insert into stg.custom_delta(id, model_name, model_feature, appler_price, icity_price, custom_delta)
select 
	id,
	model_name,
	model_feature,
	appler_price,
	icity_price,
	delta
from stg.delta_price