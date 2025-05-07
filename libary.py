import argparse
import json
import os

FILE_NAME = "library.json"
books = []

def load_books():
    global books
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            books = json.load(file)

def save_books():
    with open(FILE_NAME, "w") as file:
        json.dump(books, file, indent=4)

def add_book(title, author, year, genre, read):
    book_id = len(books) + 1
    books.append({"id": book_id, "title": title, "author": author, "year": year, "genre": genre, "read": read})
    save_books()
    print("📚 Book added successfully!")

def list_books():
    if books:
        print("📖 Library Books:")
        for book in books:
            status = "✔️ Read" if book["read"] else "❌ Unread"
            print(f"{book['id']}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("No books found in the library.")

def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    save_books()
    print("🗑️ Book deleted successfully!")

def update_book(book_id, title, author, year, genre, read):
    for book in books:
        if book['id'] == book_id:
            book['title'] = title
            book['author'] = author
            book['year'] = year
            book['genre'] = genre
            book['read'] = read
            save_books()
            print("✏️ Book updated successfully!")
            return
    print("Book not found!")

def search_books(query):
    found_books = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]
    if found_books:
        for book in found_books:
            print(f"{book['id']}. {book['title']} by {book['author']} ({book['year']})")
    else:
        print("No matching books found.")

def show_statistics():
    total_books = len(books)
    unread_books = sum(1 for book in books if not book['read'])
    genre_counts = {}
    for book in books:
        genre_counts[book['genre']] = genre_counts.get(book['genre'], 0) + 1
    print(f"📊 Total Books: {total_books}, Unread Books: {unread_books}")
    for genre, count in genre_counts.items():
        print(f"📖 {genre}: {count}")

def main():
    load_books()
    parser = argparse.ArgumentParser(prog="library", description="Personal Library Manager CLI Tool")
    parser.add_argument("--add", nargs=5, metavar=("title", "author", "year", "genre", "read"), help="Add a new book")
    parser.add_argument("--list", action="store_true", help="List all books")
    parser.add_argument("--delete", metavar="book_id", type=int, help="Delete a book by ID")
    parser.add_argument("--update", nargs=6, metavar=("book_id", "title", "author", "year", "genre", "read"), help="Update book details")
    parser.add_argument("--search", metavar="query", help="Search for a book by title or author")
    parser.add_argument("--stats", action="store_true", help="Show library statistics")
    
    args = parser.parse_args()
    
    if args.add:
        add_book(args.add[0], args.add[1], int(args.add[2]), args.add[3], args.add[4].lower() == "true")
    elif args.list:
        list_books()
    elif args.delete:
        delete_book(args.delete)
    elif args.update:
        update_book(int(args.update[0]), args.update[1], args.update[2], int(args.update[3]), args.update[4], args.update[5].lower() == "true")
    elif args.search:
        search_books(args.search)
    elif args.stats:
        show_statistics()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
