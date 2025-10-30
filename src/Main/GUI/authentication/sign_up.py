import customtkinter as ctk

class SignUpScreen(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Configure grid to center contents and scale with window
        self.grid_rowconfigure(0, weight=1)   # top spacer
        self.grid_rowconfigure(1, weight=0)   # content row
        self.grid_rowconfigure(2, weight=1)   # bottom spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer
        self.grid_columnconfigure(1, weight=0)  # content column
        self.grid_columnconfigure(2, weight=1)  # right spacer

        # Create a container frame for the centered widgets
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=1)

        # Elements added to center 
        ctk.CTkLabel(content, text="Sign Up", font=("Arial", 56)).pack(pady=30)
        ctk.CTkEntry(content, width=300, height=40, placeholder_text="Username").pack(pady=10)
        ctk.CTkEntry(content, width=300, height=40, placeholder_text="Email").pack(pady=10)
        ctk.CTkEntry(content, width=300, height=40, placeholder_text="Password", show="*").pack(pady=10)

        ctk.CTkButton(content, width=300, height=40, text="Sign-Up", command=lambda: controller.show_frame("")).pack(pady=20)
        ctk.CTkButton(content, width=300, height=40, text="Back", command=lambda: controller.show_frame("WelcomeScreen")).pack(pady=5)