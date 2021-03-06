import re
import datetime
import sys
import csv


class Entries:

    def __init(self):
        self.records = []

    # Prompt menu to add a new entry or lookup previous entries
    def prompt_menu(self):
        self.clear_screen()

        while True:
            print(('*' * 10)+"MENU"+('*' * 10))
            print("Would you like to add a [N]ew Entry,"
                  " [L]ookup an entry,or [E]xit?")
            new_input = input('> ').lower()

            if new_input in 'nle':
                if new_input == 'n':
                    self.clear_screen()
                    self.new_entry()
                    continue
                if new_input == 'l':
                    self.lookup()
                    continue
                if new_input == 'e':
                    sys.exit()

    # Adds an entry
    def new_entry(self):
        self.clear_screen()

        # task name
        print("What do you want to name this task? Enter[Q] to go back")
        while True:
            task_name = input('> ')
            if task_name.lower() == 'q':
                self.prompt_menu()
                break
            elif not task_name:
                input("You must name the task. Press Enter to continue.")
            else:
                break

        # time took to complete
        self.clear_screen()
        time = self.add_time()
        date = self.add_date()

        # notes
        self.clear_screen()
        print('Would you like to add additional notes? Y/N')
        while True:
            notes = input('> ').lower()
            if notes in 'yn':
                if notes == 'n':
                    notes = ''
                    break
                elif notes == 'y':
                    while True:
                        self.clear_screen()
                        print("Enter your notes.")
                        notes = input('> ')
                        if notes:
                            break
                        else:
                            input("You must enter notes. Pres Enter")
                            continue
                    break
            else:
                input(" Please select 'Y' for yes and 'N' for no. Press Enter ")
                continue
            

        self.add_entry_summary(task_name, time, notes, date)

    # function to add a date
    def add_date(self):
        self.clear_screen()
        while True:
            date = input("Enter the date you completed the task."
                         "Date format MM/DD/YY\n").strip()
            try:
                date = datetime.datetime.strptime(date, '%m/%d/%y')
                if date.date() > datetime.datetime.now().date():
                    input("Sorry you cannot select"
                          " a date in the futue.  Press enter")
                    continue
            except ValueError:
                input("Sorry, that's not a valid date.  Use MM/DD/YY format.")
                continue
            else:
                return date.strftime("%m/%d/%y")

    # function to add time
    def add_time(self):
        while True:
            time = input("Enter a time worked for this"
                         " task in HH:MM format\n").strip()
            if not re.match(r'^\d{1,2}:\d{2}$', time):
                input("Invalid entry, pleas use the HH:MM format. Press Enter")
                continue
            elif re.match(r'^\d{1,2}:\d{2}$', time):
                split_time = time.split(':')
                # check time is not 0
                if (int(split_time[0]) < 1) and (int(split_time[1]) < 1):
                    input('Your time cannot be at'
                          ' 0 hrs and 0 min. Press Enter')
                    continue
                elif (int(split_time[0]) > 24):
                    input("Your time can't be longer than 24 hours")
                    continue
                elif (int(split_time[0]) == 24) and (int(split_time[1]) > 0):
                    input("Your time can't be longer than 24 hours")
                    continue
                elif (int(split_time[0]) == 23) and (int(split_time[1]) > 60):
                    input("Your time can't be longer than 24 hours")
                    continue
                else:
                    time = round(((int(split_time[0]) * 60) + (
                        int(split_time[1]))) / 60, 2)
                    return time

    # verifies entries before saving
    def add_entry_summary(self, task_name, time, notes, date):
        self.clear_screen()
        print("Are these entries correct?\n")
        print("Task Name: {}\n".format(task_name))
        print("Time: {}\n".format(time))
        print("Notes: {}\n".format(notes))
        print('Date: {}\n'.format(date))
        self.confirm_entry(task_name, time, notes, date)

    # asks to save, edit or delete an entry
    def confirm_entry(self, task_name, time, notes, date):
        while True:
            response = input("Would you like to"
                             " [S]ave, [E]dit or [D]elete this enry?\n")
            if response.lower() not in 'sde':
                input("\n That was an invalid input.  Press Enter")
                continue
            elif response.lower() == 's':
                self.save_entry(task_name, time, notes, date)
                input("Entry will be saved")
                break
            elif response.lower() == 'd':
                while True:
                    delete = input("Are you sure you want to delete? Y/N\n")
                    if delete.lower() in 'yn':
                        if delete.lower() == 'y':
                            task_name, time, notes, date = (None,) * 4
                            input("Entry has been deleted. Press Enter")
                            self.prompt_menu()
                            break
                        if delete.lower() == 'n':
                            self.clear_screen()
                            self.add_entry_summary(task_name,
                                                   time, notes, date)
                            break
                    else:
                        input("You must enter 'Y' or 'N'\n")
            elif response.lower() == 'e':
                self.edit_entry(task_name, time, notes, date)
                break

    # saves the entry
    def save_entry(self, task_name, time, notes, date):
        # writes data to csv file
        self.clear_screen()

        with open('work_log.csv', 'a', newline='') as csvfile:
            fields = ['Task Name', 'Time(hours)', 'Notes', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow({
                'Task Name': task_name,
                'Time(hours)': time,
                'Notes': notes,
                'Date': date
            })
        input("Entry saved press Enter")
        self.prompt_menu()

    # edit entry function
    def edit_entry(self, task_name, time, notes, date):
        self.clear_screen
        print(' ' * 10 + " Edit Entries " + ' ' * 10)
        entry_items = (task_name, time, notes, date)
        for entry_item in entry_items:
            if entry_item == entry_items[0]:
                while True:
                    self.clear_screen()
                    response = input("Would you like"
                                     " to edit Task Name? Y/N\n").strip()
                    if response.lower() in 'yn':
                        if response.lower() == 'y':
                            self.clear_screen()
                            print(' ' * 10 + ' Edit task name '
                                  + ' ' * 10 + '\n')
                            print(' Current Task name: {}'.format(task_name))
                            task_name = input('Edit here \n ')
                            break
                        elif response.lower() == 'n':
                            break
                    else:
                        input("Please select 'Y' for yes"
                              " and 'N' for no. Press Enter")
                        continue
            elif entry_item == entry_items[1]:
                while True:
                    self.clear_screen()
                    response = input("Would you like to edit Time? Y/N\n")
                    if response.lower() in 'yn':
                        if response.lower() == 'y':
                            self.clear_screen()
                            print(' ' * 10 + ' Edit time ' + ' ' * 10 + '\n')
                            print(' Current Time: {}'.format(time))
                            time = input('Edit here \n ')
                            break
                        elif response.lower() == 'n':
                            break
                    else:
                        input("Please select 'Y' for yes"
                              " and 'N' for no. Press Enter")
                        continue
            elif entry_item == entry_items[2]:
                while True:
                    self.clear_screen()
                    response = input("Would you like to edit Notes? Y/N\n")
                    if response.lower() in 'yn':
                        if response.lower() == 'y':
                            self.clear_screen()
                            print(' ' * 10 + ' Edit notes ' + ' ' * 10 + '\n')
                            print(' Current Notes: {}'.format(notes))
                            notes = input('Edit here \n ')
                            break
                        elif response.lower() == 'n':
                            break
                    else:
                        input("Please select 'Y' for yes"
                              " and 'N' for no. Press Enter")
                        continue
            elif entry_item == entry_items[3]:
                while True:
                    self.clear_screen()
                    response = input("Would you like to edit Date? Y/N\n")
                    if response.lower() in 'yn':
                        if response.lower() == 'y':
                            self.clear_screen()
                            print(' ' * 10 + ' Edit date ' + ' ' * 10 + '\n')
                            print(' Current Date: {}'.format(date))
                            date = input('Edit here \n ')
                            break
                        elif response.lower() == 'n':
                            break
                    else:
                        input("Please select 'Y' for yes"
                              " and 'N' for no. Press Enter")
                        continue
        self.add_entry_summary(task_name, time, notes, date)

    # ecides how to look up entries
    def lookup(self):
        self.clear_screen()

        print(('*' * 15) + "Search" + ('*' * 15))
        print("Search entries by [D]ate, [T]ime spent working,"
              " [K]ey word search, or [B]ack.")
        search_type = input('> ').lower()

        while True:
            if search_type in 'dtkpb':
                if search_type == 'd':
                    self.clear_screen()
                    self.search_date()
                    break
                if search_type == 't':
                    self.clear_screen()
                    self.search_time()
                    break
                if search_type == 'k':
                    self.clear_screen()
                    self.search_key()
                    break

                if search_type == 'b':
                    self.prompt_menu()
                    break

    # look up a date by range or specific date
    def search_date(self):
        dt_list = []
        reselect = []
        print("Search by Date")
        print("_" * 100+'\n')
        sel = input('To search by [S]pecific date or [R]ange?\n')
        while True:
            if sel.lower() == 's':
                self.clear_screen()
                dates = self.show_list('d')
                print("Enter a date by MM/DD/YY")
                while True:
                    date = input(' ').strip()
                    if not date:
                            input("\n Kindly enter a date. "
                                  "Press enter to continue... ")
                            continue
                    elif not re.match(r'[0-9]{2}/'
                                      '[0-9]{2}/[0-9]{2}$',
                                      date):
                            input("\n Invalid date. Date must be "
                                  "in the right format."
                                  " Press enter to continue... ")
                            continue
                    else:
                        for entry in self.records:
                            if entry['Date'] == date:
                                reselect.append(entry)
                                self.display_results(reselect)
                                break
            if sel.lower() == 'r':
                self.clear_screen()
                self.show_list('d')
                while True:
                    print('Enter a date range (dd/mm/yy to dd/mm/yy) '
                          'to search date')
                    date = input('> ')
                    if not date:
                        input("Enter a date range")
                        continue
                    if not re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{2}\s?'
                                    'to\s?[0-9]{2}/[0-9]{2}/[0-9]{2}', date):
                        input("Enter a valid date range")
                        continue
                    else:
                        dates = []
                        for key in self.records:
                            dates.append(key['Date'])
                            dt = sorted(dates)
                            for dates_sorted in dt:
                                if (dates_sorted >= date[0]) and (
                                        dates_sorted <= date[-1]):
                                    dt_list.append(dates_sorted)
                        for entry in self.records:
                            if entry['Date'] in dt_list:
                                reselect.append(entry)
                        self.display_results(reselect)
                        break

    # looks up by time
    def search_time(self):
        reselect = []
        searched = []
        print("Search by Time Entry")
        print("_" * 100+'\n')

        self.clear_screen()
        print("Enter time(hours) to complete task in minutes i.e. 20, 45")
        self.show_list('t')
        time = input('> ')

        try:
            time = float(time)
        except ValueError:
            print("Please enter an interger only")
            self.search_time()
        for entry in self.records:
            hrs = entry['Time(hours)']
            hrs = float(hrs)
            duration = datetime.timedelta(hours=hrs)
            duration = str(duration)
            duration = duration[:-3]
            if duration not in reselect:
                reselect.append(duration)

        while True:
            self.clear_screen()
            print('-' * 13 + " Current Task Time" + '-')
            for duration in reselect:
                print(' '*10+duration+' ')

            time_search = self.add_time()
            time_search = str(time_search)

            for ent in self.records:
                if ent['Time(hours)'] == time_search:
                    searched.append(ent)
            if not searched:
                input("Sorry no avalable entries for that time")
                continue
            else:
                self.display_results(searched)
                break

    # looks up by string and regex
    def search_key(self):
        searched_key = []
        self.clear_screen()
        print(' '*10 + "Search by text or regular"
              "expression in Task name or Notes")
        print("_" * 100+'\n')

        self.show_list('k')
        print("Enter a text or regular expression")
        while True:
            note = input('> ')
            if not note:
                input(' Nothing was entered.  Press Enter. \n')
                continue
            else:
                search_key = r'' + note + '+'
                for entry in self.records:
                    if (re.search(search_key, entry['Task name']) or
                            re.search(search_key, entry['Notes'])):
                        if entry not in searched_key:
                            searched_key.append(entry)
                            break
                if not searched_key:
                    input("There were no results by that search."
                          " Press Enter to try again")
                    continue
                else:
                    self.display_results(searched_key)
                break

    # looks up list from saved csv file
    def show_list(self, a_list):
        while True:
            try:
                with open('work_log.csv', 'r') as csvfile:
                    fields = ['Task name', 'Time(hours)', 'Notes', 'Date']
                    testreader = csv.DictReader(csvfile, fieldnames=fields)
                    self.records = list(testreader)
                    break
            except FileNotFoundError:
                input("There isn't data to look up")
                self.prompt_menu()
                break

        for key in self.records:
            # dates sorted
            if a_list == 'd':
                print((' ' * 10) + key['Date'])
            # time filter
            if a_list == 't':
                print((' ' * 10) + key['Time(hours)'])
            # task names and notes filtered
            if a_list == 'k':
                print(key['Task name'] + (' ' * 10) + key['Notes'])

    # shows search results
    def display_results(self, entries):
        self.clear_screen()
        results = True
        while results:
            index = 0
            while True:
                page = ['[N]ext', '[P]revious', '[B]ack to menu']
                items_dis = entries[index]
                # print heading
                print(' ' + '-' * 10 + "Search Results" + '-' * 10)
                print(' Task name: {}\n'
                      ' Time(hours): {}\n'
                      ' Notes: {}\n'
                      ' Date: {}'.format(items_dis['Task name'],
                                         items_dis['Time(hours)'],
                                         items_dis['Notes'],
                                         items_dis['Date']))
                # disables previous in the begining
                if index == 0:
                    page.remove('[P]revious')
                # disable next at the end
                if index == len(entries) - 1:
                    page.remove('[N]ext')
                page_options = 'n'.join(page) + ': '
                navigate = input('\nOptions: ' + page_options).strip().lower()
                if navigate in 'npbe' and navigate.upper() in page_options:
                    if navigate == 'n':
                        index += 1
                        continue
                    elif navigate == 'p':
                        index -= 1
                        continue
                    elif navigate == 'b':
                        break
                    else:
                        input('\nInvalid entry.'
                              '  Use available entries. Press Enter')
                        continue
            if results:
                break
        self.lookup()

    def clear_screen(self):
        print("\033c", end="")
