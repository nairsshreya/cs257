#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
    Partners : Nate and Shreya Nair
    Revisions by Shreya Nair
'''

import csv

from functools import cmp_to_key

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

    def __str__(self):
        return f'Author({self.surname}, {self.given_name})'

    # def __repr__(self):
    #     return f'Author({self.surname}, {self.given_name})'


class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title


class BooksDataSource:
    def __init__(self, books_csv_file_name):

        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.debug = False
        book_info = []
        self.book_list = []
        self.author_list = []
        book_auth_list = []
        with open(books_csv_file_name) as book_file:
            book_file = book_file.readlines()
        if self.debug:
            print("File has been read length of file = ", len(book_file))
        for line in csv.reader(book_file, quotechar='"', delimiter=",", skipinitialspace=True):
            if self.debug:
                print(line)
            if self.debug:
                print("Line in file before split : ", line)
            if self.debug:
                print("Line in temp_split[2] before split : ", line[2])

            temp_split2 = line[2].split(' and ')
            book_auth_list = []
            for auth_info in temp_split2:
                if self.debug:
                    print("Line in temp_split2 before split : ", auth_info)
                temp_auth_string = auth_info.split('(')
                name = temp_auth_string[0].strip().split(" ")
                first_name = ""
                first_name = " ".join(name[:-1])
                last_name = name[-1]
                year_split = temp_auth_string[1].strip().strip(')').split('-')
                year1 = year_split[0]
                year2 = year_split[1]
                if len(year2) == 0:
                    year2 = None
                if not year1:
                    year1 = None
                new_author = Author(last_name, first_name, year1, year2)
                flag = False
                for author in self.author_list:
                    if author.__eq__(new_author):
                        book_auth_list.append(author)
                        flag = True
                        break
                if not flag:
                    self.author_list.append(new_author)
                    book_auth_list.append(new_author)

            new_book = Book(line[0], line[1], book_auth_list)
            self.book_list.append(new_book)
        if self.debug:
            print(self.author_list)

    def compare(self, auth1, auth2):

        if auth1.surname > auth2.surname:
            return 1

        elif auth1.surname < auth2.surname:
            return -1

        elif auth1.surname == auth2.surname:
            if auth1.given_name > auth2.given_name:
                return 1
            elif auth1.given_name < auth2.given_name:
                return -1
            else:
                return 0

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''

        result_list = []
        if search_text is None:
            for author in self.author_list:
                # author_name = author.given_name + author.surname
                result_list.append(author)

        else:
            for author in self.author_list:
                if search_text.lower() in author.given_name.lower() or search_text.lower() in author.surname.lower():
                    result_list.append(author)

        result_list = sorted(result_list, key=cmp_to_key(self.compare))
        # Sorting with the given name if surname is the same
        return result_list

    def book_compare_year(self, book1, book2):

        if book1.publication_year > book2.publication_year:
            return 1
        elif book1.publication_year < book2.publication_year:
            return -1
        else:
            if book1.title > book2.title :
                return 1
            elif book1.title < book2.title:
                return -1
            else:
                return 0

    def book_compare_title(self, book1, book2):
        
        if book1.title > book2.title:
            return 1
        elif book1.title < book2.title:
            return -1
        else:
            if book1.publication_year > book2.publication_year:
                return 1
            elif book1.publication_year < book2.publication_year:
                return -1
            else: return 0

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        new_book_list = []
        if search_text is not None:
            for book in self.book_list:
                if book.title.lower().__contains__(search_text.lower()):
                    new_book_list.append(book)
        else:
            for book in self.book_list:
                new_book_list.append(book)

        if sort_by == 'year':
            new_book_list = sorted(new_book_list, key=cmp_to_key(self.book_compare_year))
        else:
            new_book_list = sorted(new_book_list, key=cmp_to_key(self.book_compare_title))

        return new_book_list


    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        new_book_list = []
        if start_year != None and end_year != None:
            for book in self.book_list:
                if int(book.publication_year) >= int(start_year) and int(book.publication_year) <= int(end_year):
                    new_book_list.append(book)
        elif int(start_year) != None:
            for book in self.book_list:
                if int(book.publication_year) >= int(start_year):
                    new_book_list.append(book)
        elif int(end_year) != None:
            for book in self.book_list:
                if int(book.publication_year) <= int(end_year):
                    new_book_list.append(book)
        else:
            for book in self.book_list:
                new_book_list.append(book)

        new_book_list = sorted(new_book_list, key=cmp_to_key(self.book_compare_year))

        return new_book_list
