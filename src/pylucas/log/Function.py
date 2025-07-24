from typing import Literal

def ASCII_Art(Text: str,
              Font: Literal['univers', 'tarty8', 'tarty7', 'tarty1', 'block'] = 'starwars',
              AddSplit: bool = False) -> str:
    """
    Generate Ascii Art Characters

    Args:
        Text (str): _description_. Source String.
        Font (str, 'univers'): _description_. Set the font for generating Ascii Art.
        AddSplit (bool, False): _description_. Add a context split line

    Returns:
        str: _description_. Ascii Art Characters
    """
    from art import text2art

    ASCIIArt_Str: str = text2art(text=Text, font=Font); SplitLine: str = ''
    if AddSplit: SplitLine: str = '-'*(ASCIIArt_Str.find('\n')) + '\n'
    ASCIIArt_Str: str = SplitLine + ASCIIArt_Str + SplitLine
    LineCount: int = ASCIIArt_Str.count('\n')
    return ASCIIArt_Str, LineCount