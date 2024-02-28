import tkinter as tk
from tkinter import messagebox

class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Login System")
        self.create_widgets()

    def create_widgets(self):
        # Create registration frame
        self.reg_frame = tk.Frame(self.root)
        self.reg_frame.pack(pady=10)

        reg_label = tk.Label(self.reg_frame, text="Registration")
        reg_label.grid(row=0, column=0, columnspan=2)

        reg_username_label = tk.Label(self.reg_frame, text="Username")
        reg_username_label.grid(row=1, column=0)
        self.reg_username = tk.Entry(self.reg_frame)
        self.reg_username.grid(row=1, column=1)

        reg_password_label = tk.Label(self.reg_frame, text="Password")
        reg_password_label.grid(row=2, column=0)
        self.reg_password = tk.Entry(self.reg_frame, show="*")
        self.reg_password.grid(row=2, column=1)

        reg_email_label = tk.Label(self.reg_frame, text="Email")
        reg_email_label.grid(row=3, column=0)
        self.reg_email = tk.Entry(self.reg_frame)
        self.reg_email.grid(row=3, column=1)

        register_button = tk.Button(self.reg_frame, text="Register", command=self.register)
        register_button.grid(row=4, column=0, columnspan=2)

        # Create login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        login_label = tk.Label(self.login_frame, text="Login")
        login_label.grid(row=0, column=0, columnspan=2)

        login_username_label = tk.Label(self.login_frame, text="Username")
        login_username_label.grid(row=1, column=0)
        self.login_username = tk.Entry(self.login_frame)
        self.login_username.grid(row=1, column=1)

        login_password_label = tk.Label(self.login_frame, text="Password")
        login_password_label.grid(row=2, column=0)
        self.login_password = tk.Entry(self.login_frame, show="*")
        self.login_password.grid(row=2, column=1)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2)

        # Create forgot password frame
        self.forgot_frame = tk.Frame(self.root)
        self.forgot_frame.pack(pady=10)

        forgot_label = tk.Label(self.forgot_frame, text="Forgot Password")
        forgot_label.grid(row=0, column=0, columnspan=2)

        forgot_email_label = tk.Label(self.forgot_frame, text="Email")
        forgot_email_label.grid(row=1, column=0)
        self.forgot_email = tk.Entry(self.forgot_frame)
        self.forgot_email.grid(row=1, column=1)

        forgot_button = tk.Button(self.forgot_frame, text="Reset Password", command=self.forgot_password)
        forgot_button.grid(row=2, column=0, columnspan=2)

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        email = self.reg_email.get()
        self.controller.register(username, password, email)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        self.controller.login(username, password)

    def forgot_password(self):
        email = self.forgot_email.get()
        self.controller.forgot_password(email)

    def show_verification_code_input(self, email, verification_code):
        verification_window = tk.Toplevel(self.root)
        verification_window.title("Verification Code")

        verification_label = tk.Label(verification_window, text="Enter Verification Code:")
        verification_label.pack(pady=10)

        verification_entry = tk.Entry(verification_window)
        verification_entry.pack(pady=5)

        verify_button = tk.Button(verification_window, text="Verify", command=lambda: self.verify_code(email, verification_entry.get(), verification_code))
        verify_button.pack(pady=10)

    def verify_code(self, email, entered_code, verification_code):
        self.controller.verify_code(email, entered_code, verification_code)

    def show_reset_password_dialog(self, email):
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Password")

        new_password_label = tk.Label(reset_window, text="Enter New Password:")
        new_password_label.pack(pady=10)

        new_password_entry = tk.Entry(reset_window, show="*")
        new_password_entry.pack(pady=5)

        reset_button = tk.Button(reset_window, text="Reset Password", command=lambda: self.update_password(email, new_password_entry.get()))
        reset_button.pack(pady=10)

    def update_password(self, email, new_password):
        self.controller.update_password(email, new_password)

    def run(self):
        self.root.mainloop()
