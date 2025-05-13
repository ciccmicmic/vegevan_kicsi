import pygame
import os
import random

pygame.init()
pygame.mixer.init()  # Hangmixer inicializálása

# Hangfájlok betöltése
try:
    jump_sound = pygame.mixer.Sound("Assets/Sounds/jump.wav")
    duck_sound = pygame.mixer.Sound("Assets/Sounds/duck.wav")  # Ha a Viktor lefelé nyomja
    collision_sound = pygame.mixer.Sound("Assets/Sounds/collision.wav")
    coin_sound = pygame.mixer.Sound("Assets/Sounds/coin.wav")
    game_over_sound = pygame.mixer.Sound("Assets/Sounds/game_over.wav")
    pygame.mixer.music.load("Assets/Sounds/background_music.mp3")
    pygame.mixer.music.play(-1)  # Háttérzene folyamatos lejátszása (-1 loop)
except pygame.error as e:
    print(f"Hiba a hangfájlok betöltésekor: {e}")
    raise SystemExit(f"Hiányzó hangfájlok. Ellenőrizd az 'Assets/Sounds' könyvtárat.")
except FileNotFoundError as e:
    print(f"Hiba a hangfájl megnyitásakor: {e}")
    raise SystemExit(f"Hiányzó hangfájl. Ellenőrizd az 'Assets/Sounds' könyvtárat.")

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vége van kicsi")  # Ablak címsorának beállítása

RUNNING = []
JUMPING = None
DUCKING = []
SMALL_AVOCADO = []
LARGE_AVOCADO = []
HELI = []
CLOUD = None
BACKGROUND = None
BG = None
LANDING_PAGE = None # Új változó a kezdőoldal hátterének

try:
    RUNNING = [
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorRun1.png")),
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorRun2.png")),
    ]
    JUMPING = pygame.image.load(os.path.join("Assets/Viktor", "ViktorJump.png"))
    DUCKING = [
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorDuck1.png")),
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorDuck2.png")),
    ]
    SMALL_AVOCADO = [
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado1.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado2.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado3.png")),
    ]
    LARGE_AVOCADO = [
        pygame.image.load(os.path.join("Assets/Avocado", "LargeAvocado1.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "LargeAvocado2.png")),
    ]
    HELI = [
        pygame.image.load(os.path.join("Assets/Heli", "Heli1.png")),
        pygame.image.load(os.path.join("Assets/Heli", "Heli2.png")),
    ]
    CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
    BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "background.png"))  # Új háttér betöltése
    BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
    LANDING_PAGE = pygame.image.load(os.path.join("Assets/Other", "landingpage.png")) # Kezdőoldal hátterének betöltése
except pygame.error as e:
    print(f"Hiba a képek betöltésekor: {e}")
    raise SystemExit(f"Hiányzó képfájlok. Ellenőrizd az 'Assets' könyvtárat.")
except FileNotFoundError as e:
    print(f"Hiba a képfájl megnyitásakor: {e}")
    raise SystemExit(f"Hiányzó képfájl. Ellenőrizd az 'Assets' könyvtárat.")


class Viktosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    GROUND_LEVEL = 380  # Új: a talaj szintje

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.Viktor_duck = False
        self.Viktor_run = True
        self.Viktor_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.Viktor_rect = self.image.get_rect()
        self.Viktor_rect.x = self.X_POS
        self.Viktor_rect.y = self.Y_POS
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Maszk létrehozása a pontosabb ütközéshez

    def update(self, userInput):
        if self.Viktor_duck:
            self.duck()
        if self.Viktor_run:
            self.run()
        if self.Viktor_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.Viktor_jump:
            self.Viktor_duck = False
            self.Viktor_run = False
            self.Viktor_jump = True
            jump_sound.play()  # Ugrás hang lejátszása
        elif userInput[pygame.K_DOWN] and not self.Viktor_jump:
            self.Viktor_duck = True
            self.Viktor_run = False
            self.Viktor_jump = False
            duck_sound.play()  # Duck hang lejátszása
        elif not (self.Viktor_jump or userInput[pygame.K_DOWN]):
            self.Viktor_duck = False
            self.Viktor_run = True
            self.Viktor_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.Viktor_rect = self.image.get_rect()
        self.Viktor_rect.x = self.X_POS
        self.Viktor_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Maszk frissítése

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.Viktor_rect = self.image.get_rect()
        self.Viktor_rect.x = self.X_POS
        self.Viktor_rect.y = self.Y_POS
        self.step_index += 1
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Maszk frissítése

    def jump(self):
        self.image = self.jump_img
        if self.Viktor_jump:
            self.Viktor_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            # Korlátozzuk a ugrást a talajszinthez képest
            if (
                self.Viktor_rect.y >= self.GROUND_LEVEL - self.image.get_height()
            ):
                self.Viktor_rect.y = (
                    self.GROUND_LEVEL - self.image.get_height()
                )
                self.Viktor_jump = False
                self.jump_vel = self.JUMP_VEL
        elif not self.Viktor_jump:
            self.Viktor_rect.y = self.GROUND_LEVEL - self.image.get_height()
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Maszk frissítése

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.Viktor_rect.x, self.Viktor_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(100, 150)
        self.image = CLOUD
        self.width = self.image.get_width()
        self.collided = False  # Jelzi, hogy ütközött-e már a felhővel
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Maszk létrehozása
        self.visible = True # <<< ADDED: To control visibility

    def update(self, game_speed):  # Hozzáadtuk a game_speed paramétert
        if self.visible: # Only update if visible or to make it reappear
            self.x -= game_speed * 0.5  # Felhők fele olyan gyorsan mozognak
        
        if self.x < -self.width and not self.visible: # Logic for reappearing if it was collected
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
            self.collided = False  # Reseteljük az ütközés jelzőt
            self.visible = True # <<< ADDED: Make it visible again
        elif self.x < -self.width and self.visible: # Logic for reappearing if it just went off screen
             self.x = SCREEN_WIDTH + random.randint(2500, 3000)
             self.y = random.randint(50, 100)
             self.collided = False # Reset collision state


        # Update the rect's position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, SCREEN):
        if self.visible: # <<< ADDED: Only draw if visible
            SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 370
        self.mask = pygame.mask.from_surface(
            self.image[self.type]
        )  # Maszk létrehozása

    def update(self, game_speed):  # Hozzáadtuk a game_speed paramétert
        self.rect.x -= game_speed  # Akadályok sebessége változatlan marad
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)  # Javítva: az első elemet távolítjuk el

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallAvocado(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)  # changed
        super().__init__(image, self.type)


class LargeAvocado(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)  # changed
        super().__init__(image, self.type)


class Heli(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

    def update(self, game_speed):  # Hozzáadtuk a game_speed paramétert
        self.rect.x -= game_speed  # Akadályok sebessége változatlan marad
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)  # Javítva: az első elemet távolítjuk el



def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, cloud, x_pos_bg_background, player_name
    run = True
    clock = pygame.time.Clock()
    player = Viktosaur()
    cloud = Cloud()  # A Cloud objektum létrehozása változatlan marad
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    x_pos_bg_background = 0  # Háttér x pozíciója
    points = 0 # Pontszám inicializálása
    # Font betöltése
    font = pygame.font.Font("PressStart2P-Regular.ttf", 16)  # Kisebb betűméret
    obstacles = []
    death_count = 0
    game_over = False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Pontok: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (900, 40)  # Beljebb helyezve a vízszintes pozíciót
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg, x_pos_bg_background
        image_width_bg = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_pos_bg_background, 0))  # Háttér rajzolása
        SCREEN.blit(BACKGROUND, (image_width_bg + x_pos_bg_background, 0))
        if x_pos_bg_background <= -image_width_bg:
            SCREEN.blit(BACKGROUND, (image_width_bg + x_pos_bg_background, 0))
            x_pos_bg_background = 0
        x_pos_bg_background -= game_speed * 0.25  # Háttér fele olyan gyorsan mozog
        # Háttér sebességének csökkentése: eredetileg game_speed * 0.5 volt

        # image_width_track = BG.get_width()
        # SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        # SCREEN.blit(BG, (image_width_track + x_pos_bg, y_pos_bg))
        # if x_pos_bg <= -image_width_track:
        #     SCREEN.blit(BG, (image_width_track + x_pos_bg, y_pos_bg))
        #     x_pos_bg = 0
        # x_pos_bg -= game_speed  # Akadályok sebessége nem változik

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))

        background()  # Először a háttér rajzolása

        cloud.draw(SCREEN)
        cloud.update(game_speed)  # Felhők sebessége már a Cloud osztályban van kezelve

        player.draw(SCREEN)
        userInput = pygame.key.get_pressed()  # Itt kérdezzük le a billentyűzet állapotát
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallAvocado(SMALL_AVOCADO))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeAvocado(LARGE_AVOCADO))
            elif random.randint(0, 2) == 2:
                obstacles.append(Heli(HELI))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed)  # Akadályok sebessége nem változik

            # Pontosabb ütközésvizsgálat maszkokkal
            offset_x = obstacle.rect.x - player.Viktor_rect.x
            offset_y = obstacle.rect.y - player.Viktor_rect.y
            
            if player.mask.overlap(obstacle.mask, (offset_x, offset_y)):
                collision_sound.play()
                pygame.mixer.music.stop()
                game_over_sound.play()
                pygame.time.delay(2000)
                death_count += 1
                game_over = True  # Állítsuk a game_over változót True-ra
                menu(death_count, points) # Pass the points to the menu function
                return  # Fontos a visszatérés a main ciklusból


        # Pontosabb ütközésvizsgálat maszkokkal
        offset_x = cloud.rect.x - player.Viktor_rect.x
        offset_y = cloud.rect.y - player.Viktor_rect.y
        # Check for collision AND if the cloud is currently visible
        if cloud.visible and player.mask.overlap(cloud.mask, (offset_x, offset_y)): # <<< MODIFIED: Added cloud.visible check
            coin_sound.play()
            points += 100
            # cloud.pop(0) # <<< REMOVED/COMMENTED OUT: cloud is not a list, make it invisible instead
            cloud.visible = False # <<< ADDED: Make the cloud invisible
            # To make the cloud "disappear" and eventually reappear, we'll reset its position
            # immediately or let the update logic handle its reappearance when it goes off-screen.
            # For an immediate "new" coin, you could reset its position here:
            # cloud.x = SCREEN_WIDTH + random.randint(800, 1000)
            # cloud.y = random.randint(100, 150)
            # cloud.visible = True # if you want it to reappear immediately in a new spot
            # However, the current update logic will make it reappear once its original
            # off-screen condition is met.


        score()

        clock.tick(30)
        pygame.display.update()



def menu(death_count, points=0): # Add points as a parameter with a default value of 0
    global game_speed, obstacles, player_name, LANDING_PAGE
    run_menu = True
    pygame.mixer.music.load("Assets/Sounds/background_music.mp3")  # Zene betöltése csak egyszer
    pygame.mixer.music.play(-1)  # Zene indítása csak egyszer
    game_over_sound.stop()  # Game over hang leállítása csak egyszer
    font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 40)
    color_inactive = pygame.Color("lightskyblue")
    color_active = pygame.Color("dodgerblue")
    color = color_inactive
    active = False
    player_name = ""
    high_scores = load_high_scores()  # Betöltjük a high score listát

    while run_menu:
        # SCREEN.fill((255, 255, 255)) # Ezt a sort töröljük, hogy a háttér látszódjon
        SCREEN.blit(LANDING_PAGE, (0, 0)) # Kirajzoljuk a kezdőoldal hátterét
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos): # Changed collidePoint to collidepoint
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if player_name:
                            high_scores.append((player_name, points))
                            save_high_scores(high_scores)  # Mentjük a high score listát
                            points = 0  # Pontszám nullázása újraindításkor
                            game_speed = 20  # Sebesség visszaállítása
                            obstacles = []  # Akadályok törlése
                            # Hívjuk meg a main függvényt a megfelelő változókkal
                            player = Viktosaur() # Új Viktor példány
                            cloud = Cloud()
                            # Itt inicializáljuk újra a játék állapotát
                            game_over = False
                            death_count = 0
                            main()
                            return  # Exit the menu function
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        text = font.render("Írd be a neved:", True, (0, 0, 0)) # Keep "Írd be a neved"

        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        SCREEN.blit(text, text_rect)

        # Szövegdoboz rajzolása
        pygame.draw.rect(SCREEN, color, input_box, 2)
        text_surface = font.render(player_name, True, (0, 0, 0))
        SCREEN.blit(
            text_surface, (input_box.x + 5, input_box.y + 5)
        )  # Szöveg megjelenítése a dobozban

        # High Score lista megjelenítése
        high_score_text = font.render("Legjobb Eredmények", True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 150, # Lejjebb hozzuk a legjobb eredményeket
        )  # Középre igazítva
        SCREEN.blit(high_score_text, high_score_rect)

        # Top 5 high score megjelenítése
        sorted_high_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)[:5]
        for i, (name, score) in enumerate(sorted_high_scores):
            score_display = font.render(
                f"{i + 1}. {name}: {score}", True, (0, 0, 0)
            )
            score_rect = score_display.get_rect()
            score_rect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 190 + i * 30, # Még lejjebb hozzuk a legjobb eredményeket
            )  # Egymás alá
            SCREEN.blit(score_display, score_rect)

        pygame.display.update()


def load_high_scores():
    """Betölti a high score listát fájlból."""
    try:
        with open("high_scores.txt", "r") as f:
            lines = f.readlines()
            high_scores = []
            for line in lines:
                name, score = line.strip().split(":")
                high_scores.append((name, int(score)))
            return high_scores
    except FileNotFoundError:
        return []  # Ha nem létezik a fájl, üres listát ad vissza
    except Exception as e:
        print(f"Hiba a high score lista betöltésekor: {e}")
        return []  # Hiba esetén is üres listát ad vissza, hogy a játék ne álljon meg


def save_high_scores(high_scores):
    """Elmenti a high score listát fájlba."""
    try:
        with open("high_scores.txt", "w") as f:
            for name, score in high_scores:
                f.write(f"{name}:{score}\n")
    except Exception as e:
        print(f"Hiba a high score lista mentésekor: {e}")
        # Itt nem állítjuk meg a játékot, mert a mentés nem kritikus


# Futtasd a menüt a játék indításakor
if __name__ == "__main__":
    player_name = ""
    menu(death_count=0)
