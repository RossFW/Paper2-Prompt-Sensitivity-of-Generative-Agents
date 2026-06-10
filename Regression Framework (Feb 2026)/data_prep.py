"""
Data Preparation Utilities for GABM Regression Analysis
========================================================

Helper functions to transform raw simulation data into the format
expected by the regression_analysis module.

Expected output format for each comparison:
    - New Cases: Percentage of population infected
    - New Cases^2: Squared term
    - [Treatment]: Dummy variable (0 or 1)
    - NC [Treatment]: Interaction term (New Cases * Treatment)
    - Mobility: Dependent variable
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple


def prepare_treatment_data(
    baseline_df: pd.DataFrame,
    treatment_df: pd.DataFrame,
    treatment_name: str,
    new_cases_col: str = 'new_cases',
    mobility_col: str = 'mobility'
) -> pd.DataFrame:
    """
    Combine baseline and treatment data into regression-ready format.

    Args:
        baseline_df: DataFrame with baseline (control) observations
        treatment_df: DataFrame with treatment observations
        treatment_name: Name for the treatment variable
        new_cases_col: Column name for new cases in source data
        mobility_col: Column name for mobility in source data

    Returns:
        DataFrame ready for regression analysis
    """
    # Add treatment dummy
    baseline = baseline_df.copy()
    baseline[treatment_name] = 0

    treatment = treatment_df.copy()
    treatment[treatment_name] = 1

    # Combine
    combined = pd.concat([baseline, treatment], ignore_index=True)

    # Standardize column names and create required variables
    result = pd.DataFrame({
        'New Cases': combined[new_cases_col],
        'New Cases^2': combined[new_cases_col] ** 2,
        treatment_name: combined[treatment_name],
        f'NC {treatment_name}': combined[new_cases_col] * combined[treatment_name],
        'Mobility': combined[mobility_col]
    })

    return result


def prepare_multi_treatment_data(
    data_dict: Dict[str, pd.DataFrame],
    baseline_key: str,
    new_cases_col: str = 'new_cases',
    mobility_col: str = 'mobility'
) -> Dict[str, pd.DataFrame]:
    """
    Prepare data for multiple treatment comparisons against a single baseline.

    Args:
        data_dict: Dict mapping condition names to DataFrames
        baseline_key: Key for the baseline condition in data_dict
        new_cases_col: Column name for new cases
        mobility_col: Column name for mobility

    Returns:
        Dict mapping treatment names to regression-ready DataFrames
    """
    baseline_df = data_dict[baseline_key]
    result = {}

    for key, df in data_dict.items():
        if key == baseline_key:
            continue

        treatment_name = key.replace(' ', '_')
        result[f'{treatment_name} Data'] = prepare_treatment_data(
            baseline_df=baseline_df,
            treatment_df=df,
            treatment_name=treatment_name,
            new_cases_col=new_cases_col,
            mobility_col=mobility_col
        )

    return result


def aggregate_simulation_runs(
    df: pd.DataFrame,
    group_cols: List[str],
    agg_col: str,
    agg_func: str = 'mean'
) -> pd.DataFrame:
    """
    Aggregate multiple simulation runs into single observations.

    Args:
        df: Raw simulation data with multiple runs
        group_cols: Columns to group by (e.g., ['day', 'condition'])
        agg_col: Column to aggregate (e.g., 'mobility')
        agg_func: Aggregation function ('mean', 'median', etc.)

    Returns:
        Aggregated DataFrame
    """
    return df.groupby(group_cols)[agg_col].agg(agg_func).reset_index()


def calculate_new_cases_pct(
    df: pd.DataFrame,
    infected_col: str = 'infected',
    population: int = 100,
    output_col: str = 'new_cases'
) -> pd.DataFrame:
    """
    Calculate new cases as percentage of population.

    Args:
        df: DataFrame with infection counts
        infected_col: Column with infected count
        population: Total population size
        output_col: Name for output column

    Returns:
        DataFrame with new_cases column added
    """
    result = df.copy()
    result[output_col] = result[infected_col] / population
    return result


def load_and_prepare_gabm_data(
    data_path: str,
    condition_col: str = 'condition',
    baseline_condition: str = 'baseline',
    new_cases_col: str = 'new_cases',
    mobility_col: str = 'mobility'
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Load GABM simulation output and prepare for regression.

    This is a template - adjust based on your actual data format.

    Args:
        data_path: Path to CSV/Excel with simulation data
        condition_col: Column identifying experimental condition
        baseline_condition: Value identifying baseline condition
        new_cases_col: Column with infection rate
        mobility_col: Column with mobility metric

    Returns:
        Tuple of (combined DataFrame, list of treatment names)
    """
    # Load data
    if data_path.endswith('.xlsx'):
        raw_df = pd.read_excel(data_path)
    else:
        raw_df = pd.read_csv(data_path)

    # Get unique conditions
    conditions = raw_df[condition_col].unique()
    treatments = [c for c in conditions if c != baseline_condition]

    # Prepare baseline
    baseline_df = raw_df[raw_df[condition_col] == baseline_condition].copy()

    # Prepare each treatment comparison
    all_dfs = {}
    for treatment in treatments:
        treatment_df = raw_df[raw_df[condition_col] == treatment].copy()
        treatment_name = treatment.replace(' ', '_').replace('-', '_')

        all_dfs[f'{treatment_name} Data'] = prepare_treatment_data(
            baseline_df=baseline_df,
            treatment_df=treatment_df,
            treatment_name=treatment_name,
            new_cases_col=new_cases_col,
            mobility_col=mobility_col
        )

    return all_dfs, treatments


def export_prepared_data(
    data_dict: Dict[str, pd.DataFrame],
    output_path: str
) -> None:
    """
    Export prepared data to Excel with multiple sheets.

    Args:
        data_dict: Dict mapping sheet names to DataFrames
        output_path: Path for output Excel file
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            # Excel sheet names max 31 chars
            safe_name = sheet_name[:31]
            df.to_excel(writer, sheet_name=safe_name, index=False)

    print(f"Prepared data exported to: {output_path}")
    print(f"Sheets: {list(data_dict.keys())}")


# Example usage
if __name__ == "__main__":
    print("Data Preparation Utilities")
    print("="*50)

    # Example: Create sample data showing expected format
    np.random.seed(42)
    n = 50

    # Simulate baseline data
    baseline = pd.DataFrame({
        'day': range(n),
        'new_cases': np.random.uniform(0, 0.12, n),
        'mobility': np.random.uniform(0.2, 0.9, n)
    })

    # Simulate treatment data
    treatment = pd.DataFrame({
        'day': range(n),
        'new_cases': np.random.uniform(0, 0.12, n),
        'mobility': np.random.uniform(0.15, 0.85, n)  # Slightly lower
    })

    # Prepare for regression
    prepared = prepare_treatment_data(
        baseline_df=baseline,
        treatment_df=treatment,
        treatment_name='MyTreatment'
    )

    print("\nSample prepared data:")
    print(prepared.head(10))
    print(f"\nShape: {prepared.shape}")
    print(f"Columns: {list(prepared.columns)}")

    print("\n" + "="*50)
    print("To prepare your actual data:")
    print("""
1. Load your raw simulation outputs
2. Identify baseline and treatment conditions
3. Use prepare_treatment_data() for each comparison
4. Export with export_prepared_data()

Example:
    from data_prep import prepare_treatment_data, export_prepared_data

    # Load your raw data
    baseline = pd.read_csv('baseline_run.csv')
    treatment_a = pd.read_csv('treatment_a_run.csv')
    treatment_b = pd.read_csv('treatment_b_run.csv')

    # Prepare each comparison
    data_dict = {
        'Treatment A Data': prepare_treatment_data(baseline, treatment_a, 'TreatmentA'),
        'Treatment B Data': prepare_treatment_data(baseline, treatment_b, 'TreatmentB'),
    }

    # Export for regression analysis
    export_prepared_data(data_dict, 'paper3_data_for_analysis.xlsx')
""")
