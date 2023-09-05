import math
import matrix as mt


class Point:
    def __init__(self, xi, yi):
        self.x = xi
        self.y = yi

    def setLocation(self, xn, yn):
        self.x = xn
        self.y = yn

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Perspectiva:
    origenX, origenY = 650, 325
    grado = math.pi/180.0
    rotEjeX1 = mt.np.array([[1, 0, 0, 0], [0, math.cos(
        grado), -math.sin(grado), 0], [0, math.sin(grado), math.cos(grado), 0], [0, 0, 0, 1]])
    rotEjeX2 = mt.np.array([[math.cos(grado), 0, math.sin(grado), 0], [
        0, 1, 0, 0], [-math.sin(grado), 0, math.cos(grado), 0], [0, 0, 0, 1]])
    rotEjeX3 = mt.np.array([[math.cos(grado), -math.sin(grado), 0, 0],
                            [math.sin(grado), math.cos(grado), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    def __init__(self, THs=30.0, PHs=60.0, RH=40, DP=300.0):
        self.TH, self.PH, self.RH = THs*self.grado, PHs*self.grado, RH
        self.C1, self.C2 = math.cos(self.TH), math.cos(self.PH)
        self.S1, self.S2 = math.sin(self.TH), math.sin(self.PH)
        self.DP, self.FE, self.error = DP, 1.1, 0.0
        self.POX1, self.POX2, self.POX3 = self.RH*self.C1 * \
            self.S2, self.RH*self.S1*self.S2, self.RH*self.C2
        self.trasPObs = mt.np.array(
            [[1, 0, 0, -self.POX1], [0, 1, 0, -self.POX2], [0, 0, 1, -self.POX3], [0, 0, 0, 1]])
        self.rot90MTH = mt.np.array(
            [[self.S1, -self.C1, 0, 0], [self.C1, self.S1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.rot180MPH = mt.np.array(
            [[1, 0, 0, 0], [0, -self.C2, self.S2, 0], [0, -self.S2, -self.C2, 0], [0, 0, 0, 1]])
        self.refEjeX1 = mt.np.array(
            [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.matTRPos = mt.np.array(mt.Matrix().producto(self.refEjeX1, mt.Matrix().producto(
            self.rot180MPH, mt.Matrix().producto(self.rot90MTH, self.trasPObs))))

    @classmethod
    def setOrigen(cls, X, Y):
        cls.origenX, cls.origenY = X, Y

    @classmethod
    def fabricaPerspectiva(cls, pobs, DP):
        return cls(pobs.getThetaSexagesimal(), pobs.getPhiSexagesimal(), pobs.getRho(), DP)

    def update(self, pobs, DP):
        self.TH = pobs.getTheta()
        self.PH = pobs.getPhi()
        self.RH = pobs.getRho()
        self.DP = DP
        self.C1 = math.cos(self.TH)
        self.C2 = math.cos(self.PH)
        self.S1 = math.sin(self.TH)
        self.S2 = math.sin(self.PH)
        self.POX1 = pobs.getX()
        self.POX2 = pobs.getY()
        self.POX3 = pobs.getZ()
        # Refresh transform
        self.trasPObs[0][3] = -self.POX1
        self.trasPObs[1][3] = -self.POX2
        self.trasPObs[2][3] = -self.POX3
        self.rot90MTH[0][0] = self.S1
        self.rot90MTH[0][1] = -self.C1
        self.rot90MTH[1][0] = self.C1
        self.rot90MTH[1][1] = self.S1
        self.rot180MPH[1][1] = -self.C2
        self.rot180MPH[1][2] = self.S2
        self.rot180MPH[2][1] = -self.S2
        self.rot180MPH[2][2] = -self.C2
        self.matTRPos = mt.Matrix().producto(self.refEjeX1, mt.Matrix().producto(
            self.rot180MPH, mt.Matrix().producto(self.rot90MTH, self.trasPObs)))

    def projectedPoint(self, pr3):
        # print(pr3.getHArr())
        VC1T = mt.Matrix().producto(self.matTRPos, pr3.getHArr())
        XP1 = self.error+self.origenX + \
            ((self.DP*VC1T[0][0])/(VC1T[2][0]*self.FE))
        YP1 = self.error+self.origenY-(self.DP*VC1T[1][0])/VC1T[2][0]
        pAux = Point(XP1, YP1)
        return pAux
