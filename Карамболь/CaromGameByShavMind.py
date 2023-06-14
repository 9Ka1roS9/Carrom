import math
import tkinter.messagebox
from tkinter import *
import random
from PIL import Image, ImageTk
import tkinter


class CaromGame(Frame):
    def __init__(self):
        self.num_of_game = 0
        self.fallen_white = 0
        self.fallen_black = 0
        self.red_active = False
        self.root = Tk()
        self.root.geometry('1022x545+100+100')
        self.messagebox = tkinter.messagebox
        self.c = 30
        self.w = 450 + 2 * self.c
        self.h = 450 + 2 * self.c
        self.vx, self.vy = float(), float()
        self.s = int()
        self.score = 0
        self.score_m = 0
        self.r = 14
        self.r2 = 9
        self.r3 = 5
        self.a = 3.5
        self.R = 17
        self.R2 = 9
        self.spaceR = 24
        self.sq3 = math.sqrt(3)
        self.line_r = 60
        self.dt = 0.003
        self.fallen = False
        self.process_of_animation = True
        self.view_menu = False
        self.boardimg_full = ImageTk.PhotoImage(Image.open("board.png").resize((520, 520), Image.ANTIALIAS))
        self.boardimg_full_rotate = ImageTk.PhotoImage(
            Image.open("board.png").resize((520, 520), Image.ANTIALIAS).rotate(180))

        self.quin = ImageTk.PhotoImage(
            Image.open("red.png").resize((2 * self.r, 2 * self.r), Image.ANTIALIAS))
        self.reddiskimg = ImageTk.PhotoImage(
            Image.open("black.png").resize((2 * self.r, 2 * self.r), Image.ANTIALIAS))
        self.blackdisk = ImageTk.PhotoImage(
            Image.open("white.png").resize((2 * self.r, 2 * self.r), Image.ANTIALIAS))
        self.whitedisk = ImageTk.PhotoImage(
            Image.open("white.png").resize((2 * self.r, 2 * self.r), Image.ANTIALIAS))
        self.maindisk = ImageTk.PhotoImage(
            Image.open("main_disk.png").resize((2 * self.R, 2 * self.R), Image.ANTIALIAS))
        self.partner = "partner_1"

        self.list_ball, self.list_fallen = list(), list()
        self.n = 18
        self.list_ofxy = [(self.w / 2 + 2 * self.r, self.h / 2),
                          (self.w / 2 - 2 * self.r, self.h / 2), (self.w / 2 + self.r, self.h / 2 - self.sq3 * self.r),
                          (self.w / 2 + self.r, self.h / 2 + self.sq3 * self.r),
                          (self.w / 2 - self.r, self.h / 2 - self.sq3 * self.r),
                          (self.w / 2 - self.r, self.h / 2 + self.sq3 * self.r), (self.w / 2 + 4 * self.r, self.h / 2),
                          (self.w / 2 - 4 * self.r, self.h / 2),
                          (self.w / 2 + 2 * self.r, self.h / 2 - self.sq3 * 2 * self.r),
                          (self.w / 2 + 2 * self.r, self.h / 2 + self.sq3 * 2 * self.r),
                          (self.w / 2 - 2 * self.r, self.h / 2 - self.sq3 * 2 * self.r),
                          (self.w / 2 - 2 * self.r, self.h / 2 + self.sq3 * 2 * self.r),
                          (self.w / 2, self.h / 2 - 4 * self.r),
                          (self.w / 2, self.h / 2 + 4 * self.r),
                          (self.w / 2 + 3 * self.r, self.h / 2 - self.sq3 * self.r),
                          (self.w / 2 + 3 * self.r, self.h / 2 + self.sq3 * self.r),
                          (self.w / 2 - 3 * self.r, self.h / 2 + self.sq3 * self.r),
                          (self.w / 2 - 3 * self.r, self.h / 2 - self.sq3 * self.r)]

        self.canvas = Canvas(self.root, width=self.w, height=self.h, bg="#ac24003b7", bd=0, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky='n')

        self.canvas_m = Canvas(self.root, width=self.w, height=self.h, bg="#ac24003b7", bd=0, highlightthickness=0)
        self.canvas_m.grid(row=1, column=1, sticky='n')

        self.canvas_scale = Canvas(self.root, width=self.w, height="35", bg="#4a1b04", bd=0, highlightthickness=0)
        self.canvas_scale.grid(row=2, column=0, sticky='n')
        self.canvas_scale_m = Canvas(self.root, width=self.w, height="35", bg="#4a1b04", bd=0, highlightthickness=0)
        self.canvas_scale_m.grid(row=2, column=1, padx=2, sticky='n')
        self.canvas_scale.create_image(self.w / 2, 15, image=self.maindisk, tag="main_ball")

        self.design_scaling_canvas()
        self.canvas.bind_all("<KeyPress-Escape>", self.window_menu)

        self.canvas_scale.bind("<B1-Motion>", self.scale_disc)
        self.canvas_scale_m.bind("<B1-Motion>", self.scale_disc_m)

        self.canvas.bind("<B1-Motion>", self.set_maindisc_velocity)
        self.canvas.bind("<ButtonRelease-1>", self.start)

        self.canvas_m.bind("<B1-Motion>", self.set_maindisc_velocity_m)
        self.canvas_m.bind("<ButtonRelease-1>", self.start)


        if self.view_menu:
            try:
                self.menu_master.destroy()
            except Exception:
                pass
            self.view_menu = False
        else:
            self.view_menu = True
            self.menu_master = tkinter.Tk()

            self.menu_master.geometry('%dx%d+%d+%d' % (1022, 565, 100, 100))
            if self.num_of_game == 0:
                self.menu_master.attributes("-topmost", True)
            self.menu_master.configure(background='#F0E68C')
            btn = Button(self.menu_master,
                         text="Новая игра",
                         command=self.new_game,
                         width=18, height=3, compound='center', background='brown')
            btn.pack(pady=25)

            btn_settings = Button(self.menu_master,
                                  text="Правила",
                                  command=self.game_description,
                                  width=18, height=3, background='brown')
            btn_settings.pack(pady=60)

            '''label = Label(self.menu_master,
                          text=f"Правила\n\nРозыгрыш\n\n  Перед началом каждого матча судья прячет в одной руке белую фишку, а в другой — "
                               f"чёрную.\n После этого игроки угадывают, фишка какого цвета в какой руке спрятана. Этот "
                               f"процесс называется розыгрышем или «вызовом фишки».\n  Игрок, победивший в розыгрыше, "
                               f"получает право выбора. Он может выбрать либо право первого удара в игре, либо замены "
                               f"цвета своих фишек (с чёрного на белый).\n Если победитель выбирает право первого удара, "
                               f"проигравший может выбрать смену цвета, но если победитель выбирает смену цвета, "
                               f"то проигравший должен бить первым.\n  В игре два на два команда, одержавшая победу в "
                               f"розыгрыше, имеет право сделать точно такой же выбор, что и при игре один на "
                               f"один.\n\nУдар\n\n  Цель игры загнать в лузы все девять фишек противника до того, "
                               f"как он сделает то же самое с вашими фишками.", font='Arial 9', foreground='black',
                          background='#F0E68C')

            label.pack(pady=15)'''

            btn_exit = Button(self.menu_master,
                              text="Выход",
                              command=self.resume,
                              width=18, height=3, background='brown')
            btn_exit.pack(pady=55)


    def window_menu(self, event=None):
        if self.view_menu:
            try:
                self.menu_master.destroy()
            except Exception:
                pass
            self.view_menu = False
        else:
            self.view_menu = True
            self.menu_master = Tk()

            self.menu_master.geometry('%dx%d+%d+%d' % (1022, 565, 100, 100))
            if self.num_of_game == 0:
                self.menu_master.attributes("-topmost", True)

            self.menu_master.configure(background='#F0E68C')

            btn = Button(self.menu_master,
                         text="Новая игра",
                         command=self.new_game,
                         width=18, height=3, compound='center', background='brown')
            btn.pack(pady=25)

            btn_settings = Button(self.menu_master,
                                  text="Правила",
                                  command=self.game_description,
                                  width=18, height=3, background='brown')
            btn_settings.pack(pady=60)

            btn_exit = Button(self.menu_master,
                              text="Выход",
                              command=self.resume,
                              width=18, height=3, background='brown')
            btn_exit.pack(pady=55)
            self.menu_master.mainloop()

    def resume(self, event=None):
        self.root.quit()

    def game_description(self):
        self.description_menu = tkinter.Tk()
        self.description_menu.configure(background='#F0E68C')
        self.description_menu.geometry('%dx%d+%d+%d' % (1022, 565, 100, 100))
        self.description_menu.attributes("-topmost", True)
        label = Label(self.description_menu,
                      text=f"Правила\n\nРозыгрыш\n\n  Перед началом каждого матча судья прячет в одной руке белую фишку, а в другой — "
                           f"чёрную.\n После этого игроки угадывают, фишка какого цвета в какой руке спрятана.\n Этот "
                           f"процесс называется розыгрышем или «вызовом фишки».\n  Игрок, победивший в розыгрыше, "
                           f"получает право выбора.\n Он может выбрать либо право первого удара в игре, либо замены "
                           f"цвета своих фишек (с чёрного на белый).\n Если победитель выбирает право первого удара, "
                           f"проигравший может выбрать смену цвета,\n но если победитель выбирает смену цвета, "
                           f"то проигравший должен бить первым.\n  В игре два на два команда, одержавшая победу в "
                           f"розыгрыше, \nимеет право сделать точно такой же выбор, что и при игре один на "
                           f"один.\n\nУдар\n\n  Цель игры загнать в лузы все девять фишек противника до того, "
                           f"как он сделает то же самое с вашими фишками.", font='Arial 14', foreground='black',
                      background='#F0E68C')

        label.pack(pady=15)

    def end_game(self):
        self.end_master = Tk()
        self.end_master.configure(background='#F0E68C')
        self.end_master.geometry('%dx%d+%d+%d' % (1022, 565, 100, 100))

        if self.score == self.score_m:
            who_win = 'It is draw'
        elif self.score > self.score_m:
            who_win = 'White win'
        else:
            who_win = 'Black win'

        label = Label(self.end_master,
                      text=f"{who_win}", font='Arial 34', background='#F0E68C')

        label.pack(pady=20)

        btn = Button(self.end_master,
                     text="Restart",
                     command=self.new_game, width=14,
                     height=4, background='#3B14AF')
        btn.pack(pady=20)

        btn_exit = Button(self.end_master,
                          text="Выход",
                          command=self.resume,
                          width=14, height=4, background='#3B14AF')
        btn_exit.pack(pady=15)

        label = Label(self.end_master,
                      text=f"Описание\n\nРозыгрыш\n\n  Перед началом каждого матча судья прячет в одной руке белую фишку, а в другой — "
                           f"чёрную.\n После этого игроки угадывают, фишка какого цвета в какой руке спрятана. Этот "
                           f"процесс называется розыгрышем или «вызовом фишки».\n  Игрок, победивший в розыгрыше, "
                           f"получает право выбора. Он может выбрать либо право первого удара в игре, либо замены "
                           f"цвета своих фишек (с чёрного на белый).\n Если победитель выбирает право первого удара, "
                           f"проигравший может выбрать смену цвета, но если победитель выбирает смену цвета, "
                           f"то проигравший должен бить первым.\n  В игре два на два команда, одержавшая победу в "
                           f"розыгрыше, имеет право сделать точно такой же выбор, что и при игре один на "
                           f"один.", font='Arial 9', foreground='black',
                      background='#F0E68C')
        label.pack()
        self.end_master.attributes("-topmost", True)
        self.end_master.mainloop()

    def scale_disc(self, event):
        if self.line_r + 3 * self.R + self.c - 5 < event.x < self.w - self.line_r - 3 * self.R - self.c + 5 and self.partner == "partner_1" and (
                self.process_of_animation):
            self.canvas_scale.delete("scale_disc")
            self.canvas_scale.create_image(event.x, 15, image=self.maindisk, tag="scale_disc")
            self.main_disc["x"] = event.x
            self.main_disc["y"] = self.h - (self.line_r + self.R + self.c)
            self.canvas.delete("main_ball")
            self.canvas_m.delete("main_ball")
            self.canvas_scale.delete("main_ball")
            self.canvas.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                     tag=self.main_disc["id"])
            self.canvas_m.create_image(self.w - self.main_disc["x"], self.h - self.main_disc["y"], image=self.maindisk,
                                       tag=self.main_disc["id"])

    def scale_disc_m(self, event):
        if self.line_r + 3 * self.R + self.c - 5 < event.x < self.w - self.line_r - 3 * self.R - self.c + 5 and self.partner == "partner_2" and (
                self.process_of_animation):
            self.canvas_scale_m.delete("scale_disc")
            self.canvas_scale_m.create_image(event.x, 15, image=self.maindisk, tag="scale_disc")
            self.main_disc["x"] = event.x
            self.main_disc["y"] = self.h - (self.line_r + self.R + self.c)
            self.canvas.delete("main_ball")
            self.canvas_m.delete("main_ball")
            self.canvas_m.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                       tag=self.main_disc["id"])
            self.canvas.create_image(self.w - self.main_disc["x"], self.h - self.main_disc["y"], image=self.maindisk,
                                     tag=self.main_disc["id"])

    def getsin_cos(self, tantheta, type_trig):
        if type_trig == "sin":
            cot = 1 / tantheta
            cosec = math.sqrt(1 + pow(cot, 2))
            sin = 1 / cosec
            return sin
        elif type_trig == "cos":
            sec = math.sqrt(1 + pow(tantheta, 2))
            cos = 1 / sec
            return cos

    def set_maindisc_velocity(self, event):
        if self.partner == "partner_1" and (
                self.process_of_animation ):
            click_x, click_y = self.main_disc["x"], self.main_disc["y"]
            l = math.sqrt(pow(click_x - event.x, 2) + pow(click_y - event.y, 2))
            self.main_disc["vx"] = 0
            self.main_disc["vy"] = 0
            self.canvas.delete("vline")
            self.canvas.create_line(click_x, click_y, click_x + (click_x - event.x), click_y - (event.y - click_y),
                                    fill="blue2",
                                    tag="vline", width="1.2")
            self.canvas.create_line(event.x, event.y, click_x, click_y, fill="yellow", tag="vline", width="2",
                                    dash=(200, 1))
            self.canvas.create_oval(click_x - l, click_y - l, click_x + l, click_y + l, outline="blue2", tag="vline",
                                    width="1.2",
                                    dash=(2, 2))
            try:
                self.main_disc["vx"] = 40 * l * ((click_x - event.x) / l)
                self.main_disc["vy"] = 40 * l * ((event.y - click_y) / l)
            except Exception:
                self.main_disc["vx"] = 0
                self.main_disc["vy"] = 0
            while self.main_disc["vy"] >= 3000:
                self.main_disc["vx"] -= 40 * l * ((click_x - event.x) / l) / 10
                self.main_disc["vy"] -= 40 * l * ((event.y - click_y) / l) / 10

    def set_maindisc_velocity_m(self, event):
        if self.partner == "partner_2" and (
                self.process_of_animation):
            click_x, click_y = self.main_disc["x"], self.main_disc["y"]
            l = math.sqrt(pow(click_x - event.x, 2) + pow(click_y - event.y, 2))
            try:
                self.main_disc["vx"] = 40 * l * ((click_x - event.x) / l)
                self.main_disc["vy"] = 40 * l * ((event.y - click_y) / l)
            except:
                self.main_disc["vx"] = 0
                self.main_disc["vy"] = 0
            while self.main_disc["vy"] >= 3000:
                self.main_disc["vx"] -= 40 * l * ((click_x - event.x) / l) / 10
                self.main_disc["vy"] -= 40 * l * ((event.y - click_y) / l) / 10
            self.canvas_m.delete("vline")
            self.canvas_m.create_line(click_x, click_y, click_x + (click_x - event.x), click_y - (event.y - click_y),
                                      fill="blue2",
                                      tag="vline", width="1.2")
            self.canvas_m.create_line(event.x, event.y, click_x, click_y, fill="yellow", tag="vline", width="2",
                                      dash=(200, 1))
            self.canvas_m.create_oval(click_x - l, click_y - l, click_x + l, click_y + l, outline="blue2", tag="vline",
                                      width="1.2",
                                      dash=(2, 2))

    def set_velocity(self, ball_1, ball_2):
        e = 0.9
        l = math.sqrt(pow(ball_1["y"] - ball_2["y"], 2) + pow(ball_1["x"] - ball_2["x"], 2))
        try:
            sin = (ball_1["y"] - ball_2["y"]) / l
            cos = (ball_2["x"] - ball_1["x"]) / l
        except Exception:
            sin = 0
            cos = 0
        vx1 = ball_1["vx"]
        vx2 = ball_2["vx"]

        vy1 = ball_1["vy"]
        vy2 = ball_2["vy"]

        k1 = (vx1 - vx2) * cos + (vy1 - vy2) * sin
        v1 = k1 * (1 - e) / 2
        v2 = k1 * (1 + e) / 2
        ball_1["vx"] = v1 * cos + (vx1 * sin - vy1 * cos) * sin + vx2
        ball_1["vy"] = v1 * sin + (vy1 * cos - vx1 * sin) * cos + vy2
        ball_2["vx"] = v2 * cos + vx2
        ball_2["vy"] = v2 * sin + vy2

    def start(self, event):

        self.process_of_animation = False

        def check_impact_with_maindisk():
            for b in self.list_ball:
                if math.sqrt(
                        pow(b["y"] - self.main_disc["y"], 2) + pow(b["x"] - self.main_disc["x"], 2)) < self.r + self.R:
                    self.set_velocity(b, self.main_disc)
                    l1 = math.sqrt(pow(b["y"] - self.main_disc["y"], 2) + pow(b["x"] - self.main_disc["x"], 2))
                    try:
                        b["x"] = self.main_disc["x"] + (self.R + self.r) * ((b["x"] - self.main_disc["x"]) / l1)
                        b["y"] = self.main_disc["y"] - (self.R + self.r) * ((self.main_disc["y"] - b["y"]) / l1)
                    except Exception:
                        b["x"] = 0
                        b["y"] = 0

        def check_collide_with_walls_maindisk():
            if self.main_disc["x"] + self.R > self.w - self.c:
                self.main_disc["vx"] = -0.8 * self.main_disc["vx"]
                self.main_disc["x"] = self.w - self.R - self.c
            if self.main_disc["x"] - self.R < self.c:
                self.main_disc["vx"] = -0.8 * self.main_disc["vx"]
                self.main_disc["x"] = self.R + self.c
            if self.main_disc["y"] + self.R > self.h - self.c:
                self.main_disc["vy"] = -0.8 * self.main_disc["vy"]
                self.main_disc["y"] = self.h - self.R - self.c
            if self.main_disc["y"] - self.R < self.c:
                self.main_disc["vy"] = -0.8 * self.main_disc["vy"]
                self.main_disc["y"] = self.R + self.c

        self.s = 1
        self.canvas.delete("vline")
        self.canvas_m.delete("vline")
        self.fallen = False
        self.fallen_black = 0
        self.fallen_white = 0
        while self.s == 1:
            check_impact_with_maindisk()
            check_collide_with_walls_maindisk()
            am = -self.a * self.main_disc["vx"]
            an = -self.a * self.main_disc["vy"]
            self.main_disc["vx"] += am * self.dt
            self.main_disc["vy"] += an * self.dt
            if -10 <= self.main_disc["vx"] <= 10 and self.main_disc["vx"] != 0:
                self.main_disc["vx"] = 0
                self.main_disc["vy"] = 0
            self.main_disc["x"] += self.main_disc["vx"] * self.dt
            self.main_disc["y"] += (-self.main_disc["vy"] * self.dt)

            self.canvas.delete("main_ball")
            self.canvas_m.delete("main_ball")
            if self.partner == "partner_1":
                self.canvas.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                         tag=self.main_disc["id"])
                self.canvas_m.create_image(self.w - self.main_disc["x"], self.h - self.main_disc["y"],
                                           image=self.maindisk, tag=self.main_disc["id"])
            else:
                self.canvas_m.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                           tag=self.main_disc["id"])
                self.canvas.create_image(self.w - self.main_disc["x"], self.h - self.main_disc["y"],
                                         image=self.maindisk, tag=self.main_disc["id"])

            remove_disks = []

            for b1 in self.list_ball:
                for b2 in self.list_ball:
                    if not (b1 == b2) and not (b2 in remove_disks):
                        if math.sqrt(pow(b1["y"] - b2["y"], 2) + pow(b1["x"] - b2["x"], 2)) < 2 * self.r:
                            self.set_velocity(b1, b2)
                            l = math.sqrt(pow(b1["y"] - b2["y"], 2) + pow(b1["x"] - b2["x"], 2))
                            try:
                                b2["x"] = b1["x"] + 2 * self.r * ((b2["x"] - b1["x"]) / (l))
                                b2["y"] = b1["y"] - 2 * self.r * ((b1["y"] - b2["y"]) / (l))
                            except Exception:
                                b2["x"] = 0
                                b2["y"] = 0
                ax = -self.a * b1["vx"]
                ay = -self.a * b1["vy"]
                b1["vx"] += ax * self.dt
                b1["vy"] += ay * self.dt

                if 10 >= b1['vx'] >= -10 and b1['vx'] != 0:
                    b1['vx'] = 0
                if 10 >= b1['vx'] >= -10 and b1['vy'] != 0:
                    b1['vy'] = 0

                if b1['vx'] > 1400:
                    b1['vx'] = 1400
                if b1['vy'] > 1400:
                    b1['vy'] = 1400
                b1["x"] += b1["vx"] * self.dt
                b1["y"] += (-b1["vy"] * self.dt)
                if b1["x"] + self.r > self.w - self.c:
                    b1["vx"] = -0.8 * b1["vx"]
                    b1["x"] = self.w - self.r - self.c
                if b1["x"] - self.r < self.c:
                    b1["vx"] = -0.8 * b1["vx"]
                    b1["x"] = self.r + self.c
                if b1["y"] + self.r > self.h - self.c:
                    b1["vy"] = -0.8 * b1["vy"]
                    b1["y"] = self.h - self.c - self.r
                if b1["y"] - self.r < self.c:
                    b1["vy"] = -0.8 * b1["vy"]
                    b1["y"] = self.c + self.r


                self.canvas.delete(b1["id"])
                self.canvas_m.delete(b1["id"])
                if b1['color'] == 'red':
                    if self.partner == "partner_1":
                        self.canvas.create_image(b1["x"], b1["y"], image=self.quin, tag=b1["id"])
                        self.canvas_m.create_image(self.w - b1["x"], self.h - b1["y"], image=self.quin,
                                                   tag=b1["id"])
                    else:
                        self.canvas_m.create_image(b1["x"], b1["y"], image=self.quin, tag=b1["id"])
                        self.canvas.create_image(self.w - b1["x"], self.h - b1["y"], image=self.quin,
                                                 tag=b1["id"])
                elif b1["color"] == 1:
                    if self.partner == "partner_1":
                        self.canvas.create_image(b1["x"], b1["y"], image=self.reddiskimg, tag=b1["id"])
                        self.canvas_m.create_image(self.w - b1["x"], self.h - b1["y"], image=self.reddiskimg,
                                                   tag=b1["id"])
                    else:
                        self.canvas_m.create_image(b1["x"], b1["y"], image=self.reddiskimg, tag=b1["id"])
                        self.canvas.create_image(self.w - b1["x"], self.h - b1["y"], image=self.reddiskimg,
                                                 tag=b1["id"])
                else:
                    if self.partner == "partner_1":
                        self.canvas.create_image(b1["x"], b1["y"], image=self.blackdisk, tag=b1["id"])
                        self.canvas_m.create_image(self.w - b1["x"], self.h - b1["y"], image=self.blackdisk,
                                                   tag=b1["id"])
                    else:
                        self.canvas_m.create_image(b1["x"], b1["y"], image=self.blackdisk, tag=b1["id"])
                        self.canvas.create_image(self.w - b1["x"], self.h - b1["y"], image=self.blackdisk,
                                                 tag=b1["id"])


                if (math.sqrt(pow(b1["x"] - (self.spaceR + self.c), 2) + pow(b1["y"] - (self.spaceR + self.c),
                                                                             2)) < self.spaceR - self.r
                    or math.sqrt(pow(b1["x"] - (self.w - self.spaceR - self.c), 2) + pow(
                            b1["y"] - (self.spaceR + self.c), 2)) < self.spaceR - self.r
                    or math.sqrt(pow(b1["x"] - (self.spaceR + self.c), 2) + pow(
                            b1["y"] - (self.h - self.spaceR - self.c), 2)) < self.spaceR - self.r
                    or math.sqrt(pow(b1["x"] - (self.w - self.spaceR - self.c), 2) + pow(
                            b1["y"] - (self.h - self.spaceR - self.c), 2)) < self.spaceR - self.r) and (
                        abs(b1["vx"] < 3000)) and abs(b1["vy"]) < 3000:

                    if b1['color'] == 'red':
                        self.red_active = True
                    elif b1['color'] == 0:
                        self.fallen_white += 1
                        self.score += 1
                    else:
                        self.fallen_black += 1
                        self.score_m += 1

                    if b1['color'] == 0 and self.red_active and self.score == 9:
                        self.end_game()
                    elif b1['color'] == 1 and self.red_active and self.score_m == 9:
                        self.end_game()

                    if b1['color'] == 'red' and self.partner == 'partner_1' and self.score == 9:
                        self.end_game()
                    elif b1['color'] == 'red' and self.partner == 'partner_2' and self.score_m == 9:
                        self.end_game()

                    self.list_fallen.append(b1)
                    self.list_ball.remove(b1)
                    self.fallen = True
                    self.canvas.delete(b1["id"])
                    self.canvas_m.delete(b1["id"])

                    self.canvas.delete('score')
                    self.canvas_m.delete('score_m')
                    self.canvas_m.create_text(245, 14,
                                              text=f"{self.score_m}", justify=CENTER, tags='score_m', font="Arial 23",
                                              fill="white")
                    self.canvas.create_text(245, 14,
                                            text=f"{self.score}", justify=CENTER, tags='score', font="Arial 23",
                                            fill="white")

                    self.canvas.create_rectangle((225, 0), (265, 28), width=4, outline='grey')
                    self.canvas_m.create_rectangle((225, 0), (265, 28), width=4, outline='grey')
                n = 0
                if abs(self.main_disc["vx"]) < 0.1 and abs(self.main_disc["vy"]) < 0.1:
                    n += 1
                for disk in self.list_ball:
                    if abs(disk["vx"]) < 2 and abs(disk["vy"]) < 2:
                        n += 1
                    if n == len(self.list_ball) + 1:
                        if self.fallen:
                            if self.partner == "partner_1":
                                self.partner = "partner_2"
                            else:
                                self.partner = "partner_1"
                        self.process_of_animation = True
                        self.new()

                remove_disks.append(b1)

            self.canvas.update()
            self.canvas_m.update()
            self.canvas.after(int(self.dt * 1000))

    def new(self):
        if self.partner == "partner_1":
            self.partner = "partner_2"
        else:
            self.partner = "partner_1"
        self.main_disc["vx"] = 0
        self.main_disc["vy"] = 0
        self.main_disc["x"] = self.w / 2
        self.main_disc["y"] = self.h - self.line_r - self.R - self.c
        self.s = 0
        self.canvas.delete("main_ball")
        if self.partner == "partner_1":
            self.canvas.delete("main_ball")
            self.canvas.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                     tag=self.main_disc["id"])
            self.canvas_scale.delete("scale_disc")
            self.canvas_scale.create_image(self.main_disc["x"], 15, image=self.maindisk, tag="scale_disc")
        else:
            self.canvas_m.delete("main_ball")
            self.canvas_m.create_image(self.main_disc["x"], self.main_disc["y"], image=self.maindisk,
                                       tag=self.main_disc["id"])
            self.canvas_scale_m.delete("scale_disc")
            self.canvas_scale_m.create_image(self.main_disc["x"], 15, image=self.maindisk, tag="scale_disc")
        if not (self.fallen):
            self.invert_disks()

    def invert_disks(self):
        for ball in self.list_ball:
            ball["x"] = self.w - ball["x"]
            ball["y"] = self.h - ball["y"]

    def new_game(self):
        '''try:
            self.menu_master.attributes("-topmost", False)
        except Exception:
            pass'''
        self.red_active = False
        self.root.attributes("-topmost", False)
        if self.num_of_game == 0:
            self.root.attributes("-topmost", True)
        self.num_of_game += 0
        self.score = 0
        self.score_m = 0
        try:
            self.menu_master.destroy()
        except Exception:
            pass
        try:
            self.end_master.destroy()
        except Exception:
            pass
        self.list_ball = []
        self.canvas.delete(ALL)
        self.canvas_m.delete(ALL)
        self.canvas.delete('main_ball')
        for i in range(0, self.n):
            self.canvas.delete(f"{i}ball")
            self.canvas_m.delete(f"{i}ball")
        self.canvas.delete("main_ball")
        self.canvas_m.delete("main_ball")
        self.canvas_scale.delete("main_ball")
        self.canvas_scale_m.delete("main_ball")
        self.process_of_animation = True
        self.canvas.create_image(260, 260, image=self.boardimg_full)
        self.canvas_m.create_image(260, 260, image=self.boardimg_full)

        self.canvas_m.create_text(245, 14,
                                  text=f"{self.score_m}", justify=CENTER, tags='score_m', font="Arial 23", fill="white")
        self.canvas.create_text(245, 14,
                                text=f"{self.score_m}", justify=CENTER, tags='score', font="Arial 23", fill="white")

        self.canvas.create_rectangle((225, 0), (265, 28), width=4, outline='grey')
        self.canvas_m.create_rectangle((225, 0), (265, 28), width=4, outline='grey')
        white_count = 0
        black_count = 0
        for i in range(0, self.n):
            if white_count <= 8 and black_count <= 8:
                color = random.randint(0, 1)
                if color == 0:
                    white_count += 1
                else:
                    black_count += 1
            elif white_count == 9:
                color = 1
                black_count += 1
            elif black_count == 9:
                color = 0
                white_count += 1
            x = random.randrange(self.r, self.w - self.r)
            y = random.randrange(self.r, self.h - self.r)
            ball = {"x": self.list_ofxy[i][0],
                    "y": self.list_ofxy[i][1],
                    "vx": 0,
                    "vy": 0,
                    "id": f"{i}ball",
                    "color": color,
                    }
            self.list_ball.append(ball)
        self.quin_ball = {"x": self.w / 2,
                          "y": self.h / 2,
                          "vx": 0,
                          "vy": 0,
                          "id": "quin",
                          "color": 'red'
                          }
        self.main_disc = {"x": self.w / 2,
                          "y": 400,
                          "vx": 0,
                          "vy": 0,
                          "id": "main_ball",
                          }
        self.list_ball.append(self.quin_ball)
        for b in self.list_ball:
            if b["color"] == 'red':
                self.canvas.create_image(b["x"], b["y"], image=self.quin, tag=b["id"])
                self.canvas_m.create_image(self.w - b["x"], self.h - b["y"], image=self.quin, tag=b["id"])
            elif b["color"] == 0:
                self.canvas.create_image(b["x"], b["y"], image=self.blackdisk, tag=b["id"])
                self.canvas_m.create_image(self.w - b["x"], self.h - b["y"], image=self.blackdisk, tag=b["id"])
            else:
                self.canvas.create_image(b["x"], b["y"], image=self.reddiskimg, tag=b["id"])
                self.canvas_m.create_image(self.w - b["x"], self.h - b["y"], image=self.reddiskimg, tag=b["id"])

    def design_scaling_canvas(self):
        color_scale = ["#f46925", "#e9530a", "#d24b08", "#b84208", "#a33a07"]
        k = 0
        for i in range(25, 0, -5):
            center_x11, center_y11 = self.line_r + 3 * self.R + self.c - 5 - i, 35 / 2
            self.canvas_scale.create_oval(center_x11 - 35 / 2, center_y11 - 35 / 2, center_x11 + 35 / 2,
                                          center_y11 + 35 / 2,
                                          fill=color_scale[k], outline=color_scale[k])
            self.canvas_scale_m.create_oval(center_x11 - 35 / 2, center_y11 - 35 / 2, center_x11 + 35 / 2,
                                            center_y11 + 35 / 2,
                                            fill=color_scale[k], outline=color_scale[k])

            center_x22, center_y22 = self.w - self.line_r - 3 * self.R - self.c + 5 + i, 35 / 2
            self.canvas_scale.create_oval(center_x22 - 35 / 2, center_y22 - 35 / 2, center_x22 + 35 / 2,
                                          center_y22 + 35 / 2,
                                          fill=color_scale[k], outline=color_scale[k])
            self.canvas_scale_m.create_oval(center_x22 - 35 / 2, center_y22 - 35 / 2, center_x22 + 35 / 2,
                                            center_y22 + 35 / 2,
                                            fill=color_scale[k], outline=color_scale[k])
            k += 1
        center_x1, center_y1 = self.line_r + 3 * self.R + self.c - 5, 35 / 2
        self.canvas_scale.create_oval(center_x1 - 35 / 2, center_y1 - 35 / 2, center_x1 + 35 / 2, center_y1 + 35 / 2,
                                      fill="#7c2f09", outline="#7c2f09")
        self.canvas_scale_m.create_oval(center_x1 - 35 / 2, center_y1 - 35 / 2, center_x1 + 35 / 2, center_y1 + 35 / 2,
                                        fill="#7c2f09", outline="#7c2f09")

        center_x2, center_y2 = self.w - self.line_r - 3 * self.R - self.c + 5, 35 / 2
        self.canvas_scale.create_oval(center_x2 - 35 / 2, center_y2 - 35 / 2, center_x2 + 35 / 2, center_y2 + 35 / 2,
                                      fill="#7c2f09", outline="#7c2f09")
        self.canvas_scale_m.create_oval(center_x2 - 35 / 2, center_y2 - 35 / 2, center_x2 + 35 / 2, center_y2 + 35 / 2,
                                        fill="#7c2f09", outline="#7c2f09")

        self.canvas_scale.create_rectangle(center_x1, 0, center_x2, 35, fill="#7c2f09", outline="#7c2f09")
        self.canvas_scale_m.create_rectangle(center_x1, 0, center_x2, 35, fill="#7c2f09", outline="#7c2f09")


def main():
    CaromGame().root.mainloop()


if __name__ == "__main__":
    main()
