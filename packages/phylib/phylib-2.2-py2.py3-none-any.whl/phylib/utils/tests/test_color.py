# -*- coding: utf-8 -*-

"""Test colors."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import colorcet as cc
import numpy as np
from numpy.testing import assert_almost_equal as ae

from phylib.utils import Bunch
from ..color import (
    _is_bright, _random_bright_color, spike_colors, add_alpha, selected_cluster_color,
    _override_hsv,
    _hex_to_triplet, _continuous_colormap, _categorical_colormap, ClusterColorSelector,
    colormaps, _add_selected_clusters_colors)


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_random_color():
    for _ in range(20):
        assert _is_bright(_random_bright_color())


def test_hex_to_triplet():
    assert _hex_to_triplet('#0123ab')


def test_add_alpha():
    assert add_alpha((0, .5, 1), .75) == (0, .5, 1, .75)
    assert add_alpha(np.random.rand(5, 3), .5).shape == (5, 4)

    assert add_alpha((0, .5, 1, .1), .75) == (0, .5, 1, .75)
    assert add_alpha(np.random.rand(5, 4), .5).shape == (5, 4)


def test_override_hsv():
    assert _override_hsv((.1, .9, .5), h=1, s=0, v=1) == (1, 1, 1)


def test_selected_cluster_color():
    c = selected_cluster_color(0)
    assert isinstance(c, tuple)
    assert len(c) == 4


def test_colormaps():
    colormap = np.array(cc.glasbey_bw_minc_20_minl_30)
    values = np.random.randint(10, 20, size=100)
    colors = _categorical_colormap(colormap, values)
    assert colors.shape == (100, 3)

    colormap = np.array(cc.rainbow_bgyr_35_85_c73)
    values = np.linspace(0, 1, 100)
    colors = _continuous_colormap(colormap, values)
    assert colors.shape == (100, 3)


def test_spike_colors():
    spike_clusters = [1, 0, 0, 3]
    cluster_ids = [0, 1, 2, 3]
    colors = spike_colors(spike_clusters, cluster_ids)
    assert colors.shape == (4, 4)
    ae(colors[1], colors[2])


def test_cluster_color_selector():
    # Mock ClusterMeta instance, with 'fields' property and get(field, cluster) function.
    cluster_meta = Bunch(fields=('label',), get=lambda f, cl: {1: 10, 2: 20, 3: 30}[cl])
    cluster_metrics = {'quality': lambda c: c * .1}
    cluster_ids = [1, 2, 3]
    c = ClusterColorSelector(
        cluster_meta=cluster_meta,
        cluster_metrics=cluster_metrics,
        cluster_ids=cluster_ids,
    )

    assert len(c.get(1, alpha=.5)) == 4
    ae(c.get_values([None, 0]), np.arange(2))

    for color_field, colormap in (
            ('label', 'linear'),
            ('quality', 'rainbow'),
            ('cluster', 'categorical'),
            ('nonexisting', 'diverging')):
        c.set_color_mapping(color_field=color_field, colormap=colormap)
        colors = c.get_colors(cluster_ids)
        assert colors.shape == (3, 4)

    # Get the state.
    assert c.state == {
        'color_field': 'nonexisting', 'colormap': 'diverging',
        'categorical': True, 'logarithmic': False}

    # Set the state.
    state = Bunch(c.state)
    state.color_field = 'label'
    state.colormap = colormaps.rainbow
    state.categorical = False
    c.set_state(state)

    # Check that the state was correctly set.
    assert c._color_field == 'label'
    ae(c._colormap, colormaps.rainbow)
    assert c._categorical is False


def test_cluster_color_group():
    # Mock ClusterMeta instance, with 'fields' property and get(field, cluster) function.
    cluster_meta = Bunch(fields=('group',), get=lambda f, cl: {1: None, 2: 'mua', 3: 'good'}[cl])
    cluster_ids = [1, 2, 3]
    c = ClusterColorSelector(
        cluster_meta=cluster_meta,
        cluster_ids=cluster_ids,
    )

    c.set_color_mapping(color_field='group', colormap='cluster_group')
    colors = c.get_colors(cluster_ids)
    assert colors.shape == (3, 4)


def test_cluster_color_log():
    cluster_ids = [1, 2, 3]
    c = ClusterColorSelector(
        cluster_ids=cluster_ids,
    )

    c.set_color_mapping(logarithmic=True)
    colors = c.get_colors(cluster_ids)
    assert colors.shape == (3, 4)


def test_add_selected_clusters_colors():
    cluster_colors = np.tile(np.c_[np.arange(3)], (1, 3))
    cluster_colors = add_alpha(cluster_colors)
    cluster_colors_sel = _add_selected_clusters_colors([1], [0, 1, 3], cluster_colors)
    ae(cluster_colors_sel[[0]], add_alpha(np.zeros((1, 3))))
    ae(cluster_colors_sel[[2]], add_alpha(2 * np.ones((1, 3))))
    # Cluster at index 0 is selected, should be in blue.
    r, g, b, _ = cluster_colors_sel[1]
    assert b > g > r
