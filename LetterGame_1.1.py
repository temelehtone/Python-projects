
import pygame as pg
import os
import time
import random
from keyboardlayout.key import Key
import keyboardlayout as kl
import keyboardlayout.pygame as klp
import webbrowser



pg.init()
pg.font.init()

class Information:
    # Basic properties
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 100, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BLUE = 0, 0, 250
    YELLOW = 255, 100, 0
    LINK_COLOR = 70, 29, 219

    SPEED = 2
    APPLE_SIZE = 100

    FONT = pg.font.SysFont('comicsans', 40)
    MENU_FONT = pg.font.SysFont('Arial', 30, True)

    FPS = 60

    APPLE_IMAGE = pg.image.load(os.path.join('Assets/apple.png'))
    APPLE = pg.transform.scale(APPLE_IMAGE, (APPLE_SIZE, APPLE_SIZE))

    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    WORDS = [
             "happy", "sun", "cat", "dog", "horse", "bark", "bat", "bite", "bolt", "bowl", "box", "can", "check", "clip", "club",
             "dip", "down", "dress", "eye", "fair", "file", "foot", "fly", "gum", "hard", "hide", "jam", "last", "left", "right",
             "mean", "miss", "nails", "over", "park", "pen", "play", "punch", "ring", "rock", "shake", "stick", "stuff", "swing",
             "France", "Dubai", "German", "Moon", "Blue", "Red", "Green", "White", "Black", "Fiji", "Peru", "Iran", "Cuba", "Oman"
            ]

    def __init__(self, width: int, height: int):
        # Sets up the window
        self.width = width
        self.height = height

        self.window = pg.display.set_mode((width, height))
        pg.display.set_caption("Letter Game")

        self.start_image = pg.image.load(os.path.join('Assets/start_menu.jpg'))
        self.start = pg.transform.scale(self.start_image, (self.width, self.height))
        
        self.background_image = pg.image.load(os.path.join('Assets/background.jpg'))
        self.background = pg.transform.scale(self.background_image, (self.width, self.height))
    

def menu(info):
    # Displays the start screen
    info.window.blit(info.start, (0, 0))
    start_game_button = pg.draw.rect(info.window, info.BLACK, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 3, info.width // 3, 60), 5, 6)
    start_text = info.FONT.render("START", True, info.BLACK)
    info.window.blit(start_text, (start_game_button.x + start_game_button.width // 2 - start_text.get_width() // 2, start_game_button.y))

    exit_button = pg.draw.rect(info.window, info.RED, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 3 + 80, info.width // 3, 60), 5, 6)
    exit_text = info.FONT.render("EXIT", True, info.RED)
    info.window.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y))

    welcome_label = pg.draw.rect(info.window, info.WHITE, 
        pg.Rect(info.width // 2 - 100, 100, 200, 40))
    welcome_text = info.MENU_FONT.render("WELCOME!", True, info.BLACK)
    info.window.blit(welcome_text, (welcome_label.x + welcome_label.width // 2 - welcome_text.get_width() // 2,
                     welcome_label.y + welcome_label.height // 2 - welcome_text.get_height() // 2))
    pg.draw.rect(info.window, info.BLACK, 
        pg.Rect(info.width // 2 - 100 - 2, 100 - 2, 200 + 4, 40 + 4), 2)

    second_label = pg.draw.rect(info.window, info.WHITE, 
        pg.Rect(info.width // 2 - 200, 180, 400, 90))
    second_text = info.MENU_FONT.render("Afromtmi Falling Letters Game", True, info.BLACK)
    info.window.blit(second_text, (second_label.x + second_label.width // 2 - second_text.get_width() // 2,
                     second_label.y + 5))
    pg.draw.rect(info.window, info.BLACK, 
        pg.Rect(info.width // 2 - 200 - 2, 180 - 2, 400 + 4, 90 + 4), 2)
    third_text = info.MENU_FONT.render("Learn Typing Fast", True, info.BLACK)
    info.window.blit(third_text, (second_label.x + second_label.width // 2 - third_text.get_width() // 2,
                     second_label.y + 45))

    link_label = pg.draw.rect(info.window, info.WHITE, 
        pg.Rect(info.width // 2 - 170, 800, 340, 40))
    link_text = info.MENU_FONT.render("www.afromtmi.com", True, info.LINK_COLOR)
    copyright_sign = info.MENU_FONT.render("(c)", True, info.BLACK)
    year_text = info.MENU_FONT.render("2022", True, info.BLACK)
    info.window.blit(copyright_sign, (link_label.x + 5,
                     link_label.y + link_label.height // 2 - copyright_sign.get_height() // 2))
    link_button = info.window.blit(link_text, (link_label.x + 40,
                     link_label.y + link_label.height // 2 - link_text.get_height() // 2))
    info.window.blit(year_text, (link_label.x + link_text.get_width() + 50,
                     link_label.y + link_label.height // 2 - year_text.get_height() // 2))
    pg.draw.rect(info.window, info.BLACK, 
        pg.Rect(info.width // 2 - 170 - 2, 800 - 2, 340 + 4, 40 + 4), 2)

    return start_game_button, exit_button, link_button


def draw(info, start_menu, apples, score, elapsed_time, lives, the_end, 
         difficulty, keyboard, easy, medium, hard, word, word_location, word_colors, ind):
    # Draws the components to the window
    
    if start_menu:
        menu(info)
    elif the_end:
        info.window.blit(info.background, (0, 0))
        game_over(info, score, elapsed_time)
    elif difficulty:
        info.window.blit(info.start, (0, 0))
        choose_difficulty(info)
    else:
        info.window.blit(info.background, (0, 0))
        if easy:
            draw_apples(info, apples)
        elif medium or hard:
            draw_words(info, word, word_location, word_colors, ind)
        draw_score(info, score, elapsed_time, lives)
        keyboard.draw(info.window)
    pg.display.update()


def draw_words(info, word, word_location, word_colors, ind):
    # Draws the word    
    word_lenght = 0
    for i in range(len(word)):
        word_text = info.FONT.render(f"{word[i]}", True, word_colors[i])
        info.window.blit(word_text, (word_location[0] + word_lenght, word_location[1]))
        word_lenght += word_text.get_width()

    word_rect = pg.draw.rect(info.window, info.WHITE, pg.Rect(word_location[0] - 10, word_location[1], word_lenght + 20, 60), 4, 6)
    word_location[1] += info.SPEED


def choose_difficulty(info):
    # Displays the difficulty selection
    easy_button = pg.draw.rect(info.window, info.GREEN, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 3, info.width // 3, 60), 5, 6)
    easy_text = info.FONT.render("EASY", True, info.GREEN)
    info.window.blit(easy_text ,(easy_button.x + easy_button.width // 2 - easy_text.get_width() // 2, easy_button.y))

    medium_button = pg.draw.rect(info.window, info.BLUE, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 3 + 80, info.width // 3, 60), 5, 6)
    medium_text = info.FONT.render("MEDIUM", True, info.BLUE)
    info.window.blit(medium_text, (medium_button.x + medium_button.width // 2 - medium_text.get_width() // 2, medium_button.y))

    hard_button = pg.draw.rect(info.window, info.RED, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 3 + 160, info.width // 3, 60), 5, 6)
    hard_text = info.FONT.render("HARD", True, info.RED)
    info.window.blit(hard_text, (hard_button.x + hard_button.width // 2 - hard_text.get_width() // 2, hard_button.y))

    return_button = pg.draw.rect(info.window, info.BLACK, 
        pg.Rect(10, 10, info.width // 4, 60), 5, 6)
    return_text = info.FONT.render("RETURN", True, info.BLACK)
    info.window.blit(return_text, (return_button.x + return_button.width // 2 - return_text.get_width() // 2, return_button.y))

    return easy_button, medium_button, hard_button, return_button


def game_logic(info, apples, lives, word, easy, medium, hard, score, word_location, key_info, keyboard, word_colors, ind):
    # Handles the remove of the apple that hits the ground
    if easy:
        for apple in apples:
            if apples[apple][1] > 770 - info.APPLE_SIZE:
                while True:
                    new_letter, new_location = random.choices(info.LETTERS)[0], [random.randint(100, 500), random.randint(0, 100) * -1]
                    if new_letter not in apples:
                        break
                apples[new_letter] = new_location
                keyboard.update_key(Key(apple.lower()), key_info)
                apples.pop(apple)
                lives -= 1
                return lives, score, word, word_location, apples, word_colors, ind, keyboard
        

    # Handles new word spawning and if the word hits the ground
    elif medium or hard:
        if len(word) == ind:
            keyboard.update_key(Key(word[ind - 1].lower()), key_info)
            word = random.choice(info.WORDS)
            word_location = [random.randint(100, 500), random.randint(0, 100) * -1]
            word_colors = set_word_colors(info, word)  
            ind = 0
            score += 1
            
        elif word_location[1] > 770 - 50:
            keyboard.update_key(Key(word[ind].lower()), key_info)
            word = random.choice(info.WORDS)
            word_location = [random.randint(100, 500), random.randint(0, 100) * -1]
            word_colors = set_word_colors(info, word)
            ind = 0
            lives -= 1
            
            
    return lives, score, word, word_location, apples, word_colors, ind, keyboard


def set_word_colors(info, word):
    # Sets the color for each letter when new word is made
    word_colors = []
    for i in range(len(word)):
        word_colors.append(info.WHITE)
    return word_colors

def key_examination(apples, score, letter, info):
    # If the pressed key is correct creates a new apple and letter
    while True:
        new_letter, new_location = random.choices(info.LETTERS)[0], [random.randint(100, 500), random.randint(0, 100) * -1]
        if new_letter not in apples:
            break

    apples.pop(letter)
    apples[new_letter] = new_location
    score += 1
    
    return score
    

def draw_apples(info, apples):
    # Draws the apples and letters in game
    
    for apple in list(apples.values()):
        info.window.blit(info.APPLE, (apple[0], apple[1]))
        apple[1] += info.SPEED
    for letter in apples:
        letter_text = info.FONT.render(f"{letter}", True, info.BLUE)
        info.window.blit(letter_text, (apples[letter][0] + info.APPLE_SIZE // 2 - letter_text.get_width() + info.APPLE_SIZE // 7,
                         apples[letter][1] + info.APPLE_SIZE // 3))


def draw_score(info, score, elapsed_time, lives):
    # Draws the score, lives, and time texts
    pg.draw.rect(info.window, info.WHITE, pg.Rect(0, 0, info.width, 60))

    score_text = info.FONT.render(f"Score: {score}", True, info.BLUE)
    info.window.blit(score_text, (5, 5))

    lives_text = info.FONT.render(f"Lives: {lives}", True, info.RED)
    info.window.blit(lives_text, (info.width // 2 - lives_text.get_width() // 2, 5))

    time_text = info.FONT.render(f"Time: {int(elapsed_time)}", True, info.BLACK)
    info.window.blit(time_text, (info.width - time_text.get_width(), 5))


def game_over(info, score, elapsed_time):
    # Displays the game over screen
    time_text = info.FONT.render(f"Time: {int(elapsed_time)}", True, info.BLACK)
    info.window.blit(time_text, (info.width // 2 - time_text.get_width() // 2, 180))

    score_text = info.FONT.render(f"Score: {score}", True, info.BLUE)
    info.window.blit(score_text, (info.width // 2 - time_text.get_width() // 2, 130))

    end_text = info.FONT.render(f"Game Over", True, info.RED)
    info.window.blit(end_text, (info.width // 2 - score_text.get_width() // 2, 70))

    exit_button = pg.draw.rect(info.window, info.RED, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 2 + 100, info.width // 3, 60), 5, 6)
    exit_text = info.FONT.render("EXIT", True, info.RED)
    info.window.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y))

    new_game_button = pg.draw.rect(info.window, info.BLUE, 
        pg.Rect(info.width // 2 - info.width // 6, info.height // 2, info.width // 3, 60), 5, 6)
    new_game_text = info.FONT.render("NEW GAME", True, info.BLUE)
    info.window.blit(new_game_text, (new_game_button.x + new_game_button.width // 2 - new_game_text.get_width() // 2, new_game_button.y))

    return new_game_button, exit_button


def create_keyboard(info):
    layout_name = kl.LayoutName.QWERTY
    # set the letter key size in pixels
    key_size = 47
    # set the keyboard position and color info
    keyboard_info = kl.KeyboardInfo(
        position=(0, 770),
        padding=2,
        color=info.WHITE
    )
    # set the letter key color, padding, and margin info in px
    key_info = kl.KeyInfo(
        margin=10,
        color=info.BLACK,
        txt_color=info.WHITE, 
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    # set the letter key size info in px
    letter_key_size = (key_size, key_size)  # width, height
    keyboard_layout = klp.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info
    )

    wrong_key_info = kl.KeyInfo(
        margin=14,
        color=info.RED,
        txt_color=info.WHITE,
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    right_key_info = kl.KeyInfo(
        margin=14,
        color=info.GREEN,
        txt_color=info.WHITE,
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    highlighted_key_info = kl.KeyInfo(
        margin=14,
        color=pg.Color("yellow"),
        txt_color=info.BLACK,
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )

    return keyboard_layout, wrong_key_info, key_info, right_key_info, highlighted_key_info


def draw_keys(word, keyboard, highlighted_key_info, apples, ind, easy, medium, hard):
    # Draws the higlights for keys that have to be pressed
    try:
        if easy:
            letters = sorted(apples, key=lambda t: apples[t][1])

            letter = letters[-1]
            keyboard.update_key(Key(letter.lower()), highlighted_key_info)    
        
        elif medium or hard:
            first_letter = word[ind]
            if first_letter.isupper():
                keyboard.update_key(Key(first_letter.lower()), highlighted_key_info)
                keyboard.update_key(Key.LEFT_SHIFT, highlighted_key_info)
            else:
                keyboard.update_key(Key(first_letter.lower()), highlighted_key_info)
    except IndexError or AttributeError:
        return


def main():
    # Setups the starting values
    clock = pg.time.Clock()
    start_menu = True
    info = Information(700, 1000)
    running = True
    the_end = False
    difficulty = False
    caps = False
    start_game_button, exit_button, link_button = menu(info)
    new_game_button, exit_button = game_over(info, 0, 0)
    easy_button, medium_button, hard_button, return_button = choose_difficulty(info)
    keyboard, wrong_key_info, key_info, right_key_info, highlighted_key_info = create_keyboard(info)

    
    # GAME LOOP
    while running:
        clock.tick(info.FPS)
        if not start_menu and not the_end and not difficulty:
            # Setups the buttons for game over screen and counts the time
            new_game_button, exit_button = game_over(info, 0, 0)
            elapsed_time = time.time() - start_time
        elif start_menu:
            # Setups the game starting values
            start_game_button, exit_button, link_button = menu(info)
            difficulty = False
            the_end = False
            easy, medium, hard = False, False, False
            keyboard, wrong_key_info, key_info, right_key_info, highlighted_key_info = create_keyboard(info)
            word = ""
            word_location = []
            word_colors = {}
            apples = {}
            score = 0
            lives = 5
            elapsed_time = 0
            ind = 0
            for i in range(3):
                apples.update({random.choices(info.LETTERS)[0]: [random.randint(100, 500), random.randint(0, 100) * -1]})
            start_time = time.time()
            end_text = ""
        draw_keys(word, keyboard, highlighted_key_info, apples, ind, easy, medium, hard)
        for event in pg.event.get():
            # If exit is pressed quits the game
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                # Handles which button is pressed
                if start_game_button.collidepoint(pg.mouse.get_pos()) and start_menu:
                    start_menu = False
                    difficulty = True
                elif exit_button.collidepoint(pg.mouse.get_pos()) and (start_menu or the_end):
                    running = False
                elif link_button.collidepoint(pg.mouse.get_pos()) and start_menu:
                    webbrowser.open(r"www.afromtmi.com")
                elif easy_button.collidepoint(pg.mouse.get_pos()) and difficulty:
                    easy = True
                    info.SPEED = 3
                    difficulty = False
                elif medium_button.collidepoint(pg.mouse.get_pos()) and difficulty:
                    medium = True
                    word = random.choice(info.WORDS)
                    word_colors = set_word_colors(info, word)
                    ind = 0
                    word_location = [random.randint(100, 500), random.randint(0, 100) * -1]
                    info.SPEED = 3
                    difficulty = False
                elif hard_button.collidepoint(pg.mouse.get_pos()) and difficulty:
                    hard = True
                    word = random.choice(info.WORDS)
                    word_colors = set_word_colors(info, word)
                    ind = 0
                    word_location = [random.randint(100, 500), random.randint(0, 100) * -1]
                    info.SPEED = 4
                    difficulty = False
                elif new_game_button.collidepoint(pg.mouse.get_pos()) and the_end:
                    the_end = False
                    difficulty = False
                    start_menu = True
                elif return_button.collidepoint(pg.mouse.get_pos()) and difficulty:
                    the_end = False
                    start_menu = True
                    difficulty = False
                    
            key = keyboard.get_key(event)
            
            if key is None:
                    continue
            
            elif event.type == pg.KEYDOWN:
                
                # Handles the pressed keys
                try: 
                    if easy:
                        if key.name in apples:
                            letter = key.name
                            score = key_examination(apples, score, letter, info)
                            keyboard.update_key(key, right_key_info)
                        else:
                            keyboard.update_key(key, wrong_key_info)
                
                    elif medium or hard:

                        if key.name == "LEFT_SHIFT":
                            caps = True
                            
                            
                        if word[ind].isupper():
                            
                            if caps:
                                keyboard.update_key(Key.LEFT_SHIFT, right_key_info)
                            elif not caps:
                                keyboard.update_key(Key.LEFT_SHIFT, key_info)
        
                            if caps and key.name == word[ind]:
                                first_letter = key.name        
                            else:
                                first_letter = key.value
                            
                        if word[ind].islower():
                            if caps:
                                keyboard.update_key(Key.LEFT_SHIFT, wrong_key_info)
                                first_letter = key.name
                            else:
                                first_letter = key.value
                        
                        
                        if first_letter == word[ind]:
                            keyboard.update_key(key, right_key_info)
                            word_colors[ind] = info.GREEN
                            ind += 1
                    
                        else:
                            if key.name == "LEFT_SHIFT":
                                continue 
                            else:
                                keyboard.update_key(key, wrong_key_info)
                                keyboard.update_key(Key(word[ind].lower()), key_info)
                                word_colors[ind] = info.RED
                                lives -= 1
                                ind += 1

                except IndexError or AttributeError:
                    continue

            elif event.type == pg.KEYUP:
                if key.name == "LEFT_SHIFT":
                    caps = False
                keyboard.update_key(key, key_info)
                
        # End the game if run out of lives
        if lives == 0:
            end_text = "You Lost!"
        if end_text != "":
            the_end = True 
        
        lives, score, word, word_location, apples, word_colors, ind, keyboard = game_logic(info, apples, lives, word, easy, medium, hard, score, 
                                                                                        word_location, key_info, keyboard, word_colors, ind)
        
        # Draws everything on the screen 
        draw(info, start_menu, apples, score, elapsed_time, lives, the_end, 
             difficulty, keyboard, easy, medium, hard, word, word_location, word_colors, ind)
        
    pg.quit
    
if __name__ == "__main__":
    main()
