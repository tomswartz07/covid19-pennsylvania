CREATE TEMP TABLE temp_us
(LIKE covid19.covid19us INCLUDING ALL);

\COPY temp_us from '~/git/nytimes-covid19-data/us-counties.csv' delimiter ',' header csv;

INSERT INTO covid19.covid19us (date, county, state, fips, cases, deaths)
SELECT t2.* FROM temp_us t2
LEFT JOIN covid19.covid19us t1 ON
t1.date = t2.date
WHERE
t1.date is NULL
ON CONFLICT (date, fips) DO
UPDATE SET
cases = excluded.cases,
deaths = excluded.deaths
RETURNING *;

ANALYZE covid19.covid19us;

\pset pager off
SELECT DISTINCT on (county)
  county AS "County",
  date::timestamptz AS "Date",
  lag(cases, 1) over (partition BY county ORDER BY date::timestamptz) AS "Previous Cases",
  cases AS "Current Cases",
  cases - lag(cases, 1) over (partition BY county ORDER BY date::timestamptz) AS "New Cases"
FROM covid19.covid19us
WHERE
  state = 'Pennsylvania'
ORDER BY 1,2 desc
;
