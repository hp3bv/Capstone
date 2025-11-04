import customtkinter as ctk
from Callers.login_caller import LoginCaller

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.loginCaller = LoginCaller()
        
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
        ctk.CTkLabel(content, text="Login", font=("Arial", 56)).pack(pady=30)

        # Username / Email entry
        self.credentialEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Username / Email")
        self.credentialEntry.pack(pady=10)

        # Password entry
        self.passwordEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Password", show="*")
        self.passwordEntry.pack(pady=10)

        # Error
        self.errorLabel = ctk.CTkLabel(content, text="", text_color="red")
        self.errorLabel.pack(pady=5)
        self.errorLabel.pack_forget()

        ctk.CTkButton(content, text="Login", width=300, height=40, command=self.handleLogin).pack(pady=20)
        ctk.CTkButton(content, text="Back", width=300, height=40, command=lambda: controller.showFrame("WelcomeScreen")).pack(pady=5)

    def handleLogin(self):
        self.hideError()

        credential = self.credentialEntry.get()
        password = self.passwordEntry.get()

        if not credential or not password:
            self.showError("Must fill out all fields")
            return
        response = self.loginCaller.login(credential, password)
        try:
            data = response.json()
        except:
            self.showError(f"Server error: {response.status_code}")

        # Non-200 responses
        if not response.ok:
            message = data.get("detail")
            self.showError(message)
            return

        if not data.get("success"):
            self.showError(data["message"])
        else:
            self.controller.userToken = data.get("token")
            self.controller.username = data.get("username")
            self.controller.showFrame("MessageBoard")

    def showError(self, message):
        self.errorLabel.configure(text=message)
        self.errorLabel.pack(pady=5)

    def hideError(self):
        self.errorLabel.pack_forget()
        
    def handleEnter(self):
        self.handleLogin()