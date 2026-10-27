"""Image utility functions"""

import ipaddress
import os
import socket
from urllib.parse import urlparse

import requests
from PIL import Image
from utils.logger import get_logger

logger = get_logger(__name__)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address string resolves to a private/reserved range.

    Blocks loopback, link-local, private, multicast, and any other
    address that is not a globally routable unicast address.
    """
    try:
        addr = ipaddress.ip_address(ip_str)
    except ValueError:
        # Not a valid IP literal — treat as unsafe
        return True
    return (
        addr.is_loopback
        or addr.is_private
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def validate_url(url: str) -> None:
    """Validate that a URL is safe to fetch.

    Raises ``ValueError`` if the URL:
    - Does not use the ``https`` scheme
    - Has an empty or missing host
    - Resolves to a private, loopback, link-local, or otherwise
      non-globally-routable IP address (SSRF prevention)

    Args:
        url: The URL to validate.

    Raises:
        ValueError: If the URL fails any safety check.
    """
    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise ValueError(
            f"Unsafe URL scheme '{parsed.scheme}': only 'https' is allowed."
        )

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL has no hostname.")

    # Resolve hostname to its IP address(es) and reject any private address.
    # We check every address returned so an attacker cannot slip through by
    # providing a hostname that has both a public and a private address.
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for addr_info in addr_infos:
        # addr_info is (family, type, proto, canonname, sockaddr)
        # sockaddr is (address, port) for IPv4 or (address, port, flow, scope) for IPv6
        ip_str = addr_info[4][0]
        if _is_private_ip(ip_str):
            raise ValueError(
                f"URL hostname '{hostname}' resolves to a private/reserved "
                f"IP address ({ip_str}), which is not allowed."
            )


def download_image(url: str, output_path: str) -> bool:
    """Download image from URL and save locally.

    Only ``https`` URLs that resolve to globally routable addresses are
    accepted.  Attempts to fetch ``http``, ``file``, or URLs pointing at
    private/loopback IPs (including cloud-metadata endpoints such as
    ``169.254.169.254``) are rejected to prevent SSRF.

    Args:
        url: Image URL (must be https and resolve to a public IP)
        output_path: Path to save image

    Returns:
        True if successful, False otherwise
    """
    try:
        validate_url(url)
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save image
        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Downloaded image: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download image: {str(e)}")
        return False


def optimize_image(input_path: str, output_path: str, max_width: int = 1024) -> bool:
    """Optimize image size and quality.

    Args:
        input_path: Path to input image
        output_path: Path to save optimized image
        max_width: Maximum width in pixels

    Returns:
        True if successful, False otherwise
    """
    try:
        with Image.open(input_path) as img:
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Save optimized
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, quality=85, optimize=True)
            logger.info(f"Optimized image: {output_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to optimize image: {str(e)}")
        return False


def get_image_info(image_path: str) -> dict:
    """Get image information.

    Args:
        image_path: Path to image file

    Returns:
        Dictionary with image info
    """
    try:
        with Image.open(image_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_kb": os.path.getsize(image_path) / 1024,
            }
    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        return {}
