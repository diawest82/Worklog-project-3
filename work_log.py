from entries import Entries


class Work_log(Entries):

    def __init__(self):
        self.entry = Entries()

    # clears screen
    def clear_screen(self):
        print("\033c", end="")

    # starts program
    def welcome(self):
        self.clear_screen()
        print(' ' * 15 + ' Welcome ' + ' ' * 15)
        input('Press enter to get started')
        self.entry.prompt_menu()

    # executes program
if __name__ == '__main__':
    test = Work_log()
    test.welcome()
