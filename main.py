#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/tres-en-raya
import random
import time

import pygame as pg
from pygame import sprite


class Casilla(sprite.Sprite):
    def __init__(self, x, y, pos):
        super(Casilla, self).__init__()
        self.image = pg.image.load("images/vacia.png")
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = x + 142
        self.rect.y = y + 68
        self.estado = False

    def cambiar_estado(self, turno):
        self.estado = True
        self.cambiar_imagen(turno)

    def cambiar_imagen(self, turno):
        if turno == "bill":
            self.image = pg.image.load("images/equis.png")
        elif turno == "steve":
            self.image = pg.image.load("images/circulo.png")

    def limpiar(self):
        self.image = pg.image.load('images/vacia.png')
        self.estado = False


class JugadorBill(sprite.Sprite):
    def __init__(self):
        super(JugadorBill, self).__init__()
        self.image = pg.image.load("images/bill.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 75


class JugadorSteve(sprite.Sprite):
    def __init__(self):
        super(JugadorSteve, self).__init__()
        self.image = pg.image.load("images/steve.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 360
        self.rect.y = 75


class EscenaJuego(object):
    def __init__(self):
        self.turno = "bill"
        self.hay_ganador = False
        self.turnos = 9
        self.fondo = pg.image.load("images/escenario.jpg")

        #self.jugadores = pg.sprite.Group()
        #self.jugadores.add(JugadorBill())
        #self.jugadores.add(JugadorSteve())

        self.tablero = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

        self.fila_bill = ["bill", "bill", "bill"]
        self.fila_steve = ["steve", "steve", "steve"]

        self.crear_casillas_vacias()

    def actualizar(self):
        if self.hay_ganador:
            self.reiniciar()

        if self.turno == "steve" and not self.hay_ganador:
            self.clic_autonomo()
        elif self.turno == "bill" and not self.hay_ganador:
            self.clic_autonomo()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def clic_autonomo(self):
        time.sleep(.3)
        event = random.randint(142, 358), random.randint(68, 284)
        self.verificar_colision_mouse_con_casillas(event)

    def verificar_colision_mouse_con_casillas(self, pos_mouse):
        for casilla in self.casillas.sprites():
            if casilla.rect.collidepoint(pos_mouse[0], pos_mouse[1]):
                self.presionando_casilla_con_mouse(casilla)

    def presionando_casilla_con_mouse(self, casilla):
        if not casilla.estado:
            casilla.cambiar_estado(self.turno)
            self.cambiar_turno(casilla)
            self.verificar_ganador()
            self.verificar_empate()

    def verificar_ganador(self):
        self.verificar_ganador_en_horizontal()
        self.verificar_ganador_en_vertical()
        self.verificar_ganador_en_diagonal()

    def verificar_empate(self):
        if not self.hay_ganador and self.turnos < 1:
            self.hay_ganador = True
            print "Empate"

    def verificar_ganador_en_horizontal(self):
        if self.fila_bill in self.tablero:
            print "Ganó Bill en horizontal"
            self.hay_ganador = True
        elif self.fila_steve in self.tablero:
            print "Ganó Steve en horizontal"
            self.hay_ganador = True

    def verificar_ganador_en_vertical(self):
        cols = [list(col) for col in zip(*self.tablero)]
        if self.fila_bill in cols:
            print "Ganó Bill en vertical"
            self.hay_ganador = True
        elif self.fila_steve in cols:
            print "Ganó Steve en vertical"
            self.hay_ganador = True

    def verificar_ganador_en_diagonal(self):
        diagonal1 = [self.tablero[0][0],
                     self.tablero[1][1],
                     self.tablero[2][2]]

        diagonal2 = [self.tablero[0][2],
                     self.tablero[1][1],
                     self.tablero[2][0]]

        if diagonal1 == self.fila_bill or diagonal2 == self.fila_bill:
            print "Ganó Bill en diagonal"
            self.hay_ganador = True
        elif diagonal1 == self.fila_steve or diagonal2 == self.fila_steve:
            print "Ganó Steve en diagonal"
            self.hay_ganador = True

    def cambiar_turno(self, casilla):
        self.tablero[casilla.pos[0]][casilla.pos[1]] = self.turno
        self.turnos -= 1
        self.turno = 'steve' if self.turno == "bill" else 'bill'

    def crear_casillas_vacias(self):
        self.casillas = pg.sprite.Group()
        for fila, _ in enumerate(self.tablero):
            for columna, _ in enumerate(self.tablero[fila]):
                self.casillas.add(Casilla(72*columna, 72*fila, (fila, columna)))

    def reiniciar(self):
        time.sleep(1.5)

        for casilla in self.casillas.sprites():
            casilla.limpiar()

        self.hay_ganador = False
        self.turnos = 9
        self.tablero = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        self.casillas.draw(pantalla)
        #self.jugadores.draw(pantalla)
        pg.display.update()


def main():
    pg.init()
    pantalla = pg.display.set_mode((500, 320))
    pg.display.set_caption("Tres en Raya")
    reloj = pg.time.Clock()

    escena = EscenaJuego()

    while True:
        escena.actualizar()
        escena.dibujar(pantalla)
        reloj.tick(20)

if __name__ == '__main__':
    main()