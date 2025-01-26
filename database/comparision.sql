select 
	ap.model_name,
	ap.model_feature,
	ap.price,
	bckp.model_name,
	bckp.model_feature,
	bckp.price,
	ap.time_updated
from source.appler_price ap
full join source.appler_price_bckp_20250125 bckp 
	on 1 = 1
	and ap.model_name = bckp.model_name
	and ap.model_feature = bckp.model_feature
where 1 = 1
	and bckp.model_name is null or ap.model_name is null
order by ap.model_name, ap.model_feature
;
select * 
from source.appler_price
where lower(model_name) like '%pencil%'