from graph import *

# Constants
R = 1

# Initialize network topology
node_s = Node("S")
node_t = Node("T")
node_u = Node("U")
node_w = Node("W")
node_x = Node("X")
node_y = Node("Y")
node_z = Node("Z")

create_link(node_s, node_t, R)
create_link(node_s, node_u, R)
create_link(node_t, node_w, R)
create_link(node_t, node_y, R)
create_link(node_u, node_w, R)
create_link(node_u, node_z, R)
create_link(node_x, node_y, R)
create_link(node_x, node_z, R)
create_link(node_w, node_x, R)

# Simulute Multicast Throughput without Network Coding on above topology
def simulate(src, dst_list, num_packets):
    """ 
    Modifies the network connected to the specified source node, then
    outputs the maximum achievable throughput.
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
    Output:
        (float) Maximum achievable throughput
    """
    bit = 1
    for node in src.outgoing_links:
        src.outgoing_links

# Simulute Multicast Throughput with Network Coding on above topology
def simulate_NC(src, dst_list):
    """ 
    Modifies the network connected to the specified source node, then
    outputs the maximum achievable throughput.
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
    Output:
        (float) Maximum achievable throughput
    """
    pass
