import pytest
import yaml
import json

from json.decoder import JSONDecodeError

from jsonrouter import JsonMatchEngine


with open('examples/rules/minimal.rule.yaml') as f:
  rules_minimal = yaml.load(f)

with open('examples/data/singleton.record.json') as f:
  records_single = json.load(f)

with open('examples/data/iterable.json') as f:
  records_iterable = json.load(f)

def print_router(record):
  print(record) 

registered_routers = { 'minimal-router': print_router }


def test_singleton(capsys):
  eng = JsonMatchEngine(rules_minimal, registered_routers)
  matches = eng.route_matches(records_single)
  print(json.dumps(matches, indent=4))

  assert isinstance(matches, list)
  assert len(matches) == 1
  

def test_iterable(capsys):
  eng = JsonMatchEngine(rules_minimal, registered_routers)
  matches = eng.route_matches(records_iterable)
  print(json.dumps(matches, indent=4))

  assert isinstance(matches, list)
  assert len(matches) == 2


goog_json_string = '''{
  "one": 1,
  "two": 2,
  "three": 3
}
'''
def test_json_decode(capsys):
  eng = JsonMatchEngine(rules_minimal, registered_routers)
  matches = eng.route_matches(goog_json_string)


bad_json_string = '''{
  "one": 1,
  "no": "comma"
  "three": 3
}
'''
def test_JSONDecodeError(capsys):
  with pytest.raises(JSONDecodeError):
    eng = JsonMatchEngine(rules_minimal, registered_routers)
    matches = eng.route_matches(bad_json_string)
