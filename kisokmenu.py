import mysql.connector
from mysql.connector import Error
from collections import Counter

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='fast_food_kiosk',
            user='root',
            password='root'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to display the menu
def display_menu(cursor):
    cursor.execute("SELECT id, name, price FROM menu")
    items = cursor.fetchall()
    if items:
        print("\nMenu:")
        for index, (id, name, price) in enumerate(items, start=1):
            print(f"{index}. {name}: ${price:.2f}")
    else:
        print("Menu is empty.")
    return items

# Function to handle user orders
def handle_order(cursor):
    order = []
    
    # Fetch all menu items
    cursor.execute("SELECT id, name FROM menu")
    menu_items = cursor.fetchall()
    
    # Create a dictionary to map item numbers to item IDs
    items = {str(index + 1): item[0] for index, item in enumerate(menu_items)}
    
    while True:
        print("\nAvailable items:")
        for num, id in items.items():
            cursor.execute("SELECT name FROM menu WHERE id = %s", (id,))
            item_name = cursor.fetchone()[0]
            print(f"{num}. {item_name}")
            
        item_number = input("Enter the number of the item you want to add (or '0' to finish): ").strip()
        if item_number == '0':
            break
        if item_number in items:
            item_id = items[item_number]
            cursor.execute("SELECT id, name, price FROM menu WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if item:
                order.append(item)
            else:
                print("Error retrieving item. Please try again.")
        else:
            print("Invalid item number. Please try again.")
    
    return order


# Function to print the receipt
def print_receipt(order):
    if not order:
        print("No items in order.")
        return

    item_counts = Counter(order)
    total = 0
    print("\nReceipt:")
    print("=" * 40)
    for (id, name, price), count in item_counts.items():
        item_total = price * count
        total += item_total
        print(f"{name:<20} x{count:<3} ${item_total:>7.2f}")
    print("=" * 40)
    print(f"{'Total':<20} ${total:>7.2f}")
    print("=" * 40)

def main():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        while True:
            choice = input("\nEnter 'menu' to view the menu, 'order' to start an order, or 'exit' to quit: ").strip().lower()
            if choice == 'menu':
                display_menu(cursor)
            elif choice == 'order':
                order = handle_order(cursor)
                print_receipt(order)
            elif choice == 'exit':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
