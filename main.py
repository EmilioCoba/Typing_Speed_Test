import customtkinter as ctk
import requests
import random
url = "https://random-word-api.herokuapp.com/all"

class SpeedTest:
    def __init__(self):
        self.time = 60
        self.words = 0
        self.words_list=[]
        self.current_word = ""
        self.mistakes=0

        self.app = ctk.CTk()
        self.app.title("Speed Test")
        self.app.geometry("600x600")
        self.response = requests.get(url)
        self.words_list=self.response.json()

        self.initialize_app()

    def initialize_app(self):
        self.label_title = ctk.CTkLabel(
            self.app,
            text="WELCOME TO TYPING SPEED TEST!",
            font=("Arial Bold", 20)
        )
        self.label_title.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=110,
            pady=20
        )

        self.ready_button = ctk.CTkButton(
            self.app,
            text="READY!",
            command=self.game_prepare,
            font=("Arial Bold", 20)
        )
        self.ready_button.grid(
            row=1,
            column=0,
            padx=200,
            pady=20
        )

    def game_prepare(self):
        self.ready_button.destroy()

        self.time_in_game = ctk.CTkLabel(
            self.app,
            text="Time: 30",
            font=("Arial Bold", 20)
        )
        self.time_in_game.grid(
            row=1,
            column=0,
            padx=20,
            pady=20
        )

        self.words_per_min = ctk.CTkLabel(
            self.app,
            text="Words/Minutes: 0",
            font=("Arial Bold", 20)
        )
        self.words_per_min.grid(
            row=1,
            column=1,
            padx=20,
            pady=20
        )
        self.words_mistake = ctk.CTkLabel(
            self.app,
            text="Mistakes: 0",
            font=("Arial Bold", 20)
        )
        self.words_mistake.grid(
            row=1,
            column=2,
            padx=20,
            pady=20
        )

        self.word_to_type = ctk.CTkLabel(
            self.app,
            text="Press Start!",
            font=("Arial Bold", 20)
        )
        self.word_to_type.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=20,
            pady=20
        )

        self.user_entry = ctk.CTkEntry(
            self.app,
            state="disabled",
            width=200
        )
        self.user_entry.grid(
            row=3,
            column=1,
            padx=20,
            pady=20
        )

        # Pressing Enter checks the word
        self.user_entry.bind("<Return>", self.check_word)

        self.start_button = ctk.CTkButton(
            self.app,
            text="Start",
            fg_color="green",
            command=self.start_game,
            font=("Arial Bold", 20)
        )
        self.start_button.grid(
            row=4,
            column=0,
            padx=20,
            pady=20
        )

        self.restart_button = ctk.CTkButton(
            self.app,
            text="Restart",
            fg_color="red",
            command=self.restart_game,
            font=("Arial Bold", 20),
            state="disabled"
        )
        self.restart_button.grid(
            row=4,
            column=2,
            padx=20,
            pady=20
        )

    def get_word(self):
        self.current_word =random.choice(self.words_list)
        self.word_to_type.configure(
            text=self.current_word
        )

    def start_game(self):
        self.time =60
        self.words = 0
        self.mistakes=0

        self.start_button.configure(state="disabled")
        self.restart_button.configure(state="disabled")
        self.user_entry.configure(state="normal")

        self.user_entry.delete(0, "end")
        self.user_entry.focus()

        self.get_word()

        self.timer()

    def timer(self):
        if self.time > 0:
            self.time -= 1

            self.time_in_game.configure(
                text=f"Time: {self.time}"
            )

            # Update words per minute
            self.words_per_min.configure(
                text=f"Words/Minutes: {self.words}"
            )
            self.words_mistake.configure(
                text=f"Mistakes : {self.mistakes}"
            )

            self.app.after(1000, self.timer)

        else:
            self.end_game()

    def check_word(self, event=None):
        typed_word = self.user_entry.get().strip()

        if typed_word == self.current_word:
            self.words += 1

            self.words_per_min.configure(
                text=f"Words/Minute: {self.words}"
            )

            self.user_entry.delete(0, "end")

            self.get_word()
        else :
            self.words += 1
            self.mistakes += 1
            self.user_entry.delete(0, "end")
            self.get_word()


    def end_game(self):
        self.user_entry.configure(state="disabled")
        self.start_button.configure(state="normal")
        self.restart_button.configure(state="normal")

        self.word_to_type.configure(
            text=f"Game Over! You typed {self.words} words and made {self.mistakes} mistakes."
        )

    def restart_game(self):
        self.time = 60
        self.words = 0
        self.mistakes=0
        self.current_word = ""

        self.time_in_game.configure(text="Time: 30")
        self.words_per_min.configure(text="Words/Minute: 0")
        self.word_to_type.configure(text="Press Start!")

        self.user_entry.configure(state="disabled")
        self.user_entry.delete(0, "end")

        self.start_button.configure(state="normal")
        self.restart_button.configure(state="disabled")


game = SpeedTest()
game.app.mainloop()