import customtkinter as ctk
from Callers.message_caller import MessageCaller
from Callers.group_caller import GroupCaller

class MessageBoard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.messageCaller = MessageCaller()
        self.groupCaller = GroupCaller()
        
        # State variables
        self.lastMessageIds = set()
        self.currentGroupId = None
        self.groupButtons = {} # To keep track of buttons for highlighting

        self.configure(fg_color="transparent")

        # --- Main Layout Configuration ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Sidebar (Fixed/Content width)
        self.grid_columnconfigure(1, weight=1) # Chat Area (Expandable)

        # ==============================
        # LEFT COLUMN: Group Selector
        # ==============================
        self.sidebarFrame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        self.sidebarFrame.grid_rowconfigure(1, weight=1)
        self.sidebarFrame.grid_columnconfigure(0, weight=1)

        # Sidebar Header
        self.sidebarLabel = ctk.CTkLabel(self.sidebarFrame, text="Your Groups", font=("Arial", 16, "bold"))
        self.sidebarLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Scrollable Group List
        self.groupListFrame = ctk.CTkScrollableFrame(self.sidebarFrame, fg_color="transparent")
        self.groupListFrame.grid(row=1, column=0, sticky="nsew")

        # ==============================
        # RIGHT COLUMN: Chat Interface
        # ==============================
        self.chatContainer = ctk.CTkFrame(self, fg_color="transparent")
        self.chatContainer.grid(row=0, column=1, sticky="nsew")
        
        self.chatContainer.grid_rowconfigure(0, weight=1) # Chat area
        self.chatContainer.grid_rowconfigure(1, weight=0) # Input area
        self.chatContainer.grid_columnconfigure(0, weight=1)

        # 1. Chat Display Area
        self.chatArea = ctk.CTkScrollableFrame(self.chatContainer, fg_color="#f0f0f0", corner_radius=10)
        self.chatArea.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 5))
        self.chatArea.grid_columnconfigure(0, weight=1)

        # 2. Input Area Container
        self.inputContainer = ctk.CTkFrame(self.chatContainer, fg_color="transparent")
        self.inputContainer.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))
        self.inputContainer.grid_columnconfigure(0, weight=1)

        # Character count
        self.charCountLabel = ctk.CTkLabel(self.inputContainer, text="0 / 1000", anchor="w")
        self.charCountLabel.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Input Wrapper
        inputFrame = ctk.CTkFrame(self.inputContainer, fg_color="transparent")
        inputFrame.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        inputFrame.grid_columnconfigure(0, weight=1)
        inputFrame.grid_columnconfigure(1, weight=0)

        # Message Entry
        self.messageEntry = ctk.CTkEntry(inputFrame, placeholder_text="Select a group to chat...")
        self.messageEntry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.messageEntry.bind("<KeyRelease>", self.updateCharCount)
        self.messageEntry.bind("<Return>", lambda event: self.handleEnter()) # Bind Enter key
        
        # Disable entry until group selected
        self.messageEntry.configure(state="disabled")

        # Send Button
        self.sendBtn = ctk.CTkButton(inputFrame, text="Send", command=self.messagePosted)
        self.sendBtn.grid(row=0, column=1)
        self.sendBtn.configure(state="disabled")

    def onShow(self):
        """Called when this view is brought to front"""
        self.populateGroups()
        # Start polling loop
        self.pollMessages()

    def populateGroups(self):
        """Fetches groups and builds the sidebar buttons"""
        # Clear existing buttons
        for widget in self.groupListFrame.winfo_children():
            widget.destroy()
        self.groupButtons = {}

        try:
            response = self.groupCaller.getGroupsForUser(self.controller.userToken)
            groups = response.get("data", [])

            for group in groups:
                btn = ctk.CTkButton(
                    self.groupListFrame, 
                    text=group["group_name"],
                    fg_color="transparent",
                    border_width=1,
                    text_color=("gray10", "#DCE4EE"),
                    anchor="w",
                    command=lambda g=group: self.selectGroup(g)
                )
                btn.pack(fill="x", pady=2, padx=5)
                self.groupButtons[group["group_id"]] = btn

            # Optional: Select first group automatically
            if groups:
                self.selectGroup(groups[0])

        except Exception as e:
            print("Error fetching groups:", e)

    def selectGroup(self, group):
        """Switches the active chat context"""
        if self.currentGroupId == group["group_id"]:
            return

        self.currentGroupId = group["group_id"]
        
        # 1. Update UI Visuals (Highlight selected)
        for gid, btn in self.groupButtons.items():
            if gid == self.currentGroupId:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

        # 2. Enable Inputs
        self.messageEntry.configure(state="normal", placeholder_text=f"Message #{group["group_name"]}")
        self.sendBtn.configure(state="normal")
        self.messageEntry.focus()

        # 3. Clear Chat Area
        for widget in self.chatArea.winfo_children():
            widget.destroy()
        
        # 4. Reset Message Tracking
        self.lastMessageIds.clear()
        
        # 5. Immediate Poll
        # (The polling loop is running, but we can force a fetch now)
        # We don't call pollMessages directly to avoid creating double loops,
        # usually tracking ids clearing is enough for the next loop to catch it.

    def pollMessages(self):
        if self.currentGroupId is not None:
            try:
                response = self.messageCaller.getMessages(self.controller.userToken, self.currentGroupId)
                
                # Check if valid response
                if response: 
                    messages = response.get("messages", [])
                    for msg in messages:
                        msgId = msg.get("message_id")
                        if msgId not in self.lastMessageIds:
                            self.lastMessageIds.add(msgId)
                            
                            username = msg.get("username")
                            content = msg.get("content")
                            isMe = (username == self.controller.username)
                            
                            self.showMessage(username, content, isMe)
            except Exception as e:
                print(f"Error polling messages for group {self.currentGroupId}:", e)

        # Schedule next check
        self.after(1000, self.pollMessages)

    def updateCharCount(self, event=None):
        if self.messageEntry.cget("state") == "disabled":
            return
        messageLen = len(self.messageEntry.get())
        self.charCountLabel.configure(text=f"{messageLen} / 1000")

    def messagePosted(self):
        if self.currentGroupId is None:
            return

        message = self.messageEntry.get()
        if not message or len(message) > 1000:
            return 
        
        try:
            response = self.messageCaller.send(self.controller.userToken, self.currentGroupId, message)
            
            data = response.json()
            
            if data.get("messageId"):
                self.lastMessageIds.add(data.get("messageId"))
            
            self.showMessage(self.controller.username, message, True)
            
            self.messageEntry.delete(0, "end")
            self.updateCharCount()
            
        except Exception as e:
            print("Error sending message:", e)

    def showMessage(self, username, message, isMe):
        # Determine alignment and colors
        align = "e" if isMe else "w"  # e = right (Me), w = left (Others)
        bg_color = "#DCF8C6" if isMe else "#FFFFFF" # Light Green for me, White for others
        
        # Container for the bubble (to help with alignment)
        bubble_frame = ctk.CTkFrame(self.chatArea, fg_color="transparent")
        bubble_frame.pack(fill="x", pady=5, anchor=align)

        # The Message Bubble
        # We use a button or label with corner radius to look like a bubble
        bubble = ctk.CTkLabel(
            bubble_frame,
            text=f"{username}:\n{message}",
            fg_color=bg_color,
            text_color="black",
            corner_radius=10,
            justify="left",
            wraplength=400, # Wrap text
            width=20 # Minimum width
        )
        
        # Pack with different padding based on alignment
        if isMe:
            bubble.pack(side="right", padx=(50, 10)) 
        else:
            bubble.pack(side="left", padx=(10, 50))

        # Auto-scroll
        self.chatArea.after(50, self.scrollToBottom)

    def scrollToBottom(self):
        try:
            self.chatArea._parent_canvas.yview_moveto(1.0)
        except:
            pass
            
    def handleEnter(self):
        self.messagePosted()