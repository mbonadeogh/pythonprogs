import sys
import pygame
from pygame.locals import *
import matrix as mt
import forma as frm
import perspectiva as prsp

# total arguments
na = len(sys.argv)
print(f"Numero de argumentos={na}")
if (na > 2 or (na == 2 and not (sys.argv[1] == "1" or sys.argv[1] == "2" or sys.argv[1] == "3"))):
    print(f"Valor de argumento 1={sys.argv[1]}")
    print("Uso: python.exe prueba.py [1|2|3]")
    print("Donde:\n      1-<Elipsoide>\n      2-<Toro>\n      3-<Esfera>]")
    sys.exit()
elif na == 1:
    opt = 1
else:
    opt = int(sys.argv[1])

pygame.init()
# Set up the window.
windowSurface = pygame.display.set_mode((1300, 650), 0, 32)

# Set up the colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PVO = frm.PointR3(60.0, 34.641, 40.0)
pers = prsp.Perspectiva().fabricaPerspectiva(PVO, 1500)

# Draw the white background onto the surface.
windowSurface.fill(WHITE)

# Draw the window onto the screen.
pygame.display.update()

if opt == 1:
    myForma = frm.Elipsoide(frm.PointR3(0.0, 0.0, 0.0),
                            8.0, 17.0, 8.0, 17, 28, 0)
elif opt == 2:
    myForma = frm.Toro(frm.PointR3(0.0, 0.0, 0.0), 10.0, 4.5, 14, 26, None)
elif opt == 3:
    myForma = frm.Esfera(frm.PointR3(0.0, 0.0, 0.0), 10.0, 14, 26, None)

for s in range(1080):
    sup_visible = []
    for t in range(myForma.size()):
        currTriang = myForma.getElem(t)
        if currTriang.esVisible(PVO):
            sup_visible.append(currTriang)
    if opt == 2:  # Toro - por su forma se ordena por triangulos visibles mas lejanos a mas cercanos al PVO antes de presentar
        sup_visible.sort(
            key=lambda Triangulo: Triangulo.get_last_dist_pvo(), reverse=True)
    for currTriang in sup_visible:
        p1 = pers.projectedPoint(currTriang.getPoint(1))
        p2 = pers.projectedPoint(currTriang.getPoint(2))
        p3 = pers.projectedPoint(currTriang.getPoint(3))
        pygame.draw.polygon(windowSurface, currTriang.get_fill_color(), [
                            (p1.getX(), p1.getY()), (p2.getX(), p2.getY()), (p3.getX(), p3.getY())], width=0)
        pygame.draw.line(windowSurface, BLACK, (p1.getX(), p1.getY()),
                         (p2.getX(), p2.getY()), width=1)
        pygame.draw.line(windowSurface, BLACK, (p2.getX(), p2.getY()),
                         (p3.getX(), p3.getY()), width=1)
        pygame.draw.line(windowSurface, BLACK, (p3.getX(), p3.getY()),
                         (p1.getX(), p1.getY()), width=1)
    # print(s)
    # Draw the window onto the screen.
    pygame.display.update()
    pygame.time.delay(100)
    rotEje = prsp.Perspectiva().rotEjeX1
    if s > 359 and s < 720:
        rotEje = prsp.Perspectiva().rotEjeX2
    elif s > 719:
        rotEje = prsp.Perspectiva().rotEjeX3

    # Rotate the "Forma"
    for r in range(myForma.size()):
        currTriang = myForma.getElem(r)
        VC = mt.Matrix().producto(mt.Matrix().potencia(rotEje, 1), currTriang.getHArr())
        myForma.setElem(r, currTriang.from_Array(
            VC, currTriang.get_fill_color()))
    windowSurface.fill(WHITE)

pygame.quit()
sys.exit()
