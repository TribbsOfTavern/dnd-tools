'''
    Dicts to be used in test_models
'''

# Table is valid
table_a = {
    'table-name': 'Test Table A',
    'group': 'examples',
    'roll': 'length',
    'results': {
        1: "Example 1: single inline rolls -> [1d4]",
        2: "Example 2: single inline link -> [1@Test Table B]",
        3: "Example 3: multiple inline rolls -> [1d4] [2d6]",
        4: "Example 4: multiple inline links -> [1@Test Table B] [1@Test Table C]",
        5: "Example 5: mix of inline roll and link -> [1d6] [1@Test Table B]",
        6: "Example 6: inline link with embedded inline roll -> [2d4@Test Table B]",
        7: "Example 7: there is no link in this example"
    }
}

# Table is missing 'roll'
table_b = {
    'table-name': 'Test Table B',
    'group': 'examples',
    'results': {
        1: "Example 1: single inline rolls -> [1d4]",
        2: "Example 2: single inline link -> [1@Test Table B]",
        3: "Example 3: multiple inline rolls -> [1d4] [2d6]",
        4: "Example 4: multiple inline links -> [1@Test Table B] [1@Test Table C]",
        5: "Example 5: mix of inline roll and link -> [1d6] [1@Test Table B]",
        6: "Example 6: inline link with embedded inline roll -> [2d4@Test Table B]",
        7: "Example 7: there is no link in this example",
        8: "Example 8: inline roll with invalid roll notation -> [1f4]"
    }
}

# Table has an invalid roll
table_c = {
    'table-name': 'Test Table',
    'group': 'examples',
    'roll': '1f8',
    'results': {
        1: "Example 1: single inline rolls -> [1d4]",
        2: "Example 2: single inline link -> [1@Test Table B]",
        3: "Example 3: multiple inline rolls -> [1d4] [2d6]",
        4: "Example 4: multiple inline links -> [1@Test Table B] [1@Test Table C]",
        5: "Example 5: mix of inline roll and link -> [1d6] [1@Test Table B]",
        6: "Example 6: inline link with embedded inline roll -> [2d4@Test Table B]",
        7: "Example 7: there is no link in this example",
        8: "Example 8: inline roll with invalid roll notation -> [1f4]"
    }
}

# Table is missing table-name
table_d = {
    'group': 'examples',
    'roll': 'length',
    'results': {
        1: "Example 1: single inline rolls -> [1d4]",
        2: "Example 2: single inline link -> [1@Test Table B]",
        3: "Example 3: multiple inline rolls -> [1d4] [2d6]",
        4: "Example 4: multiple inline links -> [1@Test Table B] [1@Test Table C]",
        5: "Example 5: mix of inline roll and link -> [1d6] [1@Test Table B]",
        6: "Example 6: inline link with embedded inline roll -> [2d4@Test Table B]",
        7: "Example 7: there is no link in this example",
        8: "Example 8: inline roll with invalid roll notation -> [1f4]"
    }
}

# Table has an invalid table-name
table_e = {
    'table-name': None,
    'group': 'examples',
    'roll': 'length',
    'results': {
        1: "Example 1: single inline rolls -> [1d4]",
        2: "Example 2: single inline link -> [1@Test Table B]",
        3: "Example 3: multiple inline rolls -> [1d4] [2d6]",
        4: "Example 4: multiple inline links -> [1@Test Table B] [1@Test Table C]",
        5: "Example 5: mix of inline roll and link -> [1d6] [1@Test Table B]",
        6: "Example 6: inline link with embedded inline roll -> [2d4@Test Table B]",
        7: "Example 7: there is no link in this example",
        8: "Example 8: inline roll with invalid roll notation -> [1f4]"
    }
}