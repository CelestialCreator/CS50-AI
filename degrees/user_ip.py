from degrees import load_data, person_id_for_name, neighbors_for_person, movies, people
from util import Node, QueueFrontier

def construct_path_string(path, source):
    """
    Constructs a readable string showing the path between actors.
    """
    if path is None:
        return "Not connected."
    
    degrees = len(path)
    result = [f"{degrees} degrees of separation."]
    
    # Start with source
    current_person = source
    
    # Add each connection
    for i, (movie_id, person_id) in enumerate(path):
        person1 = people[current_person]["name"]
        person2 = people[person_id]["name"]
        movie = movies[movie_id]["title"]
        result.append(f"{i+1}: {person1} and {person2} starred in {movie}")
        current_person = person_id
    
    return "\n".join(result)

def find_actor_connection(source_name, target_name, directory="large"):
    """
    Finds connection between two actors.
    Returns path and prints the connection details.
    """
    # Load data
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get person IDs
    source = person_id_for_name(source_name)
    if source is None:
        return "Source person not found."
        
    target = person_id_for_name(target_name)
    if target is None:
        return "Target person not found."

    # Find shortest path
    path = shortest_path(source, target)
    
    if path is None:
        return "Not connected."
    else:
        return construct_path_string(path, source)

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    """
    # Initialize frontier with starting position
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    
    # Initialize explored set
    explored = set()
    
    # Keep track of path
    while True:
        if frontier.empty():
            return None
        
        node = frontier.remove()
        explored.add(node.state)
        
        # Check neighbors
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                if person_id == target:
                    # Found target - construct path
                    path = []
                    current = Node(
                        state=person_id,
                        parent=node,
                        action=(movie_id, person_id)
                    )
                    # Add the final connection
                    path.append(current.action)
                    # Add all previous connections
                    while current.parent.parent is not None:
                        current = current.parent
                        path.append(current.action)
                    path.reverse()
                    return path
                
                child = Node(
                    state=person_id,
                    parent=node,
                    action=(movie_id, person_id)
                )
                frontier.add(child)

def main():
    # Let user choose dataset
    while True:
        dataset = input("Choose dataset (small/large) [default: large]: ").lower().strip()
        if dataset == "":
            dataset = "large"
        if dataset in ["small", "large"]:
            break
        print("Please enter either 'small' or 'large'")

    # Keep running until user wants to quit
    while True:
        print("\nEnter names of two actors to find their connection")
        print("(Press Ctrl+C or type 'quit' at any prompt to exit)")
        
        try:
            # Get first actor
            source = input("\nFirst actor: ")
            if source.lower() == 'quit':
                break
                
            # Get second actor
            target = input("Second actor: ")
            if target.lower() == 'quit':
                break
            
            # Find and display connection
            result = find_actor_connection(source, target, dataset)
            print("\n" + result)
            
            # Ask if user wants to continue
            again = input("\nTry another pair? (y/n): ").lower().strip()
            if again != 'y':
                break
                
        except KeyboardInterrupt:
            print("\nExiting program...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    print("Welcome to the Six Degrees of Separation Finder!")
    print("=" * 45)
    main()
    print("\nThank you for using the program!")