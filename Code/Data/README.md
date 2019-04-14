# Data

The anonymized ordinal preference data provided by the U.S. Navy Cryptologic Warfare, Medical Corps, and Explosive Ordinance Disposal communitieis can be found in the directories `cw`, `med`, and `eod` respectively.

In each of the directories there are subdirectories `raw` and `completed`. In `raw` the files are those privded directly from the source, almost always without complete preferences (the parties did not rank accross the entirity of selection universe). Thus we use the implied ordinal preference (IOP) method developed by one of our authors. The IOP project can be found at [this](https://github.com/ieshaw/Imp_Ord_Pref) repository.

In each of the subdirectories you will find the three csv files

- `S.csv`: Preference of seekers (columns) for jobs (rows)
- `O.csv`: Preference of job owners (Columns) for job seekers (rows)
- `A.csv`: Number of positions open at each job



