import customtkinter as ctk
from GUI.authentication.welcome import WelcomeScreen
from GUI.authentication.login import LoginScreen
from GUI.authentication.sign_up import SignUpScreen

class StudyBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Study Buddy")
        self.minsize(600,475)
        
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True)
        
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for ScreenClass in (WelcomeScreen, LoginScreen, SignUpScreen):
            frame = ScreenClass(main, self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("WelcomeScreen")
        
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()