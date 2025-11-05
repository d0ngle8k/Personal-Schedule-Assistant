"""
Dialogs Package
Event management dialogs (Create, Edit, Delete, Search, Settings, Statistics)
"""
from app.views.dialogs.event_dialog import EventDialog
from app.views.dialogs.delete_confirm_dialog import DeleteConfirmDialog
from app.views.dialogs.date_picker_dialog import DatePickerDialog
from app.views.dialogs.search_dialog import SearchDialog
from app.views.dialogs.settings_dialog import SettingsDialog
from app.views.dialogs.statistics_dialog import StatisticsDialog

__all__ = ['EventDialog', 'DeleteConfirmDialog', 'DatePickerDialog', 'SearchDialog', 'SettingsDialog', 'StatisticsDialog']
