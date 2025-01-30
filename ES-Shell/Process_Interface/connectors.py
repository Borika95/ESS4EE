# Add "Helpers" to the path and import the necessary libraries
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'Helpers')))

import data_point_addresses as dp
from opcua import Client

# OPC UA connector
def read_opcua_values(server_url, node_ids):
    # Create a client
    client = Client(server_url)

    try:
        # Connect to the OPC UA server
        client.connect()

        # Create a list to store the read values
        values = []

        # Read values for each specified NodeID
        for node_id in node_ids:
            # Find the Node object by NodeID
            node = client.get_node(node_id)

            # Read the value attribute of the Node
            value = node.get_value()
            values.append((node_id, value))

        return values

    finally:
        # Disconnect from the OPC UA server
        client.disconnect()

# Runs as main if you want to test the connection to the server
if __name__ == "__main__":

    # Read OPC UA values
    result = read_opcua_values(dp.server_url, dp.node_ids)

    # Display the results
    for node_id, value in result:
        print(f"NodeID: {node_id}, Value: {value}")