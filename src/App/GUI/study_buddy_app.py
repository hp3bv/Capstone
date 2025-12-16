import customtkinter as ctk
from GUI.authentication.welcome import WelcomeScreen
from GUI.authentication.login import LoginScreen
from GUI.authentication.sign_up import SignUpScreen
from GUI.message_board.message_board import MessageBoard

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
        for ScreenClass in (WelcomeScreen, LoginScreen, SignUpScreen, MessageBoard):
            frame = ScreenClass(main, self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.userToken = None
        self.username = None
        
        self.bind("<Return>", self.handleEnter)

        self.currFrame = None
        self.showFrame("WelcomeScreen")

    def showFrame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        self.currFrame = frame

        if hasattr(frame, "onShow"):
            frame.onShow()
            
    def handleEnter(self, event=None):
        if hasattr(self.currFrame, "handleEnter"):
            self.currFrame.handleEnter()