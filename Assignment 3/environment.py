from bayes_network import create_bayes_network
import names

if __name__ == '__main__':
    network = create_bayes_network(names.input_file)
    print(network)
