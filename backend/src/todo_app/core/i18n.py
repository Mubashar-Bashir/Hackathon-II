"""
Internationalization (i18n) module for the Todo CLI application.

This module provides translation capabilities for multiple languages,
starting with Urdu support as required for Phase I.
"""

from typing import Dict, Optional
from enum import Enum


class Language(str, Enum):
    """Supported languages for the application."""
    ENGLISH = "en"
    URDU = "ur"


class I18nService:
    """
    Service class for handling internationalization and localization.

    Provides translation capabilities for UI labels, messages, and priority levels.
    """

    def __init__(self):
        """Initialize the i18n service with translation dictionaries."""
        self.translations = {
            Language.ENGLISH: {
                # CLI command labels
                "add": "Add Task",
                "add_ur": "ٹاسک شامل کریں",
                "list": "List Tasks",
                "list_ur": "ٹاسکس کی فہرست",
                "complete": "Complete Task",
                "complete_ur": "ٹاسک مکمل کریں",
                "update": "Update Task",
                "update_ur": "ٹاسک اپ ڈیٹ کریں",
                "delete": "Delete Task",
                "delete_ur": "ٹاسک حذف کریں",

                # Priority labels
                "high": "High",
                "high_ur": "اعلی",
                "medium": "Medium",
                "medium_ur": "درمیانہ",
                "low": "Low",
                "low_ur": "کم",

                # Status labels
                "pending": "Pending",
                "pending_ur": "زیر التوا",
                "complete_status": "Complete",
                "complete_ur_status": "مکمل",

                # General labels
                "id": "ID",
                "id_ur": "شناخت",
                "title": "Title",
                "title_ur": "عنوان",
                "description": "Description",
                "description_ur": "تفصیل",
                "status": "Status",
                "status_ur": "حالت",
                "priority": "Priority",
                "priority_ur": "اہمیت",
                "tags": "Tags",
                "tags_ur": "ٹیگز",
                "due_date": "Due Date",
                "due_date_ur": "واجب الادا تاریخ",
                "created": "Created",
                "created_ur": "تخلیق کردہ",

                # Messages
                "no_tasks_found": "No tasks found.",
                "no_tasks_found_ur": "کوئی ٹاسک نہیں ملا۔",
                "task_added": "Added task",
                "task_added_ur": "ٹاسک شامل کیا گیا",
                "task_updated": "Task updated",
                "task_updated_ur": "ٹاسک اپ ڈیٹ ہو گیا",
                "task_deleted": "Task deleted",
                "task_deleted_ur": "ٹاسک حذف ہو گیا",
                "task_completed": "Task marked as complete",
                "task_completed_ur": "ٹاسک مکمل کے بطور نشان زد کیا گیا",
                "task_pending": "Task marked as pending",
                "task_pending_ur": "ٹاسک زیر التوا کے بطور نشان زد کیا گیا",
            }
        }

        # Create Urdu-specific dictionary
        self.urdu_translations = {
            "high": "اعلی",
            "medium": "درمیانہ",
            "low": "کم",
            "pending": "زیر التوا",
            "complete": "مکمل",
            "add": "ٹاسک شامل کریں",
            "list": "ٹاسکس کی فہرست",
            "complete_task": "ٹاسک مکمل کریں",
            "update": "ٹاسک اپ ڈیٹ کریں",
            "delete": "ٹاسک حذف کریں",
            "id": "شناخت",
            "title": "عنوان",
            "description": "تفصیل",
            "status": "حالت",
            "priority": "اہمیت",
            "tags": "ٹیگز",
            "due_date": "واجب الادا تاریخ",
            "created": "تخلیق کردہ",
            "no_tasks": "کوئی ٹاسک نہیں ملا۔",
            "task_added": "ٹاسک شامل کیا گیا",
            "task_updated": "ٹاسک اپ ڈیٹ ہو گیا",
            "task_deleted": "ٹاسک حذف ہو گیا",
            "task_completed": "ٹاسک مکمل کے بطور نشان زد کیا گیا",
            "task_pending": "ٹاسک زیر التوا کے بطور نشان زد کیا گیا",
        }

    def get_translation(self, key: str, language: Language = Language.ENGLISH, urdu_mode: bool = False) -> str:
        """
        Get the translation for a given key in the specified language or Urdu mode.

        Args:
            key: The translation key to look up
            language: The language to use (default: English)
            urdu_mode: Whether to return Urdu translation for the key (default: False)

        Returns:
            The translated string
        """
        if urdu_mode and key in self.urdu_translations:
            return self.urdu_translations[key]

        if language in self.translations:
            return self.translations[language].get(key, key)

        return key

    def get_priority_translation(self, priority_value: str, urdu_mode: bool = False) -> str:
        """
        Get the translated priority label.

        Args:
            priority_value: The priority value (high, medium, low)
            urdu_mode: Whether to return Urdu translation (default: False)

        Returns:
            The translated priority label
        """
        translations = {
            "high": ("High", "اعلی"),
            "medium": ("Medium", "درمیانہ"),
            "low": ("Low", "کم")
        }

        if priority_value.lower() in translations:
            eng_label, urdu_label = translations[priority_value.lower()]
            return urdu_label if urdu_mode else eng_label

        return priority_value

    def get_status_translation(self, status_value: str, urdu_mode: bool = False) -> str:
        """
        Get the translated status label.

        Args:
            status_value: The status value (pending, complete)
            urdu_mode: Whether to return Urdu translation (default: False)

        Returns:
            The translated status label
        """
        translations = {
            "pending": ("Pending", "زیر التوا"),
            "complete": ("Complete", "مکمل")
        }

        if status_value.lower() in translations:
            eng_label, urdu_label = translations[status_value.lower()]
            return urdu_label if urdu_mode else eng_label

        return status_value


# Global instance for easy access
i18n_service = I18nService()