#!/usr/bin/env python

"""Extractor algorithm implementation file
"""

def calculate(pxarray):
    """Algorithm
    Args:
        pxarray(numpy array): RGB pixel data at the plot level
    Returns:
    """
    # Replace this following line with your algorithm
    return pxarray[:, :, 1].size  # Returning the size of a single color channel in pixels
