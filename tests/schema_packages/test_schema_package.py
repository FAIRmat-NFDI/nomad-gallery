import os.path
from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # Check that the data matches what we put in the yaml file
    assert entry_archive.data.name == 'Test Gallery Entry'
    assert entry_archive.data.research_field == 'Battery Science'
    assert entry_archive.data.institution == 'Test Institute'