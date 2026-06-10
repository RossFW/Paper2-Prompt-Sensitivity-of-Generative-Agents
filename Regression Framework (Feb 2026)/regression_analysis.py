"""
Multilinear Regression Analysis Framework for GABM Paper 3
==========================================================

This module provides reusable functions for running regression models
comparing mobility responses across different experimental conditions.

Models supported:
1. Base model: Mobility = β₀ + β₁NC + β₂NC² + β₃*Treatment
2. Interaction model: Mobility = β₀ + β₁NC + β₂NC² + β₃*Treatment + β₄NC*Treatment

Usage:
    from regression_analysis import RegressionAnalyzer

    analyzer = RegressionAnalyzer('path/to/data.xlsx')
    results = analyzer.run_comparison('Sheet Name', 'TreatmentVar')
    analyzer.print_summary(results)
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


@dataclass
class RegressionResult:
    """Stores results from a single regression model."""
    model_name: str
    treatment_var: str
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    t_values: Dict[str, float]
    p_values: Dict[str, float]
    r_squared: float
    adj_r_squared: float
    n_obs: int
    f_statistic: float
    f_pvalue: float
    ols_result: sm.regression.linear_model.RegressionResultsWrapper


class RegressionAnalyzer:
    """
    Main class for running regression comparisons.

    Attributes:
        data_path: Path to Excel file with data
        sheets: Dict of sheet names to DataFrames
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the analyzer.

        Args:
            data_path: Path to Excel file. If None, use set_data() later.
        """
        self.data_path = data_path
        self.sheets: Dict[str, pd.DataFrame] = {}

        if data_path:
            self.load_data(data_path)

    def load_data(self, data_path: str) -> None:
        """Load all sheets from an Excel file."""
        self.data_path = data_path
        xl = pd.ExcelFile(data_path)
        for sheet in xl.sheet_names:
            self.sheets[sheet] = pd.read_excel(xl, sheet_name=sheet)
        print(f"Loaded {len(self.sheets)} sheets: {list(self.sheets.keys())}")

    def set_data(self, name: str, df: pd.DataFrame) -> None:
        """Manually set a DataFrame for analysis."""
        self.sheets[name] = df

    def list_sheets(self) -> List[str]:
        """Return list of available sheet names."""
        return list(self.sheets.keys())

    def get_sheet_info(self, sheet_name: str) -> None:
        """Print info about a specific sheet."""
        if sheet_name not in self.sheets:
            print(f"Sheet '{sheet_name}' not found. Available: {self.list_sheets()}")
            return
        df = self.sheets[sheet_name]
        print(f"\n--- {sheet_name} ---")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())

    def run_base_model(
        self,
        df: pd.DataFrame,
        treatment_var: str,
        dep_var: str = 'Mobility',
        nc_var: str = 'New Cases',
        nc_sq_var: str = 'New Cases^2'
    ) -> RegressionResult:
        """
        Run base model: Mobility = β₀ + β₁NC + β₂NC² + β₃*Treatment

        Args:
            df: DataFrame with the data
            treatment_var: Name of the treatment dummy variable
            dep_var: Name of dependent variable (default: 'Mobility')
            nc_var: Name of new cases variable (default: 'New Cases')
            nc_sq_var: Name of new cases squared variable (default: 'New Cases^2')

        Returns:
            RegressionResult with model outputs
        """
        X = sm.add_constant(df[[nc_var, nc_sq_var, treatment_var]])
        y = df[dep_var]
        model = sm.OLS(y, X).fit()

        return self._extract_results(
            model,
            f"Base Model ({treatment_var})",
            treatment_var
        )

    def run_interaction_model(
        self,
        df: pd.DataFrame,
        treatment_var: str,
        interaction_var: str,
        dep_var: str = 'Mobility',
        nc_var: str = 'New Cases',
        nc_sq_var: str = 'New Cases^2'
    ) -> RegressionResult:
        """
        Run interaction model: Mobility = β₀ + β₁NC + β₂NC² + β₃*Treatment + β₄NC*Treatment

        Args:
            df: DataFrame with the data
            treatment_var: Name of the treatment dummy variable
            interaction_var: Name of the NC*Treatment interaction variable
            dep_var: Name of dependent variable (default: 'Mobility')
            nc_var: Name of new cases variable (default: 'New Cases')
            nc_sq_var: Name of new cases squared variable (default: 'New Cases^2')

        Returns:
            RegressionResult with model outputs
        """
        X = sm.add_constant(df[[nc_var, nc_sq_var, treatment_var, interaction_var]])
        y = df[dep_var]
        model = sm.OLS(y, X).fit()

        return self._extract_results(
            model,
            f"Interaction Model ({treatment_var})",
            treatment_var
        )

    def _extract_results(
        self,
        model: sm.regression.linear_model.RegressionResultsWrapper,
        model_name: str,
        treatment_var: str
    ) -> RegressionResult:
        """Extract results from fitted OLS model into RegressionResult."""
        return RegressionResult(
            model_name=model_name,
            treatment_var=treatment_var,
            coefficients=dict(model.params),
            std_errors=dict(model.bse),
            t_values=dict(model.tvalues),
            p_values=dict(model.pvalues),
            r_squared=model.rsquared,
            adj_r_squared=model.rsquared_adj,
            n_obs=int(model.nobs),
            f_statistic=model.fvalue,
            f_pvalue=model.f_pvalue,
            ols_result=model
        )

    def run_comparison(
        self,
        sheet_name: str,
        treatment_var: str,
        interaction_var: Optional[str] = None,
        dep_var: str = 'Mobility',
        nc_var: str = 'New Cases',
        nc_sq_var: str = 'New Cases^2'
    ) -> Tuple[RegressionResult, Optional[RegressionResult]]:
        """
        Run both base and interaction models for a treatment variable.

        Args:
            sheet_name: Name of the sheet in the Excel file
            treatment_var: Name of the treatment dummy variable
            interaction_var: Name of NC*Treatment variable. If None, tries 'NC {treatment_var}'
            dep_var: Name of dependent variable
            nc_var: Name of new cases variable
            nc_sq_var: Name of new cases squared variable

        Returns:
            Tuple of (base_result, interaction_result)
        """
        if sheet_name not in self.sheets:
            raise ValueError(f"Sheet '{sheet_name}' not found. Available: {self.list_sheets()}")

        df = self.sheets[sheet_name]

        # Run base model
        base_result = self.run_base_model(df, treatment_var, dep_var, nc_var, nc_sq_var)

        # Run interaction model if interaction variable exists
        if interaction_var is None:
            interaction_var = f"NC {treatment_var}"

        interaction_result = None
        if interaction_var in df.columns:
            interaction_result = self.run_interaction_model(
                df, treatment_var, interaction_var, dep_var, nc_var, nc_sq_var
            )
        else:
            print(f"Warning: Interaction variable '{interaction_var}' not found. Skipping interaction model.")

        return base_result, interaction_result

    def run_all_comparisons(
        self,
        comparisons: List[Dict],
        dep_var: str = 'Mobility',
        nc_var: str = 'New Cases',
        nc_sq_var: str = 'New Cases^2'
    ) -> List[Tuple[RegressionResult, Optional[RegressionResult]]]:
        """
        Run multiple comparisons at once.

        Args:
            comparisons: List of dicts with keys 'sheet' and 'treatment'
                         e.g., [{'sheet': 'Aware Data', 'treatment': 'Aware'}, ...]
            dep_var, nc_var, nc_sq_var: Variable names

        Returns:
            List of (base_result, interaction_result) tuples
        """
        results = []
        for comp in comparisons:
            sheet = comp['sheet']
            treatment = comp['treatment']
            interaction = comp.get('interaction')

            result = self.run_comparison(
                sheet, treatment, interaction, dep_var, nc_var, nc_sq_var
            )
            results.append(result)

        return results

    @staticmethod
    def significance_stars(p_value: float) -> str:
        """Return significance stars based on p-value."""
        if p_value < 0.001:
            return "***"
        elif p_value < 0.01:
            return "**"
        elif p_value < 0.05:
            return "*"
        return ""

    def print_full_summary(self, result: RegressionResult) -> None:
        """Print full OLS summary for a single model."""
        print(f"\n{'='*70}")
        print(f"{result.model_name}")
        print(f"{'='*70}")
        print(result.ols_result.summary())

    def print_beta_summary(
        self,
        results: List[Tuple[RegressionResult, Optional[RegressionResult]]],
        focus_vars: Optional[List[str]] = None
    ) -> None:
        """
        Print a summary table focused on β₃ and β₄ coefficients.

        Args:
            results: List of (base_result, interaction_result) tuples
            focus_vars: List of variable names to focus on. If None, auto-detect treatment vars.
        """
        print(f"\n{'='*80}")
        print("SUMMARY: β₃ and β₄ COEFFICIENTS")
        print(f"{'='*80}")
        print(f"\n{'Model':<25} {'Variable':<18} {'Coef':<12} {'Std Err':<10} {'P>|t|':<10} {'Sig':<6}")
        print("-"*85)

        for base_result, interaction_result in results:
            treatment = base_result.treatment_var

            # Base model β₃
            coef = base_result.coefficients[treatment]
            se = base_result.std_errors[treatment]
            p = base_result.p_values[treatment]
            sig = self.significance_stars(p)
            print(f"{'Base':<25} {'β₃ ('+treatment+')':<18} {coef:<12.4f} {se:<10.4f} {p:<10.4f} {sig:<6}")

            # Interaction model
            if interaction_result:
                # β₃ in interaction model
                coef = interaction_result.coefficients[treatment]
                se = interaction_result.std_errors[treatment]
                p = interaction_result.p_values[treatment]
                sig = self.significance_stars(p)
                print(f"{'Interaction':<25} {'β₃ ('+treatment+')':<18} {coef:<12.4f} {se:<10.4f} {p:<10.4f} {sig:<6}")

                # β₄ (interaction term)
                interaction_var = f"NC {treatment}"
                if interaction_var in interaction_result.coefficients:
                    coef = interaction_result.coefficients[interaction_var]
                    se = interaction_result.std_errors[interaction_var]
                    p = interaction_result.p_values[interaction_var]
                    sig = self.significance_stars(p)
                    print(f"{'Interaction':<25} {'β₄ (NC*'+treatment+')':<18} {coef:<12.4f} {se:<10.4f} {p:<10.4f} {sig:<6}")

            print("-"*85)

        print("\n*** p<0.001, ** p<0.01, * p<0.05")

    def print_model_fit_comparison(
        self,
        results: List[Tuple[RegressionResult, Optional[RegressionResult]]]
    ) -> None:
        """Print R² comparison across all models."""
        print(f"\n{'='*70}")
        print("MODEL FIT COMPARISON")
        print(f"{'='*70}")

        for base_result, interaction_result in results:
            treatment = base_result.treatment_var
            print(f"\n{treatment}:")
            print(f"  Base model:        R² = {base_result.r_squared:.4f}, Adj R² = {base_result.adj_r_squared:.4f}, N = {base_result.n_obs}")
            if interaction_result:
                print(f"  Interaction model: R² = {interaction_result.r_squared:.4f}, Adj R² = {interaction_result.adj_r_squared:.4f}, N = {interaction_result.n_obs}")

    def export_results_to_dataframe(
        self,
        results: List[Tuple[RegressionResult, Optional[RegressionResult]]]
    ) -> pd.DataFrame:
        """
        Export results to a DataFrame for further analysis or export.

        Returns:
            DataFrame with columns: Model, Treatment, Variable, Coef, StdErr, t, p, Sig, R2, N
        """
        rows = []

        for base_result, interaction_result in results:
            treatment = base_result.treatment_var

            # Base model
            for var in base_result.coefficients:
                rows.append({
                    'Model': 'Base',
                    'Treatment': treatment,
                    'Variable': var,
                    'Coefficient': base_result.coefficients[var],
                    'Std Error': base_result.std_errors[var],
                    't-value': base_result.t_values[var],
                    'p-value': base_result.p_values[var],
                    'Significance': self.significance_stars(base_result.p_values[var]),
                    'R²': base_result.r_squared,
                    'N': base_result.n_obs
                })

            # Interaction model
            if interaction_result:
                for var in interaction_result.coefficients:
                    rows.append({
                        'Model': 'Interaction',
                        'Treatment': treatment,
                        'Variable': var,
                        'Coefficient': interaction_result.coefficients[var],
                        'Std Error': interaction_result.std_errors[var],
                        't-value': interaction_result.t_values[var],
                        'p-value': interaction_result.p_values[var],
                        'Significance': self.significance_stars(interaction_result.p_values[var]),
                        'R²': interaction_result.r_squared,
                        'N': interaction_result.n_obs
                    })

        return pd.DataFrame(rows)

    def export_to_excel(
        self,
        results: List[Tuple[RegressionResult, Optional[RegressionResult]]],
        output_path: str
    ) -> None:
        """Export results to an Excel file."""
        df = self.export_results_to_dataframe(results)
        df.to_excel(output_path, index=False)
        print(f"Results exported to: {output_path}")


def create_placeholder_data() -> pd.DataFrame:
    """
    Create placeholder data matching the expected format.
    Use this as a template for preparing your actual data.

    Expected columns:
        - New Cases: Percentage of population infected (0.0 to ~0.15)
        - New Cases^2: Squared term for nonlinear relationship
        - Treatment: Dummy variable (0 or 1) for experimental condition
        - NC Treatment: Interaction term (New Cases * Treatment)
        - Mobility: Dependent variable (0.0 to 1.0)
    """
    np.random.seed(42)
    n = 400

    # Generate new cases (percentage)
    new_cases = np.random.uniform(0, 0.15, n)
    new_cases_sq = new_cases ** 2

    # Treatment dummy (half treated, half control)
    treatment = np.concatenate([np.zeros(n//2), np.ones(n//2)])
    np.random.shuffle(treatment)

    # Interaction term
    nc_treatment = new_cases * treatment

    # Generate mobility with realistic relationship
    # Base: high mobility at low infection, decreasing exponentially
    mobility = (
        0.9  # baseline
        - 25 * new_cases  # linear effect
        + 180 * new_cases_sq  # quadratic effect (captures nonlinearity)
        - 0.05 * treatment  # treatment effect (β₃)
        - 2.0 * nc_treatment  # interaction effect (β₄)
        + np.random.normal(0, 0.08, n)  # noise
    )
    mobility = np.clip(mobility, 0, 1)

    return pd.DataFrame({
        'New Cases': new_cases,
        'New Cases^2': new_cases_sq,
        'Treatment': treatment,
        'NC Treatment': nc_treatment,
        'Mobility': mobility
    })


# Example usage and demonstration
if __name__ == "__main__":
    print("="*70)
    print("REGRESSION ANALYSIS FRAMEWORK - DEMO")
    print("="*70)

    # Create analyzer with placeholder data
    analyzer = RegressionAnalyzer()

    # Add placeholder data
    placeholder_df = create_placeholder_data()
    analyzer.set_data('Placeholder Data', placeholder_df)

    print("\nPlaceholder data created:")
    analyzer.get_sheet_info('Placeholder Data')

    # Run comparison
    print("\n" + "="*70)
    print("RUNNING REGRESSION MODELS")
    print("="*70)

    base_result, interaction_result = analyzer.run_comparison(
        sheet_name='Placeholder Data',
        treatment_var='Treatment',
        interaction_var='NC Treatment'
    )

    # Print full summaries
    analyzer.print_full_summary(base_result)
    if interaction_result:
        analyzer.print_full_summary(interaction_result)

    # Print focused summary
    results = [(base_result, interaction_result)]
    analyzer.print_beta_summary(results)
    analyzer.print_model_fit_comparison(results)

    print("\n" + "="*70)
    print("EXAMPLE: How to use with your actual data")
    print("="*70)
    print("""
# Load your Excel file
analyzer = RegressionAnalyzer('path/to/Paper3_data_for_analysis.xlsx')

# See available sheets
print(analyzer.list_sheets())

# Run single comparison
base, interaction = analyzer.run_comparison(
    sheet_name='Treatment A Data',
    treatment_var='TreatmentA'
)

# Run multiple comparisons at once
comparisons = [
    {'sheet': 'Treatment A Data', 'treatment': 'TreatmentA'},
    {'sheet': 'Treatment B Data', 'treatment': 'TreatmentB'},
    {'sheet': 'Treatment C Data', 'treatment': 'TreatmentC'},
]
all_results = analyzer.run_all_comparisons(comparisons)

# Print summaries
analyzer.print_beta_summary(all_results)
analyzer.print_model_fit_comparison(all_results)

# Export to Excel
analyzer.export_to_excel(all_results, 'regression_results.xlsx')
""")
