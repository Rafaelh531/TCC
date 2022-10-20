import enum
from haversine import haversine, Unit
from urllib.request import urlopen
import math
import matplotlib.pyplot as plt
# import json
import json
import time
from scipy.interpolate import interp1d
import numpy as np

P1=[-25.266667,-54.433333]
P2=[-25.40798486,-54.58897424]

print(haversine(P1, P2))
samples =2000
distancias = []
elevat = []
dist = 0


link_base = "https://api.opentopodata.org/v1/srtm30m?locations="

url = link_base + str(P1[0]) + ","
url = url + str(P1[1]) + "|"
url = url + str(P2[0]) + ","
url = url + str(P2[1]) 




if samples <= 100:
   
    url = url + "&samples=" + str(samples)
    url = url + "&interpolation=cubic"


    #link = "https://api.opentopodata.org/v1/srtm30m?locations=-25.266667,-54.433333|-25.40798486,-54.58897424&samples=100&interpolation=cubic"
    #print(link)

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    x = data_json['results']

    for idx,element in enumerate(x):
        #print(element['elevation'])
        elevat.append(element['elevation'])
        if idx == 99:
            break
        xx = element
        y = x[idx+1]
        p1 = [xx['location']['lat'],xx['location']['lng']]
        p2 = [y['location']['lat'],y['location']['lng']]
        dist = dist + haversine(p1, p2)
        distancias.append(dist)

    #print(idx)


else:
    #url = link_base
    n_divisoes = int(math.ceil(samples/100)) + 1
    print("N DIVISOES = " + str(n_divisoes))
    sample_by_divisao = int(samples/(n_divisoes -1))
    url = url + "&samples=" + str(n_divisoes)
    url = url + "&interpolation=cubic"
    print(url)
    response = urlopen(url)
    divisoes_raw = json.loads(response.read())
    divisoes = divisoes_raw['results']
    print(divisoes)

    for idx,element in enumerate(divisoes):
        print("LEN DIST = " + str(len(distancias)))
        if idx == len(divisoes) -1:
                break
        yy = divisoes[idx+1]
        url = link_base + str(element['location']['lat']) + ","
        url = url + str(element['location']['lng']) + "|"
        url = url + str(yy['location']['lat']) + ","
        url = url + str(yy['location']['lng'])
        url = url + "&samples=" + str(sample_by_divisao)
        url = url + "&interpolation=cubic"
        print(url)
        time.sleep(1.01)
        response = urlopen(url)
        print("respondeu")
        data_json = json.loads(response.read())
        x = data_json['results']
        print("AAAAAAAAA= " + str(len(x)))
        for idx2,element in enumerate(x):
            #print(element['elevation'])
            elevat.append(element['elevation'])
            xx = element
            p1 = [xx['location']['lat'],xx['location']['lng']]
            #p2 = [y['location']['lat'],y['location']['lng']]
            dist = haversine(P1, p1)
            #print(dist)
            distancias.append(dist)


for idx,element in enumerate(elevat):
    print(distancias[idx], elevat[idx])

print(distancias)
print("passo " + str(distancias[2]))
plt.figure(figsize=(10,6))
plt.plot(distancias,elevat)
# #plt.plot([0,distance],[min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
# #plt.plot([0,distance],[max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
# #plt.plot([0,distance],[mean_elev,mean_elev],'--y',label='ave: '+str(mean_elev)+' m')
# #plt.fill_between(d_list_rev,elev_list,base_reg,alpha=0.1)
# plt.text(distancias[0],elevat,"Paulistania")
# plt.text(distancias[-1],elevat,"Estação Central")
# plt.xlabel("Distance(km)")
# plt.ylabel("Elevation(m)")
# #plt.grid()
# #plt.legend(fontsize='small')
plt.show()

