def ReadExcel(io: str,
              sheet_name: int = 0,
              KeyTags: list = [],
              SearchRange: int = 15):
    """_用于简化读取Excel文件并进行基础清洗的过程._

    Args:
        io (str): _Excel文件路径_
        sheet_name (int | str, optional): _数据表名称或是索引._ 默认为 0.
        KeyTags (list[list[str]], optional): _数据表列标签中必须包含的关键字, 若单个列标签存在多个可能的关键字则使用列表包裹, 允许缺省._ 默认为 [].
        SearchRange (int, optional): _检索标题行的范围._ 默认为 15, 为 -1 时无限制.

    Raises:
        Exception: _在预设的范围内[header < {TagLine}]无法找到标题行._

    Returns:
        DataFrame: _完成读取与基础清晰的 DataFrame 实例._
    """
    from pandas import DataFrame, read_excel
    from numpy import nan
    Sheet: DataFrame = read_excel(io=io,
                                  sheet_name=sheet_name,
                                  header=None,
                                  dtype=str).fillna('')
    Sheet = Sheet.replace(['', ' '], nan).dropna(how='all').fillna('')
    SearchRange = Sheet.shape[0] if SearchRange == -1 else SearchRange
    KeyTags = [KeyTag if isinstance(KeyTag, list) else [KeyTag] for KeyTag in KeyTags]
    for Index_Row, Row in Sheet.iterrows():
        ColTags = Row.tolist()
        IsTittle: bool = all([any([Tag in ColTags for Tag in KeyTag]) for KeyTag in KeyTags])
        if Index_Row > SearchRange:
            raise Exception(f"在预设的范围内[header < {Index_Row}]无法匹配到标题行.")
        elif IsTittle or not KeyTags:
            Sheet = Sheet.iloc[Index_Row+1:].reset_index(drop=True)
            Sheet.columns = [Tag.strip() if Tag else f'Unnamed: {Index}' for Index, Tag in enumerate(ColTags)]
            return Sheet
    else:
        raise Exception(f"在数据表内无法匹配到标题行.")
