truncate table dicts.feature_to_emoji
;
insert into dicts.feature_to_emoji
with a as 
(
	select distinct
		model_feature,
		regexp_replace(
			regexp_replace(model_feature, '[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/\* ]', '', 'g'),
			'\s+',
			' '
		) as clear_model_feature,
		(regexp_matches(replace(model_feature, '🔥', ''), '[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/\* ]', 'g'))[1] as feature_emoji
	from source.icity_price
	order by 1
)
select 
	--model_feature,
	trim(clear_model_feature) as clear_model_feature,
	case feature_emoji
		when '🇹' then '🇹🇷'
		else feature_emoji
	end as feature_emoji
from a
where ascii(feature_emoji) <> 65039