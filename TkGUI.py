import tkinter as tk
import tkinter.filedialog   #crashes if not imported explicitly
import os
import subprocess
from functools import partial

class app(tk.Tk):
    """_summary_ Controller class for all of the frames in the UI, referred to as self.controller in child frame classes

    Args:
        tk (_type_): _description_ Allows use of self as tk.tk
    """

    def __init__(self):
        tk.Tk.__init__(self)

        self.width, self.height = 450, 200

        self.geometry(f"{self.width}x{self.height}")
        self.title("IPWM")

        self.frame_container = tk.Frame(self)
        self.frame_container.pack(side="top", fill="both", expand=True)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        self.frame_dict = {
            "EncryptionPage": EncryptionPage, "DecryptionPage":DecryptionPage}
        self.show_frame("EncryptionPage")

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

            print("Password Written")
        
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
        choose_dest_label = tk.Label(self,text = "Choose Dest: ")
        dest_entry_widget = tk.Entry(self)
        dest_entry_widget.insert(0,os.getcwd())
        dest_explorer_button = tk.Button(self,text = "File", command=partial(controller.select_file,dest_entry_widget))

        choose_dest_label.grid(row = 0, column = 0, sticky = tk.W)
        dest_explorer_button.grid(row = 0, column = 1, sticky = tk.W)
        dest_entry_widget.grid(row = 0, column = 2, sticky = tk.W)

        #Draw password entry
        password_label = tk.Label(self,text = "Password: ")
        password_entry = tk.Entry(self)
        password_label.grid(row=1,column=0,sticky=tk.W)
        password_entry.grid(row=1,column=1,sticky=tk.W)


        encrypt_tab = tk.Button(self,text="Switch to encrypt",command=partial(self.controller.show_frame,"EncryptionPage"))
        encrypt_tab.grid(row=2,column=1)

        show_password_label = tk.Label(self,text = "PasswordShownHere")
        copy_password_button = tk.Button(self,text = "Copy")
        show_password_label.grid(row=3,column=0)
        copy_password_button.grid(row=3,column=1)

        #Draw run button

        run_command = partial(controller.run_program,
            "Decrypt",dest_entry_widget,password_entry,show_password_label
        )

        run_button = tk.Button(self,text="RUN",command=run_command)
        run_button.grid(row=2,column=0,sticky=tk.W)


class EncryptionPage(tk.Frame):
    

    def __init__(self:tk.Frame, parent: tk.Frame, controller:tk.Tk):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Draw choose source
        choose_source_label = tk.Label(self,text = "Choose Source: ")
        source_entry_widget = tk.Entry(self)
        source_entry_widget.insert(0,os.getcwd())
        source_explorer_button = tk.Button(self,text = "File", command=partial(controller.select_file,source_entry_widget))

        choose_source_label.grid(row = 1, column = 0, sticky = tk.W)
        source_explorer_button.grid(row = 1, column = 1, sticky = tk.W)
        source_entry_widget.grid(row = 1, column = 2, sticky = tk.W)

        #Draw choose dest
        choose_dest_label = tk.Label(self,text = "Choose Dest: ")
        dest_entry_widget = tk.Entry(self)
        dest_entry_widget.insert(0,os.getcwd())
        dest_explorer_button = tk.Button(self,text = "File", command=partial(controller.select_file,dest_entry_widget))

        choose_dest_label.grid(row = 2, column = 0, sticky = tk.W)
        dest_explorer_button.grid(row = 2, column = 1, sticky = tk.W)
        dest_entry_widget.grid(row = 2, column = 2, sticky = tk.W)

        #Add button that shows/hides password entry.

        #Draw secret entry
        secret_label = tk.Label(self,text = "Secret: ")
        secret_entry = tk.Entry(self)
        secret_label.grid(row = 3, column = 0, sticky=tk.W)
        secret_entry.grid(row=3,column=1,sticky=tk.W)

        #Draw password entry
        password_label = tk.Label(self,text = "Password: ")
        password_entry = tk.Entry(self)
        password_label.grid(row=4,column=0,sticky=tk.W)
        password_entry.grid(row=4,column=1,sticky=tk.W)

        #Draw run button
        run_command = partial(controller.run_program,
            "Encrypt",source_entry_widget,dest_entry_widget,secret_entry,password_entry
        )

        run_button = tk.Button(self,text="RUN",command=run_command)
        run_button.grid(row=5,column=0,sticky=tk.W)

        #Tkinter tabs
        encrypt_tab = tk.Button(self,text="Switch to decrypt",command=partial(self.controller.show_frame,"DecryptionPage"))
        encrypt_tab.grid(row=5,column=1)



if __name__ == "__main__":
    app()   