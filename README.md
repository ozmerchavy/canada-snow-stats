# canada-snow-stats
Code that fetches weather stats from Canada's goverment website
This script allows you to enter a year, station and province to analyze precipitation data. The optional parameter "verbose" can be set to either "True", "False", or "little" to control the level of detail in the results.


#### Inputs:
Year start/end: The year for which you want to analyze precipitation data
Station: The ID of the weather station from which you want to retrieve data
Province code: The province where the weather station is located
Verbose (optional): Determines the level of detail in the results. Can be set to "True", "False", or "little".
#### Outputs:
Snowy days: The number of days that had snow on the ground during the specified year
Full data: A Boolean value indicating whether the existing data for the specified year is complete
Note:
In case days are missing in the data, 0 precipitation is assumed and the year would have a "full data" False.

