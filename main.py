import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat
import time
import navigation_system as ns
import math
import server
import robot


# zmienne globalne
# xmax, ymax -  wymiary przestrzeni konfiguracyjnej
# xaim, yaim - współrzędne punktu docelowego
# first_filling - wartość początkowego wypełnienia tablicy odpowiadającej mapie
# obstacle - wartość wypełnienia komórek w których znajdują się przeszkody

resolution=4

xmax=200
ymax=160
xaim=180
yaim=140
buffer=7
first_filling=1000
obstacle=first_filling*2
#x0=180
#y0=140

start_time=time.time()

# Pobieranie wartości poszczególnych markerów przy działającej kamerze
# do odkomentowania przy pracy z kamerą
"""
with server.Client() as c:
    markers = c.read(server.READ_MARKERS)["markers"]

# dodanie numeru ID kodu
counter=0
for marker in markers:
    marker.insert(3,float(counter))
    counter=counter+1
"""
# pobieranie wartości markerów z pliku tekstowego
# do zakomentowania przy pracy z kamerą

file = open('markers.txt', 'r').read()
lines=file.replace("{'markers': [[", "")
lines=lines.replace("]]}", "")
lines = lines.split('], [')
markers=[]

# do zakomentowania przy pracy z kamerą
# wpisywanie wartości do tablicy markers
# dodanie numeru ID kodu
counter=0
for line in lines:
    point=[]
    fields=line.split(', ')
    for field in fields:
        point.append(float(field))
    point.insert(3, float(counter))
    markers.append(point)
    counter=counter+1



# struktura pliku figures.txt:
# ID, TYP, parametry
# TYP - 0 - koło; parametry: r
# TYP - 3 - trójkąt; parametry: [a1, b1, a2, b2, a3, b3] - a_i, b_i - współrzędne i-tego wierzchołka
                                                                                        #względem układu współrzędnych kodu ArUco
# TYP - 4 - prostokąt, parametry: [a, b] - bok a równoległy do osi y, bok b równoległy do osi x

# pobieranie wartości parametrów
file = open('figures.txt', 'r').read()
lines=file.split('\n')
dimensions=[]

#przypisanie parametrów do tablicy dimensions
for line in lines:
    point=[]
    fields=line.split(',  ')
    for field in fields:
        point.append(field)
    dimensions.append(point)
   

#nowy obiekt
virtual_map=ns.Drawing_map()

#transformacja wartości markerów do układu współrzędnych związanego z mapą -> 1j. = 1cm
markers=virtual_map.markers_transformation(markers)
    
# utworzenie tablicy wirtualnie odpowiadającej mapie przestrzeni konfiguracyjnej
P=virtual_map.create_tab(first_filling, resolution, xmax, ymax)

#oznaczenie rogów stołu
virtual_map.corners(xmax, ymax)

# rysowanie przeszkód i wypełnanie zajętych komórek na mapie
virtual_map.drawing_obstacles(markers, dimensions, P, resolution, obstacle, buffer, xmax, ymax)

#nowy obiekt
virtual_path=ns.Path_planning()

x0=markers[4][0]
y0=markers[4][1]
# wypełnienie mapy wartościami za pomocą algorytmu propagacji fali
virtual_path.wave_propagation_map(x0, y0, P, resolution, obstacle, xmax, ymax)

#Znalezienie ścieżki
#do odkomentowania przy pracy z kamerą

path=virtual_path.create_path(xaim, yaim, P, resolution, xmax, ymax)


#wyznaczenie kolejnych katów obrotu
alpha=virtual_path.rotation_angle(markers[4][2], path)


# wyznaczenie dlugosci
distance=virtual_path.distance(path)


#do odkomentowania przy pracy z kamerą
# przekazywanie danych wyjściowych (alpha i distance) do robota  
"""
with robot.RobotNetwork() as rn:
    for i in range(len(alpha)):
        rn.setRobotVelocity(4, robot.ROBOTPATH_TURN, [abs(alpha[i])/np.pi, alpha[i]])
        time.sleep(abs(alpha[i])/np.pi)
        rn.setRobotVelocity(4, robot.ROBOTPATH_LINE, [distance[i]/10, distance[i]*10])
        time.sleep(distance[i]/10)
"""

end_time=time.time()


# wyznaczenie czasu i długości (wyniki doświadczeń)
virtual_path.characteristic_values(distance, alpha, start_time, end_time)
#print(x0, y0)

# rysowanie mapy
plt.grid(which='both', axis='both')
plt.axis('equal')
plt.show()
plt.axis('scaled')
