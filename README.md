pairwise-geo-distances
======================

Find pairwise distances between a list of geolocations and cache them locally.

I wrote this script to get data that [Alex Soble][1] could cache in his [DivvyBrags Chrome extension][2]:

> This is a Chrome extension that lets you scrape, download, chart, and extend your Divvy bikeshare data.

With this data, he was able to avoid calling the [Google Maps API][3] every time, which he wanted to do without for two reasons.

1. There are currently 300 bike stations with fixed locations and it doesn't make a lot of sense to call the API over and over for something that could easily be precalculated.
2. There are limits to how often someone can call the Google Maps API depending on whether you're paying for a Google Maps API account. If the extension became popular, and we would like to plan for that being the case, Alex would soon get into the territory of needing a premium API account.



 [1]: https://github.com/alexsoble
 [2]: https://chrome.google.com/webstore/detail/divvybrags/obpfmeilmeicjimgkpekfgmaoelbbfpf
 [3]: https://developers.google.com/maps/documentation/webservices/


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/tothebeat/pairwise-geo-distances/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

