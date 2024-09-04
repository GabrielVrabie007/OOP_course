class Book():
    def __init__(self,title,author,ISBN):
        self.title = title
        self.author =author
        self.ISBN =ISBN

class Library():
    def __init__(self,book_list):
        self.book_list = book_list

    def add_book(self,book):
        self.book_list.append(book)
        return self.book_list
    def remove_book(self,book):
        self.book_list.remove(book)
        return self.book_list
    def display_books(self):
        for book in self.book_list:
            return f"{"Title:"+book.title+"\n","Author:"+book.author,"ISBN:"+book.ISBN}"