# SpeedTheRepo (Aka: The Network That Couldn't Slow Down)

This repository is the home of our work exploring how network speeds vary accross Alberta so we can identify underserved areas. Currently, this repository only joins data and creates a heatmap - however to run the notebook `networkheatmap.ipynb`, you will need to first gather some data from Statistics Canada

1. The shapefiles and network data from [Statistics Canada](https://open.canada.ca/data/en/dataset/00a331db-121b-445d-b119-35dbbe3eedd9)
2. Canada Boundary files from [Statistics Canada](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lpr_000a16a_e.zip&k=%20%20%20%20%201341&loc=http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lpr_000a16a_e.zip)
3. Forward sortation areas from [Statistics Canada](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lfsa000b16a_e.zip&k=%20%20%20%2044221&loc=http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lfsa000b16a_e.zip)

Using this data, the notebook will join this appropriately and make a heatmap to help understand network access and speed in Alberta.

## Future Work

Expand this analysis to beyond Alberta, as well as quantify network access beyond a simple heatmap showing the extent of network access accross Alberta. 
