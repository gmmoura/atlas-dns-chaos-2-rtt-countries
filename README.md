#Atlas-dns-chaos-2-rtt-countries stats


## Summary 

   * This country does the following:
      1. Download and parses and RIPE CHAOS atlas DNS measurements
      1. Produces a CSV file with the results, and enriches the results with:
         * probe's country
         * probe's continent
         * probe's subregion
         * probe's firmware version
         * probe's version (v1--v4)
      1. Produces *ready to use* aggregate stats file for the measurement, per country,
      in both JSON and CSV format, so OPS teams can easily integrate into their dashboards and 
      other graphs tools
      

## Demo

 ```bash
 
 #1. Clone the repository
 $ git clone https://github.com/gmmoura/atlas-dns-chaos-2-rtt-countries.git
 
 #go to tests dir
 $ cd atlas-dns-chaos-2-rtt-countries/tests
 
 #let's user a Atlas b-root measurement
 #you can get these from https://atlas.ripe.net/measurements/$MEASUREMENT_ID/#!download
 #WARNING: the variable start and stop below  are in UNIX timpestamp
 #and set how much data you want to collect
 #Start with a few minutes only
 
 #here we are having 300s only (stop - start)
 
 url="https://atlas.ripe.net/api/v2/measurements/10310/results/?start=1544572800&stop=1544573100&format=json"
 
 #this variable tells the date the measurement was executed; we need it to download the appropriate
 #probe datatade file
 #format : YYYYMMDD
 
 mdate=20181212
 
 #read to go:
 $ python3  ../chaos2countries/run.py  $url $mdate
 
  ```   
  
### Output files


The demo below will produce the following output files on your local dir:
   * ``20181212-atlas-results.csv``: a csv file with the parsed results from Atlas' JSON. In other words, 
   a easier version to read from the ``$url`` above, enriched with metadata about gelocation and probes.
   * ``20181212-stats.csv``: stats filea for the file below, perduced per country
   * ``20181212-stats.json``: same as above, but in JSON


### What can you do with this?
 
   * Use JSON or CSV output to produce nice World heatmaps
      