# Data

The anonymized ordinal preference data provided by the U.S. Navy Cryptologic Warfare, Medical Corps, and Explosive Ordinance Disposal communitieis can be found in the directories `cw`, `med`, and `eod` respectively.

In each of the directories there are subdirectories `raw` and `completed`. In `raw` the files are those privded directly from the source, almost always without complete preferences (the parties did not rank accross the entirity of selection universe). Thus we use the implied ordinal preference (IOP) method developed by one of our authors. The IOP project can be found at [this](https://github.com/ieshaw/Imp_Ord_Pref) repository.

In each of the subdirectories you will find the three csv files

- `S.csv`: Preference of seekers (columns) for jobs (rows)
- `O.csv`: Preference of job owners (Columns) for job seekers (rows)
- `A.csv`: Number of positions open at each job

And you will find a sub-subdirectory called `results/` with the following files

- `post_match.csv`: a csv with some calculated post-match metrics
- `X_da.csv`: a csv of the X matrix of matching using deferred acceptance (seeker optimal) with 1 indicating a match, 0 if not.
- `X_mip.csv`: a csv of the X matrix of matching using MIP (specifically the BIP prototype explained in our paper) with 1 indicating a match, 0 if not.

## A note on the post match metrics

More than average preference sum (called `mu_combined`) in the csv, we also have `##_y_count` indicating the number of preferences matched on the `y` side of the market (`s` for job seeker, and `o` for job owner) that are less that `##`. For example `5_s_count` is the number of job seekers assigned thir first, second, third, fourth, or fifth preference. 



