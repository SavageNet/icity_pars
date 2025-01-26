truncate table dicts.model_to_emoji
;
insert into dicts.model_to_emoji
with a as 
(
	select distinct
		model_name,
		regexp_replace(
			regexp_replace(model_name, '[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/\* ]', '', 'g'),
			'\s+',
			' '
		) as clear_model_name,
		(regexp_matches(replace(model_name, '🔥', ''), '[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/\* ]'))[1] as model_emoji
	from source.icity_price
)
select 
	--model_name,
	trim(clear_model_name) as clear_model_name,
	case model_emoji
		when '🇹' then '🇹🇷'
		else model_emoji
	end as model_emoji
from a

