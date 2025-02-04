truncate table stg.delta_price;
insert into stg.delta_price(id, model_name, model_feature, icity_price, delta, time_updated)
select 
	appler_id,
	model_name,
	model_feature,
	icity_price,
	case 
		when coalesce(delta, 0) >= 0 and icity_price >= 11000
			then -1000
		when coalesce(delta, 0) >= 0
			then 0
		else coalesce(delta, 0)
	end as delta,
	time_updated
from source.dm_delta_price
