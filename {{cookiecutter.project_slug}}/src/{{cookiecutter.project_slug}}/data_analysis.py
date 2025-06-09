"""数据分析模块。

此模块实现了数据科学项目的核心数据分析功能。
"""
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_dataset(file_path: Union[str, Path]) -> pd.DataFrame:
    """加载数据集。

    支持CSV、Excel和Parquet格式的数据文件。

    Args:
        file_path: 数据文件路径

    Returns:
        加载的数据集

    Raises:
        ValueError: 不支持的文件格式
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"数据文件不存在: {file_path}")

    logger.info(f"加载数据集: {file_path}")

    # 根据文件扩展名选择加载方法
    if file_path.suffix.lower() == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix.lower() in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif file_path.suffix.lower() == '.parquet':
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {file_path.suffix}")


def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """分析数据集并返回摘要统计信息。

    Args:
        df: 要分析的数据集

    Returns:
        包含统计信息的字典
    """
    logger.info("生成数据集摘要统计信息")

    # 基本统计信息
    stats = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_types': df.dtypes.apply(lambda x: str(x)).to_dict(),
        'missing_values': df.isna().sum().to_dict(),
        'numeric_summary': {},
        'categorical_summary': {},
    }

    # 数值列统计
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        stats['numeric_summary'][col] = {
            'min': df[col].min(),
            'max': df[col].max(),
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
        }

    # 分类列统计
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        stats['categorical_summary'][col] = {
            'unique_values': df[col].nunique(),
            'top_values': df[col].value_counts().head(5).to_dict(),
        }

    return stats


def create_visualizations(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    columns: Optional[List[str]] = None
) -> List[Path]:
    """为数据集创建可视化图表。

    Args:
        df: 数据集
        output_dir: 输出目录路径
        columns: 要可视化的列名列表，默认为None（自动选择）

    Returns:
        生成的图表文件路径列表
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if columns is None:
        # 如果未指定列，则选择数值列
        columns = df.select_dtypes(include=['number']).columns.tolist()[:5]  # 最多5列

    logger.info(f"为以下列创建可视化: {columns}")

    generated_files = []

    # 直方图
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            plt.figure(figsize=(10, 6))
            plt.hist(df[col].dropna(), bins=30, alpha=0.7)
            plt.title(f"{col}的分布")
            plt.xlabel(col)
            plt.ylabel("频率")
            plt.grid(True, alpha=0.3)

            output_file = output_dir / f"{col}_histogram.png"
            plt.savefig(output_file)
            plt.close()
            generated_files.append(output_file)

    # 散点矩阵
    if len(columns) >= 2:
        scatter_cols = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])][:4]  # 最多4列
        if len(scatter_cols) >= 2:
            pd.plotting.scatter_matrix(df[scatter_cols], figsize=(12, 12), alpha=0.5)
            plt.tight_layout()

            output_file = output_dir / "scatter_matrix.png"
            plt.savefig(output_file)
            plt.close()
            generated_files.append(output_file)

    # 相关性热图
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty and len(numeric_df.columns) >= 2:
        plt.figure(figsize=(10, 8))
        corr = numeric_df.corr()
        plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title("特征相关性热图")

        output_file = output_dir / "correlation_heatmap.png"
        plt.savefig(output_file)
        plt.close()
        generated_files.append(output_file)

    logger.info(f"创建了 {len(generated_files)} 个可视化图表")
    return generated_files


def train_model(
    df: pd.DataFrame,
    target_column: str,
    feature_columns: Optional[List[str]] = None,
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict[str, Any]:
    """训练简单的机器学习模型。

    Args:
        df: 数据集
        target_column: 目标列名
        feature_columns: 特征列名列表，默认为None（使用所有数值列）
        test_size: 测试集比例
        random_state: 随机种子

    Returns:
        包含训练结果的字典

    Raises:
        ValueError: 如果目标列不在数据集中或特征列为空
    """
    if target_column not in df.columns:
        raise ValueError(f"目标列 '{target_column}' 不在数据集中")

    if feature_columns is None:
        # 如果未指定特征列，使用所有数值列（排除目标列）
        feature_columns = df.select_dtypes(include=['number']).columns.tolist()
        if target_column in feature_columns:
            feature_columns.remove(target_column)

    if not feature_columns:
        raise ValueError("没有可用的特征列")

    logger.info(f"使用特征 {feature_columns} 训练模型，目标列: {target_column}")

    # 准备数据
    X = df[feature_columns].copy()
    y = df[target_column].copy()

    # 处理缺失值
    X.fillna(X.mean(), inplace=True)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # 训练模型 (这里使用简单的随机森林作为示例)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(random_state=random_state)
    model.fit(X_train, y_train)

    # 评估模型
    y_pred = model.predict(X_test)

    # 如果是分类问题
    if len(np.unique(y)) < 10:  # 假设类别数小于10为分类问题
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'feature_importance': dict(zip(feature_columns, model.feature_importances_)),
        }
    else:  # 回归问题
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'feature_importance': dict(zip(feature_columns, model.feature_importances_)),
        }

    logger.info(f"模型训练完成，评估指标: {metrics}")

    return {
        'model': model,
        'metrics': metrics,
        'feature_columns': feature_columns,
        'target_column': target_column,
    }


def save_model(
    model_data: Dict[str, Any],
    output_path: Union[str, Path]
) -> Path:
    """保存训练好的模型。

    Args:
        model_data: 包含模型的字典（train_model的返回值）
        output_path: 模型输出路径

    Returns:
        保存的模型路径
    """
    import joblib

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 提取要保存的信息
    save_data = {
        'model': model_data['model'],
        'feature_columns': model_data['feature_columns'],
        'target_column': model_data['target_column'],
        'metrics': model_data['metrics'],
    }

    joblib.dump(save_data, output_path)
    logger.info(f"模型已保存到 {output_path}")

    return output_path


def load_model(model_path: Union[str, Path]) -> Dict[str, Any]:
    """加载保存的模型。

    Args:
        model_path: 模型文件路径

    Returns:
        加载的模型数据

    Raises:
        FileNotFoundError: 如果模型文件不存在
    """
    import joblib

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"模型文件不存在: {model_path}")

    model_data = joblib.load(model_path)
    logger.info(f"从 {model_path} 加载了模型")

    return model_data
