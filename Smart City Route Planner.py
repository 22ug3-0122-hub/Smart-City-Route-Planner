# Smart City Route Planner


# - Group Members - #
# 22ug3-0122 - K. G. S. Madusanka #
# 22ug3-0474 - K. D. T. Ishinika  #
# 22ug3-0604 - Kalana Helanjith 
# 22ug3-0257 - Niranjan Wijebandara 



class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        # Normal BST insertion
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # Duplicate keys not allowed
            return root

        # Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Get balance
        balance = self.get_balance(root)

        # Rotate if unbalanced
        # Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        # Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        # Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node with one child or no child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            # Node with two children
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        # Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Balance
        balance = self.get_balance(root)

        # Rotate if unbalanced
        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def in_order(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.in_order(root.left, result)
            result.append(root.key)
            self.in_order(root.right, result)
        return result

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_location(self, location):
        if location in self.adj_list:
            print("Location already exists.")
        else:
            self.adj_list[location] = []

    def remove_location(self, location):
        if location in self.adj_list:
            self.adj_list.pop(location)
            for neighbors in self.adj_list.values():
                if location in neighbors:
                    neighbors.remove(location)
        else:
            print("Location does not exist.")

    def add_road(self, loc1, loc2):
        if loc1 not in self.adj_list or loc2 not in self.adj_list:
            print("One or both locations do not exist.")
            return
        if loc2 not in self.adj_list[loc1]:
            self.adj_list[loc1].append(loc2)
        if loc1 not in self.adj_list[loc2]:
            self.adj_list[loc2].append(loc1)

    def remove_road(self, loc1, loc2):
        if loc1 in self.adj_list and loc2 in self.adj_list[loc1]:
            self.adj_list[loc1].remove(loc2)
        if loc2 in self.adj_list and loc1 in self.adj_list[loc2]:
            self.adj_list[loc2].remove(loc1)

    def display_connections(self):
        print("\nConnections:")
        for loc, neighbors in self.adj_list.items():
            print("{} -> {}".format(loc, ", ".join(neighbors) if neighbors else "No connections"))


    def bfs_traversal(self, start):
        visited = set()
        queue = [start]
        traversal = []
        while queue:
            node = queue.pop(0)
            if node not in visited:
                traversal.append(node)
                visited.add(node)
                queue.extend([n for n in self.adj_list[node] if n not in visited])
        return traversal

    def dfs_traversal(self, start):
        visited = set()
        stack = [start]
        traversal = []
        while stack:
            node = stack.pop()
            if node not in visited:
                traversal.append(node)
                visited.add(node)
                stack.extend([n for n in self.adj_list[node] if n not in visited])
        return traversal

def main():
    avl = AVLTree()
    root = None
    graph = Graph()

    while True:
        print("\n--- Smart City Route Planner ---")
        print("1. Add a new location")
        print("2. Remove a location")
        print("3. Add a road between locations")
        print("4. Remove a road")
        print("5. Display all connections")
        print("6. Display all locations (AVL Tree)")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            loc = input("Enter location name: ").strip()
            root = avl.insert(root, loc)
            graph.add_location(loc)
            print(f"Location '{loc}' added.")

        elif choice == '2':
            loc = input("Enter location name to remove: ").strip()
            root = avl.delete(root, loc)
            graph.remove_location(loc)
            print(f"Location '{loc}' removed.")

        elif choice == '3':
            loc1 = input("Enter first location: ").strip()
            loc2 = input("Enter second location: ").strip()
            graph.add_road(loc1, loc2)
            print(f"Road added between '{loc1}' and '{loc2}'.")

        elif choice == '4':
            loc1 = input("Enter first location: ").strip()
            loc2 = input("Enter second location: ").strip()
            graph.remove_road(loc1, loc2)
            print(f"Road removed between '{loc1}' and '{loc2}'.")

        elif choice == '5':
            graph.display_connections()

        elif choice == '6':
            locations = avl.in_order(root)
            print("\nLocations in AVL Tree (in-order):")
            print(", ".join(locations) if locations else "No locations available.")

        elif choice == '7':
            print("Exiting program.")
            break

        else:
            print("Invalid choice! Please enter a number between 1-7.")

if __name__ == "__main__":
    main()
