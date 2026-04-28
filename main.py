"""
Concepts We Are Practicing:
- Functions
- Loops and Menu-Driven Programs
- Lists and Data Filtering
- Dictionaries
- Counter (from collections)

Modules and Libraries:
- API Requests (requests)
- Text Processing (re - regular expressions)
"""

"""
Author: Amarys Aranda
GitHub Link: https://github.com/dramidesu/your-repo
Project: Book Analyzer (CS I Project)
Extra credit: 
- I was able to implement a deletion system (line 150)
- Made timeout length 15 to allow a larger request time (line 52)
- Added an extra "else" statement if input > 5 or < 0 (line 199)
"""

import requests
import re
from collections import Counter


# -----------------------------
# INITIAL DATA
# -----------------------------

my_library = {
    "Moby Dick": "https://www.gutenberg.org/files/2701/2701-0.txt"
}

# TODO 3: Read stop words from a file instead; this file "EN-Stopwords" contains thousands stop words(2 points)
STOP_WORDS = []
opened_txt = open("EN-Stopwords.txt", "r")
for line in opened_txt:
    stop_word = line.strip()
    STOP_WORDS.append(stop_word)


# -----------------------------
# FETCH BOOK
# -----------------------------
def fetch_book(url):
    """Download text from a URL."""
    # TODO 4: Handle exceptions (network errors, invalid URLs, etc.) (1 point)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except exceptions.Timeout:
        print("ERROR: Request timeout.")
        return ""
    except exceptions.ConnectionError:
        print("ERROR: Connection error")
        return ""
    except:
        print("An error has occurred. Please try again.")
        return ""

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(raw_text):
    """Lowercase text and remove punctuation."""
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

# -----------------------------
# ANALYZE TEXT
# -----------------------------
def analyze_text(words):
    """Remove stop words and count frequencies."""
    filtered_words = [] 
    for w in words: 
        if w not in STOP_WORDS and len(w) > 2:   #checking len(w)> 2 to remove tiny words((is, to, at))
            filtered_words.append(w)

    return Counter(filtered_words).most_common(10)



# -----------------------------
# VISUALIZATION (BAR CHART)
# -----------------------------

def plot_results(stats, title):
    print(f"\n||===== MOST COMMON WORDS: {title} =====||\n")

    for r in stats:
        if r not in STOP_WORDS:

            minus_space = (10 - len(r[0])) * " " #Measures whitespace length
            print(r[0] + minus_space + "| ", end="")
            for f in range(0, (r[1] // 2), 20):
                print("█", end="")
            print(f" ({r[1]})")

    """Create a bar chart of word frequencies."""
    pass 

# -----------------------------
# MENU SYSTEM
# -----------------------------
def main():
    while True:
        print("\n||=== LIBRARY MANAGER ===||")
        print(f"Current Books: {list(my_library.keys())}")
        print("1. Add New Book 📚")
        print("2. Remove Book 🗑️")
        print("3. Update Book URL 🔗")
        print("4. Analyze a Book 🔎")
        print("5. Exit")

        choice = input("\nSelect (1-5): ")

        if choice == '1':
            # Add new books to the dictionary (use this website: https://www.gutenberg.org/browse/scores/top)

            name = input("Enter Book Title: ").strip().title() #Ignores whitespace and upper/lowercase
            if name == "": #Checks invalid name
                print("INVALID TITLE: Please try again")
                continue
            url = input("Enter Gutenberg .txt URL: ")
            if url == "": #Checks invalid URL
                print("INVALID URL: Please try again")
                continue

            if name in my_library: #Checks duplicate title
                print("DUPLICATE TITLE: Please try again")
                continue

            my_library[name] = url
            print(f"'{name}' successfully added.")

        elif choice == '2':
            # Remove books from the dictionary

            name = input("Enter title to remove: ").strip().title()

            if name not in my_library: #Checks if book exists
                print("Title not found in library.")
                continue           
            
            del my_library[name] #Deletes book from my_library
            print(f" '{name}' successfully deleted.")

        elif choice == '3':
            # UPDATE OPERATION
            name_input = input("Enter the book title to update: ").strip().lower()
            target_key = None  # Start with None in case we don't find it

            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break  # We found it, so stop looking

            if target_key:
                print(f"Current URL: {my_library[target_key]}")
                new_url = input("Enter new URL: ").strip()
                if new_url == "":
                    print("Invalid URL. Update cancelled.")
                else:
                    my_library[target_key] = new_url
                    print(f"'{target_key}' updated successfully.")
            else:
                print("Book not found.")

        elif choice == '4':
            name_input = input("Which book to analyze? ").strip().lower()
            
            target_key = None
            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break

            if target_key:
                url = my_library[target_key]
                print(f"Fetching and analyzing '{target_key}'...")
                raw_text = fetch_book(url)

                if raw_text:
                    words = clean_text(raw_text)
                    stats = analyze_text(words)
                    plot_results(stats, target_key)
            else:
                print("ERROR: Book not found.")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Incorrect input. Please try again.")

if __name__ == "__main__":
    main()