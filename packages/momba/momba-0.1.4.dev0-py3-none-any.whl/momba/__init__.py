# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020, Maximilian Köhl <mkoehl@cs.uni-saarland.de>

"""
Momba is a Python library for *quantitative models*.

It's core modeling formalism are *stochastic hybrid automata* (SHA).
"""

from __future__ import annotations

from . import ext, model

from .metadata import version

__version__ = version


__all__ = ["ext", "model"]
