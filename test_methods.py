# just a misc. file to test individual functions for bugs

import json

from fetch_api_test import get_puuid
from fetch_api_test import get_matches
from fetch_api_test import get_match_info
from lookup import id_to_name

peter = 'meth%20damon'

# test
print(get_puuid(peter))
# '-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'

#test
print(get_matches('-oXMqiG7Iz4jfAcbhR09AeP44KvBCtL9cEejVh-adG5LlQ0PEQFLJSwJV0Xk7upjLNKm5l3fygLhWA'))
# ['NA1_4226412134', 'NA1_4226345907', 'NA1_4218138569', 'NA1_4218105594', 'NA1_4211723295', 'NA1_4211687221', 'NA1_4211653877', 'NA1_4209587154', 'NA1_4209487127', 'NA1_4209475699', 'NA1_4208089388', 'NA1_4208092029', 'NA1_4207995324', 'NA1_4200313716', 'NA1_4200273950', 'NA1_4200232990', 'NA1_4200174394', 'NA1_4199167723', 'NA1_4199144987', 'NA1_4199171572']

# peter's match info
print(get_match_info('NA1_4226412134'))

data = []
data.extend(get_match_info('NA1_4226412134'))
data.extend(get_match_info('NA1_4226345907'))

with open('test_data.json', 'w') as s:
		s.write(json.dumps(data, indent = 4))

print(id_to_name('23'))