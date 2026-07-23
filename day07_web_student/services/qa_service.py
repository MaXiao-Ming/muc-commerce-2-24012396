from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    # 1. 总用户数问答（已存在）
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # ========== TODO 4-1：补充以下四类问答 ==========
    
    # 2. 流失率问答
    if any(word in normalized for word in ["流失率", "流失比例", "整体流失", "总体流失"]):
        return (f"总体流失率为 {metrics['流失率']:.1%}，"
                f"共有 {int(metrics['流失人数']):,} 名用户流失。")
    
    # 3. 偏好品类问答
    if any(word in normalized for word in ["品类", "用户最多", "哪个品类", "最多用户", "偏好品类"]):
        category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
        top_category = category_df.loc[category_df['用户数'].idxmax()]
        return (f"用户最多的偏好品类是「{top_category['PreferedOrderCat']}」，"
                f"共有 {int(top_category['用户数']):,} 名用户。")
    
    # 4. 生命周期风险问答
    if any(word in normalized for word in ["生命周期", "风险最高", "哪个阶段", "流失最高", "最高风险"]):
        segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
        highest_risk = segment_df.loc[segment_df['流失率'].idxmax()]
        return (f"生命周期风险最高的阶段是「{highest_risk['TenureGroup']}」，"
                f"流失率高达 {highest_risk['流失率']:.1%}，"
                f"该阶段共有 {int(highest_risk['用户数']):,} 名用户，"
                f"其中 {int(highest_risk['流失人数']):,} 人已流失。")
    
    # 5. 订单问答
    if any(word in normalized for word in ["订单数", "平均订单", "订单量", "人均订单"]):
        return (f"所有用户的平均订单数为 {metrics['平均订单数']:.2f} 单，"
                f"订单数中位数为 {metrics['订单数中位数']:.0f} 单。")
    
    # 6. 不支持的问题（友好提示）
    return (
        "抱歉，我目前只能回答以下类型的问题：\n"
        "• 总用户数（例如：系统中有多少用户？）\n"
        "• 流失情况（例如：总体流失率是多少？）\n"
        "• 偏好品类（例如：哪个品类用户最多？）\n"
        "• 生命周期风险（例如：哪个阶段风险最高？）\n"
        "• 订单统计（例如：平均订单数是多少？）\n"
        "请换一种更具体的问法。"
    )