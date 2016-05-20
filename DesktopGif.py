from tkinter import * 
from PIL import Image, ImageTk

class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 10

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0], bg='white')

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)  

class WindowDraggable():
	def __init__(self, label):
		self.label = label
		label.bind('<ButtonPress-1>', self.StartMove)
		label.bind('<ButtonRelease-1>', self.StopMove)
		label.bind('<B1-Motion>', self.OnMotion)
	   
	def StartMove(self, event):
		self.x = event.x
		self.y = event.y
		
	def StopMove(self, event):
		self.x = None
		self.y = None
		
	def OnMotion(self,event):
		x = (event.x_root - self.x) 
		y = (event.y_root - self.y) 
		root.geometry("+%s+%s" % (x, y))		

root = Tk()
anim = MyLabel(root, 'original.gif')
WindowDraggable(anim)
root.overrideredirect(True)
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")
root.bind('<Escape>', lambda e: root.destroy())
anim.pack()
root.mainloop()

# def stop_it():
    # anim.after_cancel(anim.cancel)

# Button(root, text='stop', command=stop_it).pack()