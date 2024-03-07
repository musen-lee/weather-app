#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses
from typing import Dict, Any, Type
from dataclasses import asdict, is_dataclass
from .convert import to_camel_case


class DictMixin:
    @classmethod
    def from_dict(cls: Type, data: Dict[str, Any]) -> Any:
        """
        Create dataclass object from a dictionary, only match the exist keys
        """
        if not is_dataclass(cls):
            raise ValueError(f"{cls.__name__} is not a dataclass")
        field_names = {field.name for field in dataclasses.fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in field_names}
        return cls(**kwargs)

    def to_dict(self, camel_case: bool = True) -> Dict[str, Any]:
        data = asdict(self)
        if camel_case and is_dataclass(type(self)):
            data = {
                to_camel_case(k): self._convert_value(v, camel_case)
                for k, v in data.items()
            }
        return data

    def _convert_value(self, value: Any, camel_case: bool) -> Any:
        if is_dataclass(type(value)):
            return value.to_dict(camel_case=camel_case)
        elif isinstance(value, (list, tuple)):
            return [self._convert_value(item, camel_case) for item in value]
        elif isinstance(value, dict):
            return {
                to_camel_case(k): self._convert_value(v, camel_case)
                for k, v in value.items()
            }
        else:
            return value
