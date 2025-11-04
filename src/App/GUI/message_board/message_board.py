import customtkinter as ctk
import time
from Callers.message_caller import MessageCaller

class MessageBoard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.messageCaller = MessageCaller()
        self.lastMessageIds = set()

        self.configure(fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Chat window
        self.chatArea = ctk.CTkScrollableFrame(self, fg_color="#f0f0f0", corner_radius=10)
        self.chatArea.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 5))
        self.chatArea.grid_columnconfigure(0, weight=1)

        # User input
        bottomFrame = ctk.CTkFrame(self, fg_color="transparent")
        bottomFrame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))
        bottomFrame.grid_columnconfigure(0, weight=1)
        bottomFrame.grid_columnconfigure(1, weight=0)

        # Character count
        self.charCountLabel = ctk.CTkLabel(bottomFrame, text="0 / 1000", anchor="w")
        self.charCountLabel.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Input & send button
        inputFrame = ctk.CTkFrame(bottomFrame, fg_color="transparent")
        inputFrame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        inputFrame.grid_columnconfigure(0, weight=1)
        inputFrame.grid_columnconfigure(1, weight=0)

        # Message entry
        self.messageEntry = ctk.CTkEntry(inputFrame, placeholder_text="Message Here")
        self.messageEntry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.messageEntry.bind("<KeyRelease>", self.updateCharCount)

        # Send button
        sendBtn = ctk.CTkButton(inputFrame, text="Send", command=self.messagePosted)
        sendBtn.grid(row=0, column=1)

    def onShow(self):
        self.pollMessages()
        self.chatArea.after(50, self.scrollToBottom)

    def pollMessages(self):
        try:
            response = self.messageCaller.getMessages(self.controller.userToken)
            messages = response.get("messages")
            for msg in messages:
                msgId = msg.get("message_id")
                if msgId not in self.lastMessageIds:
                    msgUser = msg.get("username")
                    self.lastMessageIds.add(msgId)
                    if msgUser != self.controller.username:
                        self.showMessage(msg.get("username"), msg.get("content"), False)
                    else:
                        self.showMessage(msg.get("username"), msg.get("content"), True)

        except Exception as e:
            print("Error polling messages:", e)

        # Schedule next check (every 2 seconds)
        self.after(1000, self.pollMessages)

    def updateCharCount(self, event=None):
        messageLen = len(self.messageEntry.get())
        self.charCountLabel.configure(text=f"{messageLen} / 1000")

    def messagePosted(self):
        message = self.messageEntry.get()

        if len(message) > 1000:
            return # TODO maybe make an error here
        
        response = self.messageCaller.send(self.controller.userToken, message)
        data = response.json()
        
        # Non-200 responses
        # if not response.ok:
        #     try:
        #         errorData = response.json()
        #         message = errorData.get("message")
        #     except Exception:
        #         message = f"Server error ({response.status_code})"
        #     self.showError(message)
        #     return
        
        self.lastMessageIds.add(data.get("messageId"))
        self.showMessage(self.controller.username, message, True)
        
        self.messageEntry.delete(0, "end")
        self.updateCharCount()

    def showMessage(self, username, message, isMe):
        align = "w" if isMe else "e"
        ctk.CTkLabel(
            self.chatArea,
            text=f"{username}:\n{message}",
            anchor=align,
            justify="left" if align == "w" else "right",
            wraplength=500,
            text_color="black"
        ).pack(fill="x", padx=10, pady=10, anchor=align)
        self.chatArea.after(50, self.scrollToBottom)
        
    def scrollToBottom(self):
        self.chatArea._parent_canvas.yview_moveto(1.0)
        
    def handleEnter(self):
        self.messagePosted()