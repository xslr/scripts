#!/usr/bin/env python

# Dump interesting parameters for selected processors from ark.intel.com
# and convert them to CSV for easier comparison

import csv
import time
from lxml import html
import requests

cpus = [
    'Intel Xeon E5603',
    'Intel Xeon E5606',
    'Intel Xeon E5607',
    'Intel Xeon E5620',
    'Intel Xeon E5630',
    'Intel Xeon E5640',
    'Intel Xeon E5645',
    'Intel Xeon E5649',
    'Intel Xeon L5609',
    'Intel Xeon L5618',
    'Intel Xeon L5630',
    'Intel Xeon L5638',
    'Intel Xeon L5639',
    'Intel Xeon L5640',
    'Intel Xeon X5647',
    'Intel Xeon X5650',
    'Intel Xeon X5660',
    'Intel Xeon X5667',
    'Intel Xeon X5670',
    'Intel Xeon X5672',
    'Intel Xeon X5675',
    'Intel Xeon X5677',
    'Intel Xeon X5679',
    'Intel Xeon X5680',
    'Intel Xeon X5687',
    'Intel Xeon X5690',
    'Intel Xeon E5502',
    'Intel Xeon E5503',
    'Intel Xeon E5504',
    'Intel Xeon E5506',
    'Intel Xeon L5506',
    'Intel Xeon E5507',
    'Intel Xeon L5508',
    'Intel Xeon L5518',
    'Intel Xeon E5520',
    'Intel Xeon L5520',
    'Intel Xeon E5530',
    'Intel Xeon L5530',
    'Intel Xeon E5540',
    'Intel Xeon X5550',
    'Intel Xeon X5560',
    'Intel Xeon X5570',
    'Intel Xeon W5580',
    'Intel Xeon W5590'
]


def get_cpu_tree(cpu_name):
    query_base = 'https://ark.intel.com/search?q=CPU_NAME_HERE'
    cpu_page_xpath = '//h4[@class=\'result-title\']/a/@href'
    
    query = query_base.replace('CPU_NAME_HERE', cpu_name.replace(' ', '+'))
    print 'query=' + query
    page = requests.get(query)
    tree = html.fromstring(page.content)
    
    url = tree.xpath(cpu_page_xpath)
    if not url:
        return None
    
    url = 'https://ark.intel.com' + url[0]
    print 'cpu_url=' + url
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree


def parse_cpu_tree(tree):
    fields = [
        'ProcessorNumber',
        'CodeNameText',
        'BornOnDate',
        'Lithography',
        'CoreCount',
        'ThreadCount',
        'ClockSpeed',
        'Cache',
        'BusNumPorts',
        'MaxTDP',
        'MemoryTypes',
        'NumMemoryChannels',
        'MaxMemoryBandwidth',
        'SocketsSupported',
        'MaxCPUs',
        'HyperThreading',
        'VTX',
        'VTD'
    ]
    xpath_base = '//li[@class=\'REPLACEME_FIELD_NAME\']/span[@class=\'value\']/*/text()'

    results = {}
    for field in fields:
        xpath = xpath_base.replace('REPLACEME_FIELD_NAME', field)
        #print 'xpath=' + xpath
        element = tree.xpath(xpath)
        if not element:
            results[field] = 'NOT_FOUND'
        else:
            results[field] = tree.xpath(xpath)[0]
            
    print results
    return results


def tocsv(cpu_info):
    keys = cpu_info[0].keys()
    with open('z800cpus.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(cpu_info)


def process_cpus(cpu_names):
    cpu_info = []
    for cpu_name in cpu_names:
        tree = get_cpu_tree(cpu_name)
        if tree is None:
            print 'CPU NOT FOUND ' + cpu_name
        else:
            cpu_info.append(parse_cpu_tree(tree))
            
        print
        time.sleep(2) # seconds

    tocsv(cpu_info)
    return cpu_info


if __name__ == '__main__':
    cpu_info = process_cpus(cpus)
