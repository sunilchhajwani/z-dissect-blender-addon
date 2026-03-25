"""State management utilities for Z-Dissect."""
import bpy
import json
from .properties import DissectionState


def get_state(context):
    """Get dissection state from context."""
    return context.scene.dissect_state


def export_state_json(state):
    """Export dissection state to JSON dict."""
    data = {
        'version': (0, 1, 0),
        'current_system': state.current_system,
        'current_region': state.current_region,
        'current_layer': state.current_layer,
        'cut_count': state.cut_count,
        'cuts': [],
        'hidden': []
    }
    for cut in state.cut_history:
        data['cuts'].append({
            'object_name': cut.object_name,
            'cut_type': cut.cut_type,
            'timestamp': cut.timestamp,
            'description': cut.description
        })
    for hidden in state.hidden_layers:
        data['hidden'].append({
            'object_name': hidden.object_name,
            'hidden': hidden.hidden
        })
    return data


def import_state_json(state, data):
    """Import dissection state from JSON dict."""
    state.current_system = data.get('current_system', 'Muscular System')
    state.current_region = data.get('current_region', '')
    state.current_layer = data.get('current_layer', 0)
    state.cut_count = data.get('cut_count', 0)
    state.cut_history.clear()
    state.hidden_layers.clear()
    for cut_data in data.get('cuts', []):
        cut = state.cut_history.add()
        cut.object_name = cut_data['object_name']
        cut.cut_type = cut_data['cut_type']
        cut.timestamp = cut_data['timestamp']
        cut.description = cut_data['description']
    for hidden_data in data.get('hidden', []):
        hidden = state.hidden_layers.add()
        hidden.object_name = hidden_data['object_name']
        hidden.hidden = hidden_data['hidden']
    state.is_modified = False
