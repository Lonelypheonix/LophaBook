import customtkinter as tk
from customtkinter import *
import PyPDF2
import pyttsx3
from customtkinter import filedialog
import pygame
import wave
import os

pygame.mixer.init(frequency=44100, size=-16, channels=2)

#creating GUI Window
root=tk.CTk() 
root.geometry('400x550')
root.title("LophAbook")

tk.CTkLabel(root,text="LophABook").pack()
m=tk.IntVar()
f=tk.IntVar()

pdfReader = None
def browse():
    global pdfReader,filename
    file=filedialog.askopenfilename(title="Select a PDF", filetype=(("PDF FILES","*.pdf"),("All Files","*.*")))
    fil =os.path.basename(file)
    filename = os.path.splitext(fil)[0]
    print(filename)
    pdfReader = PyPDF2.PdfReader(open(file,'rb'))
    pathlabel.configure(text=file)

def save():
    global speaker
    speaker = pyttsx3.init()

    text = ""
    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()
        

    voices = speaker.getProperty('voices')
    if m.get() == 0:
        speaker.setProperty('voice',voices[0].id) #0 for male
    elif f.get() == 1:
        speaker.setProperty('voice',voices[1].id) #1 for female

    print(filename)
    speaker.save_to_file(text,'test.wav',name=filename)
    speaker.runAndWait()
    tk.CTkLabel(root,text="The Audio File is Saved").pack()
    

pathlabel = tk.CTkLabel(root)
pathlabel.pack()

tk.CTkButton(root,text="Browse a File",command=browse).pack()
tk.CTkButton(root,text="Crate and Save the audio file",command=save).pack()

tk.CTkCheckBox(root,text="Male voice",onvalue=0,offvalue=10,variable=m).pack()
tk.CTkCheckBox(root,text="Female voice",onvalue=1,offvalue=10,variable=f).pack()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.song_file = None
        self.playing_time = 0
        self.user_action = True

        self.song_label = tk.CTkLabel(self.root, text="", font=("Arial", 12))
        self.song_label.pack(pady=10)

        #self.browse_button = tk.CTkButton(self.root, text="Browse", command=self.browse_file)
        #self.browse_button.pack()

        self.play_button = tk.CTkButton(self.root, text="Play", command=self.play_song)
        self.play_button.pack(pady=10)

        self.stop_button = tk.CTkButton(self.root, text="Pause", command=self.pause_song)
        self.stop_button.pack(pady=10)

        self.stop_button = tk.CTkButton(self.root, text="Continue", command=self.continue_song)
        self.stop_button.pack(pady=10)

        self.stop_button = tk.CTkButton(self.root, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=10)

        self.playing_time_label = tk.CTkLabel(self.root, text="00:00", font=("Arial", 12))
        self.playing_time_label.pack(pady=10)

        self.slider = tk.CTkSlider(master=root,from_=0,to=0,orientation=HORIZONTAL,command=self.set_playing_time)
        self.slider.pack(padx=20, pady=10)

        #self.time_slider = Scale(self.root, from_=0, to=0, orient=HORIZONTAL, command=self.set_playing_time)
        #self.time_slider.pack(pady=10)

    #def browse_file(self):
     #   file = filedialog.askopenfilename(title="Select a song file", filetypes=(("All files", "."), ("MP3 files", ".mp3"), ("WAV files", ".wav"), ("OGG files", "*.ogg")))
     #   self.song_label.configure(text=file)
     #   self.song_file = file
     

    def play_song(self):
        self.song_file = filename 
        if self.song_file:
            with wave.open(self.song_file, 'rb') as wave_file:
                audio_params = wave_file.getparams()
                pygame.mixer.init(frequency=audio_params[2], channels=audio_params[0])
                audio_data = wave_file.readframes(audio_params[3])
                pygame.mixer.music.load(self.song_file)
                pygame.mixer.music.play(start=self.playing_time)
                song_length = audio_params[3] / audio_params[2]
                self.slider.configure(to=song_length)
                self.update_playing_time()

    def pause_song(self):
        pygame.mixer.music.pause()
 
    def continue_song(self):
        pygame.mixer.music.unpause()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.song_label.configure(text="")
        self.song_file = None
        self.playing_time = 0
        self.user_action = False
        self.slider.set(0)

    def update_playing_time(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            self.user_action = False
            self.slider.set(current_time)
            minutes, seconds = divmod(current_time, 60)
            self.playing_time_label.configure(text="{:02}:{:02}".format(int(minutes), int(seconds)))
            self.job = self.root.after(1000, self.update_playing_time)

    def set_playing_time(self, value):
        if self.user_action:
            self.root.after_cancel(self.job)
            self.playing_time = int(float(value))
            pygame.mixer.music.pause()
            pygame.mixer.music.set_pos(self.playing_time)
            minutes, seconds = divmod(self.playing_time, 60)
            self.playing_time_label.configure(text="{:02}:{:02}".format(int(minutes), int(seconds)))
            self.update_playing_time()
            pygame.mixer.music.unpause()
        else:
            self.user_action = True

music_player = MusicPlayer(root)  

root.mainloop()
