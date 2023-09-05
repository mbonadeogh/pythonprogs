import math
from pygame.locals import *
from structlinks.DataStructures import LinkedList
import matrix as mt


class Forma:
    PA = (math.sqrt(5.0)+1.0)/2.0

    def __init__(self):
        self.surface = LinkedList()

    def size(self):
        return len(self.surface)

    def getElem(self, indexPos):
        return self.surface[indexPos]

    def setElem(self, indexPos, triangulo):
        self.surface[indexPos] = triangulo


class PointR3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.rho = math.sqrt(math.pow(x, 2)+math.pow(y, 2)+math.pow(z, 2))
        self.phi = (math.pi/2) if z == 0 else (0 if (z/self.rho) >=
                                               1 else (math.pi if (z/self.rho) <= -1 else math.acos(z/self.rho)))
        # print(f"x={x}, y={y}, z={z}, self.rho={self.rho}, self.phi={self.phi}")
        # sthe = y/(self.rho*math.sin(self.phi))  # ver cero
        # sthe = -1.0 if sthe < -1.0 else (1.0 if sthe > 1.0 else sthe)
        # self.theta = (math.acos(x/(self.rho*math.sin(self.phi))) if y > 0 else ((math.pi-math.asin(
        #     y/(self.rho*math.sin(self.phi)))) if x < 0 else math.asin(sthe)))
        self.theta = math.atan(
            y/x) if x != 0 else (math.pi/2 if y >= 0 else (3*math.pi/2))

    @classmethod
    def toCartesian(cls, sx_, sy_, sz_, theta_, phi_):  # Elipsoidales a Cartesianas
        return cls(sx_ * math.cos(theta_) * math.sin(phi_), sy_ * math.sin(theta_) * math.sin(phi_), sz_ * math.cos(phi_))

    # @classmethod
    # def toCartesian(cls, rho_, theta_, phi_):  # Esfericas a Cartesianas
    #     return cls(rho_ * math.cos(theta_) * math.sin(phi_), rho_ * math.sin(theta_) * math.sin(phi_), rho_ * math.cos(phi_))

    @classmethod
    def toCartesianFT(cls, R_, r_, theta_, phi_):  # Toro a Cartesianas
        return cls(math.cos(theta_)*(R_+r_*math.cos(phi_)), math.sin(theta_)*(R_+r_*math.cos(phi_)), r_*math.sin(phi_))

    @classmethod
    def toCartesianF8(cls, t, theta_, phi_):  # Parametrica 8 de revolucion a Cartesianas
        return cls(t*math.cos(phi_)*math.sin(phi_), t*math.cos(theta_)*math.sin(theta_)*math.sin(phi_), t*math.sin(theta_)*math.sin(phi_))

    @classmethod
    def toCartesianPF(cls, a, b, theta_, phi_):  # Piriforme a Cartesianas
        return cls(b*(1+math.sin(phi_))*math.cos(phi_)*math.sin(theta_), b*(1+math.sin(phi_))*math.cos(phi_)*math.cos(theta_), a*(1+math.sin(phi_)))

    @classmethod
    def toCartesianLem(cls, a, theta_, phi_):  # Patametrica Lemniscata
        return cls((a*Math.sin(phi_)*Math.cos(phi_)/(1+Math.pow(Math.sin(phi_), 2)))*Math.sin(theta_), (a*math.sin(phi_)*math.cos(phi_)/(1+math.pow(math.sin(phi_), 2)))*math.cos(theta_), a*math.cos(phi_)/(1+math.pow(math.sin(phi_), 2)))

    @classmethod
    def from_PointR3(cls, p):
        if isinstance(p, PointR3):
            return cls(p.x, p.y, p.z)
        else:
            return cls(p[0][0], p[1][0], p[2][0])

    @classmethod
    def getPointDiff(cls, pEnd, pIni):
        return cls(pEnd.x-pIni.x, pEnd.y-pIni.y, pEnd.z-pIni.z)

    @classmethod
    def getPointSum(cls, pEnd, pIni):
        return cls(pEnd.x+pIni.x, pEnd.y+pIni.y, pEnd.z+pIni.z)

    @classmethod
    def getPointAvg(cls, pEnd, pIni):
        return cls((pEnd.x+pIni.x)/2, (pEnd.y+pIni.y)/2, (pEnd.z+pIni.z)/2)

    @classmethod
    def getProdVect(cls, U, V):
        return cls(U.y*V.z-U.z*V.y, U.z*V.x-U.x*V.z, U.x*V.y-U.y*V.x)

    def escalado(self, escala):
        return PointR3(self.getX()*escala, self.getY()*escala, self.getZ()*escala)

    def getRho(self):
        return self.rho

    def getTheta(self):
        return self.theta

    def getPhi(self):
        return self.phi

    def getThetaSexagesimal(self):
        return (self.theta*180)/math.pi

    def getPhiSexagesimal(self):
        return (self.phi*180)/math.pi

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getArr(self):
        hArr = mt.np.array([[self.x], [self.y], [self.z]])
        return hArr

    def getHArr(self):
        hArr = mt.np.array([[self.x], [self.y], [self.z], [1.0]])
        return hArr


class AristR3:
    def __init__(self, pIni, pEnd):
        self.pIni = pIni
        self.pEnd = pEnd

    @classmethod
    def from_AristR3(cls, xi, yi, zi, xf, yf, zf):
        return cls(PointR3(xi, yi, zi), PointR3(xf, yf, zf))

    def getIPoint(self):
        return self.pIni

    def getEPoint(self):
        return self.pEnd

    def getLength(self):
        return math.sqrt(math.pow(self.pEnd.getX()-self.pIni.getX(), 2)+math.pow(self.pEnd.getY()-self.pIni.getY(), 2)+math.pow(self.pEnd.getZ()-self.pIni.getZ(), 2))

    def getVersor(self):
        return PointR3((self.pEnd.getX()-self.pIni.getX())/self.getLength(), (self.pEnd.getY()-self.pIni.getY())/self.getLength(), (self.pEnd.getZ()-self.pIni.getZ())/self.getLength())


class Triangulo:
    def __init__(self, p1, p2, p3):
        self.pR3 = mt.np.empty((3, 1), dtype=PointR3)
        self.aR3 = mt.np.empty((3, 1), dtype=AristR3)
        self.pR3[0] = p1
        self.pR3[1] = p2
        self.pR3[2] = p3
        self.aR3[0] = AristR3(p1, p2)
        self.aR3[1] = AristR3(p2, p3)
        self.aR3[2] = AristR3(p3, p1)
        self.last_dist_pvo = -1

    @classmethod
    def from_Triangulo(cls, a1, a2, a3):
        return cls(a1.getIPoint(), a2.getIPoint(), a3.getIPoint())

    @classmethod
    def from_Array(cls, tArr):
        return cls(PointR3(tArr[0][0], tArr[1][0], tArr[2][0]), PointR3(tArr[0][1], tArr[1][1], tArr[2][1]), PointR3(tArr[0][2], tArr[1][2], tArr[2][2]))

    def getPoint(self, nPoint):
        if (nPoint < 1 and nPoint > 3):
            return None
        else:
            return self.pR3[nPoint-1][0]

    def getNormal(self):
        # print(f"Tipo1: {type(self.pR3[1])}, Tipo2: {type(self.pR3[1][0])}")
        U = PointR3.getPointDiff(self.pR3[1][0], self.pR3[0][0])
        V = PointR3.getPointDiff(self.pR3[2][0], self.pR3[1][0])
        return PointR3.getProdVect(U, V)

    def esVisible(self, PVO):
        self.last_dist_pvo = AristR3(self.pR3[0][0], PVO).getLength()
        mat_ = mt.Matrix()
        return True if mat_.prod_escalar(PointR3.getPointDiff(PVO, self.pR3[0][0]).getArr(), self.getNormal().getArr()) > 0 else False

    def getHArr(self):
        hArr = mt.np.array([[self.pR3[0][0].x, self.pR3[1][0].x, self.pR3[2][0].x], [self.pR3[0][0].y, self.pR3[1][0].y, self.pR3[2][0].y], [
                           self.pR3[0][0].z, self.pR3[1][0].z, self.pR3[2][0].z], [1.0, 1.0, 1.0]])
        return hArr

    def get_last_dist_pvo(self):
        return self.last_dist_pvo


class Triangulo_Coloreado(Triangulo):
    def __init__(self, p1, p2, p3, fill_color):
        super().__init__(p1, p2, p3)
        self.fill_color = fill_color

    def get_fill_color(self):
        return self.fill_color

    @classmethod
    def from_Array(cls, tArr, fill_color):
        return cls(PointR3(tArr[0][0], tArr[1][0], tArr[2][0]), PointR3(tArr[0][1], tArr[1][1], tArr[2][1]), PointR3(tArr[0][2], tArr[1][2], tArr[2][2]), fill_color)


class Elipsoide(Forma):
    def __init__(self, center, radX, radY, radZ, vSteps, hSteps, fillColor):
        super().__init__()
        vArcLen = math.pi / vSteps
        hArcLen = (2 * math.pi) / hSteps
        for i in range(vSteps):
            for j in range(hSteps):
                # print(f"i:{i},j:{j}")
                if i == 0:
                    self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3(0, 0, radZ)), PointR3.getPointSum(center, PointR3.toCartesian(
                        radX, radY, radZ, hArcLen*j, vArcLen*(i+1))), PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*(j+1), vArcLen*(i+1))), list(mt.np.random.choice(range(255), size=3))))
                elif i < (vSteps-1):
                    self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*j, vArcLen*i)), PointR3.getPointSum(center, PointR3.toCartesian(
                        radX, radY, radZ, hArcLen*j, vArcLen*(i+1))), PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*(j+1), vArcLen*(i+1))), list(mt.np.random.choice(range(255), size=3))))
                    self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*(j+1), vArcLen*(i+1))), PointR3.getPointSum(
                        center, PointR3.toCartesian(radX, radY, radZ, hArcLen*(j+1), vArcLen*i)), PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*j, vArcLen*i)), list(mt.np.random.choice(range(255), size=3))))
                else:
                    self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*j, vArcLen*i)), PointR3.getPointSum(
                        center, PointR3.toCartesian(radX, radY, radZ, hArcLen*j, vArcLen*(i+1))), PointR3.getPointSum(center, PointR3.toCartesian(radX, radY, radZ, hArcLen*(j+1), vArcLen*i)), list(mt.np.random.choice(range(255), size=3))))


class Toro(Forma):
    def __init__(self, center, dR, dr, vSteps, hSteps, fillColor):
        super().__init__()
        vArcLen = 2*math.pi / vSteps
        hArcLen = 2*math.pi / hSteps
        for i in range(vSteps):
            for j in range(hSteps):
                self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3.toCartesianFT(dR, dr, hArcLen*j, vArcLen*i)), PointR3.getPointSum(
                    center, PointR3.toCartesianFT(dR, dr, hArcLen*(j+1), vArcLen*(i+1))), PointR3.getPointSum(center, PointR3.toCartesianFT(dR, dr, hArcLen*j, vArcLen*(i+1))), list(mt.np.random.choice(range(255), size=3))))
                self.surface.append(Triangulo_Coloreado(PointR3.getPointSum(center, PointR3.toCartesianFT(dR, dr, hArcLen*(j+1), vArcLen*(i+1))), PointR3.getPointSum(
                    center, PointR3.toCartesianFT(dR, dr, hArcLen*j, vArcLen*i)), PointR3.getPointSum(center, PointR3.toCartesianFT(dR, dr, hArcLen*(j+1), vArcLen*i)), list(mt.np.random.choice(range(255), size=3))))


class Esfera(Elipsoide):
    def __init__(self, center, radio, vSteps, hSteps, fillColor):
        super().__init__(center, radio, radio, radio, vSteps, hSteps, fillColor)


# myMat1 = mt.Matrix()
# M = [[8, 14, -6], [12, 7, 4], [-11, 3, 21]]
# Minv = myMat1.inversa(M)
# print(f"Inversa M1: {myMat1.inversa(Minv)}")
# print(f"Producto MxM**-1:{myMat1.producto(M,Minv)}")

# tri1 = Triangulo.from_Triangulo(
#     AristR3(PointR3(-1, -1, 0), PointR3(1, 1, 1)), AristR3(PointR3(1, 1, 1), PointR3(1, 1, -1)), AristR3(PointR3(1, 1, -1), PointR3(-1, -1, 0)))
# print(
#     f"Triangulo1 = {tri1.getHArr()}, visible:{tri1.esVisible(PointR3(-10,10,10))}")
