class Library:
    def __init__(self):
        self.books = []          # list of all books
        self.issued_books = {}   # student_id : list of books

    def add_book(self, book_title):
        self.books.append(book_title)
        return f"Book '{book_title}' added to library."

    def issue_book(self, student_id, book_title):
        if book_title not in self.books:
            raise ValueError("Book not available in library.")
        if student_id not in self.issued_books:
            self.issued_books[student_id] = []
        self.issued_books[student_id].append(book_title)
        self.books.remove(book_title)
        return f"Book '{book_title}' issued to Student {student_id}."

    def return_book(self, student_id, book_title):
        if student_id in self.issued_books and book_title in self.issued_books[student_id]:
            self.issued_books[student_id].remove(book_title)
            self.books.append(book_title)
            return f"Book '{book_title}' returned by Student {student_id}."
        else:
            raise ValueError("Book not found in issued list.")

    def search_book(self, book_title):
        if book_title in self.books:
            return f"Book '{book_title}' is available in library."
        for sid, books in self.issued_books.items():
            if book_title in books:
                return f"Book '{book_title}' is currently issued to Student {sid}."
        return f"Book '{book_title}' not found in library records."

    def __str__(self):
        return f"Library(Available: {len(self.books)}, Issued: {sum(len(b) for b in self.issued_books.values())})"

    def __repr__(self):
        return f"Library(books={self.books}, issued_books={self.issued_books})"
