import tkinter as tk
from tkinter import messagebox
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

def create_table():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, email TEXT)''')
    conn.commit()
    conn.close()

def register():
    username = reg_username.get()
    password = reg_password.get()
    email = reg_email.get()

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

    reg_username.delete(0, tk.END)
    reg_password.delete(0, tk.END)
    reg_email.delete(0, tk.END)
    messagebox.showinfo("Success", "Registration successful!")

def login():
    username = login_username.get()
    password = login_password.get()

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password")

def send_verification_email(email):
    # Generate verification code
    verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Send email with verification code
    smtp_server = 'sandbox.smtp.mailtrap.io' # SMTP Server URL
    smtp_port = 2525  # SMTP server Port
    
    server_username = '8b78a03d0e70b9'  # SMTP Server Username
    server_login = '51d9feccfb8f48'  # SMTP Server Password

    private_email = 'sample@main2.com' # change to your email

    # Email configuration
    msg = MIMEMultipart()
    msg['From'] = private_email
    msg['To'] = email # email from db
    msg['Subject'] = 'Verification Code for Password Reset'
    body = f'Your verification code is: {verification_code}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(server_username, server_login)
        server.sendmail(private_email, email, msg.as_string())
        server.quit()
        messagebox.showinfo("Success", "Verification code sent to your email!")
        return verification_code
    
    except smtplib.SMTPException as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")
        return None

def reset_password():
    email = forgot_email.get()

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()

    if user:
        verification_code = send_verification_email(email)
        if verification_code:
            # Create a new window for verification
            verification_window = tk.Toplevel(root)
            verification_window.title("Verification Code")

            verification_label = tk.Label(verification_window, text="Enter Verification Code:")
            verification_label.pack(pady=10)

            verification_entry = tk.Entry(verification_window)
            verification_entry.pack(pady=5)

            def verify_code():
                entered_code = verification_entry.get()
                if entered_code == verification_code:
                    messagebox.showinfo("Success", "Verification successful!")
                    # Close the verification window
                    verification_window.destroy()
                    # Create a new window for password reset
                    reset_window = tk.Toplevel(root)
                    reset_window.title("Reset Password")

                    new_password_label = tk.Label(reset_window, text="Enter New Password:")
                    new_password_label.pack(pady=10)

                    new_password_entry = tk.Entry(reset_window, show="*")
                    new_password_entry.pack(pady=5)

                    def update_password():
                        new_password = new_password_entry.get()
                        conn = sqlite3.connect('user.db')
                        c = conn.cursor()
                        c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Password updated successfully!")
                        reset_window.destroy()

                    reset_button = tk.Button(reset_window, text="Reset Password", command=update_password)
                    reset_button.pack(pady=10)
                else:
                    messagebox.showerror("Error", "Invalid verification code!")

            verify_button = tk.Button(verification_window, text="Verify", command=verify_code)
            verify_button.pack(pady=10)
    else:
        messagebox.showerror("Error", "Email not found")

# Create the main window
root = tk.Tk()
root.title("Login System")

# Create registration frame
reg_frame = tk.Frame(root)
reg_frame.pack(pady=10)

reg_label = tk.Label(reg_frame, text="Registration")
reg_label.grid(row=0, column=0, columnspan=2)

reg_username_label = tk.Label(reg_frame, text="Username")
reg_username_label.grid(row=1, column=0)
reg_username = tk.Entry(reg_frame)
reg_username.grid(row=1, column=1)

reg_password_label = tk.Label(reg_frame, text="Password")
reg_password_label.grid(row=2, column=0)
reg_password = tk.Entry(reg_frame, show="*")
reg_password.grid(row=2, column=1)

reg_email_label = tk.Label(reg_frame, text="Email")
reg_email_label.grid(row=3, column=0)
reg_email = tk.Entry(reg_frame)
reg_email.grid(row=3, column=1)

register_button = tk.Button(reg_frame, text="Register", command=register)
register_button.grid(row=4, column=0, columnspan=2)

# Create login frame
login_frame = tk.Frame(root)
login_frame.pack(pady=10)

login_label = tk.Label(login_frame, text="Login")
login_label.grid(row=0, column=0, columnspan=2)

login_username_label = tk.Label(login_frame, text="Username")
login_username_label.grid(row=1, column=0)
login_username = tk.Entry(login_frame)
login_username.grid(row=1, column=1)

login_password_label = tk.Label(login_frame, text="Password")
login_password_label.grid(row=2, column=0)
login_password = tk.Entry(login_frame, show="*")
login_password.grid(row=2, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2)

# Create forgot password frame
forgot_frame = tk.Frame(root)
forgot_frame.pack(pady=10)

forgot_label = tk.Label(forgot_frame, text="Forgot Password")
forgot_label.grid(row=0, column=0, columnspan=2)

forgot_email_label = tk.Label(forgot_frame, text="Email")
forgot_email_label.grid(row=1, column=0)
forgot_email = tk.Entry(forgot_frame)
forgot_email.grid(row=1, column=1)

forgot_button = tk.Button(forgot_frame, text="Reset Password", command=reset_password)
forgot_button.grid(row=2, column=0, columnspan=2)

create_table()

root.mainloop()
