from graph import *

# Constants
R = 1

# Helper function to determine bits on links in the non-network coding case
def populate_bits(src):
    """
    Fills in the bit values on each link in a multicasted, non-network coded network.
    Inputs:
        src (node): starting node of network
    """
    def fill_same_bits(node, bit):
        for link in node.outgoing_links:
            if link.bit == 0:
                link.bit = bit
                fill_same_bits(link.to_node, bit)

    bit_num = 1
    for link in src.outgoing_links:
        if link.bit == 0:
            link.bit = bit_num
            fill_same_bits(link.to_node, bit_num)
        bit_num += 1    

# Simulute Multicast Throughput without Network Coding on above topology
def simulate(src, dst_list, num_packets):
    """ 
    Modifies the network connected to the specified source node, then
    outputs the maximum achievable throughput.
    Inputs:
        src (node): source node
        dst_list (List[node]): list of destination nodes to be multicasted to
    Output:
        (float) Maximum achievable network throughput
    """
    if num_packets != len(src.outgoing_links):
        print("Not supported currently :(")
        return   

    populate_bits(src)

    # FIXME due to being sus: network throughput is average of dest node throughputs
    network_throughput = 0
    for dst_node in dst_list:
        received_bits = set()
        for in_link in dst_node.incoming_links:
            received_bits.add(in_link.bit)
        node_throughput = len(received_bits)
        network_throughput += node_throughput
    network_throughput /= len(dst_list)

    return network_throughput

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

if __name__ == '__main__':
    # Initialize network topology
    source, dst_list, num_packets = fig_5_15()

    # Simulate without network coding
    net_throughput = simulate(source, dst_list, num_packets)
    print("===== Without Network Coding =====")
    print("Network throughput =", net_throughput)
    source.print_network()
    print()
    print("===== With Network Coding =====")
    print('not implemented')