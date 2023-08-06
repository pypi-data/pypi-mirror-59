import unittest
from test.asserting.policy import PolicyAssertion, get_fixture_path

from vint.linting.level import Level
from vint.linting.policy.prohibit_implicit_scope_variable import ProhibitImplicitScopeVariable

PATH_VALID_VIM_SCRIPT = get_fixture_path('prohibit_implicit_scope_variable_valid.vim')
PATH_INVALID_VIM_SCRIPT = get_fixture_path('prohibit_implicit_scope_variable_invalid.vim')


class TestProhibitImplicitScopeVariable(PolicyAssertion, unittest.TestCase):
    def test_get_violation_if_found_when_file_is_valid(self):
        self.assertFoundNoViolations(PATH_VALID_VIM_SCRIPT,
                                     ProhibitImplicitScopeVariable)


    def create_violation(self, line, column):
        return {
            'name': 'ProhibitImplicitScopeVariable',
            'level': Level.STYLE_PROBLEM,
            'position': {
                'line': line,
                'column': column,
                'path': PATH_INVALID_VIM_SCRIPT
            }
        }


    def test_get_violation_if_found_when_file_is_invalid(self):
        expected_violations = [
            self.create_violation(2, 5),
            self.create_violation(4, 10),
            self.create_violation(9, 10),
            self.create_violation(13, 5),
            self.create_violation(16, 11),
        ]

        self.assertFoundViolationsEqual(PATH_INVALID_VIM_SCRIPT,
                                        ProhibitImplicitScopeVariable,
                                        expected_violations)


if __name__ == '__main__':
    unittest.main()
