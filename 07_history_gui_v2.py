from tkinter import *
from functools import partial  # This will prevent unwanted windows
from datetime import date
import re


class Converter:

    def __init__(self):
        # common format for all the buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # Five item list
        self.all_calculations = ['0 F° is -18 C°', '0 C° is 32 F°',
                                 '30 F° is -1 C°', '0 C° is 86 F°',
                                 '40 F° is -4 C°']

        # Six item list
        # self.all_calculations = ['0 F° is -18 C°', '0 C° is 32 F°',
        #                          '30 F° is -1 C°', '0 C° is 86 F°',
        #                          '30 F° is -1 C°', '0 C° is 86 F°',
        #                          '40 F° is -4 C°', '100 C° is 212 C°']

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=10, pady=10)
        self.button_frame.grid(row=0)

        self.to_history_button = Button(self.button_frame,
                                        text="history / Info",
                                        bg="#006deb",
                                        fg=button_fg,
                                        font=button_font, width=12,
                                        command=lambda: self.to_history(self.all_calculations))
        self.to_history_button.grid(row=1, column=0, padx=5, pady=5)

    #     ***** Remove when integrating!! ****

    def to_history(self, all_calculations):
        HistoryExport(self, all_calculations)


class HistoryExport:

    def __init__(self, partner, calc_list):

        # set maximum number to 5
        # this can be changed if we want to show fewer /
        # more calculations
        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # Set variables to hold filename and date
        # for when writing to file
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()

        # Function converts contents of calculation list
        # into a string
        calc_string_text = self.get_calc_string(calc_list)

        background = "#ffffff"
        self.history_box = Toplevel()

        # disable history button
        partner.to_history_button.config(state=DISABLED)

        # If users press cross at the top, that will close the history button and release it
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300, height=200,
                                   bg=background)
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame, bg=background,
                                           text="history / Information",
                                           font=("Arial", "14", "bold"))
        self.history_heading_label.grid(row=0)

        # Customize text and background colour for calculation
        # area depending on whether all or only some calculations
        # are shown.
        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#E5D383"  # something
            calc_fg = "#000000"
            showing_all = "Here are your recent calculations " \
                          "({}/{} calculations shown). Please export your " \
                          "calculations to see your full calculation " \
                          "history.".format(max_calcs, num_calcs)

        else:
            calc_background = "#337FCC"  # yeet
            calc_fg = "#FFFFFF"
            showing_all = "Below is your calculation history."

        history_text = f"{showing_all} \n\nAll calculations are shown to the nearest degree."

        self.text_instructions_label = Label(self.history_frame,
                                             text=history_text, wraplength=300,
                                             justify="left",
                                             padx=10, pady=10)
        self.text_instructions_label.grid(row=1, padx=10)

        self.all_cacls_label = Label(self.history_frame,
                                     text=calc_string_text,
                                     justify="left", width=40,
                                     fg=calc_fg,
                                     padx=10, pady=10, bg=calc_background,
                                     font=("Arial", "12", "bold"))
        self.all_cacls_label.grid(row=2)

        # instructions for saving files
        save_text = "Either choose a custom file name and push " \
                    "<Export> or simply push <exploit> to save your " \
                    "calculations in a text file. If the " \
                    "filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # Filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_error_label = Label(self.history_frame,
                                          text="FILENAME ERROR",
                                          fg="#CD3632",
                                          font=("Arial", "14", "bold"))
        self.filename_error_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold",),
                                    text="Export", bg="#337FCC",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="DISMISS", bg="#807e7e",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history,
                                                     partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

        # change calculation list into a string so that it
        # can be outputted as a label.

    def get_calc_string(self, var_calculations):
        # get maximum calculations to display
        # (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        # work out how many times we need to loop
        # to output either the last five calculations
        # or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)

        # iterate to all but last item,
        # adding item and line break to calculation string
        for item in range(0, stop - 1):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]
            calc_string += "\n"

        # add final item without an extra linebreak
        # ie: last item on the list will be fifth from the end
        calc_string += var_calculations[-max_calcs]

        return calc_string

    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()

        filename_ok = ""

        if filename == "":
            # get date and create default filename
            date_part = self.get_date()
            filename = "{}_temperature_calculations".format(date_part)

        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            self.filename_error_label.config(text="You are OK")

        else:
            self.filename_error_label.config(text=filename_ok)

    # retrieves date and creates YYYY_MM_DD string
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}/{}/{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    def check_filename(self,filename):
        problem = ""

        # Regular expression to check filename is valid
        valid_char = "[A=Za-z0-9]"

        # iterates through filename and checks each letter.
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

    # closes help dialogue (used by button and x at top of dialogue)
    def close_history(self, partner):
        # Put help button back to normal...
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
