"""
Exercise 4: Mini-Project - Library Management System
=====================================================
Combine everything: functions, classes, files, and JSON

This exercise brings together all the concepts from the course.
Build a simple library system that tracks books and borrowers.

Instructions:
- Complete all TODOs
- The system should persist data to JSON files
- Run this file to test your implementation

Run with: python exercise_4_project.py
"""

import json
import os
from datetime import datetime


# =============================================================================
# PART 1: HELPER FUNCTIONS
# =============================================================================

def format_date(dt: datetime = None) -> str:
    """
    Format a datetime object as a string "YYYY-MM-DD".
    If no datetime provided, use current date.

    Example:
        format_date(datetime(2024, 1, 15)) -> "2024-01-15"
        format_date() -> "2024-02-04" (today's date)
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")



def generate_id(prefix: str, existing_ids: list) -> str:
    """
    Generate a new unique ID with the given prefix.

    Parameters:
        prefix: String prefix (e.g., "BOOK", "USER")
        existing_ids: List of existing IDs to avoid duplicates

    Returns:
        New ID in format "{prefix}_{number:04d}"

    Example:
        generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) -> "BOOK_0003"
        generate_id("USER", []) -> "USER_0001"
    """
    # Hint: Find the highest existing number and add 1
    max_id = 1
    for existing_id in existing_ids:
        id = int(existing_id.split("_")[1])
        if id >= max_id:
            max_id = id + 1
    return f"{prefix}_{max_id:04d}"


def search_items(items: list, **criteria) -> list:
    """
    Search a list of dictionaries by matching criteria.
    Uses **kwargs to accept any search fields.

    Parameters:
        items: List of dictionaries to search
        **criteria: Field-value pairs to match (case-insensitive for strings)

    Returns:
        List of matching items

    Example:
        books = [
            {"title": "Python 101", "author": "Smith"},
            {"title": "Java Guide", "author": "Smith"},
            {"title": "Python Advanced", "author": "Jones"}
        ]
        search_items(books, author="Smith") -> [first two books]
        search_items(books, title="Python 101") -> [first book]
    """
    # Hint: For each item, check if ALL criteria match
    results = []

    for item in items:
        match = True
        for field, value in criteria.items():
            if field not in item:
                match = False
                break

            item_val = item[field]

            # Case‑insensitive comparison for strings
            if isinstance(item_val, str) and isinstance(value, str):
                if item_val.lower() != value.lower():
                    match = False
                    break
            else:
                if item_val != value:
                    match = False
                    break

        if match:
            results.append(item)

    return results



# =============================================================================
# PART 2: BOOK CLASS
# =============================================================================

class Book:
    """
    Represents a book in the library.

    Class Attributes:
        GENRES: List of valid genres ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    Instance Attributes:
        book_id (str): Unique identifier
        title (str): Book title
        author (str): Author name
        genre (str): Must be one of GENRES
        available (bool): Whether book is available for borrowing

    Methods:
        to_dict(): Convert to dictionary for JSON serialization
        from_dict(data): Class method to create Book from dictionary
        __str__(): Return readable string representation
    """

    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    def __init__(self, book_id: str, title: str, author: str, genre: str, available: bool = True):
        if genre not in Book.GENRES:
            raise ValueError(f"Genre {genre} is not valid")
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        pass

    def to_dict(self) -> dict:
        return {'book_id': self.book_id, 'title': self.title, 'author': self.author, 'genre': self.genre, 'available': self.available}

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(data["book_id"], data["title"], data["author"], data["genre"], data["available"])

    def __str__(self) -> str:
        return f"[{self.book_id}] {self.title} by {self.author} ({self.genre}) - {self.available}"


# =============================================================================
# PART 3: BORROWER CLASS
# =============================================================================

class Borrower:
    """
    Represents a library member who can borrow books.

    Instance Attributes:
        borrower_id (str): Unique identifier
        name (str): Borrower's name
        email (str): Borrower's email
        borrowed_books (list): List of book_ids currently borrowed

    Methods:
        borrow_book(book_id): Add book to borrowed list
        return_book(book_id): Remove book from borrowed list
        to_dict(): Convert to dictionary
        from_dict(data): Class method to create Borrower from dictionary
    """

    MAX_BOOKS = 3  # Maximum books a borrower can have at once

    def __init__(self, borrower_id: str, name: str, email: str, borrowed_books: list = None):
        self.borrower_id = borrower_id
        self.name = name
        self.email = email
        if borrowed_books is None:
            self.borrowed_books = []
        else:
            self.borrowed_books = borrowed_books
        pass

    def can_borrow(self) -> bool:
        """Check if borrower can borrow more books."""
        return len(self.borrowed_books) < Borrower.MAX_BOOKS

    def borrow_book(self, book_id: str) -> bool:
        if self.can_borrow():
            self.borrowed_books.append(book_id)
            return True
        return False

    def return_book(self, book_id: str) -> bool:
        """Remove book from borrowed list. Return False if not found."""
        for book in self.borrowed_books:
            if book_id == book:
                self.borrowed_books.remove(book)
                return True
        return False


    def to_dict(self) -> dict:
        return {
            "borrower_id": self.borrower_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        return cls(data["borrower_id"], data["name"], data["email"], data["borrowed_books"])


# =============================================================================
# PART 4: LIBRARY CLASS (Main System)
# =============================================================================

class Library:
    """
    Main library system that manages books and borrowers.
    Persists data to JSON files.

    Attributes:
        name (str): Library name
        books (dict): book_id -> Book
        borrowers (dict): borrower_id -> Borrower
        books_file (str): Path to books JSON file
        borrowers_file (str): Path to borrowers JSON file

    Methods:
        add_book(title, author, genre) -> Book: Add a new book
        add_borrower(name, email) -> Borrower: Add a new borrower
        checkout_book(book_id, borrower_id) -> bool: Borrower checks out a book
        return_book(book_id, borrower_id) -> bool: Borrower returns a book
        search_books(**criteria) -> list: Search books by criteria
        get_available_books() -> list: Get all available books
        get_borrower_books(borrower_id) -> list: Get books borrowed by a borrower
        save(): Save all data to JSON files
        load(): Load data from JSON files
    """

    def __init__(self, name: str, data_dir: str = "."):
        self.name = name
        self.books = {}
        self.borrowers = {}
        self.books_file = os.path.join(data_dir, "library_books.json")
        self.borrowers_file = os.path.join(data_dir, "library_borrowers.json")
        self.load()

    def load(self) -> None:
        """Load books and borrowers from JSON files."""
        # Hint: Use try/except to handle files not existing
        try:
            with open(self.books_file, "r") as read_books:
                books = json.load(read_books)
                for book_id, book_data in books.items():
                    self.books[book_id] = Book.from_dict(book_data)
        except FileNotFoundError:
            self.books = {}
        try:
            with open(self.borrowers_file, "r") as read_borrowers:
                borrowers = json.load(read_borrowers)
                for borrower_id, borrower_data in borrowers.items():
                    self.borrowers[borrower_id] = Borrower.from_dict(borrower_data)
        except FileNotFoundError:
            self.borrowers = {}
        return

    def save(self) -> None:
        """Save books and borrowers to JSON files."""
        # Hint: Convert Book/Borrower objects to dicts using to_dict()
        with open(self.books_file, "w") as write_books:
            books = {}
            for book_id, book in self.books.items():
                books[book_id] = book.to_dict()
            json.dump(books, write_books, indent=2)
        with open(self.borrowers_file, "w") as write_borrowers:
            borrowers = {}
            for borrower_id, borrower in self.borrowers.items():
                borrowers[borrower_id] = borrower.to_dict()
            json.dump(borrowers, write_borrowers, indent=2)
        return

    def add_book(self, title: str, author: str, genre: str) -> Book:
        """Add a new book to the library."""
        ids = []
        for book in self.books:
            ids.append(book)
        new_id = generate_id('BOOK', ids)
        new_book = Book(new_id, title, author, genre)
        self.books[new_id] = new_book
        self.save()
        return new_book

    def add_borrower(self, name: str, email: str) -> Borrower:
        """Register a new borrower."""
        ids = []
        for borrower in self.borrowers:
            ids.append(borrower)
        new_id = generate_id('BORROWER', ids)
        borrower = Borrower(new_id, name, email)
        self.borrowers[new_id] = borrower
        self.save()
        return borrower

    def checkout_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower checks out a book.
        Returns False if book unavailable, borrower not found, or at max limit.
        """
        wanted_book =  None
        if self.books[book_id] and self.books[book_id].available:
           wanted_book = self.books[book_id]
        if wanted_book is None:
            return False
        wanted_borrower = None
        if self.borrowers[borrower_id] and self.borrowers[borrower_id].can_borrow():
                wanted_borrower = self.borrowers[borrower_id]
        if wanted_borrower is None:
            return False
        wanted_book.available = False
        wanted_borrower.borrow_book(wanted_book.book_id)
        self.save()
        return True

    def return_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower returns a book.
        Returns False if book/borrower not found or book wasn't borrowed by this person.
        """
        wanted_book =  None
        if self.books[book_id]:
           wanted_book = self.books[book_id]
        if wanted_book is None:
            return False
        wanted_borrower = None
        if self.borrowers[borrower_id] and book_id in self.borrowers[borrower_id].borrowed_books:
                wanted_borrower = self.borrowers[borrower_id]
        if wanted_borrower is None:
            return False
        wanted_book.available = True
        wanted_borrower.return_book(wanted_book.book_id)
        return True

    def search_books(self, **criteria) -> list:
        """Search books by any criteria (title, author, genre, available)."""
        # Hint: Convert self.books.values() to list of dicts first
        books = []
        for book, book_data in self.books.items():
            books.append(book_data.to_dict())
        return search_items(books, **criteria)


    def get_available_books(self) -> list:
        """Get list of all available books."""
        available_books = []
        for book in self.books.values():
            if book.available:
                available_books.append(book)
        return available_books

    def get_borrower_books(self, borrower_id: str) -> list:
        """Get list of books currently borrowed by a borrower."""
        borrower = self.borrowers[borrower_id]
        if borrower is None:
            return []
        if len(borrower.borrowed_books) == 0:
            return []
        borrower_books = []
        for book in borrower.borrowed_books:
            borrower_books.append(self.books[book])
        return borrower_books

    def get_statistics(self) -> dict:
        """
        Return library statistics.
        Uses the concepts of dict comprehension and aggregation.
        """
        # - total_books: total number of books
        # - available_books: number of available books
        # - checked_out: number of checked out books
        # - total_borrowers: number of borrowers
        # - books_by_genre: dict of genre -> count
        stats = {}

        stats["total_books"] = len(self.books)
        stats["total_borrowers"] = len(self.borrowers)
        checked_out = 0
        available = 0
        books_by_genre = {}
        for book in self.books.values():
            if book.available:
                available += 1
            else:
                checked_out += 1
            if book.genre in books_by_genre:
                books_by_genre[book.genre] += 1
            else:
                books_by_genre[book.genre] = 1
        stats["checked_out"] = checked_out
        stats["available"] = available
        stats["books_by_genre"] = books_by_genre
        return stats


