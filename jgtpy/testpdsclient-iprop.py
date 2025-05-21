import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jgtpy import pdsclient
from jgtpy import jgt2312

# Use the ProxyClient

# Default value
pds_server_url_default = "http://localhost:5000"

var_name_to_read = "pds_server_url"

pds_server_url = jgt2312.read_value_from_config(
    var_name_to_read, pds_server_url_default
)

client = pdsclient.JGTPDSProxyClient(pds_server_url)

#print(client.getPH("AUD/USD", "H1"))

def get_instrument_properties(instrument):
    # Call the cli method
    response = client.fetch_get_instrument_properties(instrument=instrument)
    # Print the response
    print("--------Get iprop----" + instrument + '  ' +  str(response['properties']) )

instrument = 'EUR/USD'
get_instrument_properties(instrument)


instrument = 'AUD/USD'
get_instrument_properties(instrument)


instrument = 'XAU/USD'
get_instrument_properties(instrument)


instrument = 'SPX500'
get_instrument_properties(instrument)


instrument = 'USD/JPY'
get_instrument_properties(instrument)



