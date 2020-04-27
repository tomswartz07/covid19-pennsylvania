-- Update the covid database, updating unknown values from known
-- values. Equivalent to previous 'spreadsheet' method, but with fewer steps.
--
-- Data is loaded into db directly (eventually automatically via covid.py script)
-- and the remaining values are calculated via this script.

\pset footer off
\pset fieldsep ' '
\pset format unaligned

-- Update New Cases
with new_values as (
  select date,
  confirmed - lag(confirmed, 1) over (order by date) as new_cases
  from covid19.covid19pa
)
update covid19.covid19pa as tr
set new_cases = nv.new_cases
from new_values nv
where nv.date = tr.date
and tr.new_cases is Null
--returning tr.*
;

-- Update Growth Ratio
with new_values as (
  select date,
  confirmed::numeric / nullif(lag(confirmed, 1) over (order by date),0) as growth_ratio
  from covid19.covid19pa
)
update covid19.covid19pa as tr
set growth_ratio = nv.growth_ratio
from new_values nv
where nv.date = tr.date
and tr.growth_ratio is Null
--returning tr.*
;

-- Update Estimate
with new_values as (
  select date,
  lag(growth_ratio, 1) over (order by date) * lag(confirmed, 1) over (order by date) as estimated_day
  from covid19.covid19pa
)
update covid19.covid19pa as tr
set estimated_day = nv.estimated_day
from new_values nv
where nv.date = tr.date
and tr.estimated_day is Null
--returning tr.*
;

-- Update Off By
update covid19.covid19pa
set
off_by = estimated_day - confirmed
where off_by is Null
--returning *
;

-- Update pct_error
with new_values as (
  select date,
 -- (abs(estimated_day - confirmed)/confirmed) * 100 as pct_error
  (abs(estimated_day - confirmed)/COALESCE(NULLIF(confirmed,0), 1)) * 100 as pct_error
  from covid19.covid19pa
)
update covid19.covid19pa as tr
set pct_error = nv.pct_error
from new_values nv
where nv.date = tr.date
and tr.pct_error is Null
--returning tr.*
;

\o cases.data
select * from covid19.covid19pa order by date asc;
