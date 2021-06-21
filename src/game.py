import pygame
from pygame.locals import *
import sys
import time
import random


pygame.init()

screen = pygame.display.set_mode((800, 600))
FONT = pygame.font.SysFont('Comic Sans MS', 32)
IMAGE_NORMAL = pygame.Surface((100, 32))
IMAGE_NORMAL.fill(pygame.Color('dodgerblue1'))
IMAGE_HOVER = pygame.Surface((100, 32))
IMAGE_HOVER.fill(pygame.Color('lightskyblue'))
IMAGE_DOWN = pygame.Surface((100, 32))
IMAGE_DOWN.fill(pygame.Color('aquamarine1'))

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):
        super().__init__()
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.image_down = pygame.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal
            
class Game:

    def __init__(self):

        self.w=750

        self.h=500

        self.reset=True

        self.active = False

        self.input_text=''

        self.word = ''

        self.time_start = 0

        self.total_time = 0

        self.accuracy = '0%'

        self.results = 'Time:0 Accuracy:0 % Wpm:0 '

        self.wpm = 0

        self.end = False

        self.HEAD_C = (255,213,102)

        self.TEXT_C = (240,240,240)

        self.RESULT_C = (255,70,70)
    

        # self.open_img = pygame.image.load('../resources/entry.jpg')

        # self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))
        
        self.easy_button = Button(
            320, 70, 170, 65, self.button_clicked,
            FONT, 'Increment', (255, 255, 255),
            IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)




        self.bg = pygame.image.load('../resources/background.jpg')

        self.bg = pygame.transform.scale(self.bg, (750,500))



        self.screen = pygame.display.set_mode((self.w,self.h))

        pygame.display.set_caption('PyTypingTest')

       

        
    def button_clicked(self):
        print("I got clicked")

    def draw_text(self, screen, msg, y ,fsize, color):

        font = pygame.font.Font(None, fsize)

        text = font.render(msg, 1,color)

        text_rect = text.get_rect(center=(self.w/2, y))

        screen.blit(text, text_rect)

        pygame.display.update()   

        

    def get_sentence(self):

        f = open('../resources/sentences.txt').read()

        sentences = f.split('\n')

        sentence = random.choice(sentences)

        return sentence



    def show_results(self, screen):

        if(not self.end):

            #Calculate time

            self.total_time = time.time() - self.time_start

               

            #Calculate accuracy

            count = 0

            for i,c in enumerate(self.word):

                try:

                    if self.input_text[i] == c:

                        count += 1

                except:

                    pass

            self.accuracy = count/len(self.word)*100

           

            #Calculate words per minute

            self.wpm = len(self.input_text)*60/(5*self.total_time)

            self.end = True

            print(self.total_time)

                

            self.results = 'Time:'+str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))



            # draw icon image

            self.time_img = pygame.image.load('../resources/icon.png')

            self.time_img = pygame.transform.scale(self.time_img, (150,150))

            #screen.blit(self.time_img, (80,320))

            screen.blit(self.time_img, (self.w/2-75,self.h-140))

            self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))

            

            print(self.results)

            pygame.display.update()



    def run(self):

        self.reset_game()

    

       

        self.running=True

        while(self.running):

            clock = pygame.time.Clock()

            self.screen.fill((0,0,0), (50,250,650,50))

            pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)

            # update the text of user input

            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == QUIT:

                    self.running = False

                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:

                    x,y = pygame.mouse.get_pos()

                    # position of input box

                    if(x>=50 and x<=650 and y>=250 and y<=300):

                        self.active = True

                        self.input_text = ''

                        self.time_start = time.time() 

                     # position of reset box

                    if(x>=310 and x<=510 and y>=390 and self.end):

                        self.reset_game()

                        x,y = pygame.mouse.get_pos()

         

                        

                elif event.type == pygame.KEYDOWN:

                    if self.active and not self.end:

                        if event.key == pygame.K_RETURN:

                            print(self.input_text)

                            self.show_results(self.screen)

                            print(self.results)

                            self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)  

                            self.end = True

                            

                        elif event.key == pygame.K_BACKSPACE:

                            self.input_text = self.input_text[:-1]

                        else:

                            try:

                                self.input_text += event.unicode

                            except:

                                pass

            

            pygame.display.update()

             

                

        clock.tick(60)



    def reset_game(self):

        #self.screen.blit(self.open_img, (0,0))



        pygame.display.update()

        time.sleep(1)

        

        self.reset=False

        self.end = False



        self.input_text=''

        self.word = ''

        self.time_start = 0

        self.total_time = 0

        self.wpm = 0



        # Get random sentence 

        self.word = self.get_sentence()

        if (not self.word): self.reset_game()

        #drawing heading

        self.screen.fill((0,0,0))

        self.screen.blit(self.bg,(0,0))

        msg = "Typing Speed Test"

        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)  

        # draw the rectangle for input box

        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)



        # draw the sentence string

        self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)

        

        pygame.display.update()
