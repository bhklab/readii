"""Module to perform analysis on READII outputs."""
from .correlation import (
    getCrossCorrelations,
    getFeatureCorrelations,
    getSelfCorrelations,
    getSelfAndCrossCorrelations
)
from .plot_correlation import plotCorrelationHeatmap, plotCorrelationHistogram

__all__ = [
    'getFeatureCorrelations',
    'getSelfCorrelations',
    'getCrossCorrelations',
    'getSelfAndCrossCorrelations',
    'plotCorrelationHeatmap',
    'plotCorrelationHistogram'
]