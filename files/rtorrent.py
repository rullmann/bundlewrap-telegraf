#!/usr/bin/python3

import xmlrpc.client
import json

rtorrent = xmlrpc.client.ServerProxy('${node.metadata['telegraf']['rtorrent']['url']}')

data = {}
for datapoint in ['get_memory_usage', 'get_max_memory_usage', 'get_upload_rate', 'get_up_rate', 'get_download_rate', 'get_down_rate', 'get_up_total', 'get_down_total']:
    function = getattr(rtorrent, datapoint)
    data[datapoint] = function()

json_data = json.dumps(data)
print(json_data)
