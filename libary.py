import sqlite3

# SQLite database se connect karega (Agar file nahi hai to naye database banayega)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Books table create kar raha hai agar pehle se nahi bani
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        status TEXT DEFAULT 'Available'
    )
''')
conn.commit()

# Function: Nayi book add karna
def add_book(title, author, genre, year):
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", 
                   (title, author, genre, year))
    conn.commit()
    print(f"✅ Book '{title}' add ho gayi!")

# Function: Saari books dikhana
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("❌ Koi book nahi mili!")

# Function: Title ya author ke basis pe search karna
def search_book(keyword):
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   (f'%{keyword}%', f'%{keyword}%'))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("❌ Koi matching book nahi mili!")

# Function: Book ki details update karna
def update_book(book_id, title, author, genre, year):
    cursor.execute("UPDATE books SET title=?, author=?, genre=?, year=? WHERE id=?", 
                   (title, author, genre, year, book_id))
    conn.commit()
    print("✅ Book update ho gayi!")

# Function: Book delete karna
def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    print("✅ Book delete ho gayi!")

# Function: Book borrow karna (Available se Borrowed status change hoga)
def borrow_book(book_id):
    cursor.execute("UPDATE books SET status='Borrowed' WHERE id=? AND status='Available'", (book_id,))
    if cursor.rowcount:
        conn.commit()
        print("📖 Book borrow ho gayi!")
    else:
        print("❌ Book pehle se borrowed hai ya nahi mili!")

# Function: Book wapas karna
def return_book(book_id):
    cursor.execute("UPDATE books SET status='Available' WHERE id=?", (book_id,))
    conn.commit()
    print("📖 Book return ho gayi!")

# Menu system (CLI Interface)
while True:
    print("\n📚 Library Management System")
    print("1. ➕ Add Book")
    print("2. 📜 View Books")
    print("3. 🔎 Search Book")
    print("4. ✏ Update Book")
    print("5. ❌ Delete Book")
    print("6. 📖 Borrow Book")
    print("7. 🔄 Return Book")
    print("8. 🚪 Exit")
    
    choice = input("➡ Enter your choice: ")
    
    if choice == '1':
        title = input("📖 Title: ")
        author = input("✍ Author: ")
        genre = input("📂 Genre: ")
        year = input("📅 Year: ")
        add_book(title, author, genre, year)
    elif choice == '2':
        view_books()
    elif choice == '3':
        keyword = input("🔎 Enter title/author: ")
        search_book(keyword)
    elif choice == '4':
        book_id = int(input("🔢 Book ID: "))
        title = input("📖 New Title: ")
        author = input("✍ New Author: ")
        genre = input("📂 New Genre: ")
        year = input("📅 New Year: ")
        update_book(book_id, title, author, genre, year)
    elif choice == '5':
        book_id = int(input("🔢 Enter Book ID: "))
        delete_book(book_id)
    elif choice == '6':
        book_id = int(input("🔢 Enter Book ID to borrow: "))
        borrow_book(book_id)
    elif choice == '7':
        book_id = int(input("🔢 Enter Book ID to return: "))
        return_book(book_id)
    elif choice == '8':
        print("🚪 System exit ho raha hai...")
        break
    else:
        print("❌ Invalid choice, try again!")

# Database connection close karna
conn.close()