
# Snake Game
# Daniel Lumbu and Kritika Pandit

import random
import time

from graphics import *

# Class Snake
# It draws snake which is a rectangle.
# Increase the length of the snake after it eats the food.

class Snake:
    def __init__(self,length):
        '''Creates our list of rectangles.
         Takes the parameter length that controls the size of our list of snakes.
         As the length grows our snake grows'''
        self.length =  length
        self.lst = []
        self.lst_of_Y_movements = [0]
        self.lst_of_X_movements = [0]
        self.sizeofsnake = 40  

    def increase_length(self,window):
        '''this function increases the length of the snake as it
         eats the food by adding an extra rectangle to our list of rectangles. It 
         then moves the added rectangle using the second last values in our X and Y list of movements'''
        # moving the function using the second last values in our X and Y list of movements'
        self.length += 1
        # creating a new rectangle by getting coordinates from the last rectangle and appending it to our list.
        side1_point = Point(self.lst[-1].getP1().getX() , self.lst[-1].getP1().getY() )
        side2_point1 = Point(self.lst[-1].getP2().getX(), self.lst[-1].getP2().getY())
        self.lst.append(Rectangle(side1_point,side2_point1)) 
        self.lst[-1].draw(window)
        self.lst[-1].setFill("blue")
        # adding one to the length parameter every time the increase fuction is called.
        self.lst[-1].move(-self.lst_of_X_movements [-2],-self.lst_of_Y_movements [-2])

    def lastrectangleX(self):
        '''Returns the X coordinate of the last rectangle'''
        return self.lst[-1].getP1().getX()
        
    def drawrectangle(self,window):
        '''Draws our starting rectangles depending on the length parameter'''
        # Creating the x and y for the list of rectangles
        self.x = [self.sizeofsnake] * self.length
        self.y = [self.sizeofsnake + self.sizeofsnake] * self.length

        # Looping over the x and y list to draw the rectangles and appending them to our list.
        for i in range(self.length):
             side1_point = Point(self.x[i], self.x[i])
             side2_point1 = Point(self.y[i], self.y[i])
             self.lst.append(Rectangle(side1_point,side2_point1))
            
        # loop through the list of rectangles to draw and color them in the window.
        for x in self.lst:
            x.setFill("blue")
            x.draw(window)
                  
    def head(self):
        '''Returns the first rectangle in the list'''
        return self.lst[0]

    def lengthofsnake(self):
        '''Returns the lenth of the snake'''
        return self.length

    # def undraw(self):      
    # self.win.undraw()

    def move(self,x,y):
        '''moves the rectangle dx units in x direction and dy units in y
        direction'''
        self.move(x,y)

    def collision(self, lst):
        '''Takes in the head of the rectangle as a parameter and
         return True if the head colides with the rest of the body'''
        # getting the coordinates of the current location of the head
        x1 = lst.getP1().getX() 
        x2 = lst.getP2().getX()
        y1 = lst.getP1().getY()
        y2 = lst.getP2().getY()
        # Checking if the two ends of the head touch any ends on the rest of the snake.
        for i in range(3, self.length):
            if x2 == self.lst[i].getP2().getX() and y1 == self.lst[i].getP1().getY():
                return True

    def checkkey(self,direction):
        '''Takes user input as the parameter and moves the snake up,
        down or left depending on the input.'''

        x_movement = 0
        y_movement = 0
        
        # should work only within the dimensions of the window.
        if self.lst[0].getP2().getX() != 640 and self.lst[0].getP2().getY() != 640 :
            if self.lst[0].getP2().getY() != 0 and self.lst[0].getP2().getX() != 0:
    
                # uses move function to move the head of the snake upwards
                # Stops the head of the snake from moving in the opposite direction 
                if direction in ["Up","w"]  and self.lst_of_Y_movements[0] != self.sizeofsnake or direction in ["Down","s"]  and self.lst_of_Y_movements[0] == -self.sizeofsnake : 
                        self.lst[0].move(0,-self.sizeofsnake)
                        y_movement = -self.sizeofsnake
                        x_movement = 0
                # uses move function to  move the head of the snake downwards  
                # Stops the head of the snake from moving in the opposite direction 
                elif direction in ["Down","s"] and self.lst_of_Y_movements[0] != -self.sizeofsnake or direction in ["Up","w"]  and self.lst_of_Y_movements[0] == self.sizeofsnake:
                    self.lst[0].move(0,self.sizeofsnake)
                    y_movement= self.sizeofsnake
                    x_movement = 0
                # uses move function to  move the head of the snake left
                # Stops the head of the snake from moving in the opposite direction 
                elif direction in ["Left","a"]  and self.lst_of_X_movements[0] != self.sizeofsnake or direction in ["Right","d"]  and self.lst_of_X_movements[0] == -self.sizeofsnake:
                        self.lst[0].move(-self.sizeofsnake,0)
                        x_movement = -self.sizeofsnake
                        y_movement  = 0
                # uses move function to  move the head of the snake right  
                # Stops the head of the snake from moving in the opposite direction      
                elif direction in ["Right","d"]  and self.lst_of_X_movements[0] != -self.sizeofsnake or direction in ["Left","a"]  and self.lst_of_X_movements[0] == self.sizeofsnake:
                        self.lst[0].move(self.sizeofsnake,0)
                        x_movement = self.sizeofsnake
                        y_movement = 0

                # Only adding directions to our lists of X and Y values when one of the values is not 0
                if  y_movement  != 0 or x_movement != 0:
                    self.lst_of_Y_movements.insert(0,y_movement)
                    self.lst_of_X_movements.insert(0,x_movement)
                    
                    # Deleting the last direction when the lists become greater than the lenth of the snake
                    if len(self.lst_of_X_movements ) > self.length:
                        del self.lst_of_X_movements [-1]
                        del self.lst_of_Y_movements [-1]

                    #looping through the X and Y lists and moving the rest of the body in the added directions
                    for i in range(1,len(self.lst_of_Y_movements )):
                        self.lst[i].move(self.lst_of_X_movements [i - 1],self.lst_of_Y_movements [i - 1])
    
    
    def gameover(self):
            ''' this function returns True when the snake
                 hits the boundaries or hits itself'''

            # Return True when the snake hits the upper or left boundaries of the window
            if self.lst[0].getP2().getX() == 640 or self.lst[0].getP2().getY() == 640 :
                return True
             
            # Return True when the snake hits the down or right boundaries of the window
            elif self.lst[0].getP2().getY() == 0 or self.lst[0].getP2().getX() == 0:
                return True
            
            # Return True when the snake hits itself.
            elif self.collision(self.lst[0]) == True:
                return True
            # Otherwise Returns false
            else:
                False

# class Food and AI
# this class creates the food for the snake to eat.
# it makes the food to disappear after it collides with the snake and redraws new food.
class foodAI:
    def __init__(self):
        '''Takes no Parameter. This fuctions controls 
        the food of the snake'''
        
        
    def drawfood(self,window,tail,length):
        ''' this function draws the food in the window. Takes in two parameters the length
         of the snake and the X coordinate of the last rectangle. It uses the tail to control 
         the simple AI of the food strategically placing it harder for the snake to eat '''
        
        # checking to make sure the x coordinate is not 0 or 600
        # To prevent food from leaving the window
        if tail == 600:
            tail - 20

        elif tail == 0:
            tail + 20
        # Creating the food points using the tail
        side1 = Point(tail + 5,tail + 5)
        side2 = Point(tail + 20,tail + 20) 
        
        # placing the food in the corners when mode 10 of the length is between 0 and 5
        # to make the game harder
        if length % 10 in [1,2,3,4] and length not in [1,2,3,4]:
            # Creating specific codes that take the food at the corner.
            specificornercodes = random.choice([[5,5,20,20],[5,575,20,590],[575,575,590,590],[575,5,590,20]])
            side1 = Point(specificornercodes[0],specificornercodes[1])
            side2 = Point(specificornercodes[2],specificornercodes[3])      
        # Drawing the food
        self.rectangle = Rectangle(side1,side2)
        self.rectangle.setFill("red")
        self.rectangle.draw(window)

 
    def undraw(self):
        ''' Fuction that undraws the food.'''
        self.rectangle.undraw()
   
    def collision(self, lst):
        '''Fuction that takes the head of the snake and returns
         True if the head colides with the food'''
        # getting the coordinates of the current location of the head
        x1 = lst.getP1().getX() 
        x2 = lst.getP2().getX()
        y1 = lst.getP1().getY()
        y2 = lst.getP2().getY()

        # Checking if the head of the snake collides with the food
        if x1 < self.rectangle.getP1().getX() < x2:
            if y1 < self.rectangle.getP1().getY() < y2:
                return True

#class main
# Puts Our two previous Classes Together and runs the game
class main:
   
     def __init__(self):
        '''create a window of desired leghth and breadth with desired background color. Draw snake using snake class.
        Draw the food using food class. dispaly_movement score after playing the game.'''
        # Winddow, food, background and snake
        self.win = GraphWin("Snake game", 600, 600)
        self.win.setBackground("green")
        self.Oursnake= Snake(2)
        self.Food = foodAI()

        # Drawing our initial snake and food and creating a random food start point
        self.Oursnake.drawrectangle(self.win)
        foodstartoint= random.randint(0,580)
        self.Food.drawfood(self.win,foodstartoint,self.Oursnake.lengthofsnake() - 1)
        
        # Initial direction of the head
        self.direction = "Down"
        
        # Creating and  drawing the initial Score
        self.score = Text(Point(50,60),f"Score: {self.Oursnake.lengthofsnake() - 1}")
        self.score.setSize(20)
        self.score.setTextColor("Gold")
        self.score.draw(self.win)
        
        # Creating pause object that is drawn when self check == 1
        self.pause = Text(Point(300,300)," Game Paused Press Direction Keys To Continue")
        self.pause.setTextColor("lavender")
        self.pause.setSize(20)
        self.pause.setStyle("bold")
        self.check = 0
    
    # update the score each time the snake eats the food.
     def undraw(self):
         ''' Undraws the score'''
         self.score.undraw()

     def playgame(self):
        '''' A fuction that controls '''

        # Checking if the direction is not in our predescribed directions 
        # then drawing a pause text on the window
        if self.direction not in ["Down","Up","Left","Right","a","w","s","d"] and self.check == 0:
            self.pause.draw(self.win)
            self.check += 1

        # Checking if the direction is in the predescribed directions 
        # and also checking if the pause was created then undrawing it
        if self.check == 1 and self.direction in ["Down","Up","Left","Right","a","w","s","d"]  :
            self.check = 0
            self.pause.undraw()

        # running the checkkey function
        self.Oursnake.checkkey(self.direction)
        
        # increases the leghth after colliding with food.
        # undraws the food after eating it
        # updates the score each time it eats the food.
        if self.Food.collision(self.Oursnake.head()) == True:
            self.Oursnake.increase_length(self.win)
            self.Food.undraw()
            self.Food.drawfood(self.win,self.Oursnake.lastrectangleX(),self.Oursnake.lengthofsnake() - 1)
            self.score.undraw()
            self.score= Text(Point(50,60),f"Score: {self.Oursnake.lengthofsnake() - 1}")
            self.score.setSize(20)
            self.score.setTextColor("Gold")
            self.score.draw(self.win)
          
        # display gameover if False.
        # update the window each time
        
        
           
     def rungame(self): 
        '''A fuction that runs our game,controls replays and exits in the game '''

        runningtime = 0.15
        running = True
        while running:    
            save = self.win.checkKey()
            # only changing the direction when the user enter a direction
            if save != "":
                self.direction = save 
            self.playgame()

            # Ending the looping when its gameover
            if self.Oursnake.gameover() == True:
                running = False
            # Increasing the speed of the snake at score 15 to increase the difficulty
            if self.Oursnake.lengthofsnake() - 1 == 15:
                runningtime = 0
            time.sleep(runningtime)

        #closing the window when the loop ends
        self.win.close()

        # Creating a new window that displays game over and asks the user to replay or exit
        self.win = GraphWin("Snake game", 600, 600)
        self.win.setBackground("black")
        GameoverText = Text(Point(300,300),"Game Over You lose")
        Exit_or_ReplayText = Text(Point(300,350),"Press Return to Replay or Esc to Exit")
        GameoverText.setTextColor("white")
        Exit_or_ReplayText.setTextColor("blue")
        GameoverText.setSize(25)
        Exit_or_ReplayText.setSize(20)
        Exit_or_ReplayText.draw(self.win)
        GameoverText.draw(self.win)

        # Waits for the user to make a choice between escape or return key
        user_choice = self.win.getKey()

        # runs the game again if the user presses return key.
        if user_choice == "Return":
              self.win.close()
              game = main()
              game.rungame()
        
        # closes the window if the user presses escape key.
        elif user_choice  == "Escape":
            self.win.close()     

        input("When done, press Enter")

# runs the main function
if __name__ == "__main__":
   game = main()
   game.rungame()


