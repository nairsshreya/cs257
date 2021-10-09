'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021

   Partners : Nate and Shreya
'''

# from booksdatasource import Author, Book, BooksDataSource
import booksdatasource
import unittest


class BooksDataSourceTester(unittest.TestCase):

    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == booksdatasource.Author('Pratchett', 'Terry'))

    # Checks that return type of .authors function is a list
    def test_authors_return(self):
        authors = []
        self.assertEqual(authors, self.data_source.authors("Smith"))

    # Checks that the return of an unspecified call to author returns all the
    def test_authors_return_full(self):
       # auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
       # auth2 = booksdatasource.Author("Brontë", "Charlotte", 1816, 1855)
       # auth3 = booksdatasource.Author("Brontë", "Ann", 1820, 1849)
       # authors = [auth1, auth3, auth2]
        self.assertEqual(22, len(self.data_source.authors()))

    def test_author_return_value(self):
        auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
        authors = [auth1]
        self.assertEqual(authors, self.data_source.authors("Baldwin"))

    def test_author_return_value_half(self):
        auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
        auth2 = booksdatasource.Author("Brontë", "Charlotte", 1816, 1855)
        authors = [auth1]
        self.assertEqual(authors, self.data_source.authors("Bald"))

    def test_author_order(self):

        auth1 = booksdatasource.Author("Brontë", "Charlotte", 1816, 1855)
        auth2 = booksdatasource.Author("Brontë", "Ann", 1820, 1849)
        auth3 = booksdatasource.Author("Brontë", "Emily", 1818, 1848)
        authors = [auth2, auth1, auth3]
        print("authors list ", authors)
        print("function return list ", self.data_source.authors("Brontë"))
        # if length is the same then compare by checking the object eq
        self.assertEqual(authors,  self.data_source.authors("Brontë"))

    def test_book_return(self):
        bookslist = []
        self.assertEqual(bookslist, self.data_source.books("Blue"))

    # def test_book_return_full(self):
    #     auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
    #     auth2 = booksdatasource.Author("Brontë", "Charlotte", 1816, 1855)
    #     auth3 = booksdatasource.Author("Brontë", "Ann", 1820, 1849)
    #     auth4 = booksdatasource.Author("Orange", "Tommy", 1982)
    #     auth5 = booksdatasource.Author("Willis", "Connie", 1945)
    #     auth6 = booksdatasource.Author("Murakami", "Haruki", 1949)
    #     authors = [auth1, auth3, auth2]
    #     a1 = [auth1]
    #     a2 = [auth2]
    #     a3 = [auth3]
    #     a4 = [auth4]
    #     a5 = [auth5]
    #     a6 = [auth6]
    #     book1 = booksdatasource.Book("The Fire Next Time", 1963, authors)
    #     book2 = booksdatasource.Book("There, There", 2018, a)
    #
    #     bookslist = []
    #     self.assertEqual(bookslist,booksdatasource.BooksDataSource.books("Blue"))

    def test_book_return_value(self):
        auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
        authors = [auth1]
        book1 = booksdatasource.Book("The Fire Next Time", 1963, authors )
        bookslist = [book1]
        self.assertEqual(bookslist, self.data_source.books("The Fire Next Time", "title"))

    def test_book_order(self):
        auth1 = booksdatasource.Author("Christie", "Agatha", 1890, 1976)
        auth2 = booksdatasource.Author("Orange", "Tommy", 1982)
        author_c = [auth1]
        author_o = [auth2]
        book1 = booksdatasource.Book("And Then There Were None", 1939, author_c)
        book2 = booksdatasource.Book("There, There", 2018, author_o)
        bookslist = [book1, book2]
        print("bookslist", bookslist)
        print("function return list", self.data_source.books("There", "title"))
        self.assertEqual(bookslist, self.data_source.books("There", "title"))


    def test_booksbwyrs_return(self):
        booklist = []
        self.assertEqual(booklist, self.data_source.books_between_years(2030, 2038))

    def test_booksbwyrs_return_value(self):
        auth1 = booksdatasource.Author("Baldwin", "James", 1924, 1987)
        author_b = [auth1]
        book1 = booksdatasource.Book("The Fire Next Time", 1963, author_b)
        booklistyrs = [book1]
        self.assertEqual(booklistyrs, self.data_source.books_between_years(1963, 1963))

    def test_booksbwyrs_order(self):
        auth1 = booksdatasource.Author("Willis", "Connie", 1945)
        author_w = [auth1]
        auth2 = booksdatasource.Author("Murakami", "Haruki", 1949)
        author_m = [auth2]
        book1 = booksdatasource.Book("Blackout", 2010, author_w)
        book2 = booksdatasource.Book("1Q84", 2009, author_m)
        book3 = booksdatasource.Book("All Clear", 2010, author_w)
        booklistyrs = [book2, book3, book1]
        self.assertEqual(booklistyrs, self.data_source.books_between_years(2009, 2010))


if __name__ == '__main__':
    unittest.main()
