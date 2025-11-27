"""UI Tabs V2 - Reorganized 7 tabs."""

from .tab_recording import create_recording_tab
from .tab_upload import create_upload_tab
from .tab_chat import create_chat_tab
from .tab_analysis_history import create_analysis_history_tab
from .tab_recording_history import create_recording_history_tab
from .tab_search_export import create_search_export_tab
from .tab_checklist import create_checklist_tab

__all__ = [
    'create_recording_tab',
    'create_upload_tab',
    'create_chat_tab',
    'create_analysis_history_tab',
    'create_recording_history_tab',
    'create_search_export_tab',
    'create_checklist_tab',
]
