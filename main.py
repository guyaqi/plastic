import tkinter as tk
from PIL import Image, ImageTk
import os
import json

PLANE_X = 60
PLANE_Y = 300
TEXT_X = PLANE_X + 20
TEXT_Y = PLANE_Y + 15

LITTLE_PLANE_W = 200
LITTLE_PLANE_H = 30

PLANE1_X = 200
PLANE1_Y = 100
TEXT1_X = 300
TEXT1_Y = PLANE1_Y + 15

PLANE2_X = 200
PLANE2_Y = 200
TEXT2_X = 300
TEXT2_Y = PLANE2_Y + 15

class Game:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'script', '1.json')
        with open(path, 'r', encoding='utf-8') as f:
            res = f.read()
        self.scenes = json.loads(res)['scenes']
        self.scene_index = -1
        self.vars = {'_always':True}

        window = tk.Tk()
        window.title('ddmc')
        window.geometry('600x400')
        window.resizable(0, 0)

        canvas = tk.Canvas(width=600, height=400, highlightthickness=0, borderwidth=0)
        canvas.place(x=0, y=0)

        # photo = ImageTk.PhotoImage(file='assets/black.png')
        # bgid = canvas.create_image(0, 0, image=photo, anchor='nw')

        # photo2 = ImageTk.PhotoImage(file='assets/plane.png')
        # bgid = canvas.create_image(PLANE_X, PLANE_Y, image=photo2, anchor='nw')

        # canvas.create_text(TEXT_X, TEXT_Y, text='你醒了，四处都是黑的', fill='white', anchor='nw')

        self.window = window
        self.canvas = canvas
        # self.v1 = photo
        # self.v2 = bgid
        # self.v3 = photo2
        # self.v4 = bgid
        # window.mainloop()
        self.resource = []
        self.res_plane = ImageTk.PhotoImage(file='assets/plane.png')
        self.res_plane_little = ImageTk.PhotoImage(file='assets/plane_little.png')

    def next_scene(self):
        self.scene_index += 1
        res = self.scenes[self.scene_index]
        return res
    def current_scene(self):
        return self.scenes[self.scene_index]
    
    def render_next_scene(self):
        scene = self.next_scene()
        
        while True:
            if scene['type'] == 'anchor':
                scene = self.next_scene()
            elif scene['type'] == 'action':
                go = scene['go']
                will_jump = self.vars[go['on']] == go['equal']
                if will_jump:
                    for index in range(len(self.scenes)):
                        if self.scenes[index].get('name') == go['anchor']:
                            break
                    self.scene_index = index
                    scene = self.current_scene()
                else:
                    scene = self.next_scene()
            else:
                break

        if scene['type'] == 'normal':
            self.render_normal_scene(scene)
        elif scene['type'] == 'select':
            self.render_select_scene(scene)
        elif scene['type'] == 'end':
            self.render_end_scene(scene)
    
    def render_end_scene(self, scene):
        print('[[end]]')
        bg = self.load_img(scene['image'])
        self.canvas.create_image(0, 0, image=bg, anchor='nw')

    def render_normal_scene(self, scene):
        print('[[normal]]')
        bg = self.load_img(scene['image'])
        self.canvas.create_image(0, 0, image=bg, anchor='nw')
        self.canvas.create_image(PLANE_X, PLANE_Y, image=self.res_plane, anchor='nw')
        self.canvas.create_text(TEXT_X, TEXT_Y, text=scene['text'], fill='white', anchor='nw')
    
    def render_select_scene(self, scene):
        print('[[select]]')
        choices = scene['choice']
        self.canvas.create_image(PLANE1_X, PLANE1_Y, image=self.res_plane_little, anchor='nw')
        self.canvas.create_text(TEXT1_X, TEXT1_Y, text=choices[0]['text'], fill='white')   

        if len(self.current_scene()['choice']) >= 2:
            self.canvas.create_image(PLANE2_X, PLANE2_Y, image=self.res_plane_little, anchor='nw')
            self.canvas.create_text(TEXT2_X, TEXT2_Y, text=choices[1]['text'], fill='white')
    
    def load_img(self, path):
        photo = ImageTk.PhotoImage(file=f'assets/{path}')
        self.resource.append(photo)
        return photo
    
    def on_click(self, e):

        if self.current_scene()['type'] == 'normal':
            self.render_next_scene()
        elif self.current_scene()['type'] == 'select':
            the_choice = None

            if PLANE1_X < e.x < PLANE1_X + LITTLE_PLANE_W and PLANE1_Y < e.y < PLANE1_Y + LITTLE_PLANE_H:
                the_choice = self.current_scene()['choice'][0]
            if len(self.current_scene()['choice']) >= 2:
                if PLANE2_X < e.x < PLANE2_X + LITTLE_PLANE_W and PLANE2_Y < e.y < PLANE2_Y + LITTLE_PLANE_H:
                    the_choice = self.current_scene()['choice'][1]
            
            if the_choice is not None:
                self.vars[the_choice['var']] = the_choice['val']
                self.render_next_scene()
        else:
            print(self.current_scene())

    def start_render(self):
        self.render_next_scene()
    
    def start(self):
        self.start_render()
        def click_handler(e):
            self.on_click(e)
        self.window.bind("<Button-1>", click_handler)
        self.window.mainloop()
        


        

Game().start()
