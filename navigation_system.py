import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat
import time
import math



class Drawing_map:

    def __init__(self):
        self.liczba=1

    def markers_transformation(self, markers):
        for marker in markers:
            marker[0]=marker[0]/362*200
            marker[1]=(marker[1])/289*160
        return markers
    
    # generowanie wierzchołków prostokąta
    # x, y - ArUco kod - współrzędne środka
    # alpha - kąt odchylenia osi x kodu ArUco od osi x układu współrzędnych mapy
    # a,b - wysokość i szerokość
    def create_vertices_rectangle(self,x,y,alpha,a,b):
        c=np.sqrt(a**2+b**2)
        beta=np.arctan(b/a)
        s=c/2*np.sin(alpha+beta)
        w=c/2*np.cos(alpha+beta)
        t=c/2*np.sin(alpha-beta)
        p=c/2*np.cos(alpha-beta)
        vertices=[[x+w,y+s],[x+p,y+t],[x-w, y-s],[x-p,y-t], [x+w,y+s]]
        return vertices


    # generowanie wierzchołków trójkąta
    # x, y - ArUco kod - współrzędne środka
    # alpha - kąt odchylenia osi x kodu ArUco od osi x układu współrzędnych mapy
    # a_i, b_i - położenie i-tego wierzchołka w układzie kodu ArUco
    def create_vertices_triangle(self,x,y, alpha, a1,b1,a2,b2,a3,b3):
        c1=np.sqrt(a1**2+b1**2)
        c2=np.sqrt(a2**2+b2**2)
        c3=np.sqrt(a3**2+b3**2)
        beta1=math.atan2(b1, a1)
        beta2=math.atan2(b2, a2)
        beta3=math.atan2(b3, a3)
        s1=c1*np.sin(alpha+beta1)
        w1=c1*np.cos(alpha+beta1)
        s2=c2*np.sin(alpha+beta2)
        w2=c2*np.cos(alpha+beta2)
        s3=c3*np.sin(alpha+beta3)
        w3=c3*np.cos(alpha+beta3)
        vertices=[[x+w1,y+s1],[x+w2,y+s2],[x+w3,y+s3],[x+w1,y+s1]]
        return vertices


    # zbudowanie wielokąta z zestawu wierzchołków (coordination)
    def create_polygon(self, coord):
        xs, ys=zip(*coord)
        plt.plot(xs,ys, color="black")
        #return polygon


    # generowanie koła
    # x,y - ArUco kod - współrzędne środka
    # r - promień    
    def create_circle(self, x,y,r):
        circle= plt.Circle((x,y), radius= r)
        return circle


    def show_shape(self, patch):
        ax=plt.gca()
        ax.add_patch(patch)


    # stworzenie tablicy wirtualnie odpowiadającej mapie
    def create_tab(self, filling_number, resolution, xmax, ymax):
        x_max=int(xmax/resolution)
        y_max=int(ymax/resolution)
        tab = [[filling_number for col in range(y_max)] for row in range(x_max)]
        return tab


    # rasteryzacja koła
    def create_circle_rasterization(self, x, y, r, R, resolution, obstacle, xmax, ymax):
        x_min=x-r
        x_max=x+r
        y_min=y-r
        y_max=y+r
        xr_min=int(x_min/resolution)*resolution
        yr_min=int(y_min/resolution)*resolution
        xr_max=(int(x_max/resolution)+1)*resolution
        yr_max=(int(y_max/resolution)+1)*resolution
        for i in range(xr_min, xr_max+resolution, resolution):
            for j in range(yr_min, yr_max+resolution, resolution):
                if ((i-x)**2+(j-y)**2)<=r**2:
                    rect = plt.Rectangle((i-resolution, j-resolution), resolution, resolution, color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i, j-resolution), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i-resolution, j), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i, j), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    # zaznaczenie przeszkód w tablicy
                    xR=int(i/resolution)
                    yR=int(j/resolution)
                    if xR>0 and xR<int(xmax/resolution) and yR>0 and yR<int(ymax/resolution):
                        R[xR][yR]=obstacle
                        R[xR-1][yR-1]=obstacle
                        R[xR][yR-1]=obstacle
                        R[xR-1][yR]=obstacle


    # rsteryzacja wielokąta
    def create_polygon_rasterization(self, coord, R, resolution, obstacle, xmax, ymax):
        x_min=xmax
        x_max=0
        y_min=ymax
        y_max=0
        # znalezienie granic występowania przeszkody
        number_of_row=0
        for row in coord: 
            number_of_row=number_of_row+1
            if row[0]<x_min:
                x_min=row[0]
            if row[0]>x_max:
                x_max=row[0]
            if row[1]<y_min:
                y_min=row[1]
            if row[1]>y_max:
                y_max=row[1]
        # znalezienie komórek w których znajdują się granice
        xr_min=int(x_min/resolution)*resolution
        yr_min=int(y_min/resolution)*resolution
        xr_max=(int(x_max/resolution)+1)*resolution
        yr_max=(int(y_max/resolution)+1)*resolution
        # zalezienie zajętych komórek za pomocą Równoległego algorytmu rasteryzacji wielokątów
        nonnegative=1
        for i in range(xr_min, xr_max+resolution, resolution):
            for j in range(yr_min, yr_max+resolution, resolution):
                for k in range(0, number_of_row-1):
                    if k==(number_of_row-2):
                        vector_multiplication=(i-coord[k][0])*(coord[0][1]-coord[k][1])-(j-coord[k][1])*(coord[0][0]-coord[k][0])
                    else:
                        vector_multiplication=(i-coord[k][0])*(coord[k+1][1]-coord[k][1])-(j-coord[k][1])*(coord[k+1][0]-coord[k][0])
                    if vector_multiplication<0:
                        nonnegative=0
                if nonnegative==1:
                    rect = plt.Rectangle((i-resolution, j-resolution), resolution, resolution, color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i, j-resolution), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i-resolution, j), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    rect = plt.Rectangle((i, j), resolution, resolution,color="blue")
                    self.show_shape(rect)
                    # zaznaczenie zajętych komórek w tablicy
                    xR=int(i/resolution)
                    yR=int(j/resolution)
                    if xR>0 and xR<int(xmax/resolution) and yR>0 and yR<int(ymax/resolution):
                        R[xR][yR]=obstacle
                        R[xR-1][yR-1]=obstacle
                        R[xR][yR-1]=obstacle
                        R[xR-1][yR]=obstacle
                nonnegative=1


    # Wyznaczenie strefy buforowej dla trójkątnej przeszkody
    def create_expanded_triangle_rasterization(self, vertices, R, resolution, obstacle, buffer, xmax, ymax):
        x_a=vertices[0][0]
        y_a=vertices[0][1]
        x_b=vertices[1][0]
        y_b=vertices[1][1]
        x_c=vertices[2][0]
        y_c=vertices[2][1]
        # wyznaczanie środków krawędzi
        if x_a>x_b: 
            x01=float(abs(x_b-x_a)/2+x_b)
        else:
            x01=float(abs(x_b-x_a)/2+x_a)
        if y_a>y_b:
            y01=float(abs(y_b-y_a)/2+y_b)
        else:
            y01=float(abs(y_b-y_a)/2+y_a)
        a1=2*buffer
        b1=np.sqrt((x_a-x_b)**2+(y_a-y_b)**2)
        alpha1=math.atan2((y_b-y_a),(x_b-x_a))
        rectangle_vertices1=self.create_vertices_rectangle(x01, y01, alpha1, b1, a1)
        self.create_polygon_rasterization(rectangle_vertices1, R, resolution, obstacle, xmax, ymax)

        if x_b>x_c: 
            x02=float(abs(x_c-x_b)/2+x_c)
        else:
            x02=float(abs(x_c-x_b)/2+x_b)
        if y_b>y_c:
            y02=float(abs(y_c-y_b)/2+y_c)
        else:
            y02=float(abs(y_c-y_b)/2+y_b)
        a2=2*buffer
        b2=np.sqrt((x_b-x_c)**2+(y_b-y_c)**2)
        alpha2=math.atan2((y_c-y_b),(x_c-x_b))
        rectangle_vertices2=self.create_vertices_rectangle(x02, y02, alpha2, b2, a2)
        self.create_polygon_rasterization(rectangle_vertices2, R, resolution, obstacle, xmax, ymax)

        if x_c>x_a: 
            x03=float(abs(x_a-x_c)/2+x_a)
        else:
            x03=float(abs(x_a-x_c)/2+x_c)
        if y_c>y_a:
            y03=float(abs(y_a-y_c)/2+y_a)
        else:
            y03=float(abs(y_a-y_c)/2+y_c)
        a3=2*buffer
        b3=np.sqrt((x_c-x_a)**2+(y_c-y_a)**2)
        alpha3=math.atan2((y_a-y_c),(x_a-x_c))
        rectangle_vertices3=self.create_vertices_rectangle(x03, y03, alpha3, b3, a3)
        self.create_polygon_rasterization(rectangle_vertices3, R, resolution, obstacle, xmax, ymax)
    
        self.create_circle_rasterization(x_a, y_a, 7, R, resolution, obstacle, xmax, ymax)
        self.create_circle_rasterization(x_b, y_b, 7, R, resolution, obstacle, xmax, ymax)
        self.create_circle_rasterization(x_c, y_c, 7, R, resolution, obstacle, xmax, ymax)
    

    # rysowanie przeszkód kołowych
    def circles(self, xc, yc, r, R, resolution, obstacle, buffer, xmax, ymax):
        self.create_circle_rasterization(xc, yc, r+buffer, R, resolution, obstacle, xmax, ymax)
        circle=self.create_circle(xc, yc, r)
        self.show_shape(circle)

    
    # rysowanie przeszkód prostokątnych
    def rectangle(self, xc, yc, alpha, a, b, R, resolution, obstacle, buffer, xmax, ymax):
        rectangle_vertices=self.create_vertices_rectangle(xc, yc, alpha, a, b)
        self.create_polygon(rectangle_vertices)
        rasterization_rectangle_vertices=self.create_vertices_rectangle(xc, yc, alpha, a+2*buffer, b+2*buffer)
        self.create_polygon_rasterization(rasterization_rectangle_vertices, R, resolution, obstacle, xmax, ymax)

    
    # rysowanie przeszkód trójkątnych
    def triangle(self, xc, yc, alpha, a1, b1, a2, b2, a3, b3, R, resolution, obstacle, buffer, xmax, ymax):
        triangle_vertices=self.create_vertices_triangle(xc, yc, alpha, a1, b1, a2 ,b2, a3, b3)
        self.create_polygon(triangle_vertices)
        self.create_polygon_rasterization(triangle_vertices, R, resolution, obstacle, xmax, ymax)
        self.create_expanded_triangle_rasterization(triangle_vertices, R, resolution, obstacle, buffer, xmax, ymax)


    # rysowanie punktów wyznaczających wierzchołki przestrzeni konfiguracyjnej
    def corners(self, xmax, ymax):
        circle=self.create_circle(0,0, 1)
        self.show_shape(circle)
        circle=self.create_circle(xmax,0, 1)
        self.show_shape(circle)
        circle=self.create_circle(xmax,ymax, 1)
        self.show_shape(circle)
        circle=self.create_circle(0,ymax, 1)
        self.show_shape(circle) 


    # rysowanie przeszkód na mapie 
    def drawing_obstacles(self, markers, dimensions, R, resolution, obstacle, buffer, xmax, ymax):
        for row_mar in markers:
            if row_mar[4]==0:
                pass
            else:
                for row_dim in dimensions:
                    if float(row_dim[0])==row_mar[3]:
                        if float(row_dim[1])==0:
                            self.circles(row_mar[0], row_mar[1], float(row_dim[2]), R, resolution, obstacle, buffer, xmax, ymax)
                        if float(row_dim[1])==3:
                            lines=row_dim[2].replace("[", "")
                            lines=lines.replace("]", "")
                            lines = lines.split(',')
                            vert=[]
                            for line in lines:
                                vert.append(float(line))
                            self.triangle(row_mar[0], row_mar[1], row_mar[2], vert[0], vert[1], vert[2], vert[3], vert[4], vert[5], R, resolution, obstacle, buffer, xmax, ymax)
                        if float(row_dim[1])==4:
                            lines=row_dim[2].replace("[", "")
                            lines=lines.replace("]", "")
                            lines = lines.split(', ')
                            vert=[]
                            for line in lines:
                                vert.append(float(line))
                            self.rectangle(row_mar[0], row_mar[1], row_mar[2], vert[0], vert[1],R, resolution, obstacle, buffer, xmax, ymax)



class Path_planning:

    
    
    # Algorytm propagacji fali
    def wave_propagation_map(self, x0, y0, R, resolution, obstacle, xmax, ymax):
        coordinates=[]
        x_0=int(x0/resolution)
        y_0=int(y0/resolution)
        imax=int(xmax/resolution)
        jmax=int(ymax/resolution)
        if R[x_0][y_0]<obstacle:
            R[x_0][y_0]=0
            coordinates.append([x_0,y_0])
        else:
            raise Exception("robot is on obstacle, change place")
        while coordinates!=[]:
            i=coordinates[0][0]
            j=coordinates[0][1]
            if i>0 and R[i-1][j]>R[i][j]+2 and R[i-1][j]!=obstacle:
                R[i-1][j]=R[i][j]+2
                coordinates.append([i-1,j])
            if i<imax-1 and R[i+1][j]>R[i][j]+2 and R[i+1][j]!=obstacle:
                R[i+1][j]=R[i][j]+2
                coordinates.append([i+1,j])
            if j>0 and R[i][j-1]>R[i][j]+2 and R[i][j-1]!=obstacle:
                R[i][j-1]=R[i][j]+2
                coordinates.append([i, j-1])
            if j<jmax-1 and R[i][j+1]>R[i][j]+2 and R[i][j+1]!=obstacle:
                R[i][j+1]=R[i][j]+2
                coordinates.append([i, j+1])
            if i>0 and j>0 and R[i-1][j-1]>R[i][j]+3 and R[i-1][j-1]!=obstacle:
                R[i-1][j-1]=R[i][j]+3
                coordinates.append([i-1, j-1])
            if i>0 and j<jmax-1 and R[i-1][j+1]>R[i][j]+3 and R[i-1][j+1]!=obstacle:
                R[i-1][j+1]=R[i][j]+3
                coordinates.append([i-1, j+1])
            if j>0 and i<imax-1 and R[i+1][j-1]>R[i][j]+3 and R[i+1][j-1]!=obstacle:
                R[i+1][j-1]=R[i][j]+3
                coordinates.append([i+1,j-1])
            if i<imax-1 and j<jmax-1 and R[i+1][j+1]>R[i][j]+3 and R[i+1][j+1]!=obstacle:
                R[i+1][j+1]=R[i][j]+3
                coordinates.append([i+1, j+1])
            coordinates.remove([i,j])


    # poszukiwanie ścieżki na wypełnionej wartościami tablicy
    def create_path(self, xc, yc, R, resolution, xmax, ymax, x0, y0):
        pathx=[]
        pathy=[]
        pathx.append(xc)
        pathy.append(yc)
        imax=int(xmax/resolution)
        jmax=int(ymax/resolution)
        xc=int(xc/resolution)
        yc=int(yc/resolution)
        Rmin=R[xc][yc]
        pathx.append(xc*resolution+resolution/2)
        pathy.append(yc*resolution+resolution/2)
        while Rmin!=0:
            i=xc
            j=yc
            if i>0 and R[i-1][j]<Rmin:
                Rmin=R[i-1][j]
                xc=i-1
                yc=j
            if i<imax-1 and R[i+1][j]<Rmin:
                Rmin=R[i+1][j]
                xc=i+1
                yc=j
            if j>0 and R[i][j-1]<Rmin:
                Rmin=R[i][j-1]
                xc=i
                yc=j-1
            if j<jmax-1 and R[i][j+1]<Rmin:
                Rmin=R[i][j+1]
                xc=i
                yc=j+1
            if i>0 and j>0 and R[i-1][j-1]<Rmin:
                Rmin=R[i-1][j-1]
                xc=i-1
                yc=j-1
            if i>0 and j<jmax-1 and R[i-1][j+1]<Rmin:
                Rmin=R[i-1][j+1]
                xc=i-1
                yc=j+1
            if j>0 and i<imax-1 and R[i+1][j-1]<Rmin:
                Rmin=R[i+1][j-1]
                xc=i+1
                yc=j-1
            if i<imax-1 and j<jmax-1 and R[i+1][j+1]<Rmin:
                Rmin=R[i+1][j+1]
                xc=i+1
                yc=j+1
            pathx.append(xc*resolution+resolution/2)
            pathy.append(yc*resolution+resolution/2)
        # wygładzanie ścieżki
        path=[]
        path.append([pathx[0], pathy[0]])
        counter=0      
        while counter!=(len(pathx)-3):
            differencex1=pathx[counter+1]-pathx[counter]
            differencex2=pathx[counter+2]-pathx[counter+1]
            differencey1=pathy[counter+1]-pathy[counter]
            differencey2=pathy[counter+2]-pathy[counter+1]
            if differencex1!=differencex2 or differencey1!=differencey2:
                path.append([pathx[counter+1], pathy[counter+1]])
            counter=counter+1
        path.append([pathx[len(pathx)-1], pathy[len(pathy)-1]])
        path.append([x0, y0])
        #plt.plot(pathx, pathy, color="black")
        plt.plot([p[0] for p in path], [p[1] for p in path], color="black")
        path_starttoend=[]
        for i in range(len(path)):
            path_starttoend.append(path[len(path)-i-1])
        print(path_starttoend)
        return path_starttoend
    
    
    # wyznaczanie kolejnych kątów obrotu robota
    def rotation_angle(self, orientation, path):
        alpha=[]
        gamma=[]
        gamma.append((math.atan2(path[1][1]-path[0][1], path[1][0]-path[0][0])))
        alpha.append(-orientation+gamma[0]-np.pi/2)
        for i in range(1,len(path)-2):
            gamma.append((math.atan2(path[i+1][1]-path[i][1], path[i+1][0]-path[i][0])))
            alpha.append(gamma[i]-gamma[i-1])
        print(alpha)
        return alpha


    # wyznaczanie kolejnych odległości 
    def distance(self, path):
        distance=[]
        for i in range(len(path)-1):
            distance.append(np.sqrt((path[i+1][1]-path[i][1])**2+(path[i+1][0]-path[i][0])**2))
        print(distance)
        return distance


    # wyznaczenie czasu potrzebnego na poruszanie się po ścieżce (wyniki doświadczeń)
    # robot robi obrót o 360 stopni w 2s
    # robot przejeżdża 10 cm w 1s
    def movement_time(self, alpha, distance):
        time_angle=0
        for i in alpha:
            time_angle=time_angle+np.abs((i/180))
        time_distance=0
        for i in distance:
            time_distance=time_distance+(i/10)
        time=time_distance+time_angle
        return time


    def characteristic_values(self, distance, alpha, start_time, end_time):
        length=0
        for i in distance:
            length=length+i

        angle=0
        for i in alpha:
            angle=angle+np.abs(i)

        movement_time=self.movement_time(alpha, distance)
        time=end_time-start_time+movement_time
        print("czas obliczeń: ", end_time-start_time)
        print("czas całkowity: ", time)
        print("dlugość ścieżki: ", length)
        print("kat: ", angle)
        print("ilosc zakrętów: ", len(alpha))
