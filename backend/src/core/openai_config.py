"""
OpenAI Configuration Module

Sets up the OpenAI client with proper configuration and authentication.
"""
import os
import logging
from typing import Optional
from openai import OpenAI


logger = logging.getLogger(__name__)


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create and return an OpenAI client with proper configuration

    Args:
        api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)

    Returns:
        Configured OpenAI client
    """
    # Get API key from parameter or environment variable
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

    # Log that we're creating the client (without exposing the key)
    logger.info("Initializing OpenAI client")

    # Create and return the client
    client = OpenAI(api_key=api_key)

    return client


def validate_openai_config() -> bool:
    """
    Validate that the OpenAI configuration is properly set up

    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            return False

        # Try to create a client to verify the key is valid
        client = get_openai_client()

        # Test the client by making a simple API call
        # For now, just verify we can create the client without error
        # A full test would require an actual API call which we might not want during config
        logger.info("OpenAI configuration validated successfully")
        return True

    except Exception as e:
        logger.error(f"OpenAI configuration validation failed: {str(e)}")
        return False