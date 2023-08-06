"""Support for showing device locations."""
DOMAIN = "ais_help"


async def async_setup(hass, config):
    """Register the built-in help panel."""
    hass.components.frontend.async_register_built_in_panel(
        "aishelp", "Przydatne linki", "mdi:qrcode"
    )
    """Register the built-in doc panel."""
    hass.components.frontend.async_register_built_in_panel(
        "aisdocs", "Dokumentacja", "mdi:book-open"
    )
    """Register the built-in galery panel."""
    hass.components.frontend.async_register_built_in_panel(
        "aisgalery", "Galeria", "mdi:image-search"
    )
    """Register the built-in galery panel."""
    hass.components.frontend.async_register_built_in_panel(
        "lovelace/audio", "Audio", "mdi:library-music"
    )
    """Register the built-in video panel."""
    # hass.components.frontend.async_register_built_in_panel(
    #     "aisvideo", "Video", "mdi:youtube"
    # )
    return True
