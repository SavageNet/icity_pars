--insert into dicts.feature_to_emoji
-- values
-- (
-- 	('Black', '🖤'),
-- 	('White', '🤍'),
-- 	('Desert', '🤎'),
-- 	('Natural', '🩶'),
-- 	('Ultramarine', '💙'),
-- 	('Teal', '💚'),
-- 	('Pink', '🩷'),
-- 	('Blue', '💙'),
-- 	('Green', '💚'),
-- 	('Yellow', '💛'),
-- 	('Purple', '💜'),
-- 	('Silver', '🤍'),
-- 	('Gold', '💛'),
-- 	('Purple', '💜'),
-- 	('Purple', '💜'),
-- 	('Purple', '💜'),
-- 	('Purple', '💜'),
-- 	('Purple', '💜')
-- ) 

with feture_to_emoji as 
(
	select column1 as emoji
	from 
	(
		values
		('Black', '🖤'),
		('White', '🤍'),
		('Desert', '🤎'),
		('Natural', '🩶'),
		('Ultramarine', '💙'),
		('Teal', '💚'),
		('Pink', '🩷'),
		('Blue', '💙'),
		('Green', '💚'),
		('Yellow', '💛'),
		('Purple', '💜'),
		('Silver', '🤍'),
		('Gold', '💛'),
		('Midnight', '🖤'),
		('Starlight', '🤍'),
		('Red', '❤️'),
		('Space gray', '🩶'),
		('Jet Black', '🖤'),
		('Rose Gold', '🩷💛'),
		('Indigo', '💜'),
		('Olive', '💚'),
		('Orange', '🧡'),
		('Gray', '🩶'),
		('Tan', '🤎'),
		('Navy', '💙'),
		('Blue Black', '💙🖤'),
		('Оранжевый', '🧡'),
		('Жёлтый', '💛'),
		('Розовый', '🩷'),
		('Bronze', '🤎'),
		('Ceramic Patina Topaz', '🧡'),
		('Nickel', '🩶'),
		('Fuchsia', '🩷'),
		('Ретро (Ceramic Pop)', '🧡🩵'),
		('Diffuse медь / никель (Copper / Nickel)', '🧡🩶'),
		('Диффузный клубничный бронзовый (Diffuse Strawberry Bronze)', '🩷'),
		('Красный (Topaz)', '❤️'),
		('Керамическая платина/топаз (Ceramic/Topaz)', '🩵'),
		('Медь (Cooper)', '🧡'),
		('Adapter', '🔌'),
		('Apple Vision', '🥽'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Pencil', '✏️'),
		('Nickel', '🩶')
		) t
)
select *
from source.appler_price
left join feture_to_emoji fte
	on 1 = 1
	and lower(trim(model_feature)) like '%' || lower(trim(fte.emoji)) || '%'
where 1 = 1
	and fte.emoji is null
	