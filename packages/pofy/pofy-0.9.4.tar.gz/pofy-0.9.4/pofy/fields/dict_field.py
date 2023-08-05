"""Dictionary field class & utilities."""
from gettext import gettext as _
from typing import Any

from yaml import ScalarNode

from pofy.common import LOADING_FAILED
from pofy.fields.base_field import BaseField
from pofy.interfaces import ILoadingContext


class DictField(BaseField):
    """Dictionary YAML object field."""

    def __init__(self, item_field: BaseField, *args, **kwargs):
        """Initialize dict field.

        Args:
            item_field: Field used to load dictionnary values.
            *args, **kwargs : Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        assert isinstance(item_field, BaseField), \
            _('item_field must be an implementation of BaseField.')
        self._item_field = item_field

    def _load(self, context: ILoadingContext) -> Any:
        node = context.current_node()
        if not context.expect_mapping():
            return LOADING_FAILED

        result = {}
        for key_node, value_node in node.value:
            assert isinstance(key_node, ScalarNode)
            key = key_node.value

            item = context.load(self._item_field, value_node)
            if item is LOADING_FAILED:
                continue

            result[key] = item

        return result
