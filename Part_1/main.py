from upload_data import seed_mongo_db
from models import Author, Quote, Tag
from datetime import datetime

def display_quotes_by_author_name(value):
    author_value = Author.objects(fullname=value).first()
    if author_value:
        quotes = Quote.objects(author=author_value)
        if quotes:
            print(f"\nQuotes by author: {value}")
            for quote in quotes:
                print(f"Quote: {quote.quote}")
        else:
            print(f"No quotes found by {value}.")
    else:
        print(f"No authors found with the name {value}.")

def display_quotes_by_given_tag(value):
    quotes = Quote.objects(tags__name=value)
    if quotes:
        print(f"\nQuotes with tag: {value}")
        for quote in quotes:
            print(f"Quote: {quote.quote}")
    else:
        print(f"No quotes found with the tag {value}.")

def display_quotes_by_given_tags(values):
    try:
        tags = values.split(',')
        unique_quotes = set()
        quotes = Quote.objects(tags__name__in=tags)

        if quotes:
            print(f"\nQuotes with tags: {', '.join(tags)}")
            print("-"*20)
            for quote in quotes:
                unique_quotes.add(quote.quote)

            for quote in unique_quotes:
                print(f"Quote: {quote}")
        else:
            print(f"No quotes found with the tags {', '.join(tags)}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

COMMAND_SEARCH_DICT = {
    "name": display_quotes_by_author_name,
    "tag": display_quotes_by_given_tag,
    "tags": display_quotes_by_given_tags
}

def main():
    choice = input("Would you like to populate the MongoDB database with data?(Y/N) ")
    if choice.lower().strip() in ["y", "yes"]:
        seed_mongo_db()
    print("""
          Enter command: name, tag, or tags.
          name: Steve Martin — find and display all quotes by the author Steve Martin;
          tag: life — find and display all quotes for the tag life;
          tags: life, live — find and display all quotes containing tags life or live (without spaces between tags);
          exit — close the script;"""
          )
    while True:
        user_input = input("\nEnter command\n ")
        if user_input.lower() == "exit" or user_input.lower() == "close":
            break
        input_splitted = user_input.split(":")
        command = input_splitted[0].lower().strip()
        if command in COMMAND_SEARCH_DICT:
            if len(input_splitted) > 1:
                value = input_splitted[1].strip()
                if len(value) == 0:
                    print("You have not provided any value. Please, try again.")
                else:
                    COMMAND_SEARCH_DICT[command](value)
            else:
                print(
                    f"No value provided for command: {command}. Please, try again.")
        else:
            print("Invalid command format. Please try again.")

if __name__ == "__main__":
    main()
