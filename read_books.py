
import boto3
from boto3.dynamodb.conditions import Key

from read_movies import print_all_movies, print_movie

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Books"

def get_table():
    """Return a reference to the DynamoDB Books table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_book(book):
    title = book.get("Title", "Unknown Title")
    author = book.get("Author", "Unknown Author")
    pages = book.get("Pages", "Unknown Pages")

    print(f"  Title : {title}")
    print(f"  Author: {author}")
    print(f"  Pages : {pages}")
    print()


def get_book_by_title():
    title = input("Enter a book title to search for: ")
    table = get_table()
    
    
    response = table.scan(
        FilterExpression=Key("Title").eq(title)
    )
    items = response.get("Items", [])
    
    if not items:
        print(f"No book found with title '{title}'.")
        return
    
    print(f"Book found:\n")
    print_book(items[0])

def print_all_books():
    """Scan the entire Books table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No books found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)


def main():
    print("===== Reading from DynamoDB =====\n")
    print_all_books()
    get_book_by_title()


if __name__ == "__main__":
    main()

