import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime


def main():
    to_do_list = []

    def display_tasks():
        # Function displays all the tasks and color codes their state

        task_list.delete(0, tk.END)  # Clears the existing list
        deadline_list.delete(0, tk.END)  # Clears the existing deadlines list

        if len(to_do_list) != 0:
            for index, task in enumerate(to_do_list, 1):
            # This part numbers tasks based on order in which they were added
                if task["done"]:
                    color = "forestgreen"
                # So done tasks are in green and the ones that were not finished yet in red
                else:
                    color = "maroon"

                task_list.insert(tk.END, f"{index}. {task['task']}")
                task_list.itemconfig(index - 1, {'fg': color})
                deadline_list.insert(tk.END, task.get("deadline", "No deadline"))
        else:
            task_list.insert(tk.END, "No tasks in the list.")
            deadline_list.insert(tk.END, "")

    def check_datetime(deadline):
        # This function checks the validity of the entered deadline
        # Returns false if the deadline is invalid

        try:
            datetime.strptime(deadline, "%d-%m-%Y %H:%M")
            return 1
        except ValueError:
            messagebox.showerror("Invalid Date Format",
                                 "Please enter the deadline in the format DD-MM-YYY HH:MM.")
            return 0

    def add_task():
        # This function adds a task to the 'to_do_list'

        # Loading the inputs
        description = entry_task.get()
        deadline = entry_deadline.get().strip()

        if len(description) != 0:
            data = {"task": description, "done": False}
            if deadline != "" and deadline != "DD-MM-YYYY HH:MM":
                if check_datetime(deadline):
                    data["deadline"] = deadline
                else:
                    return None
            to_do_list.append(data)
            display_tasks()

            entry_task.delete(0, tk.END)  # Clears the entry field after adding task
            entry_deadline.delete(0, tk.END)  # Clears the entry field after adding deadline
            entry_deadline.insert(0, "DD-MM-YYYY HH:MM")  # Resets the deadline field
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def add_deadline():
        # Function adds a deadline to the selected task using the 'task_number' variable

        # Checking if the entry contains only numbers
        task_number = entry_task_number.get()
        if task_number.isdigit():
            task_number = int(entry_task_number.get()) - 1
        else:
            task_number = -1

        if 0 <= task_number < len(to_do_list):
            # To check if the task number is correct (more than 0 and less than the number of tasks in the list)
            # If incorrect --> says that it is an invalid number
            task_deadline = entry_deadline.get().strip()

            if task_deadline == "" or task_deadline == "DD-MM-YYYY HH:MM":
                # If the task deadline is empty --> remove it from the list
                to_do_list[task_number].pop("deadline", None)
            else:
                if check_datetime(task_deadline):
                    # If the task deadline is not empty and added correctly --> add to the list
                    to_do_list[task_number]["deadline"] = task_deadline

                else:
                    # Incorrectly inputed deadline
                    to_do_list[task_number].pop("deadline", None)
                    return None
            display_tasks()
        else:
            messagebox.showwarning("Invalid Task Number", "Please enter a valid task number.")

        entry_task_number.delete(0, tk.END)  # Clears the entry field after adding deadline

    def mark_task_as_done():
        # Function takes task number as an input and marks it as done

        # Checking if the entry contains only numbers
        task_number = entry_mark.get()
        if task_number.isdigit():
            task_number = int(task_number) - 1
        else:
            task_number = -1

        if 0 <= task_number < len(to_do_list):
            to_do_list[task_number]["done"] = True
            display_tasks()
            check_all_tasks_done()
        else:
            messagebox.showwarning("Invalid Task Number", "Please enter a valid task number.")
        entry_mark.delete(0, tk.END)  # Clears the entry field after marking task

    def all_tasks_done():
        # Function returns true if all tasks are marked as done

        for task in to_do_list:
            if task["done"] == False:
                return 0
        # Goes through all tasks and if one of them is not done, "stops going through the list" = exits the function
        # It is then considered false: 0 represents "false"

        return 1

    def check_all_tasks_done():
        # If all tasks are done, function displays a celebrating GIF

        if all_tasks_done():
            gui.after(500, display_gif)

    def display_gif():
        # This function displays and plays the GIF

        gif_path = "pigeon.gif"

        gui_gif = tk.Toplevel()
        gui_gif.title("Congratulations, all your tasks are done!")

        gif = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        label_gif = tk.Label(gui_gif)
        label_gif.pack()

        def update_frame(idx):
            frame = gif_frames[idx]
            label_gif.configure(image=frame)
            label_gif.image = frame
            gui_gif.after(100, update_frame, (idx + 1) % len(gif_frames))

        update_frame(0)  # Start showing frames

    # Making the window
    gui = tk.Tk()
    gui.title("To-Do List")

    # Creating entries
    entry_task = tk.Entry(gui, width=50)
    entry_task.grid(row=0, column=0, padx=10, pady=10)

    entry_deadline = tk.Entry(gui, width=50, )
    entry_deadline.grid(row=1, column=0, padx=10, pady=10)
    entry_deadline.insert(0, "DD-MM-YYYY HH:MM")

    entry_task_number = tk.Entry(gui, width=10)
    entry_task_number.grid(row=1, column=1, padx=10, pady=10)

    entry_mark = tk.Entry(gui, width=50)
    entry_mark.grid(row=2, column=0, padx=10, pady=10)

    entry_mark = tk.Entry(gui, width=50)
    entry_mark.grid(row=2, column=0, padx=10, pady=10)

    # Creating labels
    lbl_task_number = tk.Label(gui, text="Task number:", anchor='w')
    lbl_task_number.grid(row=1, column=0, sticky='e', padx=10)

    # Creating buttons
    btn_add_deadline = tk.Button(gui, text="Add Deadline", command=add_deadline, bg='midnightblue', fg='white')
    btn_add_deadline.grid(row=1, column=2, padx=10, pady=10)

    btn_add_task = tk.Button(gui, text="Add Task", command=add_task, bg='midnightblue', fg='white')
    btn_add_task.grid(row=0, column=1, padx=10, pady=10)

    btn_mark_done = tk.Button(gui, text="Done Task Number", command=mark_task_as_done, bg='midnightblue', fg='white')
    btn_mark_done.grid(row=2, column=1, padx=10, pady=10)

    # Making lists
    task_list = tk.Listbox(gui, width=70, height=10)
    task_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    deadline_list = tk.Listbox(gui, width=30, height=10)
    deadline_list.grid(row=3, column=2, padx=20, pady=10)

    gui.mainloop()


if __name__ == "__main__":
    main()

