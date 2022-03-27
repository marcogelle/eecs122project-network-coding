class Node:

    # incoming_links contains tuples; (destination, bit_amount (b1 or b2), link rate)
    # outgoing_links contains tuples; (source, bit_amount (b1 or b2), link rate)

    def __init__(self, id):
        self.id = id
        self.incoming_links = []
        self.outgoing_links = []

def create_link(src, dst, rate):
        """ Creates a link from src to dst, with a link rate.
        Inputs:
            src, dst: source and destination nodes
            rate: link rate
        Outputs: None
        """
        src.outgoing_links.append((dst, 0, rate))
        dst.incoming_links.append((src, 0, rate))

def update_incoming_link(src, dst):
   for link in dst.incoming_links:
    if src.id == link.id:
       link = (src, 1, )
# class Network:
#     def __init__(self, source_id):
#         self.source = Node(source_id)

    
