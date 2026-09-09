import tkinter as tk, math, time

class Face:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.c = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.c.pack(fill='both', expand=True)

        self.target_mode = "sleep"
        self.running = True
        self.transition_speed = 0.1

        self.eye_left = self.c.create_oval(0,0,0,0, fill="white", outline="")
        self.eye_right = self.c.create_oval(0,0,0,0, fill="white", outline="")
        self.pupil_left = self.c.create_oval(0,0,0,0, fill="skyblue", outline="")
        self.pupil_right = self.c.create_oval(0,0,0,0, fill="skyblue", outline="")
        self.mouth = self.c.create_oval(0,0,0,0, fill="pink", outline="")
        self.zzz = self.c.create_text(0,0,text="",fill="white",font=("Comic Sans MS",70,"bold"))

        self.current_eye = 160
        self.current_mouth = 60

        self.root.bind("<Escape>", lambda e: self.close())
        self._draw()

    def set_mode(self, mode):
        self.target_mode = mode

    def close(self):
        self.running = False
        self.root.destroy()

    def _draw(self):
        if not self.running: return
        w,h = self.root.winfo_width(), self.root.winfo_height()
        cx,cy = w//2, h//2 - 50
        t = time.time()

        if self.target_mode=="listen":
            te,tm = 160*(1+0.05*math.sin(t*2)), 40
        elif self.target_mode=="talk":
            te,tm = 160, 40+60*abs(math.sin(t*5))
        elif self.target_mode=="sleep":
            te,tm = 20,20
        elif self.target_mode=="think":
            te,tm = 160,60
        else:
            te,tm = 160,60

        self.current_eye += (te-self.current_eye)*0.1
        self.current_mouth += (tm-self.current_mouth)*0.1

        self.c.itemconfig(self.zzz,text="Z z Z" if self.target_mode=="sleep" else "")
        self.c.coords(self.zzz,cx,cy-250)

        self.c.coords(self.eye_left, cx-280, cy-self.current_eye, cx-80, cy+self.current_eye/2)
        self.c.coords(self.eye_right,cx+80, cy-self.current_eye, cx+280, cy+self.current_eye/2)

        if self.target_mode!="sleep":
            self.c.coords(self.pupil_left, cx-190, cy-40, cx-140, cy+10)
            self.c.coords(self.pupil_right,cx+140, cy-40, cx+190, cy+10)
        else:
            self.c.coords(self.pupil_left,-1,-1,-1,-1)
            self.c.coords(self.pupil_right,-1,-1,-1,-1)

        self.c.coords(self.mouth,cx-160,cy+150,cx+160,cy+150+self.current_mouth)
        self.root.after(40,self._draw)

    def run(self):
        self.root.mainloop()

_face=None
def _get():
    global _face
    if not _face: _face=Face()
    return _face

def listen_expression(): _get().set_mode("listen")
def talk_expression(): _get().set_mode("talk")
def sleep_expression(): _get().set_mode("sleep")
def think_expression(): _get().set_mode("think")
def run_face(): _get().run()
