from dis import dis
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


class estacao:
  def __init__(self, coord, torre):
    self.coord = coord
    self.torre = torre


ESTAÇÃO_CENTRAL= estacao([-25.40798486,-54.58897424],15)

IATE_CLUBE=  estacao([-25.555556,-54.591389],5)

PEDRO_ORTELLADO=  estacao([-25.413056,-54.615278],5)

PONTE_DA_AMIZADE=  estacao([-25.511944,-54.603333],5)

R_11_MONDAY= estacao( [-25.613889,-54.599722],35)

R_4=  estacao([-25.441667,-54.602778],5)

PAULISTANIA= estacao( [-25.266667,-54.433333],5)

ENSECADEIRA_MD_MONTANTE=  estacao([-25.413056,-54.615278],5)

ENSECADEIRA_MD_JUSANTE=  estacao([-25.413056,-54.615278],5)

NOVO_POSTO_SILVA =  estacao([-25.575,-54.675],5)


############################################################################################################################################
PONTO1= PAULISTANIA
PONTO2 = ESTAÇÃO_CENTRAL
############################################################################################################################################



P1 = [-25.547221, -54.597916]
P2 = PONTO2.coord

LOS = True

#print(haversine(P1, P2))
samples =200
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
    #print("N DIVISOES = " + str(n_divisoes))
    sample_by_divisao = int(samples/(n_divisoes -1))
    url = url + "&samples=" + str(n_divisoes)
    url = url + "&interpolation=cubic"
    #print(url)
    response = urlopen(url)
    divisoes_raw = json.loads(response.read())
    divisoes = divisoes_raw['results']
    #print(divisoes)

    for idx,element in enumerate(divisoes):
        #print("LEN DIST = " + str(len(distancias)))
        if idx == len(divisoes) -1:
                break
        yy = divisoes[idx+1]
        url = link_base + str(element['location']['lat']) + ","
        url = url + str(element['location']['lng']) + "|"
        url = url + str(yy['location']['lat']) + ","
        url = url + str(yy['location']['lng'])
        url = url + "&samples=" + str(sample_by_divisao)
        url = url + "&interpolation=cubic"
        #print(url)
        time.sleep(1.01)
        response = urlopen(url)
        #print("respondeu")
        data_json = json.loads(response.read())
        x = data_json['results']
        #print("AAAAAAAAA= " + str(len(x)))
        for idx2,element in enumerate(x):
            #print(element['elevation'])
            elevat.append(element['elevation'])
            xx = element
            p1 = [xx['location']['lat'],xx['location']['lng']]
            #p2 = [y['location']['lat'],y['location']['lng']]
            dist = haversine(P1, p1)
            #print(dist)
            distancias.append(dist)


#for idx,element in enumerate(elevat):
#    print(distancias[idx], elevat[idx])


maior = elevat[0]
if elevat[-1] > maior:
    maior = elevat[-1]

for element in elevat[2:len(elevat)-2]:
    if element >= maior:
        LOS = False


CA = (distancias[-1]-distancias[0])*1000
if(elevat[0]> elevat[-1]):
    CO = (elevat[0]+PONTO1.torre) - (elevat[-1]+PONTO2.torre)
else:
    CO = (elevat[-1]+PONTO2.torre) - (elevat[0]+PONTO1.torre)
distancia_real = math.sqrt((CA**2)+(CO**2))
#print(distancias)
#print("passo " + str(distancias[2]))



texto = "Distância:" + str(round(haversine(P1, P2),2))+"km "
texto += "LOS: " + str(bool(LOS))
texto += " Distância diagonal:" + str(round((distancia_real/1000),2))+"km "


plt.figure(figsize=(10,6))
plt.plot(distancias,elevat,'g')
plt.fill_between(distancias,elevat,color='green')
plt.plot([distancias[0],distancias[-1]] ,[elevat[0]+PONTO1.torre, elevat[-1]+PONTO2.torre],'--',color='black',linewidth=0.8)
plt.vlines(distancias[0],elevat[0],elevat[0]+PONTO1.torre,colors='r',linewidth=2.0)
plt.vlines(distancias[-1],elevat[-1],elevat[-1]+PONTO2.torre,colors='r',linewidth=2.0)
plt.ylim(min(elevat)-min(elevat)*0.2, max(elevat)*1.2)     # set the ylim to bottom, top


plt.xlabel("Distance(km)\n %s"%texto)
plt.ylabel("Elevation(m)")
# #plt.grid()
# #plt.legend(fontsize='small')
plt.show()

