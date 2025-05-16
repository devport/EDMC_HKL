from l10n import translations


def ptl(x: str) -> str:
    result = translations.translate(x, context=__file__)
    return result if result != x else x
