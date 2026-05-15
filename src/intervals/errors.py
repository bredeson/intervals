
_BAD_METHOD_NAMESPACE =(
    "mismatched namespaces for method {0:s}: "
    "'{1.namespace}' and '{2.namespace}'"
).format

_BAD_OPERAND_NAMESPACE = (
    "mismatched namespaces for operand {0:s}: "
    "'{1.namespace}' and '{2.namespace}'"
).format

_BAD_OPERAND_TYPE = (
    "unsupported type(s) for operand {0:s}: "
    "'{1.__class__.__name__}' and '{2.__class__.__name__}'"
).format

_ILL_DEFINED = (
    "Result is ill-defined, use {0}() instead"
).format

_NO_METHOD = (
    '{0.__class__.__name__}.{1}()'
).format

_NOT_IN = (
    "'{1}' is not in {0.__class__.__name__}"
).format
