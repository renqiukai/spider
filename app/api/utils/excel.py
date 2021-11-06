import os
import pandas as pd
from static import BASE_PATH

def save_excel(
        data: dict,
        filepath: str = None,
        filename="数据导出",
        sheet_name="统计结果",
        file_type="xlsx"

) -> dict:
    # 导出成excel
    if not filepath:
        filepath = BASE_PATH
    filename = f"{filename}.{file_type}"
    df = pd.DataFrame(data)
    file_full_path = os.path.join(filepath, filename)
    df.to_excel(file_full_path, index=False, sheet_name=sheet_name)
    # 增加上传云存储后，这里添加方法。
    file_url = f"/tool/static/{filename}"
    doc = {
        "file_full_path": file_full_path,
        "file_url": file_url,
        "file_name": filename,
    }
    return doc
