

import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Start!")

cWIDTH = 135
cHEIGHT = 120

BACKGROUND = (230, 230, 250)
WHITE = (255, 255, 255)
DUB_COLOR = (255, 165, 0)

BORDER = pygame.Rect(0, HEIGHT//2, WIDTH, 10)



HP = pygame.font.SysFont('inkfree', 50)
DUB_SCREEN = pygame.font.SysFont('lucidasans', 100)



pb_tracer = (220, 20, 60)
mb_tracer = (70, 130, 180)


fps = 60
speed = 7
fire_rate = 10
ammo = 10

red_damage = pygame.USEREVENT + 1
blue_damage = pygame.USEREVENT + 2

mega = pygame.image.load(
    os.path.join('cheena_slayer69', 'mm.png'))
megasize = pygame.transform.scale(mega,(cWIDTH, cHEIGHT))


proto = pygame.image.load(
    os.path.join('cheena_slayer69', 'protoman1.png'))
protosize = pygame.transform.scale(proto,(cWIDTH, cHEIGHT))



def draw_window(blue, red, megabullets, protobullets, mega_health, proto_health):
    WIN.fill((BACKGROUND))
    pygame.draw.rect(WIN, WHITE, BORDER)

    proto_HP = HP.render("HP: " + str(proto_health), 1, pb_tracer)
    mega_HP = HP.render("HP: " + str(mega_health), 1, mb_tracer)
    WIN.blit(proto_HP, (WIDTH - proto_HP.get_width()- 10, 10))
    WIN.blit(mega_HP, (10, 10))


    WIN.blit(megasize,(blue.x , blue.y))
    WIN.blit(protosize,(red.x, red.y))

    for bullet in megabullets:
        pygame.draw.rect(WIN, mb_tracer, bullet)
    
    for bullet in protobullets:
        pygame.draw.rect(WIN, pb_tracer, bullet)


    pygame.display.update()



def control_protoman(pressed_keys, red):
    if pressed_keys[pygame.K_LEFT] and red.x - speed > 0:
        red.x -= speed
    if pressed_keys[pygame.K_RIGHT] and red.x + speed + red.height < 1000:
        red.x += speed
    if pressed_keys[pygame.K_UP] and red.y - speed > BORDER.y :
        red.y -= speed
    if pressed_keys[pygame.K_DOWN] and red.y + speed + red.width < HEIGHT:
        red.y += speed


def control_megaman(pressed_keys, blue):
    if pressed_keys[pygame.K_s] and blue.x - speed > 0 : 
        blue.x -= speed
    if pressed_keys[pygame.K_f] and blue.x + speed + blue.height < 1000 :
        blue.x += speed
    if pressed_keys[pygame.K_e] and blue.y - speed > 0:
        blue.y -= speed
    if pressed_keys[pygame.K_d]and blue.y + speed  < 233:
        blue.y += speed 

def shoot(protobullets, megabullets, red, blue):
    for bullet in protobullets:
        bullet.y -= fire_rate
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_damage))
            protobullets.remove(bullet)

    for bullet in megabullets:
        bullet.y += fire_rate
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_damage))
            megabullets.remove(bullet)
            
def draw_DUB(text):
    draw_text = DUB_SCREEN.render(text, 1, DUB_COLOR)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(425, 50, cWIDTH, cHEIGHT)
    red = pygame.Rect(425, 550, cWIDTH, cHEIGHT)

    protobullets = []
    megabullets = []

    proto_health = 10
    mega_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(protobullets) < ammo:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    protobullets.append(bullet)
                    


                if event.key == pygame.K_LCTRL and len(megabullets) < ammo:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height//2 - 2, 10, 5)
                    megabullets.append(bullet)
                    
            
            if event.type == red_damage:
                proto_health = proto_health - 1
                

            if event.type == blue_damage:
                mega_health = mega_health - 1
                
        
        dub = ""
        if proto_health <= 0:
            dub = "MEGAMAN WINS!"
        
        if mega_health <= 0:
            dub = "PROTOMAN WINS!"
            
        if dub != "":
            draw_DUB(dub)
            break


        
        pressed_keys = pygame.key.get_pressed()
        control_megaman(pressed_keys, blue)
        control_protoman(pressed_keys, red)

        shoot(protobullets, megabullets, red, blue)

        draw_window(blue, red, megabullets, protobullets, mega_health, proto_health)

    main()

if __name__ == "__main__":
    main()
