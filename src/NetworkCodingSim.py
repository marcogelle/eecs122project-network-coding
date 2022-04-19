from http.client import NETWORK_AUTHENTICATION_REQUIRED
from platform import node
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

    mem_used = 0
    queue = deque([src])
    while queue:
        node = queue.popleft()
        # prepare to randomly choose bits (most constrained option)
        if node == src:
            available_bits = [1, 2]
        else:
            available_bits = list({l.bit for l in node.incoming_links})
            mem_used += max(1, min(len(available_bits), len(list({l.bit for l in node.outgoing_links}))))
        random.shuffle(available_bits)

        for link in node.outgoing_links:
            # refill available_bits if we assigned everything already
            if not available_bits:
                if node == src:
                    available_bits = [1, 2]
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

    mem_used = 0
    queue = deque([src])
    while queue:
        node = queue.popleft()

        # prepare to randomly choose bits (most constrained option)
        if node == src:
            available_bits = [1, 2, 1^2][:len(src.outgoing_links)]
            for link in node.outgoing_links:
                # refill available_bits if we assigned everything already
                if not available_bits:
                    available_bits = [1, 2, 1^2][:len(src.outgoing_links)]
                    random.shuffle(available_bits)
                link.bit = available_bits.pop()
                        
                queue.append(link.to_node)
        else:
            num_unique_incoming = len({l.bit for l in node.incoming_links})
            mem_used += len(available_bits)
            available_bits = [1, 2, 1^2]

            for link in node.outgoing_links:
                # case when we need to implement network coding    
                if num_unique_incoming > 1:
                    if not available_bits:
                        available_bits = [1, 2, 1^2]
                        random.shuffle(available_bits)
                    link.bit = available_bits.pop()
                # assign a bit to the outgoing link
                else:
                    link.bit = node.incoming_links[0]
                    
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
    if len(src.outgoing_links) not in {2, 3} or num_packets != 2: 
        print("Number of packets/outgoing source links not supported currently :(")
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
    if len(src.outgoing_links) not in {2, 3} or num_packets != 2: 
        print("Number of packets/outgoing source links not supported currently :(")
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
        node_throughput = min(len(received_bits), num_packets)
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

def simulate_max(src, dst_list, num_packets, trials):
    network_throughput = float('-inf')
    for _ in range(trials):
        network_throughput = max(network_throughput, simulate(src, dst_list, num_packets))
    return network_throughput

def simulate_NC_max(src, dst_list, num_packets, trials):
    network_throughput = float('-inf')
    for _ in range(trials):
        network_throughput = max(network_throughput, simulate_NC(src, dst_list, num_packets))
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

def fig_crown():
    """
    Creates the one-source, three-sink network from Ahlswede paper.
    """
    node_s = Node("S")
    node_1 = Node("1")
    node_2 = Node("2")
    node_3 = Node("3")
    node_t1 = Node("T1")
    node_t2 = Node("T2")
    node_t3 = Node("T3")

    create_link(node_s, node_1, R)
    create_link(node_s, node_2, R)
    create_link(node_s, node_3, R)

    create_link(node_1, node_t1, R)
    create_link(node_1, node_t2, R)

    create_link(node_2, node_t1, R)
    create_link(node_2, node_t3, R)

    create_link(node_3, node_t2, R)
    create_link(node_3, node_t3, R)

    num_packets = 2
    return node_s, [node_t1, node_t2, node_t3], num_packets

def fig_crown_custom():
    """
    Creates a one-source, three-sink network that is taller than the one from the Ahlswede paper. 
    This is a custom topology
    """
    # Source
    node_s = Node("S")

    # Layer 1
    node_l1_1 = Node("L1_1")
    node_l1_2 = Node("L1_2")

    # Layer 2
    node_l2_1 = Node("L2_1")

    # Layer 3
    node_l3_1 = Node("L3_1")
    node_l3_2 = Node("L3_2")

    # Destination nodes
    node_t1 = Node("T1")
    node_t2 = Node("T2")
    node_t3 = Node("T3")

    create_link(node_s, node_l1_1, R)
    create_link(node_s, node_l1_2, R)
    
    create_link(node_l1_1, node_t1, R)
    create_link(node_l1_1, node_l2_1, R)
    create_link(node_l1_2, node_l2_1, R)
    create_link(node_l1_2, node_t3, R)

    create_link(node_l2_1, node_l3_1, R)
    create_link(node_l2_1, node_l3_2, R)

    create_link(node_l3_1, node_t1, R)
    create_link(node_l3_1, node_t2, R)
    create_link(node_l3_2, node_t2, R)
    create_link(node_l3_2, node_t3, R)

    num_packets = 2
    return node_s, [node_t1, node_t2, node_t3], num_packets


#####################
#### Main Method ####
#####################
    
# Taller crown than main_crown; custom example
def main():
    # source, dst_list, num_packets = fig_5_15()
    # source, dst_list, num_packets = fig_5_15_no_X()
    # source, dst_list, num_packets = fig_crown()
    source, dst_list, num_packets = fig_crown_custom()
    trials = 500

    # Simulate withOUT network coding
    net_throughput = simulate_max(source, dst_list, num_packets, trials)
    print("===== Without Network Coding =====")
    print("Average network throughput using", trials, "trials =", net_throughput)
    source.print_network()
    print()

    # Simulate with network coding
    nc_net_throughput = simulate_NC_max(source, dst_list, num_packets, trials)
    print("===== With Network Coding =====")
    print("Network Throughput =", nc_net_throughput)
    source.print_network() 

if __name__ == '__main__':
    main()