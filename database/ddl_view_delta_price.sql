create or replace view dm.delta_price as 
select 
	ap.model_name,
	ap.model_feature,
	ap.price as appler_price,
	ip.price as icity_price,
	ap.price - ip.price as delta
from source.appler_price ap
inner join source.icity_price ip
	on 1 = 1
	and lower(source.clear(ap.model_name)) = lower(source.clear(ip.model_name))
	and lower(source.clear(ap.model_feature)) = lower(source.clear(ip.model_feature))