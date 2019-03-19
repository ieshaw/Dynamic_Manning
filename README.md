# Dynamic_Manning
The Repository for the Dynamic Manning efforts of the Naval Algorithm team.

We proposed prototypes of our algorithm ideas in our article ["Good Will Hunting: The Strategic Threat of Poor Talent Management"](https://warontherocks.com/2018/12/good-will-hunting-the-strategic-threat-of-poor-talent-management/). 

Our effort is to develop a detailing marketplace to improve upon the Department of Defense's process of placing servicemembers in jobs around the world. The DoD embodies a unique situation where it is a bureaucracy with a 'captive' job market; entrance is almost exclusively bottom up, many members are obligated to stay due to multi-year contracts, and job movement is compulsory if ordered to do so. The bureaucracy around this process has proven slow and non-optimal at accomplishing this piece of the national mission, this is our attempt to help make incrememtal improvements enabled by technology.  Our ultimate goal is to leverage algorithms as the building blocks of machine learning application in a future state. 

In essence, we take the job preferences of seekers (sailors) and match them to the preferences of job owners (commanders) in a minimization function such that the system will not find a more optimal placement.  That objective function is tempered by constraints of DoD policy and commander's intents, which are coded into the MIP algorithm and satisfied first. 

Initially, we created a Gale-Shapley deferred acceptance algorithm, resembling those authors' work on matching markets.  Due to a need for constraints and modularity with consistent manipulations, we transitioned to linear programming, specifically a more agile mixed integer approach.  

The efforts here were executed completely open source and do not express the product or views of the US Government writ large, Department of Defense, or the Department of the Navy.
