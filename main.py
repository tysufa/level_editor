import pygame

pygame.init()


class LevelEditor:
    def __init__(self, size_w, size_h, background=""):
        self.size_h = size_h
        self.size_w = size_w
        self.liste_rect_detaille = [
            [False, True, pygame.Rect]]  # liste_rect : [[doit_etre_affiché, peut_etre_deplacé, pygame.Rect]]
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.size_w, self.size_h))
        self.hitbox_player = pygame.Rect((100, 100), (10, 40))
        self.gravity = False
        self.y_velocity = 0
        if background != "": # on traite le cas ou on ne veut pas d'image en fond
            self.background_img = pygame.image.load(background)
            self.is_background = True
        else:
            self.is_background = False

        self.pos_background = [0, 0]
        self.velocity = 4

    def level_save(self):
        with open("saves/level1", "w+") as file:
            for rect in self.liste_rect_detaille:
                for el in rect:
                    file.write(str(el) + "\n") # on ajoute individuellement chaque élément de la liste des rectangles dans le fichier
            file.write(str(self.hitbox_player) + "\n")
            if self.is_background:
                file.write(str(self.pos_background))

    def load_level(self):
        liste_rect_str = []
        bool_liste_rect = True
        with open("saves/level1", "r") as file:
            infos = file.readlines()
            for i in range(len(infos)): # on parcours chaque donnée une par une :
                if bool_liste_rect: # si on est en train de regarder les infos de la liste de rectangles :
                    if i % 3 == 0: # permet de savoir s'il faut passer au rectangle suivant
                        liste_rect_str.append([]) # on ajoute une liste vide pour le prochain rectangle
                    liste_rect_str[-1].append(infos[i]) # on ajoute l'info actuelle au dernier rectangle de la liste

                if infos[i] == "<class 'pygame.Rect'>\n": # si on arrive à cet élément, on est à la fin de la liste de rectangle
                    bool_liste_rect = False

        for liste in liste_rect_str: # on remplace les "True" et "False" par des vrais booléens
            for i in range(len(liste)):
                if "True" in liste[i]:
                    liste[i] = True
                elif "False" in liste[i]:
                    liste[i] = False
                elif liste[i] == "<class 'pygame.Rect'>\n": # on transforme le string en rectangle non déclaré
                    liste[i] = pygame.Rect
                else:
                    str_coo = "" # on stock une chaine de caractère contenant uniquement les coordonées
                    bool_coo = False # un booléen pour savoir si l'on est en train de rentrer des coordonnées
                    for ch in liste[i]:
                        if ch == ")": # on teste si on sort des coordonnées
                            bool_coo = False
                        if bool_coo: # si on est dedans on peut ajouter le caractère actuel
                            str_coo += ch
                        if ch == "(": # on teste si on entre dans les coordonnées
                            bool_coo = True

                    liste[i] = str_coo.split(", ") # on créer une liste qui ne contient que la position et la taille du rectangle sous forme de strings
                    liste[i] = pygame.Rect(int(liste[i][0]), int(liste[i][1]), int(liste[i][2]), int(liste[i][3])) # puis on créer un vrai rectangle à partir des infos extraites

        self.liste_rect_detaille = liste_rect_str # on transforme la liste actuelle de rectangles en la liste que l'on a chargé

    def player_collision(self):
        if len(self.liste_rect_detaille) > 1:
            liste_rect = [el[2] for el in
                          self.liste_rect_detaille]  # on fait une liste de rectangle pour la méthode collidelist
            liste_rect.pop(-1)  # on enlève le dernier qui n'existe pas encore réellement
            if self.hitbox_player.collidelist(liste_rect) != -1:  # si on détecte une collision :
                return True
        else:
            return False

    def apply_gravity(self):
        if self.gravity:
            self.y_velocity += 1
            self.hitbox_player.y += self.y_velocity
        else:
            self.y_velocity = 0

    def affichage_player_hitbox(self):
        pygame.draw.rect(self.window, "red", self.hitbox_player, 1)

    def affichage(self):
        self.window.fill("black")
        if self.is_background:
            self.window.blit(self.background_img, self.pos_background)

        for i in range(len(self.liste_rect_detaille)):  # on parcours la liste des rectangles
            if self.liste_rect_detaille[i][0]:  # si il doit être affiché :
                if self.liste_rect_detaille[i][1]:  # si il est en cours de déplacement :
                    self.liste_rect_detaille[i][2].width = pygame.mouse.get_pos()[0] - self.liste_rect_detaille[i][
                        2].x  # on change la taille du rectangle par rapport à la position de la souris
                    self.liste_rect_detaille[i][2].height = pygame.mouse.get_pos()[1] - self.liste_rect_detaille[i][
                        2].y  # idem

                pygame.draw.rect(self.window, "green", self.liste_rect_detaille[i][2],
                                 1)  # on affiche en vers le rectangle avec une bordure fine
        self.affichage_player_hitbox()

        pygame.display.flip()  # on update l'écran

    def dessin_rect(self):
        if not self.liste_rect_detaille[-1][0]:  # si le rectangle actuel n'était pas encore affiché :
            self.liste_rect_detaille[-1][2] = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1,
                                                          1)  # on fait un minuscule carré au niveau de la souris
            self.liste_rect_detaille[-1][0] = True
        else:  # sinon si on est en train de l'afficher et que l'on clique à nouveau :
            self.liste_rect_detaille[-1][1] = False  # on stop le déplacement du rectangle

            if self.liste_rect_detaille[-1][2].width < 0:  # si le triangle à un largeur négative :
                self.liste_rect_detaille[-1][2].width = abs(
                    self.liste_rect_detaille[-1][2].width)  # on la transforme en largeur positive
                self.liste_rect_detaille[-1][2].x -= self.liste_rect_detaille[-1][
                    2].width  # on le déplace de la taille de la largeur pour qu'il soit placé correctement
            if self.liste_rect_detaille[-1][2].height < 0:  # idem pour la hauteur
                self.liste_rect_detaille[-1][2].height = abs(self.liste_rect_detaille[-1][2].height)
                self.liste_rect_detaille[-1][2].y -= self.liste_rect_detaille[-1][2].height

            self.liste_rect_detaille.append(
                [False, True, pygame.Rect])  # on créé un noveau rectangle que l'on n'affiche pas encore

    def ctrl_z(self):
        if len(self.liste_rect_detaille) > 1:  # si on a un rectangle complet affiché (pour éviter des erreurs) :
            self.liste_rect_detaille.pop(
                -2)  # on supprime le dernier rectangle affiché (le dernier élément de la liste ressemble à ça [False, True, pygame.Rect] :

    def del_rect(self):
        for rectangle in self.liste_rect_detaille:
            if rectangle[0]:  # si le rectangle est affiché :
                if rectangle[2].collidepoint(
                        (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):  # si la souris est dans un rectangle :
                    self.liste_rect_detaille.remove(rectangle)  # on enlève le rectangle
                    # ça ne supprime pas quand le rectangle à une largeur/hauteur négative

    def deplacement_niveau(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:  # si on appuie sur la touche droite :
            self.pos_background[0] -= self.velocity  # on déplace l'image de l'arrière plan vers la gauche
            self.hitbox_player.x -= self.velocity # on déplace la hitbox du joueur pour qu'elle donne l'impression d'être immobile
            for rect in self.liste_rect_detaille:
                if rect[0]: # si le rectangle est fixé :
                    rect[2].x -= self.velocity # idem que pour hitbox player
        if keys[pygame.K_LEFT]:
            self.pos_background[0] += self.velocity
            self.hitbox_player.x += self.velocity
            for rect in self.liste_rect_detaille:
                if rect[0]:
                    rect[2].x += self.velocity
        if keys[pygame.K_DOWN]:
            self.pos_background[1] -= self.velocity
            self.hitbox_player.y -= self.velocity
            for rect in self.liste_rect_detaille:
                if rect[0]:
                    rect[2].y -= self.velocity
        if keys[pygame.K_UP]:
            self.pos_background[1] += self.velocity
            self.hitbox_player.y += self.velocity
            for rect in self.liste_rect_detaille:
                if rect[0]:
                    rect[2].y += self.velocity

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
                    if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_s]:
                        self.level_save()
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        self.gravity = not self.gravity
                    if pygame.key.get_pressed()[pygame.K_o]: #touche pour charger un niveau
                        self.load_level()

            self.deplacement_niveau()

            if not self.player_collision():
                self.apply_gravity()

            self.affichage()

            self.clock.tick(60)


test = LevelEditor(1080, 720, "images/hk.png")
test.main()
