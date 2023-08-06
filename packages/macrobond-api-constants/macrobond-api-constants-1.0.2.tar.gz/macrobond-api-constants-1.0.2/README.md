# Macrobond constants

A helper package to conveniently include the constants used by the Macrobond API.

# Installation
`pip install macrobond-api-constants`

# Usage
The namespace is `macrobond_api_constants`.

```python
from macrobond_api_constants import SeriesFrequency as f
f.DAILY
```

# Classes
The constants are grouped into classes according to their usage.

#### CalendarDateMode
Specifies which dates are included in a calendar.

Value | Description
-|-
ALL_SERIES | Use the first or last time period where there is valid data in any series.
ANY_SERIES | Use the first or last time period where there is valid data in all series.

#### CalendarMergeMode
Specifies how different calendars are merged into one.
Value | Description
-|-
AVAILABLE_IN_ALL |Use the time periods that are available in all series.
AVAILABLE_IN_ANY |Use the time periods that are available in any series.
FULL_CALENDAR    |Use all the time periods as specified by the frequency and weekdays.

#### MetadataValueType
Specifies the different types of values in the meta data.

Value | Description
-|-
BOOL | Boolean type
DATE | Date type 
DOUBLE | Double type 
INT | Int type 
STRING | String type 

#### SeriesFrequency
Specifies the different frequencies for the calendar.

Value | Description
-|-
ANNUAL       | Once a year
SEMI_ANNUAL  | Twice a year
QUAD_MONTHLY | Once in 4 months
QUARTERLY    | Once in 3 months
BI_MONTHLY   | Every second month
MONTHLY      | Once a month
WEEKLY       | Once a week
DAILY        | Once a day
LOWEST       | When specified in a series request, this corresponds to the lowest frequency of the series in set
HIGHEST      | When specified in a series request, this corresponds to the highest frequency of the series in the request

#### SeriesMissingValueMethod
Specifies the different types of missing value handling.

Value | Description
-|-
NONE                 | Do not fill in missing values. They will remain NaN in the value vector.
AUTO                 | Determine the method based on the series classification.
PREVIOUS             | Use the previous non-missing value.
ZERO                 | Use the value zero.
LINEAR_INTERPOLATION | Do a linear interpolation between the previous and next non-missing values.

#### SeriesPartialPeriodsMethod
Specifies the different types of partial period handling.

Value | Description
-|-
NONE                | Only include full periods of the lower frequency
AUTO                | Automatically select method based on series properties
REPEAT_LAST         | Use the last (or first) value to extend incomplete periods
FLOW_CURRENT_SUM    | Use the last (or first) partial average to extend incomplete periods
PAST_RATE_OF_CHANGE | Use the previous (or next) year's rate of change to extend incomplete periods
ZERO                | Extend incomplete periods with zeroes

#### SeriesToHigherFrequencyMethod
Specifies the different types of frequency conversion methods when converting to a higher frequency.

Value | Description
-|-
AUTO                    | Determine the method based on the series classification
SAME                    | Use the same value for the whole period
DISTRIBUTE              | Use the first value of the time period
PERCENTAGE_CHANGE       | Distribute the percentage change over the period
LINEAR_INTERPOLATION    | Use a linear interpolation of the values from this to the next period
PULSE                   | Use the value for the first value of the period
QUADRATIC_DISTRIBUTION  | Use quadratic interpolation to distribute the value over the period
CUBIC_INTERPOLATION     | Use a cubic interpolation of the values from this to the next period

#### SeriesToLowerFrequencyMethod
Specifies the different types of frequency conversion methods when converting to a lower frequency.

Value | Description
-|-
AUTO                            | Determine the method based on the series classification
LAST                            | Use the time periods that are available in all series.
FIRST                           | Use the first value of the time period
FLOW                            | Aggregate the values of the time period
PERCENTAGE_CHANGE               | Aggregate the percentage change over the period
HIGHEST                         | Use the highest value in the time period
LOWEST                          | Use the lowest value of the time period
AVERAGE                         | Use the average value of the period
CONDITIONAL_PERCENTAGE_CHANGE   | TODO

#### SeriesWeekdays
Specifies the different types of week days.

Value | Description
-|-
SUNDAY                          |Sunday
MONDAY                          |Monday
TUESDAY                         |Tuesday
WEDNESDAY                       |Wednesday
THURSDAY                        |Thursday
FRIDAY                          |Friday
SATURDAY                        |Saturday
FULLWEEK                        |Sun+Mon+Tue+Wed+Thu+Fri+Sat
MONDAY_TO_FRIDAY                |Mon+Tue+Wed+Thu+Fri
SATURDAY_TO_THURSDAY            |Sun+Mon+Tue+Wed+Thu+Sat
SATURDAY_TO_WEDNESDAY           |Sun+Mon+Tue+Wed+Sat
SUNDAY_TO_THURSDAY              |Sun+Mon+Tue+Wed+Thu
MONDAY_TO_THURSDAY_AND_SATURDAY |Sun+Mon+Tue+Wed+Thu+Sat
