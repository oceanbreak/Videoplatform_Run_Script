from lib.UI.Settings import Settings
import xml.etree.ElementTree as ET
from lib.data.DataStructure import data_keywords

tree = ET.parse('resources/settings.xml')
root = tree.getroot()
print(root.tag)

# for group in root:
#     for channel in group:
#         print(channel.attrib)
#         for item in channel:
#             print(item.tag, item.text)


for chan in root.iter('channel'):
    if chan.attrib['id'] == 'TEMP':
        for item in chan:
            print(item.text)

        chan[0].text = str(1)
        chan[2].text = 'COM10'
        # print(chan.items)


for l in root.iter('common'):
    print(l[0].tag, l[0].text)


for l in root.iter('IP_camera'):
    for a in l:
        print(a.tag, a.text)
# a = root.findall('IP_camera')
# for item in a:
#     print(item.attrib, item.text)
# # print(a[0].text)

