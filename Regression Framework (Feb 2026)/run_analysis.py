"""
Run Regression Analysis for GABM Papers
========================================

This script demonstrates how to use the regression_analysis module
for both Paper 2 (reference) and Paper 3 analyses.

Usage:
    python run_analysis.py
"""

from regression_analysis import RegressionAnalyzer
import os

# Paths
# Paper 2 input data lives in this repo, one level up in "Graphs and Data".
PAPER2_DATA = "../Graphs and Data/Paper2_data_for_analysis.xlsx"
PAPER3_DATA = "paper3_data_for_analysis.xlsx"  # Placeholder — Paper 3 lives in its own repo


def run_paper2_analysis():
    """
    Replicate Paper 2 analysis as a reference.
    This demonstrates the expected workflow.
    """
    print("\n" + "="*70)
    print("PAPER 2 ANALYSIS (Reference)")
    print("="*70)

    # Check if file exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, PAPER2_DATA)

    if not os.path.exists(data_path):
        print(f"Paper 2 data not found at: {data_path}")
        return

    # Initialize analyzer
    analyzer = RegressionAnalyzer(data_path)

    # Define comparisons (matching Paper 2 structure)
    comparisons = [
        {'sheet': 'Aware Data', 'treatment': 'Aware', 'interaction': 'NC Aware'},
        {'sheet': 'Learn Data', 'treatment': 'Learn', 'interaction': 'NC Learn'},
    ]

    # Run all comparisons
    results = analyzer.run_all_comparisons(comparisons)

    # Print summaries
    for base, interaction in results:
        analyzer.print_full_summary(base)
        if interaction:
            analyzer.print_full_summary(interaction)

    analyzer.print_beta_summary(results)
    analyzer.print_model_fit_comparison(results)

    # Export results
    output_path = os.path.join(script_dir, "paper2_regression_results.xlsx")
    analyzer.export_to_excel(results, output_path)


def run_paper3_analysis():
    """
    Paper 3 analysis template.
    Update this function when your data is ready.
    """
    print("\n" + "="*70)
    print("PAPER 3 ANALYSIS (Template)")
    print("="*70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, PAPER3_DATA)

    if not os.path.exists(data_path):
        print(f"Paper 3 data not found at: {data_path}")
        print("Update PAPER3_DATA path when your data is ready.")
        print("\nExpected data format:")
        print("  - Excel file with sheets for each comparison")
        print("  - Each sheet should have columns:")
        print("    * 'New Cases' - infection rate (0 to ~0.15)")
        print("    * 'New Cases^2' - squared term")
        print("    * '[Treatment]' - dummy variable (0 or 1)")
        print("    * 'NC [Treatment]' - interaction term")
        print("    * 'Mobility' - dependent variable (0 to 1)")
        return

    # Initialize analyzer
    analyzer = RegressionAnalyzer(data_path)

    # Show available sheets
    print(f"\nAvailable sheets: {analyzer.list_sheets()}")

    # ==================================================================
    # DEFINE YOUR COMPARISONS HERE
    # ==================================================================
    # Example structure - update with your actual treatment variables:
    #
    # comparisons = [
    #     {'sheet': 'Model A Data', 'treatment': 'ModelA'},
    #     {'sheet': 'Model B Data', 'treatment': 'ModelB'},
    #     {'sheet': 'Provider X Data', 'treatment': 'ProviderX'},
    #     {'sheet': 'Thinking Level Data', 'treatment': 'HighThinking'},
    #     # Add more as needed...
    # ]
    #
    # For comparing across models/providers, you might have:
    # comparisons = [
    #     {'sheet': 'Gemini Pro Data', 'treatment': 'GeminiPro'},
    #     {'sheet': 'Gemini Flash Data', 'treatment': 'GeminiFlash'},
    #     {'sheet': 'GPT4 Data', 'treatment': 'GPT4'},
    #     {'sheet': 'Claude Data', 'treatment': 'Claude'},
    # ]
    # ==================================================================

    comparisons = [
        # UPDATE THESE with your actual sheet names and treatment variables
        # {'sheet': 'Sheet Name', 'treatment': 'TreatmentVar'},
    ]

    if not comparisons:
        print("\nNo comparisons defined. Update the 'comparisons' list in run_paper3_analysis().")
        return

    # Run all comparisons
    results = analyzer.run_all_comparisons(comparisons)

    # Print summaries
    analyzer.print_beta_summary(results)
    analyzer.print_model_fit_comparison(results)

    # Export results
    output_path = os.path.join(script_dir, "paper3_regression_results.xlsx")
    analyzer.export_to_excel(results, output_path)


def run_custom_analysis(
    data_path: str,
    comparisons: list,
    output_name: str = "custom_results.xlsx"
):
    """
    Generic function for running custom analyses.

    Args:
        data_path: Path to Excel file
        comparisons: List of dicts with 'sheet' and 'treatment' keys
        output_name: Name for output Excel file

    Example:
        comparisons = [
            {'sheet': 'High Thinking', 'treatment': 'HighThink'},
            {'sheet': 'Medium Thinking', 'treatment': 'MedThink'},
            {'sheet': 'Low Thinking', 'treatment': 'LowThink'},
        ]
        run_custom_analysis('my_data.xlsx', comparisons, 'thinking_analysis.xlsx')
    """
    print(f"\n{'='*70}")
    print(f"CUSTOM ANALYSIS: {output_name}")
    print(f"{'='*70}")

    analyzer = RegressionAnalyzer(data_path)
    results = analyzer.run_all_comparisons(comparisons)

    analyzer.print_beta_summary(results)
    analyzer.print_model_fit_comparison(results)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_name)
    analyzer.export_to_excel(results, output_path)


if __name__ == "__main__":
    # Run Paper 2 analysis as reference
    run_paper2_analysis()

    # Run Paper 3 analysis (update when data is ready)
    # run_paper3_analysis()

    # Example of custom analysis:
    # run_custom_analysis(
    #     'path/to/data.xlsx',
    #     [
    #         {'sheet': 'Condition A', 'treatment': 'CondA'},
    #         {'sheet': 'Condition B', 'treatment': 'CondB'},
    #     ],
    #     'condition_comparison.xlsx'
    # )
