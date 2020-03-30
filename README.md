# Pennsylvania Coronavirus COVID-19 Scraper

In an effort to reduce the amount of strain on the Pennsylvania
Department of Health websites during the peak hours (especially around noon
when the daily updated information is posted), this script was created to quickly
and easily parse the information without any additional overhead.

The script can optionally highlight certain counties which you may be interested
in- in my case, I'm interested in Lancaster and Schuylkill counties.
If you wish to highlight different counties, simply update the array in the script.

## Current Cases

Below is a graph of confirmed cases generated using the most recent available data
and `gnuplot`.

![Graph](cases.png)

![Trajectory](trajectory.png)

For more information on how to read the trajectory graph,
please see this excellent video by [MinutePhysics](https://www.youtube.com/watch?v=54XLXg4fYsc)

## Using

To use this script, simply run it:
```
python covid.py
```

It's recommended that a virtualenv is used, for sanity reasons:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python covid.py
```


**NOTE:** Please be mindful that this script will still (in a minor way)
affect the bandwidth of the host. Please do not use this script to poll the
site more often than once every hour or so. The data does not change that often.

The scripts and data used to generate this graph are also included in the repository.
Simply install `gnuplot` and run:

```
gnuplot plot_PA_Cases.gpi
```

The image file will be updated at `cases.png`

## Sample Output
```
* Map, table and case count last updated at 12:00 p.m. on 3/26/2020
1,687 cases confirmed statewide
16 deaths confirmed statewide
48 of 67 counties affected
Adams county: 7 cases, 0 deaths
Allegheny county: 133 cases, 2 deaths
Armstrong county: 1 cases, 0 deaths
Beaver county: 13 cases, 0 deaths
Berks county: 36 cases, 0 deaths
Blair county: 1 cases, 0 deaths
Bradford county: 2 cases, 0 deaths
Bucks county: 107 cases, 0 deaths
Butler county: 19 cases, 1 deaths
Cambria county: 1 cases, 0 deaths
Carbon county: 2 cases, 0 deaths
Centre county: 9 cases, 0 deaths
Chester county: 84 cases, 0 deaths
Clearfield county: 2 cases, 0 deaths
Columbia county: 3 cases, 0 deaths
Crawford county: 1 cases, 0 deaths
Cumberland county: 15 cases, 0 deaths
Dauphin county: 13 cases, 0 deaths
Delaware county: 156 cases, 1 deaths
Erie county: 4 cases, 0 deaths
Fayette county: 8 cases, 0 deaths
Franklin county: 5 cases, 0 deaths
Greene county: 3 cases, 0 deaths
Indiana county: 1 cases, 0 deaths
Juniata county: 1 cases, 0 deaths
Lackawanna county: 28 cases, 2 deaths
Warning: 21 active cases in Lancaster county.
Lancaster county: 21 cases, 0 deaths
Lawrence county: 1 cases, 0 deaths
Lebanon county: 4 cases, 0 deaths
Lehigh county: 63 cases, 1 deaths
Luzerne county: 36 cases, 1 deaths
Lycoming county: 1 cases, 0 deaths
Mercer county: 3 cases, 0 deaths
Monroe county: 67 cases, 2 deaths
Montgomery county: 282 cases, 2 deaths
Montour county: 4 cases, 0 deaths
Northampton county: 56 cases, 3 deaths
Philadelphia county: 402 cases, 1 deaths
Pike county: 15 cases, 0 deaths
Potter county: 1 cases, 0 deaths
Warning: 9 active cases in Schuylkill county.
Schuylkill county: 9 cases, 0 deaths
Somerset county: 2 cases, 0 deaths
Susquehanna county: 1 cases, 0 deaths
Warren county: 1 cases, 0 deaths
Washington county: 12 cases, 0 deaths
Wayne county: 6 cases, 0 deaths
Westmoreland county: 24 cases, 0 deaths
York county: 21 cases, 0 deaths
```
