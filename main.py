import tkinter as tk
import time
import random
from tkinter import ttk

"""Initialises a tkinter object"""
root = tk.Tk()

"""Sets window dimensions and creates the window of that size"""
window_height = 720
window_width = 1280

root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)


class Game(tk.Canvas):
    def __init__(self):
        tk.Canvas.__init__(self, height=window_height,
                           width=window_width, bg="#abc3b8")
        self.pack()
        self.bind_all("<Key>", self.whenKeyPressed)
        self.bind("<Button-1>", self.click)
        self.image_imports()
        self.jump_key = "Up"
        self.drop_key = "Down"
        self.left_key = "Left"
        self.right_key = "Right"
        self.boss_key = "b"
        self.platform_size = 100
        self.penguin_velocity_x = 0
        self.penguin_velocity_y = 0
        self.imgOn = False
        self.pause_active = False
        self.inMenu = False
        self.score = 0
        self.firstMenu = True
        self.username_string = "No_Name"
        self.leaderboard_tuples = []
        self.keyStatus = {"up": False, "left": False, "right": False,
                          "down": False}
        self.menu()

    """Loads menu on start and after player dying"""
    def menu(self):
        self.platform_size = 100
        self.delete("all")
        self.inMenu = True
        self.create_polygon(384, 120, 896, 120, 896, 250, 384, 250,
                            fill="#FFFFFF", outline="#000000",
                            tags="button-play")
        self.create_polygon(384, 295, 896, 295, 896, 425, 384, 425,
                            fill="#FFFFFF", outline="#000000",
                            tags="button-setting")
        self.create_polygon(384, 470, 896, 470, 896, 600, 384, 600,
                            fill="#FFFFFF", outline="#000000",
                            tags="button-quit")
        self.create_polygon(64, 72, 320, 72, 320, 648, 64, 648,
                            fill="#FFFFFF", outline="#000000",
                            tags="leaderboard")
        self.create_text(192, 108, text="Leaderboard",
                         font=("Helvetica", "24", "bold"))
        self.username = tk.StringVar()
        self.username_entry = ttk.Entry(self, textvariable=self.username)
        self.create_window(1088, 500, window=self.username_entry)
        self.create_text(1088, 450, text="Enter Username",
                         font=("Helvetica", "20", "bold"))
        self.submit_button = ttk.Button(self, text="Submit",
                                        command=self.username_submitted)
        self.create_window(1088, 550, window=self.submit_button)
        self.create_text(1088, 600, text=f"Username: {self.username_string}",
                         font=("Helvetica", "20", "bold"), tags="username")
        self.create_text(640, 185, text="Play",
                         font=("Helvetica", "24", "bold"))
        self.create_text(640, 360, text="Settings",
                         font=("Helvetica", "24", "bold"))
        self.create_text(640, 535, text="Quit",
                         font=("Helvetica", "24", "bold"))
        self.create_text(1088, 120, text=f"Previous Score: {self.score}",
                         font=("Helvetica", "20", "bold"))
        if not self.firstMenu:
            with open("highscores.txt", 'a', encoding='utf-8') as f:
                if self.username_string is not None:
                    f.write(f"{self.username_string},{self.score}\n")
                else:
                    f.write(f"NO USERNAME, {self.score}\n")
        with open("highscores.txt", 'r', encoding='utf-8') as f:
            self.leaderboard = [list(line.split(',')) for line in f]
            for item in self.leaderboard:
                item[1] = item[1].rstrip("\n")
        self.leaderboard.sort(reverse=True, key=self.sortFunction)
        for i in range(6):
            if self.leaderboard[i] is None:
                break
            self.create_text(192, (i*72)+216, text=self.leaderboard[i],
                             font=("Helvetica", "24", "bold"))

    def sortFunction(self, element):
        return int(element[1])

    def click(self, event):
        self.checkButtonClick(event.x, event.y)

    def username_submitted(self):
        self.username_string = self.username.get()
        self.menu()

    def checkButtonClick(self, x, y):
        overlap = self.find_overlapping(x, y, x, y)
        for item in overlap:
            if "button-play" in self.gettags(item):
                self.firstMenu = False
                self.newLevel()
                self.score = 0
                self.runGame()
            if "button-setting" in self.gettags(item):
                self.settingsPage()
            if "button-quit" in self.gettags(item):
                quit()
            if "jump-key-button" in self.gettags(item):
                self.jump_key = self.keyPressed
                self.settingsPage()
            if "drop-key-button" in self.gettags(item):
                self.drop_key = self.keyPressed
                self.settingsPage()
            if "left-key-button" in self.gettags(item):
                self.left_key = self.keyPressed
                self.settingsPage()
            if "right-key-button" in self.gettags(item):
                self.right_key = self.keyPressed
                self.settingsPage()
            if "boss-key-button" in self.gettags(item):
                self.boss_key = self.keyPressed
                self.settingsPage()
            if "reset-key-button" in self.gettags(item):
                self.jump_key = "Up"
                self.drop_key = "Down"
                self.left_key = "Left"
                self.right_key = "Right"
                self.boss_key = "b"
                self.settingsPage()
            if "back-key-button" in self.gettags(item):
                self.menu()

    def settingsPage(self):
        self.delete("all")
        self.create_polygon(128, 30, 223, 30, 223, 125, 128, 125,
                            fill="#FFFFFF", outline="#000000",
                            tags="jump-key-button")
        self.create_polygon(128, 145, 223, 145, 223, 240, 128, 240,
                            fill="#FFFFFF", outline="#000000",
                            tags="drop-key-button")
        self.create_polygon(128, 260, 223, 260, 223, 355, 128, 355,
                            fill="#FFFFFF", outline="#000000",
                            tags="left-key-button")
        self.create_polygon(128, 375, 223, 375, 223, 470, 128, 470,
                            fill="#FFFFFF", outline="#000000",
                            tags="right-key-button")
        self.create_polygon(128, 490, 223, 490, 223, 585, 128, 585,
                            fill="#FFFFFF", outline="#000000",
                            tags="boss-key-button")
        self.create_polygon(384, 605, 896, 605, 896, 700, 384, 700,
                            fill="#FFFFFF", outline="#000000",
                            tags="reset-key-button")
        self.create_polygon(1110, 10, 1270, 10, 1270, 90, 1110, 90,
                            fill="#FFFFFF", outline="#000000",
                            tags="back-key-button")
        self.create_text(175, 77, text=self.jump_key,
                         font=("Helvetica", "18", "bold"))
        self.create_text(175, 192, text=self.drop_key,
                         font=("Helvetica", "18", "bold"))
        self.create_text(175, 307, text=self.left_key,
                         font=("Helvetica", "18", "bold"))
        self.create_text(175, 422, text=self.right_key,
                         font=("Helvetica", "18", "bold"))
        self.create_text(175, 537, text=self.boss_key,
                         font=("Helvetica", "18", "bold"))
        self.create_text(1190, 45, text="Back",
                         font=("Helvetica", "18", "bold"))
        self.create_text(512, 77, text="Jump Key",
                         font=("Helvetica", "18", "bold"))
        self.create_text(512, 192, text="Drop Key",
                         font=("Helvetica", "18", "bold"))
        self.create_text(512, 307, text="Left Key",
                         font=("Helvetica", "18", "bold"))
        self.create_text(512, 422, text="Right Key",
                         font=("Helvetica", "18", "bold"))
        self.create_text(512, 537, text="Boss Key",
                         font=("Helvetica", "18", "bold"))
        self.create_text(640, 653, text="Reset to default",
                         font=("Helvetica", "18", "bold"))
        self.create_text(960, 360, text="""Press the key you want to assign then
                        click on the button next to the control you want to
                        assign it to""", width=320,
                         font=("Helvetica", "15", "bold"))

    def runGame(self):
        self.inMenu = False
        while not self.pause_active:
            self.gameTick()
            time.sleep(0.02)

    def newLevel(self):
        self.delete("all")
        for i in range(6):
            for j in range(7):
                randomx = random.randint(10+(167*j), 10+(167*(j+1)))
                self.create_polygon(randomx, 110*(i+1),
                                    randomx+self.platform_size, 110*(i+1),
                                    randomx+self.platform_size, (110*(i+1))+10,
                                    randomx, (110*(i+1))+10, fill="#228B22",
                                    outline="#228B22", tags="platform")
                diceroll = random.randint(1, self.platform_size)
                if diceroll <= 6:
                    self.create_image(randomx+(self.platform_size/2),
                                      110*(i+1)-50, image=self.idiamond,
                                      tags="score")
        self.create_polygon(70, 660, 170, 660, 170, 670, 70, 670,
                            fill="#000000", outline="#000000", tags="platform")
        self.create_polygon(1140, 110, 1240, 110, 1240, 120, 1140, 120,
                            fill="#FFD700", outline="#CFB53B",
                            tags=("platform", "win"))
        self.penguin = self.create_image(105, 560, image=self.avatar)
        self.platform_size -= 10

    def image_imports(self):
        self.avatar = tk.PhotoImage(file="assets/avatar.png")
        self.iwork = tk.PhotoImage(file="assets/work.png")
        self.idiamond = tk.PhotoImage(file="assets/diamond.png")

    def whenKeyPressed(self, event):
        self.keyPressed = event.keysym
        if self.keyPressed == self.left_key:
            self.keyStatus["left"] = True
        if self.keyPressed == self.right_key:
            self.keyStatus["right"] = True
        if self.keyPressed == self.jump_key:
            self.keyStatus["up"] = True
        if self.keyPressed == self.drop_key:
            self.keyStatus["down"] = True
        if self.keyPressed == "Escape"and not self.inMenu:
            self.pauseKeyPressed()
        if self.keyPressed == "b" and not self.inMenu:
            self.bossKeyPressed()

    def pauseKeyPressed(self):
        if self.pause_active:
            self.pause_active = False
            self.delete("pause")
            self.runGame()
        else:
            self.pause_active = True
            self.create_rectangle(0, 0, 1280, 720, fill="black",
                                  stipple='gray50', tags="pause")
            self.create_text(640, 360, text="Paused",
                             font=("Helvetica", "48", "bold"), tags="pause")
            self.create_text(100, 100, text=f"Score:{self.score}", anchor="nw",
                             font=("Helvetica", "30", "bold"), tags="pause")

    def bossKeyPressed(self):
        if self.imgOn:
            self.delete(self.work_image)
            self.imgOn = False
        else:
            self.work_image = self.create_image(0, 0, anchor="nw",
                                                image=self.iwork)
            self.imgOn = True

    """Ticks at time intervals, checks and runs everything and progess game
    to next tick
    """
    def gameTick(self):
        self.penguin_coords = self.bbox(self.penguin)  # finds out coordinates
        """Calculates the velocities"""
        self.verticalVelocity()
        self.horizontalVelocity()
        """Moves penguin based off velocities"""
        self.penguinMove()
        """Reset keyboard flags"""
        for key in self.keyStatus:
            self.keyStatus[key] = False
        """Update screen"""
        self.update()
        """Check to see if they got a diamond"""
        self.checkTouchingDiamond()
        """Checks to see if level is completed"""
        if self.checkIfWon():
            self.newLevel()
        """Checks to see if player died"""
        if self.outOfBounds():
            self.menu()

    def outOfBounds(self):
        if self.penguin_coords[1] > 720:
            return True

    def horizontalVelocity(self):
        if self.keyStatus["left"]:
            if self.penguin_velocity_x > -6:
                self.penguin_velocity_x -= 4
        elif self.keyStatus["right"]:
            if self.penguin_velocity_x < 6:
                self.penguin_velocity_x += 4
        elif self.checkTouchingPlatform():
            if self.penguin_velocity_x > 0:
                self.penguin_velocity_x -= 2
            elif self.penguin_velocity_x < 0:
                self.penguin_velocity_x += 2

    def verticalVelocity(self):
        if self.checkTouchingPlatform():
            if self.keyStatus["up"]:
                self.penguin_velocity_y = -16
            elif self.keyStatus["down"]:
                if self.penguin_velocity_y < 16:
                    self.penguin_velocity_y = 8
            elif self.penguin_velocity_y >= 0:
                self.penguin_velocity_y = 0
        else:
            if self.penguin_velocity_y < 16:
                self.penguin_velocity_y += 1

    """If coordinates are overlapping with diamond then it increments score"""
    def checkTouchingDiamond(self):
        overlap = self.find_overlapping(self.penguin_coords[0],
                                        self.penguin_coords[1],
                                        self.penguin_coords[2],
                                        self.penguin_coords[3])
        for item in overlap:
            if "score" in self.gettags(item):
                self.score += 1
                self.delete(item)

    """If bottom coordinates are overlapping with platforms then it is true"""
    def checkTouchingPlatform(self):
        overlap = self.find_overlapping(self.penguin_coords[0],
                                        self.penguin_coords[3],
                                        self.penguin_coords[2],
                                        self.penguin_coords[3])
        for item in overlap:
            if "platform" in self.gettags(item):
                return True
        return False

    def checkIfWon(self):
        """if bottom coordinates are overlapping with winning platform
        then it is true
        """
        overlap = self.find_overlapping(self.penguin_coords[0],
                                        self.penguin_coords[3],
                                        self.penguin_coords[2],
                                        self.penguin_coords[3])
        for item in overlap:
            if "win" in self.gettags(item):
                return True
        return False

    def penguinMove(self):
        self.move(self.penguin, self.penguin_velocity_x,
                  self.penguin_velocity_y)

gameinstance = Game()
root.mainloop()
