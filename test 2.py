import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime


def main():
    to_do_list = []

    def display_tasks_in_tk():
        task_list.delete(0, tk.END)  # Clear the existing list
        deadline_list.delete(0, tk.END)  # Clear the existing deadlines list
        if not to_do_list:
            task_list.insert(tk.END, "No tasks in the list.")
            deadline_list.insert(tk.END, "")
        else:
            for index, task in enumerate(to_do_list, 1):
                color = "forestgreen" if task["done"] else "maroon"
                task_list.insert(tk.END, f"{index}. {task['task']}")
                task_list.itemconfig(index - 1, {'fg': color})
                deadline_list.insert(tk.END, task.get("deadline", "No deadline"))

    def add_task():
        task_description = entry_task.get()
        task_deadline = entry_deadline.get().strip()
        if task_description:
            task_data = {"task": task_description, "done": False}
            if task_deadline and task_deadline != "DD-MM-YYYY HH:MM":
                try:
                    datetime.strptime(task_deadline, "%d-%m-%Y %H:%M")
                    task_data["deadline"] = task_deadline
                except ValueError:
                    messagebox.showerror("Invalid Date Format",
                                         "Please enter the deadline in the format DD-MM-YYY HH:MM.")
                    return
            to_do_list.append(task_data)
            display_tasks_in_tk()
            entry_task.delete(0, tk.END)  # Clear the entry field after adding task
            entry_deadline.delete(0, tk.END)  # Clear the entry field after adding task
            entry_deadline.insert(0, "DD-MM-YYYY HH:MM")  # Reset the deadline field
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def add_deadline():
        try:
            task_number = int(entry_task_number.get()) - 1
            if 0 <= task_number < len(to_do_list):
                task_deadline = entry_deadline.get().strip()
                if not task_deadline or task_deadline == "DD-MM-YYYY HH:MM":
                    to_do_list[task_number].pop("deadline", None)
                else:
                    try:
                        datetime.strptime(task_deadline, "%d-%m-%Y %H:%M")
                        to_do_list[task_number]["deadline"] = task_deadline
                    except ValueError:
                        messagebox.showerror("Invalid Date Format",
                                             "Please enter the deadline in the format DD-MM-YYYY HH:MM.")
                        return
                display_tasks_in_tk()
            else:
                messagebox.showwarning("Invalid Task Number", "Please enter a valid task number.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer task number.")
        entry_task_number.delete(0, tk.END)  # Clear the entry field after adding deadline

    def mark_task_as_done():
        try:
            task_number = int(entry_mark.get()) - 1
            if 0 <= task_number < len(to_do_list):
                to_do_list[task_number]["done"] = True
                display_tasks_in_tk()
                check_all_tasks_done()
            else:
                messagebox.showwarning("Invalid Task Number", "Please enter a valid task number.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer task number.")
        entry_mark.delete(0, tk.END)  # Clear the entry field after marking task

    def all_tasks_done():
        return all(task["done"] for task in to_do_list)

    def check_all_tasks_done():
        if all_tasks_done():
            root.after(500, display_congrats_gif_tk)

    def display_congrats_gif_tk():
        try:
            gif_path = "pigeon.gif"

            root_gif = tk.Toplevel()
            root_gif.title("Congratulations, all your tasks are done!")

            # Load the GIF file
            gif = Image.open(gif_path)
            gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

            # Create a label to display the GIF
            label_gif = tk.Label(root_gif)
            label_gif.pack()

            def update_frame(idx):
                frame = gif_frames[idx]
                label_gif.configure(image=frame)
                label_gif.image = frame
                root_gif.after(100, update_frame, (idx + 1) % len(gif_frames))

            update_frame(0)  # Start showing frames

        except Exception as e:
            messagebox.showerror("Error", f"Could not display GIF: {e}")

    # Main tkinter window
    root = tk.Tk()
    root.title("To-Do List")

    # Entry field for adding tasks
    entry_task = tk.Entry(root, width=50)
    entry_task.grid(row=0, column=0, padx=10, pady=10)

    # Entry field for adding deadlines
    entry_deadline = tk.Entry(root, width=50, )
    entry_deadline.grid(row=1, column=0, padx=10, pady=10)
    entry_deadline.insert(0, "DD-MM-YYYY HH:MM")

    # Label for task number entry
    lbl_task_number = tk.Label(root, text="Task number:", anchor='w')
    lbl_task_number.grid(row=1, column=0, sticky='e', padx=10)

    # Entry field for task number for adding deadlines
    entry_task_number = tk.Entry(root, width=10)
    entry_task_number.grid(row=1, column=1, padx=10, pady=10)

    # Button to add deadlines
    btn_add_deadline = tk.Button(root, text="Add Deadline", command=add_deadline, bg='midnightblue', fg='white')
    btn_add_deadline.grid(row=1, column=2, padx=10, pady=10)

    # Button to add tasks
    btn_add_task = tk.Button(root, text="Add Task", command=add_task, bg='midnightblue', fg='white')
    btn_add_task.grid(row=0, column=1, padx=10, pady=10)

    # Entry field for marking tasks as done
    entry_mark = tk.Entry(root, width=50)
    entry_mark.grid(row=2, column=0, padx=10, pady=10)

    # Button to mark tasks as done
    btn_mark_done = tk.Button(root, text="Done Task Number", command=mark_task_as_done, bg='midnightblue', fg='white')
    btn_mark_done.grid(row=2, column=1, padx=10, pady=10)

    # Listbox to display tasks
    task_list = tk.Listbox(root, width=70, height=10)
    task_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Listbox to display deadlines
    deadline_list = tk.Listbox(root, width=30, height=10)
    deadline_list.grid(row=3, column=2, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
