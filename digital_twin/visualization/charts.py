"""Plotly/Matplotlib chart generation."""

import matplotlib.pyplot as plt
import numpy as np


def create_bar_chart(data: dict, title: str = "Chart") -> plt.Figure:
    """Create bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data.keys(), data.values())
    ax.set_title(title)
    return fig


def create_line_chart(x: np.ndarray, y: np.ndarray, title: str = "Chart") -> plt.Figure:
    """Create line chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y)
    ax.set_title(title)
    return fig


__all__ = ["create_bar_chart", "create_line_chart"]
