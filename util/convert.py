#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def to_camel_case(s: str) -> str:
    """Convert underscore naming to camel case naming"""
    if s and '_' in s:
        words = s.split('_')
        return words[0] + ''.join(word.capitalize() for word in words[1:]) 
    return s