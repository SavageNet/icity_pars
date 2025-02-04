-- FUNCTION: source.clear(text)
DROP FUNCTION IF EXISTS source.clear(text);
CREATE OR REPLACE FUNCTION source.clear(
	p_str text)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    RETURN TRIM(
		REGEXP_REPLACE(p_str, '[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/ ]', '', 'g')
		);
END;
$BODY$;

ALTER FUNCTION source.clear(text)
    OWNER TO postgres;
