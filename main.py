import pygame

pygame.init()

w_size = 720
h_size = 480

window = pygame.display.set_mode((w_size, h_size))

continuer = True

clock = pygame.time.Clock()

liste_rect = [[False, True, pygame.Rect]]

i = 0

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and not liste_rect[i][0]:
                liste_rect[i][2] = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
                liste_rect[i][0] = True
            elif pygame.mouse.get_pressed()[0] and liste_rect[i][0]:
                liste_rect[i][1] = False
                liste_rect.append([False, True, pygame.Rect])
                i += 1

            elif pygame.mouse.get_pressed()[2]:
                for j in range(i):
                    if not liste_rect[j][1] and liste_rect[j][2].collidepoint((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        print("test")
                        liste_rect.pop(j)
                        liste_rect.append([False, False, pygame.Rect])
                        i -= 1

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LCTRL] and i > 0 and pygame.key.get_pressed()[pygame.K_z]:
                liste_rect.pop(i)
                liste_rect[i-1] = [False, False, pygame.Rect]
                i -= 1

    window.fill("white")

    for j in range(i + 1):
        if liste_rect[j][0]:
            if liste_rect[j][1]:
                liste_rect[j][2].width = pygame.mouse.get_pos()[0] - liste_rect[j][2].x
                liste_rect[j][2].height = pygame.mouse.get_pos()[1] - liste_rect[j][2].y
            pygame.draw.rect(window, "green", liste_rect[j][2], 1)

    pygame.display.flip()
    clock.tick(60)
