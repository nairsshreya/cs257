'''
    Authors : Nate and Shreya
    For course CS 257 Books Project
    October 1st, 2021
'''
import sys
import booksdatasource


class Books:
    '''
    Usage of program cmd line
        python3 books.py "filename" -[option]/--[option] OR python3 books.py -h/--help
    '''

    # A boolean variable that is used for debugging
    debug = False

    # Prints the usage statement.
    def help_txt(self):
        log = open("usage.txt", "r").read()
        print(log)
        sys.exit()


    def book_option(self, arguments):
        '''
            Returns a list of books that have been searched for based on the type of search,
             a search text is not necessary :
                1. -p : sorting by publication year.
                2. -ti : sorting by title, alphabetically.
        '''
        new_search_b = booksdatasource.BooksDataSource(arguments[1])
        if len(arguments) == 3:
            results = new_search_b.books(None, 'title')
            return results
        elif len(sys.argv) == 2:
            print("Wrong command line syntax, refer to usage statements by using -h or --help")
            return []  # call help
        elif len(arguments) == 4:
            results = new_search_b.books(arguments[3], 'title')
            return results
        elif len(arguments) == 5:
            if self.debug:
                print("here args are 6 so printing by title or year")
            if arguments[3].strip() == "-p":
                results = new_search_b.books(arguments[4], 'year')
                return results
            elif arguments[3].strip() == "-ti":
                results = new_search_b.books(arguments[4], 'title')
                return results
        else:
            return []


    def author_option(self, arguments):
        '''
         Returns a list of authors based on search type :
            1. With a search text
            2. Without a search text, which returns a list of all the authors.
        '''
        new_search_a = booksdatasource.BooksDataSource(arguments[1])
        if arguments[2] == "-a" or arguments[2] == "--author":
            if self.debug:
                print("in author search")
            if len(arguments) == 3:
                results = new_search_a.authors()
                return results
            elif len(arguments) == 4:
                results = new_search_a.authors(arguments[3])
                return results
            else:
                return []

    def year_option(self, arguments):
        '''
        Returns a list of books that were published between some years.
        If no second year was given, return a list of books beginning at the given year.
        '''
        if arguments[2] == '-y' or arguments[2] == '--year':
            new_search_y = booksdatasource.BooksDataSource(arguments[1])
            if arguments[3].isnumeric():
                if len(arguments) == 4:
                    results = new_search_y.books_between_years(arguments[3], None)
                    return results
                elif arguments[4].isnumeric():
                    results = new_search_y.books_between_years(arguments[3], arguments[4])
                    return results
        else:
            return []

    def print_books(self, results):
        '''
        Prints the book list
        '''
        for book in results:
            if self.debug:
                print("new book print ", book)
            auth_line = ""
            for auth in book.authors:
                auth_line = auth_line + auth.given_name + " " + auth.surname + " " + auth.birth_year + "-" + \
                            str(auth.death_year) + " "
            print_line = book.title + ", " + book.publication_year + ", " + auth_line
            print(print_line)


    def print_auth(self, results):
        '''
        Prints the author list
        '''
        auth_line = ""
        for auth in results:
            auth_line = ""
            auth_line = auth_line + auth.given_name + " " + auth.surname + " " + str(auth.birth_year) + "-" + \
                        str(auth.death_year) + " "
            print(auth_line)


'''
    Instantiation of the program and calling of the function
'''

new_book_program = Books()
if "--help" in sys.argv or "-h" in sys.argv:
    new_book_program.help_txt()
else :
        if len(sys.argv) == 2:
            print("You require a search option, here are the usage statements, please run again")
            new_book_program.help_txt()

        elif sys.argv[2] == "-b" or sys.argv[2] == "--books":
            results = new_book_program.book_option(sys.argv)
            if len(results) == 0:
                print("Sorry, no items came up with your search, please try again.")
            else:
                new_book_program.print_books(results)
        elif sys.argv[2] == "-a" or sys.argv[2] == "--author":
            results = new_book_program.author_option(sys.argv)
            if len(results) == 0:
                print("Sorry, no items came up with your search, please try again.")
            else:
                new_book_program.print_auth(results)
        elif sys.argv[2] == "-y" or sys.argv[2] == "--year":
            results = new_book_program.year_option(sys.argv)
            if len(results) == 0:
                print("Sorry, no items came up with your search, please try again.")
            else:
                new_book_program.print_books(results)
        else:
            print("Invalid syntax. Refer to usage statements using -h or --help and rerun")
