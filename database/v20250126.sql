insert into source.v20250126(model_name, model_feature, price)
with bckp as 
(
	select 
		row_number() over (order by source.clear(bckp.model_name), source.clear(bckp.model_feature)) as id,
		bckp.model_name,
		bckp.model_feature,
		bckp.price
	from source.appler_price_bckp_20250125 bckp
),
ip as 
(
	select 
		row_number() over (order by source.clear(ip.model_name), source.clear(ip.model_feature)) as id,
		ip.model_name,
		ip.model_feature,
		ip.price
	from source.icity_price ip
)
select 
	ip.model_name as ip_model_name,
	ip.model_feature as ip_model_feature,
	coalesce(bckp.price, ip.price) as final_price
	-- bckp.id as bckp_id,
	-- ip.id as ip_id,
	-- bckp.price as bckp_price,
	-- ip.price as ip_price,
	-- coalesce(bckp.price, ip.price) - ip.price as delta,
	-- bckp.model_name as bckp_model_name,
	-- bckp.model_feature as bckp_model_feature,
	-- lower(source.clear(ip.model_name)) as clear_ip_model_name,
	-- lower(source.clear(ip.model_feature)) as clear_ip_model_feature
from ip 
left join bckp 
	on (1 = 1
	and lower(source.clear(bckp.model_name)) = lower(source.clear(ip.model_name))
	and lower(source.clear(bckp.model_feature)) = lower(source.clear(ip.model_feature))
	) 
	or case bckp.id
		when 3 then 15
		when 4 then 16
		when 5 then 18
		when 6 then 19
		when 530 then 508
		when 531 then 509
		when 532 then 510
		when 533 then 511
		when 534 then 512
		when 601 then 560
		when 177 then 574
		when 178 then 575
		when 179 then 576
		when 171 then 581
		when 172 then 582
		when 173 then 583
		when 174 then 584
	end = ip.id
where 1 = 1
	--and bckp.id is null
	--and coalesce(bckp.price, ip.price) is null
order by ip.id