from bayes_network import create_bayes_network
from bayes_network import enumeration_ask
import names

if __name__ == '__main__':
    network = create_bayes_network(names.input_file)
    print(network)
    print(network.str_graph_structure())
    x_query = input("Enter query separated by whitespace").split()
    evidence = set()
    print(enumeration_ask(x_query, evidence, network))
