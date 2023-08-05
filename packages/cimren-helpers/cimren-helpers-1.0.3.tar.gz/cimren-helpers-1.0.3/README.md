**Helper Functions**
=================

This repo provides helper functions for

- Listing files in a directory
- Calculating Haversine Distance in miles

Installation
------------

```
pip install cimren-helpers
```

How to use
----------

```
from helpers import files

file_list = files.get_all_files_in_directory('.')
```

```
from helpers import haversine_distance

distance = haversine_distance.calculate_haversine_distance(from_latitude=[47.6062],
                                                           from_longitude=[122.3321],
                                                           to_latitude=[47.5301],
                                                           to_longitude=[122.0326])
```
