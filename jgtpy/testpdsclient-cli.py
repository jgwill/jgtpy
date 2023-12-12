import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pdsclient
import jgt2312

# Use the ProxyClient

# Default value
pds_server_url_default = "http://localhost:5000"

var_name_to_read = "pds_server_url"

pds_server_url = jgt2312.read_value_from_config(
    var_name_to_read, pds_server_url_default
)

client = pdsclient.JGTPDSProxyClient(pds_server_url)

#print(client.getPH("AUD/USD", "H1"))

# Call the cli method
response = client.cli2(instrument='EUR/USD', timeframe='H6')
# Print the response
print(response)


response = client.cli(instrument='EUR/USD', timeframe='H3')
# Print the response
print(response)
