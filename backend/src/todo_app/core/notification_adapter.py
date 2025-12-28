"""
Notification adapter for the Todo CLI application.

This module provides cross-platform notification capabilities
using the plyer library.
"""

import logging
from typing import Optional
from plyer import notification


# Configure logging
logger = logging.getLogger(__name__)


class NotificationAdapter:
    """
    Adapter class that provides cross-platform notification capabilities.
    """

    def __init__(self):
        """
        Initialize the NotificationAdapter.
        """
        logger.info("Initializing NotificationAdapter")

    def send_notification(self, title: str, message: str, timeout: int = 10) -> bool:
        """
        Send a system notification.

        Args:
            title: The title of the notification
            message: The message content of the notification
            timeout: How long the notification should appear (in seconds)

        Returns:
            True if the notification was sent successfully, False otherwise
        """
        logger.debug(f"Sending notification: {title} - {message}")

        try:
            # Use plyer to send cross-platform notifications
            notification.notify(
                title=title,
                message=message,
                timeout=timeout
            )
            logger.info(f"Notification sent successfully: {title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False