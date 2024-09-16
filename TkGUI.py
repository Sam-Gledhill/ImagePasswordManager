import tkinter as tk
import tkinter.filedialog   #crashes if not imported explicitly
import os
import subprocess
from functools import partial
import pyperclip

class app(tk.Tk):
    """_summary_ Controller class for all of the frames in the UI, referred to as self.controller in child frame classes

    Args:
        tk (_type_): _description_ Allows use of self as tk.tk
    """

    def __init__(self):
        tk.Tk.__init__(self)

        self.width, self.height = 725, 150

        self.entry_padding = 200

        self.geometry(f"{self.width}x{self.height}")
        self.title("IPWM")

        self.frame_container = tk.Frame(self)
        self.frame_container.pack(side="top", fill="both", expand=True)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)
        self.frame_dict = {
            "EncryptionPage": EncryptionPage, "DecryptionPage":DecryptionPage}
        self.show_frame("DecryptionPage")

        self.mainloop()

    def show_frame(self, frame_name):
        """_summary_ Clears frame_container of any content and initialises the value of self.frame_dict[frame_name] in frame_container

        Args:
            frame_name (_type_):str _description_ key to be used in self.frame_dict
        """
        self.clear_frame(self.frame_container)

        frame = self.frame_dict[frame_name](self.frame_container, self)
        frame.grid(sticky="nsew")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def select_file(self, destination_widget: tk.Entry) -> None:
        path_to_file = tkinter.filedialog.askopenfilename(filetypes=[("png images", "*.png")])
        
        if not path_to_file:
            return

        destination_widget.delete(0,tk.END)
        destination_widget.insert(0,path_to_file)

    def run_program(self,type:str,*args):

        if type == "Encrypt":

            source,dest,secret,password = args

            subprocess.run(["./ipwm",source.get(),dest.get(),secret.get(),password.get()])
        
        elif type == "Decrypt":

            source,password,dest_widget = args

            output = subprocess.run(["./ipwm",source.get(),password.get()], capture_output=True, text = True)

            dest_widget.config(text = output.stdout)

        else:
            raise Exception


class DecryptionPage(tk.Frame):
    def __init__(self:tk.Frame, parent: tk.Frame, controller:tk.Tk):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Draw choose dest
        dest_frame = tk.Frame(self)
        choose_dest_label = tk.Label(dest_frame,text = "Choose Dest: ")
        dest_entry_widget = tk.Entry(dest_frame)
        dest_entry_widget.insert(0,os.getcwd())
        dest_explorer_button = tk.Button(dest_frame,text = "File", command=partial(controller.select_file,dest_entry_widget))

        choose_dest_label.grid(row = 0, column = 0, sticky = tk.W)
        dest_explorer_button.grid(row = 0, column = 1, sticky = tk.W)
        dest_entry_widget.grid(row = 0, column = 2, sticky = tk.W,ipadx=controller.entry_padding)
        dest_frame.grid(row=0,column=0, sticky= tk.W)

        #Draw password entry

        password_frame = tk.Frame(self)
        password_label = tk.Label(password_frame,text = "Password: ")
        password_entry = tk.Entry(password_frame)
        password_label.grid(row=1,column=0,sticky=tk.W)
        password_entry.grid(row=1,column=1,sticky=tk.W)
        password_frame.grid(row=1,column=0,sticky=tk.W)


        button_frame = tk.Frame(self)
        self.show_password_label = tk.Label(button_frame,text = "PasswordShownHere")
        copy_password_button = tk.Button(button_frame,text = "Copy",command = self.copy_password)
        self.show_password_label.grid(row=1,column=1,sticky=tk.E)
        copy_password_button.grid(row=1,column=0,sticky=tk.E)

        #Draw buttons
        encrypt_tab = tk.Button(button_frame,text="Switch to encrypt",command=partial(self.controller.show_frame,"EncryptionPage"))
        encrypt_tab.grid(row=2,column=1, padx = 5)

        run_command = partial(controller.run_program,
            "Decrypt",dest_entry_widget,password_entry,self.show_password_label
        )

        run_button = tk.Button(button_frame,text="RUN",command=run_command)
        run_button.grid(row=2,column=0,sticky=tk.W)

        button_frame.grid(row=2,column=0,sticky=tk.SW, pady=30)

    def copy_password(self):
        label_text = self.show_password_label.cget('text')
        pyperclip.copy(label_text)


class EncryptionPage(tk.Frame):
    

    def __init__(self:tk.Frame, parent: tk.Frame, controller:tk.Tk):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Draw choose source

        source_frame = tk.Frame(self)

        choose_source_label = tk.Label(source_frame,text = "Source Image: ")
        source_entry_widget = tk.Entry(source_frame)
        source_entry_widget.insert(0,os.getcwd())
        source_explorer_button = tk.Button(source_frame,text = "File", command=partial(controller.select_file,source_entry_widget))

        choose_source_label.grid(row = 1, column = 0, sticky = tk.W)
        source_explorer_button.grid(row = 1, column = 1, sticky = tk.W)
        source_entry_widget.grid(row = 1, column = 2, sticky = tk.W,ipadx=controller.entry_padding)
        source_frame.grid(row=0,column=0,sticky=tk.W)

        #Draw choose dest

        dest_frame = tk.Frame(self)
        choose_dest_label = tk.Label(dest_frame,text = "Dest Image: ")
        dest_entry_widget = tk.Entry(dest_frame)
        dest_entry_widget.insert(0,os.getcwd())
        dest_explorer_button = tk.Button(dest_frame,text = "File", command=partial(controller.select_file,dest_entry_widget))

        choose_dest_label.grid(row = 0, column = 0, sticky = tk.W)
        dest_explorer_button.grid(row = 0, column = 1, sticky = tk.W)
        dest_entry_widget.grid(row = 0, column = 2, sticky = tk.W,ipadx=controller.entry_padding)
        
        dest_frame.grid(row=1,column=0,sticky=tk.W)


        #Add button that shows/hides password entry.

        #Draw secret entry

        secret_frame = tk.Frame(self)
        secret_label = tk.Label(secret_frame,text = "Secret: ")
        secret_entry = tk.Entry(secret_frame)
        secret_label.grid(row = 0, column = 0, sticky=tk.W)
        secret_entry.grid(row=0,column=1,sticky=tk.W)
        secret_frame.grid(row=2,column=0,sticky=tk.W)


        #Draw password entry
        password_frame = tk.Frame(self)
        password_label = tk.Label(password_frame,text = "Password: ")
        password_entry = tk.Entry(password_frame)
        password_label.grid(row=0,column=0,sticky=tk.W)
        password_entry.grid(row=0,column=1,sticky=tk.W)
        password_frame.grid(row=3,column=0,sticky=tk.W)

        #Draw buttons

        button_frame = tk.Frame(self)

        run_command = partial(controller.run_program,
            "Encrypt",source_entry_widget,dest_entry_widget,secret_entry,password_entry
        )

        run_button = tk.Button(button_frame,text="RUN",command=run_command)
        run_button.grid(row=5,column=0,sticky=tk.W)

        #Tkinter tabs
        encrypt_tab = tk.Button(button_frame,text="Switch to decrypt",command=partial(self.controller.show_frame,"DecryptionPage"))
        encrypt_tab.grid(row=5,column=1)

        button_frame.grid(row=4,column=0,sticky=tk.W,pady=10)



if __name__ == "__main__":
    app()   