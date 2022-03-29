from collections import deque

class Node:
    def __init__(self, id):
        self.id = id

        # both of the following are lists of Link objects
        self.incoming_links = []
        self.outgoing_links = []
    
    def __repr__(self):
        return f"Node({self.id})"

    def print_network(self):
        """
        Prints the network, assuming this is the source node.
        Prints in order of breadth-first-search.
        """
        visited = set()
        visited.add(self)
        queue = deque([self])
        while queue:
            node = queue.popleft()
            print(node)
            for link in node.outgoing_links:
                print("\t", link)
                if link.to_node not in visited:
                    queue.append(link.to_node)
                    visited.add(link.to_node)

class Link:
    def __init__(self, from_node, to_node, rate):
        self.from_node = from_node
        self.to_node = to_node
        self.rate = rate

        # a bit value of 0 = unset value
        # actual bit/packet ids will be integers >= 1
        self.bit = 0
    
    def __repr__(self):
        return f"Link(from={self.from_node.id}, to={self.to_node.id}, rate={self.rate}, bit={self.bit})"

def create_link(src, dst, rate):
        """ Creates a link from src to dst, with a link rate.
        Inputs:
            src, dst: source and destination nodes
            rate: link rate
        Outputs: None
        """
        link = Link(src, dst, rate)
        src.outgoing_links.append(link)
        dst.incoming_links.append(link)


