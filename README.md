# SpeedTheRepo (Aka: The Network That Couldn't Slow Down)

This repository is the home of our work exploring how network speeds vary across Alberta and Canada so we can identify underserved areas. 

## Getting Started

Currently, this repository contains two [Jupyter](https://jupyter.org/) notebooks:

1. `networkheatmap.ipynb` that joins data and creates a heatmap; and
2. `notebooksHeatmapTutorialNotebook.ipynb` that joins data, creates a heatmap and demonstrates how to add an underlay (e.g. postal code boundaries) to the heatmap.  

Both notebooks **1** and **2** will generate broadband internet speed heatmaps but **2** explains in more detail the steps involved and also shows you how to add an underlay onto the heatmap which can be customized to the data you may have / want. We recommend you start with **2**.  

If you've never worked with Jupyter notebooks before you'll want to download and install it on your system first following the instructions "Getting started with the classic Jupyter Notebook" [here](https://jupyter.org/install). You will also need to make sure you have the right Python libraries on your system before running the notebook(s).

Next you'll need to gather some data from Statistics Canada:

1. The shapefiles and network data from [Statistics Canada](https://open.canada.ca/data/en/dataset/00a331db-121b-445d-b119-35dbbe3eedd9)
2. Canada Boundary files from [Statistics Canada](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lpr_000a16a_e.zip&k=%20%20%20%20%201341&loc=http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lpr_000a16a_e.zip)
3. Forward sortation areas from [Statistics Canada](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lfsa000b16a_e.zip&k=%20%20%20%2044221&loc=http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lfsa000b16a_e.zip)

Using this data, the notebook will join this appropriately and make a heatmap to help understand network access and speed in Alberta and Canada.

## Future Work

Quantify network access beyond a simple heatmap showing the extent of network access accross Alberta and Canada. 
