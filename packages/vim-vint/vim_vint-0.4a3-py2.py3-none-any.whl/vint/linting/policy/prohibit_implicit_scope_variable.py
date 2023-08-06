from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy_registry import register_policy
from vint.ast.plugin.scope_plugin import (
    ExplicityOfScopeVisibility,
    ScopeVisibility,
)


@register_policy
class ProhibitImplicitScopeVariable(AbstractPolicy):
    reference = 'Anti-pattern of vimrc (Scope of identifier)'
    level = Level.STYLE_PROBLEM


    def listen_node_types(self):
        return [NodeType.IDENTIFIER]


    def is_valid(self, identifier, lint_context):
        """ Whether the identifier has a scope prefix. """

        scope_plugin = lint_context['plugins']['scope']

        # NOTE: This policy interest only not builtin variables.
        scope_visibility = scope_plugin.get_objective_scope_visibility(identifier)
        if scope_visibility is ScopeVisibility.BUILTIN:
            return True

        explicity = scope_plugin.get_explicity_of_scope_visibility(identifier)

        is_valid = explicity is not ExplicityOfScopeVisibility.IMPLICIT

        if not is_valid:
            self._make_description(identifier, scope_plugin)

        return is_valid


    def _make_description(self, identifier, scope_plugin):
        self.description = 'Make the scope explicit like `{good_example}`'.format(
            good_example=scope_plugin.normalize_variable_name(identifier)
        )
