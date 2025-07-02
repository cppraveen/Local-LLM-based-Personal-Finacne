from typing import List, Dict
from local_finance_llm import LocalFinanceLLM
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

def analyze_spending(categorized_transactions: List[Dict], llm: LocalFinanceLLM) -> Dict:
    """Analyze spending patterns and generate insights"""
    category_totals = {}
    for trans in categorized_transactions:
        if trans['amount'] < 0:  # Only expenses
            cat = trans.get('category', 'Miscellaneous')
            category_totals[cat] = category_totals.get(cat, 0) + abs(trans['amount'])
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    summary_prompt = f"""Analyze these spending patterns and provide 3 key insights:

Monthly Spending by Category:
"""
    for cat, amount in sorted_categories[:5]:
        summary_prompt += f"- {cat}: ${amount:.2f}\n"
    summary_prompt += """
Provide actionable insights about spending habits. Be specific and practical."""
    insights = llm.query_llm(summary_prompt)
    return {
        'category_totals': dict(sorted_categories),
        'top_categories': sorted_categories[:3],
        'insights': insights,
        'total_spending': sum(category_totals.values())
    }

def find_recurring_transactions(transactions: List[Dict], llm: LocalFinanceLLM) -> List[Dict]:
    """Identify recurring subscriptions and payments"""
    merchant_groups = {}
    for trans in transactions:
        merchant = trans['merchant']
        if merchant not in merchant_groups:
            merchant_groups[merchant] = []
        merchant_groups[merchant].append(trans)
    recurring = []
    for merchant, trans_list in merchant_groups.items():
        if len(trans_list) >= 2:
            amounts = [abs(t['amount']) for t in trans_list]
            if amounts and max(amounts) - min(amounts) < 0.1 * max(amounts):
                recurring.append({
                    'merchant': merchant,
                    'amount': sum(amounts) / len(amounts),
                    'frequency': len(trans_list),
                    'transactions': trans_list
                })
    return sorted(recurring, key=lambda x: x['amount'] * x['frequency'], reverse=True)

def generate_report(analysis_results: Dict, output_dir: str = "./reports"):
    """Generate a privacy-conscious financial report"""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"finance_report_{timestamp}.txt")
    with open(report_path, 'w') as f:
        f.write("Personal Finance Analysis Report\n")
        f.write("=" * 40 + "\n\n")
        f.write("Top Spending Categories:\n")
        for cat, amount in analysis_results['top_categories']:
            f.write(f"  - {cat}: ${amount:.2f}\n")
        f.write(f"\nTotal Monthly Spending: ${analysis_results['total_spending']:.2f}\n")
        f.write("\nAI-Generated Insights:\n")
        f.write((analysis_results['insights'] or "No insights generated.") + "\n")
    if analysis_results['category_totals']:
        plt.figure(figsize=(10, 6))
        categories = list(analysis_results['category_totals'].keys())[:8]
        amounts = [analysis_results['category_totals'][cat] for cat in categories]
        plt.bar(categories, amounts)
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.title('Spending by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, f"spending_chart_{timestamp}.png")
        plt.savefig(chart_path)
        plt.close()
    print(f"Report generated: {report_path}")
    return report_path 