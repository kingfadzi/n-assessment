import lxml.etree as ET
from collections import Counter

file_path = 'data.xml'

tree = ET.parse(file_path)

envs = tree.xpath("//region/@env")

env_count = Counter(envs)

print(env_count)
