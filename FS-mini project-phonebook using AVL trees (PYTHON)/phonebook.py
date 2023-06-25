class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


class AVLNode:
    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self, file_name):
        self.root = None
        self.file_name = file_name
        self.load_contacts()

    def add_contact(self, contact):
        self.root = self._insert(self.root, contact)
        self.save_contacts()
        print("Contact added successfully.")

    def search_contact(self, name):
        node = self._search(self.root, name)
        if node:
            self.display_contact(node.contact)
        else:
            print("Contact not found.")

    def remove_contact(self, name):
        self.root = self._remove(self.root, name)
        self.save_contacts()
        print("Contact removed successfully.")

    def display_phonebook(self):
        if self.root:
            self._in_order_traversal(self.root)
        else:
            print("Phonebook is empty.")

    def _create_node(self, contact):
        return AVLNode(contact)

    def _get_height(self, node):
        if node:
            return node.height
        return 0

    def _get_balance_factor(self, node):
        if node:
            return self._get_height(node.left) - self._get_height(node.right)
        return 0

    def _update_height(self, node):
        if node:
            node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rotate_left(self, node):
        pivot = node.right
        sub_tree = pivot.left
        pivot.left = node
        node.right = sub_tree
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    def _rotate_right(self, node):
        pivot = node.left
        sub_tree = pivot.right
        pivot.right = node
        node.left = sub_tree
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    def _balance_node(self, node):
        if node:
            self._update_height(node)
            balance_factor = self._get_balance_factor(node)

            if balance_factor > 1:
                if self._get_balance_factor(node.left) >= 0:
                    return self._rotate_right(node)
                else:
                    node.left = self._rotate_left(node.left)
                    return self._rotate_right(node)

            if balance_factor < -1:
                if self._get_balance_factor(node.right) <= 0:
                    return self._rotate_left(node)
                else:
                    node.right = self._rotate_right(node.right)
                    return self._rotate_left(node)

        return node

    def _insert(self, node, contact):
        if not node:
            return self._create_node(contact)

        if contact.name < node.contact.name:
            node.left = self._insert(node.left, contact)
        elif contact.name > node.contact.name:
            node.right = self._insert(node.right, contact)
        else:
            # Duplicate contact, do not insert
            return node

        return self._balance_node(node)

    def _search(self, node, name):
        if not node or node.contact.name == name:
            return node

        if name < node.contact.name:
            return self._search(node.left, name)
        else:
            return self._search(node.right, name)

    def _find_minimum_node(self, node):
        current = node
        while current and current.left:
            current = current.left
        return current

    def _remove(self, node, name):
        if not node:
            return None

        if name < node.contact.name:
            node.left = self._remove(node.left, name)
        elif name > node.contact.name:
            node.right = self._remove(node.right, name)
        else:
            if not node.left and not node.right:
                # Leaf node
                del node
                return None
            elif not node.left:
                # Node with only right child
                temp = node.right
                del node
                return temp
            elif not node.right:
                # Node with only left child
                temp = node.left
                del node
                return temp
            else:
                # Node with both left and right children
                successor = self._find_minimum_node(node.right)
                node.contact = successor.contact
                node.right = self._remove(node.right, successor.contact.name)

        return self._balance_node(node)

    def _in_order_traversal(self, node):
        if node:
            self._in_order_traversal(node.left)
            self.display_contact(node.contact)
            self._in_order_traversal(node.right)

    def load_contacts(self):
        try:
            with open(self.file_name, "r") as file:
                self.root = None
                lines = file.readlines()
                for i in range(0, len(lines), 2):
                    name = lines[i].strip()
                    phone_number = lines[i + 1].strip()
                    contact = Contact(name, phone_number)
                    self.root = self._insert(self.root, contact)
        except FileNotFoundError:
            print("Phonebook file not found. Creating a new file.")

    def save_contacts(self):
        try:
            with open(self.file_name, "w") as file:
                self._save_contacts_util(self.root, file)
        except IOError:
            print("Error: Unable to save contacts.")

    def _save_contacts_util(self, node, file):
        if node:
            self._save_contacts_util(node.left, file)
            file.write(node.contact.name + "\n")
            file.write(node.contact.phone_number + "\n")
            self._save_contacts_util(node.right, file)

    @staticmethod
    def display_contact(contact):
        print("Name:", contact.name)
        print("Phone Number:", contact.phone_number)
        print()


if __name__ == "__main__":
    phonebook = AVLTree("phonebook.txt")

    while True:
        print('''

                --------------------------------------------------------------------------------------------------
                ------------------------------PhoneBook MiniProject Using AVL Trees-------------------------------
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                ********|| 1MV21IS400 M SHAKTHI RAJ || 1MV21IS401 PAVAN KUMAR || 1MV21IS404 SANDEEP RC ||*********
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        ''')
        print("Menu:")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Remove Contact")
        print("4. Display Phonebook")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Enter contact name: ")
            phone_number = input("Enter phone number: ")
            contact = Contact(name, phone_number)
            phonebook.add_contact(contact)
        elif choice == 2:
            name = input("Enter contact name to search: ")
            phonebook.search_contact(name)
        elif choice == 3:
            name = input("Enter contact name to remove: ")
            phonebook.remove_contact(name)
        elif choice == 4:
            phonebook.display_phonebook()
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

        print()
