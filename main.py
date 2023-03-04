import pygame

pygame.init()


class LevelEditor:
    def __init__(self, size_w, size_h):
        self.size_h = size_h
        self.size_w = size_w
        self.liste_rect = [
            [False, True, pygame.Rect]]  # liste_rect : [[doit_etre_affiché, peut_etre_deplacé, pygame.Rect]]
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.size_w, self.size_h))

    def affichage(self):
        self.window.fill("white")

        for i in range(len(self.liste_rect)):  # on parcours la liste des rectangles
            if self.liste_rect[i][0]:  # si il doit être affiché :
                if self.liste_rect[i][1]:  # si il est en cours de déplacement :
                    self.liste_rect[i][2].width = pygame.mouse.get_pos()[0] - self.liste_rect[i][
                        2].x  # on change la taille du rectangle par rapport à la position de la souris
                    self.liste_rect[i][2].height = pygame.mouse.get_pos()[1] - self.liste_rect[i][2].y  # idem

                pygame.draw.rect(self.window, "green", self.liste_rect[i][2],
                                 1)  # on affiche en vers le rectangle avec une bordure fine

        pygame.display.flip()  # on update l'écran

    def dessin_rect(self):
        if not self.liste_rect[-1][0]:  # si le rectangle actuel n'était pas encore affiché :
            self.liste_rect[-1][2] = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1,
                                                 1)  # on fait un minuscule carré au niveau de la souris
            self.liste_rect[-1][0] = True
        else:  # sinon si on est en train de l'afficher et que l'on clique à nouveau :
            self.liste_rect[-1][1] = False  # on stop le déplacement du rectangle

            if self.liste_rect[-1][2].width < 0:  # si le triangle à un largeur négative :
                self.liste_rect[-1][2].width = abs(self.liste_rect[-1][2].width)  # on la transforme en largeur positive
                self.liste_rect[-1][2].x -= self.liste_rect[-1][
                    2].width  # on le déplace de la taille de la largeur pour qu'il soit placé correctement
            if self.liste_rect[-1][2].height < 0: # idem pour la hauteur
                self.liste_rect[-1][2].height = abs(self.liste_rect[-1][2].height)
                self.liste_rect[-1][2].y -= self.liste_rect[-1][2].height

            self.liste_rect.append(
                [False, True, pygame.Rect])  # on créé un noveau rectangle que l'on n'affiche pas encore

    def ctrl_z(self):
        if len(self.liste_rect) > 1:  # si on a un rectangle complet affiché (pour éviter des erreurs) :
            self.liste_rect.pop(
                -2)  # on supprime le dernier rectangle affiché (le dernier élément de la liste ressemble à ça [False, True, pygame.Rect] :

    def del_rect(self):
        for rectangle in self.liste_rect:
            if rectangle[0]:  # si le rectangle est affiché :
                if rectangle[2].collidepoint(
                        (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):  # si la souris est dans un rectangle :
                    self.liste_rect.remove(rectangle)  # on enlève le rectangle
                    # ça ne supprime pas quand le rectangle à une largeur/hauteur négative

    def main(self):
        continuer = True
        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:  # si on fait un clic gauche
                        self.dessin_rect()

                    elif pygame.mouse.get_pressed()[2]:  # si on a un clic droit:
                        self.del_rect()

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_z]:
                        self.ctrl_z()

            self.affichage()

            self.clock.tick(60)


test = LevelEditor(720, 480)
test.main()
