CREATE UNLOGGED TABLE temp_us
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

DROP TABLE temp_us;

ANALYZE covid19.covid19us;

\set QUIET 1
\pset pager off
\pset footer off
\timing
\set QUIET 0
-- Show all results
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

-- Show top 10 counties
\set QUIET 1
\pset tuples_only
\set QUIET 0
WITH new AS (SELECT DISTINCT ON (county)
  county AS "County",
  date::timestamptz AS "Date",
  lag(cases, 1) over (partition BY county ORDER BY date::timestamptz) AS "Previous Cases",
  cases AS "Current Cases",
  cases - lag(cases, 1) over (partition BY county ORDER BY date::timestamptz) AS "New Cases"
FROM covid19.covid19us
WHERE
  state = 'Pennsylvania'
ORDER BY 1,2 desc)
SELECT
"County",
"New Cases"
FROM new
ORDER BY 2 DESC
LIMIT 5
;
