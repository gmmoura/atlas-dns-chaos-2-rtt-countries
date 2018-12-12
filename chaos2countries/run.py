
#main file which invokes all of the others
import sys
sys.path.append('../')
import requests
import json
from  chaos2countries.chaosParser  import json_parser
from  chaos2countries.probesParser import read_iso_countries_list, read_ripe_probe_list, read_probe_data
import numpy as np

def main():


    print("reading country code info")
    geo_data = read_iso_countries_list()

    date = sys.argv[2]
    probeFile = date + "-probemetadata.json"

    print("reading probe metadata info")
    ripe_data = read_ripe_probe_list(date, probeFile,geo_data)

    print("reading Ripe Altas CHAOS Measurements and parsing")
    url = sys.argv[1]

    r = requests.get(url)
    measurements = json_parser(r.content.decode("utf-8"))

    probeDict = read_probe_data(probeFile + ".gz")
    atlas_results = date + "-atlas-results.csv"

    # now, with all the data in hands, we gotta for each measurmenet to add the trailler
    csvFileFromAtlas = open(atlas_results, 'w')
    csvFileFromAtlas.write(
        "ip_src,ip_dst,proto,hostnameBind,rtt,probeID,timestamp,rcode,atlas_firmware,country,continent,subregion,probe_version\n")
    for k in measurements:
        # print("w")
        probeID = k.split(",")[5]
        trailler = "NA,NA"
        try:
            trailler = probeDict[probeID.strip()]
        except:
            print("Probe not found: " + str(probeID))
        csvFileFromAtlas.write(k + "," + trailler + "\n")

    csvFileFromAtlas.close()

    print("starting agg stats per country")
    print("ONLY FOR RCODE=0")

    ccDict = dict()

    with open(atlas_results, 'r') as f:
        lines = f.readlines()

        for l in lines:

            sp = l.split(",")
            # if matches rcode and if the column value matches
            if len(sp) == 13:
                # filtering rcode 0
                if sp[7].strip() == "0":
                    tempCountry = sp[9].strip()
                    tempRTT = float(sp[4].strip())

                    if tempCountry not in ccDict:
                        tempArray = []
                        tempArray.append(tempRTT)
                        ccDict[tempCountry] = tempArray
                    else:
                        tempArray = ccDict[tempCountry]
                        tempArray.append(tempRTT)
                        ccDict[tempCountry] = tempArray

    # output stats.csv
    jsonDict = dict()
    with open(date + "-stats.csv", "w") as f:

        f.write("country, nMesurements,meanRTT,percentile25RTT,medianRTT,percentile75RTT,percentile90RTT,maxRTT\n")
        for k, values in ccDict.items():
            country = k
            f.write(
                country
                + "," +
                str(len(values))
                + "," +
                str(np.mean(values))
                + "," + str(np.percentile(values, 25))
                + "," + str(np.percentile(values, 50))
                + "," + str(np.percentile(values, 75))
                + "," + str(np.percentile(values, 90))
                + "," + str(np.max(values)) + "\n")

            tempDict = dict()

            tempDict['nMeasurements'] = len(values)
            tempDict['meanRTT'] = np.mean(values)
            tempDict['percentile25RTT'] = np.percentile(values, 25)
            tempDict['medianRTT'] = np.percentile(values, 50)
            tempDict['percentile75RTT'] = np.percentile(values, 75)
            tempDict['percentile90RTT'] = np.percentile(values, 95)
            tempDict['maxRTT'] = np.max(values)

            jsonDict[country] = tempDict

            #   +","+  str(np.max(values)) + "," + str(np.percentile(values,90)) )

    print("writing json output")

    # create json format
    with open(date + "-stats.json", "w") as f:
        json.dump(jsonDict, f)


if __name__ == "__main__":


    if len(sys.argv)!=3:
        print("Wrong number of parameters\n")
        print(str(len(sys.argv)))
        print( "Usage:  python run.py $ATLAS_JSON_RAW_FILE  $DATE(YYYYMMDD) ")
    else:

        main()


    print('END')



