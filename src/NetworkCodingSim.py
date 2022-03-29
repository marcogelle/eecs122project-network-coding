from graph import *
import random
from collections import deque

# Constants
R = 1

# Helper function to determine bits on links in the non-network coding case
def populate_bits(src, num_packets):
    """
    Fills in the bit values on each link in a multicasted, non-network coded network.
    Inputs:
        src (node): starting node of network
    """
    # FIXME?: currently assumes the graph is directed and acyclic. Probably safe to assume this though.
    # Traverse the network with BFS
    queue = deque([src])
    while queue:
        node = queue.popleft()

        # prepare to randomly choose bits (most constrained option)
        if node == src:
            available_bits = list(range(1, num_packets + 1))
        else:
            available_bits = list({l.bit for l in node.incoming_links})
        random.shuffle(available_bits)

        for link in node.outgoing_links:
            # refill available_bits if we assigned everything already
            if not available_bits:
                if node == src:
                    available_bits = list(range(1, num_packets + 1))
                else:
                    available_bits = list({l.bit for l in node.incoming_links})
                random.shuffle(available_bits)

            # assign a bit to the outgoing link
            link.bit = available_bits.pop()

            queue.append(link.to_node)

# Helper function to determine bits on links in the network coding case
def populate_bits_NC(src, num_packets):
    # FIXME?: currently assumes the graph is directed and acyclic. Probably safe to assume this though.
    # Traverse the network with BFS
    queue = deque([src])
    while queue:
        node = queue.popleft()

        # prepare to randomly choose bits (most constrained option)
        if node == src:
            available_bits = list(range(1, num_packets + 1))
            random.shuffle(available_bits)
        else:
            available_bits = list({l.bit for l in node.incoming_links})

        for link in node.outgoing_links:
            if node == src:
                # refill available_bits if we assigned everything already
                if not available_bits:
                    available_bits = list(range(1, num_packets + 1))
                    random.shuffle(available_bits)
                link.bit = available_bits.pop()
            else:
                # case when we need to implement network coding    
                if len(available_bits) > 1:
                    link.bit = 3
                # assign a bit to the outgoing link
                else:
                    link.bit = available_bits[0]
                    
            queue.append(link.to_node)

##########################################
#### Throughput Calculation Functions ####
##########################################

def simulate(src, dst_list, num_packets):
    """ 
    Modifies the network connected to the specified source node, then
    outputs the network throughput, which depends on how we probabilistically
    assign bits to links. Does not use network coding.
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
        num_packets (int): number of distinct packets/bits
    Output:
        (float) Network throughput
    """
    if num_packets != len(src.outgoing_links) or num_packets != 2:
        print("Not supported currently :(")
        return   

    populate_bits(src, num_packets)

    # Taking the average node throughput for network throughput.
    # Assumes a symmetric network.
    network_throughput = 0
    for dst_node in dst_list:
        received_bits = set()
        for in_link in dst_node.incoming_links:
            received_bits.add(in_link.bit)
        node_throughput = len(received_bits)
        network_throughput += node_throughput
    network_throughput /= len(dst_list)

    return network_throughput

def simulate_NC(src, dst_list, num_packets):
    """ 
    Modifies the network connected to the specified source node, then
    outputs the maximum achievable throughput using network coding.
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
    Output:
        (float) Maximum achievable network throughput
    """
    if num_packets != len(src.outgoing_links) or num_packets != 2:
        print("Not supported currently :(")
        return   

    populate_bits_NC(src, num_packets)

    # Taking the average node throughput for network throughput.
    # Assumes a symmetric network.
    # TODO: decode the xor'd bits
    network_throughput = 0
    for dst_node in dst_list:
        received_bits = set()
        for in_link in dst_node.incoming_links:
            received_bits.add(in_link.bit)
        node_throughput = max(len(received_bits), num_packets)
        network_throughput += node_throughput
    network_throughput /= len(dst_list)

    return network_throughput

def simulate_average(src, dst_list, num_packets, trials):
    """
    Runs simulate(...) `trials` number of times, then returns the average throughput
    for this network (without network coding).
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
        num_packets (int): number of distinct packets/bits
        trials (int): number of times to simulate
    Output:
        (float) Average network throughput
    """
    network_throughput = 0
    for _ in range(trials):
        network_throughput += simulate(src, dst_list, num_packets)
    network_throughput /= trials
    return network_throughput

###############################
#### Hard-coded Topologies ####
###############################

def fig_5_15():
    """
    Creates network topology according to textbook figure 5.15. Initializes all link
    bit values to 0.

    Outputs: (src, dst_list, num_packets)
        src (node): source node of network
        dst_list (List[node]): list of destination nodes to be multicasted to
        num_packets (int): number of bits/packets to be multicasted
    """
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

    num_packets = 2
    return node_s, [node_y, node_z], num_packets

def fig_5_15_no_X():
    """
    Creates the textbook example, but with no X node.
    """
    node_s = Node("S")
    node_t = Node("T")
    node_u = Node("U")
    node_w = Node("W")
    node_y = Node("Y")
    node_z = Node("Z")

    create_link(node_s, node_t, R)
    create_link(node_s, node_u, R)
    create_link(node_t, node_w, R)
    create_link(node_t, node_y, R)
    create_link(node_u, node_w, R)
    create_link(node_u, node_z, R)
    create_link(node_w, node_y, R)
    create_link(node_w, node_z, R)

    num_packets = 2
    return node_s, [node_y, node_z], num_packets

#####################
#### Main Method ####
#####################

if __name__ == '__main__':
    # Initialize network topology
    source, dst_list, num_packets = fig_5_15_no_X()

    # Simulate without network coding
    trials = 500
    net_throughput = simulate_average(source, dst_list, num_packets, trials)
    print("===== Without Network Coding =====")
    print("Average network throughput using", trials, "trials =", net_throughput)
    source.print_network()
    print()

    # # Reset network topology
    # source, dst_list, num_packets = fig_5_15()

    # Simulate with network coding
    nc_net_throughput = simulate_NC(source, dst_list, num_packets)
    print("===== With Network Coding =====")
    print("Network Throughput =", nc_net_throughput)
    source.print_network()