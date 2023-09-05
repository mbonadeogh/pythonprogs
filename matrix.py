# Definir matrices y sus operaciones en Python
import math
import numpy as np


class Matrix:
    def producto(self, a, b):
        # MxN * NxP = MxP , M=len(a) , N=len(a[0])=len(b) , P=len(b[0])
        if (len(a[0]) != len(b)):
            print(
                "Las matrices a multiplicar deben ser del tipo MxN y NxR donde N debe ser igual en ambas")
            return None
        else:
            # print("Ok, se pueden multiplicar")
            # print(f"a: {a}, b:{b}")
            filas = len(a)
            columnas = len(b[0])
            # print(f"len(a): {len(a)}, len(b[0]):{len(b[0])}")
            n = len(b)
            c = np.zeros((filas,  columnas))
            for k in range(columnas):
                for i in range(filas):
                    for j in range(n):
                        # print(f"i: {i}, j:{j}, k:{k}")
                        c[i][k] += a[i][j]*b[j][k]
            return np.round(c, decimals=5)

    def submat(self, mat, fila, columna):
        if ((fila != -1 and (len(mat)-1) < 1) or (columna != -1 and (len(mat[0])-1) < 1) or fila >= len(mat) or columna >= len(mat[0])):
            return None
        len_fil = len(mat)
        len_col = len(mat[0])
        smat = np.zeros(((len_fil if (fila < 0) else (len_fil-1)),
                        (len_col if (columna < 0) else (len_col-1))))
        for i in range(len_fil):
            for j in range(len_col):
                if (i == fila or j == columna):
                    continue
                smat[i if (fila < 0 or i < fila) else (
                    i-1)][j if (columna < 0 or j < columna) else (j-1)] = mat[i][j]
        return smat

    def determinante(self, a):
        valDet = 0
        if (len(a) == 1):
            return a[0]
        else:
            for col in range(len(a)):
                valDet += math.pow(-1, col) * \
                    a[0][col] * self.determinante(self.submat(a, 0, col))
        return valDet

    def cofactor(self, mat):
        mat_len = len(mat)
        matcof = np.zeros((mat_len, mat_len))
        for i in range(mat_len):
            for j in range(mat_len):
                matcof[i][j] = (math.pow(-1, i+j) *
                                self.determinante(self.submat(mat, i, j)))
        return matcof

    def transpuesta(self, mat):
        mat_nfil = len(mat)
        mat_ncol = len(mat[0])
        mtran = np.zeros((mat_ncol, mat_nfil))
        for i in range(mat_nfil):
            for j in range(mat_ncol):
                mtran[j][i] = mat[i][j]
        return mtran

    def adjunta(self, mat):
        return self.transpuesta(self.cofactor(mat))

    def inversa(self, mat):
        det = self.determinante(mat)
        matinv = self.adjunta(mat)
        mat_len = len(mat)
        for i in range(mat_len):
            for j in range(mat_len):
                matinv[i][j] = matinv[i][j] / det
        return matinv

    def division(self, matn, matd):
        return self.producto(matn, self.inversa(matd))

    def potencia(self, mat, pot):
        aux = None
        if (pot < 0):
            if (self.determinante(mat) == 0):
                return None
            aux = self.inversa(mat)
            pot = -pot
        else:
            aux = mat
        mat_len = len(mat)
        mpot = np.identity(mat_len) if (pot == 0) else aux
        for i in range(1, pot):
            mpot = self.producto(aux, mpot)
        return mpot

    def suma(self, mat1, mat2):
        mat1_cfil, mat1_ccol, mat2_cfil, mat2_ccol = len(
            mat1), len(mat1[0]), len(mat2), len(mat2[0])
        if (mat1_cfil != mat2_cfil or mat1_ccol != mat2_ccol):
            print("No es posible sumar las matrices")
            return None
        mat_suma = np.zeros((mat1_cfil, mat1_ccol))
        for i in range(mat1_cfil):
            for j in range(mat1_ccol):
                mat_suma[i][j] = mat1[i][j] + mat2[i][j]
        return mat_suma

    def resta(self, mat1, mat2):
        mat1_cfil, mat1_ccol, mat2_cfil, mat2_ccol = len(
            mat1), len(mat1[0]), len(mat2), len(mat2[0])
        if (mat1_cfil != mat2_cfil or mat1_ccol != mat2_ccol):
            print("No es posible restar las matrices")
            return None
        mat_resta = np.zeros((mat1_cfil, mat1_ccol))
        for i in range(mat1_cfil):
            for j in range(mat1_ccol):
                mat_resta[i][j] = mat1[i][j] - mat2[i][j]
        return mat_resta

    def prod_escalar(self, vec1, vec2):
        if (len(vec1) != len(vec2) or len(vec1[0]) != len(vec2[0])):
            return None
        if (len(vec1) == 1):
            return self.producto(vec1, self.transpuesta(vec2))[0][0]
        else:
            return self.producto(self.transpuesta(vec1), vec2)[0][0]

    def fila(self, mat, nfil):
        if nfil > len(mat):
            return None
        ccol = len(mat[0])
        mfil = np.zeros((1, ccol))
        for j in range(ccol):
            mfil[0][j] = mat[nfil][j]
        return mfil

    def columna(self, mat, ncol):
        if ncol > len(mat[0]):
            return None
        cfil = len(mat)
        mcol = np.zeros((cfil, 1))
        for i in range(cfil):
            mcol[i][0] = mat[i][ncol]
        return mcol

    def diagonal(self, mat, distanciaALaDiagonalPrincipal):
        cfil = len(mat)
        ccol = len(mat[0])
        dist = abs(distanciaALaDiagonalPrincipal)
        if (cfil != ccol) or (dist >= cfil):
            print(
                "Error: No se puede extraer la diagonal solicitada para la matriz informada")
            return None
        mdiag = np.zeros((1, cfil-dist))
        k = 0
        for i in range(cfil):
            for j in range(ccol):
                if (i+distanciaALaDiagonalPrincipal) == j:
                    mdiag[0][k] = mat[i][j]
                    k += 1
                    break
        return mdiag

    def diagonal_ppal(self, mat):
        return self.diagonal(mat, 0)

    def traza(self, mat):
        mdiag = self.diagonal_ppal(mat)
        if (mdiag is None):
            print("Error: No se puede obtener la traza de esta matriz.")
            return None
        suma = 0
        cfil = len(mat)
        for i in range(cfil):
            suma += mdiag[0][i]
        return suma

    def simetrica(self, mat):
        cfil = len(mat)
        ccol = len(mat[0])
        if (cfil != ccol):
            print(
                "Error: La matriz informada no es cuadrada, por estructura no es simetrica.")
            return False
        for i in range(1, cfil):
            mdiagS = self.diagonal(mat, i)
            mdiagI = self.diagonal(mat, -i)
            for j in range(cfil-i):
                if (mdiagS[0][j] != mdiagI[0][j]):
                    return False
        return True

    def rango(self, mat):
        maxRng = 0
        cfil = len(mat)
        ccol = len(mat[0])
        if (cfil != ccol):
            print("Por ahora solo se calculan rangos de matrices cuadradas.")
            return maxRng
        if self.determinante(mat) != 0.0:
            maxRng = cfil
        else:
            if (cfil > 1):
                valRng = 0
                i = 0
                while (i < cfil and maxRng != (cfil-1)):
                    j = 0
                    while (j < cfil and maxRng != (cfil-1)):
                        valRng = self.rango(self.submat(mat, i, j))
                        if (valRng != 0 and valRng > maxRng):
                            maxRng = valRng
                        j += 1
                    i += 1
        return maxRng

    def triangularSup(self, mat):
        cfil = len(mat)
        ccol = len(mat[0])
        if cfil != ccol:
            print("Solo se triangularizan matrices cuadradas.")
            return None
        # mtr= np.zeros((cfil,ccol))
        mtr = mat.copy()
        for j in range(cfil):
            for i in range(j, cfil):
                if (i == j and mtr[i][j] == 0.0):
                    # k = i+1
                    for k in range(i+1, cfil, 1):
                        if mtr[k][j] != 0.0:
                            break
                    # print(f"k2:{k}")  # Raro i+1=3 pero k=2
                    if k < cfil:
                        for m in range(cfil):
                            mtr[i][m] = mtr[i][m] + mtr[k][m]
                    else:
                        print("La matriz no es triangularizable")
                        return None
                if i == j:
                    for k in range(i+1, cfil):
                        if mtr[k][j] != 0.0:
                            piv = mtr[k][j]
                            for m in range(j, cfil):
                                mtr[k][m] = ((-piv/mtr[i][j]) *
                                             mtr[i][m]) + mtr[k][m]
        return mtr


# # Test de operaciones con matrices
# myMat = Matrix()
# M1 = [[8, 14, -6], [12, 7, 4], [-11, 3, 21]]
# M2 = [[8, 14, -7], [12, 6, 4], [9, 3, 2]]
# print("M1:")
# matrix_length1 = len(M1)
# for i1 in range(matrix_length1):
#     print(M1[i1])
# print("M2:")
# matrix_length2 = len(M2)
# for i2 in range(matrix_length2):
#     print(M2[i2])

# print(myMat.producto(M1, M2))

# A = np.array([[8, 14, -6], [12, 7, 4], [-11, 3, 21]])
# print("A:")
# print(A)
# B = np.array([[8, 14, -7], [12, 6, 4], [9, 3, 2]])
# print("B:")
# print(B)

# print("A*B:")
# print(myMat.producto(A, B))

# c = np.array([[1, 1, 1, 1, 1], [-1, 2, 0, 0, 0],
#              [0, 0, 3, 0, 0], [0, 0, 0, 4, 0], [0, 0, 0, 0, 5]])
# d = np.array([[1, 0, 0, 0, -1], [0, 2, 0, 0, 0], [
#              0, 0, 3, 0, 0], [0, 0, 0, 4, 0], [-1, 0, 0, 0, 5]])
# print("c:")
# print(c)
# print("d:")
# print(d)
# print("c*d:")
# print(myMat.producto(c, d))

# print("Determinante de c:")
# print(myMat.determinante(c))

# print("Inversa de c:")
# print(myMat.inversa(c))

# print("Potencia 10 de c:")
# print(myMat.potencia(c, 10))

# print("División c/c:")
# print(myMat.division(c, c))

# print("Suma c+d:")
# print(myMat.suma(c, d))

# print("Resta c-d:")
# print(myMat.resta(c, d))

# V1 = np.array([[1, 2, 3, 4, 5]])
# V2 = np.array([[2, 3, 4, 5, 6]])
# print(f"V1: {V1}")
# print(f"V2: {V2}")
# print(f"V2 transpuesta:\n {myMat.transpuesta(V2)}")
# print(f"Producto Escalar V1xV2: {myMat.prod_escalar(V1, V2)}")
# print(f"Fila 0 de A: {myMat.fila(A,0)}")
# print(f"Columna 1 de A:\n {myMat.columna(A,1)}")
# print(f"Diagonal principal de A: {myMat.diagonal_ppal(A)}")
# print(f"Diagonal 1 sobre principal de A: {myMat.diagonal(A,1)}")
# print(f"Diagonal 1 debajo de principal de A: {myMat.diagonal(A,-1)}")
# print(f"Diagonal 2 sobre principal de A: {myMat.diagonal(A,2)}")
# print(f"Diagonal 2 debajo de principal de A: {myMat.diagonal(A,-2)}")
# print(f"Traza de A: {myMat.traza(A)}")
# if (myMat.simetrica(A)):
#     print("Matriz A es simetrica")
# else:
#     print("Matriz A NO es simetrica")
# if (myMat.simetrica(d)):
#     print("Matriz d es simetrica")
# else:
#     print("Matriz d NO es simetrica")

# print(f"Rango de A: {myMat.rango(A)}")
# print(f"Rango de c: {myMat.rango(c)}")
# E = np.array([[1, 2, 0], [2, 1, 0], [2, 4, 0]])
# print(f"Rango de E: {myMat.rango(E)}")
# print(f"Matriz Triangular superior de c:\n {myMat.triangularSup(c)}")
# print(
#     f"Det.Mat.Triang.sup.de c:\n {myMat.determinante(myMat.triangularSup(c))}")
# print(f"Matriz Triangular superior de E:\n {myMat.triangularSup(E)}")
