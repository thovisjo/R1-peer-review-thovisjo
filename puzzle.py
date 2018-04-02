#!/usr/bin/env python
import sys, pygame, random
from square import Square
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4' 

screen_size = (800,600)
dimensions = (rows,columns) = (4,4)
FPS = 60
black = (0,0,0)
red = (200, 0, 0)
green = (0, 200, 0)


#here, the program hard-codes all the possible words
threeLets = [" dad", " old", " you", " can", " day", " day", " man", " boy", " mom", " act", " bar", " car", " dew", " eat", " gym", " ink", " key", " ram", " urn", " vet", " yap"]
fourLets = ["void", "open", "acid", "aged", "army", "ball", "loon", "bank", "bath", "boom", "bush", "clam", "cook", "crew", "dawn", "dead", "dial", "disk", "drug",
            "dual", "edge", "exit", "fact", "felt", "file", "fund", "golf", "gulf", "harm", "hire", "holy", "inch", "iron", "jack", "jury","king", "kind", "lead",
            "less", "link", "mass", "menu", "mere", "navy", "nick", "note", "only", "okay", "palm", "pair", "plug", "quit", "rail", "rare", "risk", "rule", "sign",
            "snow", "suit", "text", "tour", "twin", "user", "vice", "vote", "view", "wage", "ward", "wing", "yard", "zero"]


def calculate_xy(pos,puzzle):
        ''' calculates which square is the target '''
	w = 600 / columns
	h = 600 / rows
	to_return = (int(pos[0]//w),int(pos[1]//h))
	return to_return

def record_win(words, lines):
        #checks to see if the user has won
        record = 0
        for line in lines:
                for word in words:
                        if line == word:
                                record += 1 
        if record == 4: #if all four lines are words, return true
                return True
        else:
                return False
        

def main():
        turns = 0
        pygame.init()
        words = random.sample(threeLets, 1) + random.sample(fourLets, 3)
        letters = []

        #not quite sure what this does
        for phrase in words:
                for character in phrase:
                        letters.append(character)
                
        char = 0
        win = 0
        screen = pygame.display.set_mode(screen_size)
        font = pygame.font.SysFont("arial",48)
        clock = pygame.time.Clock()

        random.shuffle(letters)
        
        puzzle = []
        (w,h) = (600/columns,600/rows)
        for i in range(rows):
                for j in range(columns):
                        position = j*rows + i #no idea what this does
                        color = red
                        puzzle.append(Square(i,j,str(letters[char]),w,h,color,font))
                        char += 1
        
        while True:
                clock.tick(FPS)

                screen.fill(black)
                #event checking
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                        if event.type == pygame.MOUSEBUTTONUP:
                                if win == 0:
                                        pos = calculate_xy(pygame.mouse.get_pos(), puzzle)
                                        for p in puzzle:
                                                #check if the user has clicked inside a square adjacent to the black square
                                                if p.position == pos:
                                                        for piece in puzzle:
                                                                if p.check_proximity(piece.position) and piece.label == " ":
                                                                        turns += 1
                                                                        saved_pos = p.position
                                                                        p.position = piece.position
                                                                        piece.position = saved_pos
                                                                        p.color = red
                                                                        
                for num in range(columns):
                        for p in puzzle:
                                for word in words:
                                        #checks to see if the square can be put in the current column
                                        #compares the letter and its position to the letter of that position in every word
                                        if p.label == word[num] and (p.position == (num, 0) or p.position == (num, 1) or p.position == (num, 2) or p.position == (num,3)):
                                                p.color = green
                                                
                
                for p in puzzle:
                        p.draw_square(pygame.draw,screen)		


                #render the turn text
                text = ("Turn: " + str(turns))
                f = font.render(text,True,(255,255,255))
                (fwidth,fheight) = font.size(text)
                screen.blit(f, (625,100))


                #initialize array variables
                line1 = [0,0,0,0]
                line2 = [0,0,0,0]
                line3 = [0,0,0,0]
                line4 = [0,0,0,0]

                #convert the arrays to be words made of the text in the puzzle squares
                for p in puzzle:
                        for num1 in range(columns):
                                        if p.position == (num1,0):
                                                line1[num1] = p.label
                                        if p.position == (num1,1):
                                                line2[num1] = p.label
                                        if p.position == (num1,2):
                                                line3[num1] = p.label
                                        if p.position == (num1,3):
                                                line4[num1] = p.label

                #converts the arrays into strings
                line1 = "".join(line1)
                line2 = "".join(line2)
                line3 = "".join(line3)
                line4 = "".join(line4)
                #makes new array of these strings
                lines = [line1, line2, line3, line4]

                
                text = ("Turn: " + str(turns))

                #runs record win using lines, so if every line is a word, returns true
                if record_win(words, lines):
                        text2 = "YOU WIN!!!"
                        w = font.render(text2, True, (255,255,255))    
                        screen.blit(w, (625, 150))
                        win += 1
                f = font.render(text,True,(255,255,255))
                
                (fwidth,fheight) = font.size(text)
                screen.blit(f, (625,100))
                
                
                pygame.display.flip()

if __name__ == '__main__':
	main()
