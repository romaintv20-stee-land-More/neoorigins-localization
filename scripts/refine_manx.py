#!/usr/bin/env python3
"""Entry point for Manx refinement with source-normalization guards."""
import bootstrap_manx as base

# Empty/whitespace-only localization values carry no semantic text to translate.
# Preserve them exactly and keep them away from external translation endpoints.
base.MANUAL_VALUES.setdefault("", "")

import refine_manx_core

if __name__ == "__main__":
    refine_manx_core.main()
