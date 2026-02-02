import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import re

# Function to safely evaluate math expressions
def evaluate_math(expression):
    """
    Safely evaluate a mathematical expression.
    Returns the result as a float, or None if invalid.
    """
    try:
        # Remove any whitespace
        expression = str(expression).strip()
        
        # If it's already a number, return it
        try:
            return float(expression)
        except ValueError:
            pass
        
        # Allow only numbers, basic operators, parentheses, and decimal points
        if not re.match(r'^[\d\+\-\*/\.\(\)\s]+$', expression):
            return None
        
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except:
        return None

# Page configuration
st.set_page_config(
    page_title="Monthly Budget Tracker",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'income_items' not in st.session_state:
    st.session_state.income_items = []
if 'expense_items' not in st.session_state:
    st.session_state.expense_items = []
if 'custom_categories' not in st.session_state:
    st.session_state.custom_categories = [
        "Housing", "Transportation", "Food & Dining", "Utilities", 
        "Healthcare", "Entertainment", "Shopping", "Savings", "Other"
    ]

# Title
st.title("💰 Monthly Budget Tracker")
st.markdown("---")

# Sidebar for adding items
with st.sidebar:
    st.header("Add Budget Items")
    
    tab1, tab2 = st.tabs(["➕ Income", "➖ Expenses"])
    
    with tab1:
        st.subheader("Add Income")
        income_source = st.text_input("Income Source", key="income_source")
        income_amount_input = st.text_input(
            "Amount ($)", 
            key="income_amount",
            placeholder="e.g., 1000 or 500+250 or 40*52/12",
            help="Enter a number or math expression (e.g., 40*52/12 for weekly to monthly)"
        )
        
        # Show calculated amount
        if income_amount_input:
            calculated = evaluate_math(income_amount_input)
            if calculated is not None and calculated > 0:
                st.caption(f"💰 Calculated: ${calculated:,.2f}")
            elif calculated is not None and calculated <= 0:
                st.warning("Amount must be greater than 0")
            else:
                st.error("Invalid expression. Use only +, -, *, /, (), and numbers")
        
        if st.button("Add Income", use_container_width=True):
            calculated_amount = evaluate_math(income_amount_input) if income_amount_input else None
            if income_source and calculated_amount and calculated_amount > 0:
                st.session_state.income_items.append({
                    'source': income_source,
                    'amount': calculated_amount
                })
                st.success(f"Added {income_source}: ${calculated_amount:.2f}")
                st.rerun()
            else:
                st.error("Please enter valid source and amount")
    
    with tab2:
        st.subheader("Add Expense")
        
        # Category management
        with st.expander("➕ Add New Category"):
            new_category = st.text_input("New Category Name", key="new_category")
            if st.button("Add Category", use_container_width=True):
                if new_category and new_category not in st.session_state.custom_categories:
                    st.session_state.custom_categories.append(new_category)
                    st.success(f"Added category: {new_category}")
                    st.rerun()
                elif new_category in st.session_state.custom_categories:
                    st.warning("Category already exists!")
                else:
                    st.error("Please enter a category name")
        
        expense_category = st.selectbox(
            "Category",
            sorted(st.session_state.custom_categories),
            key="expense_category"
        )
        expense_name = st.text_input("Expense Name", key="expense_name")
        expense_amount_input = st.text_input(
            "Amount ($)", 
            key="expense_amount",
            placeholder="e.g., 50 or 25*4 or 100/2",
            help="Enter a number or math expression (e.g., 25*4 for weekly to monthly)"
        )
        
        # Show calculated amount
        if expense_amount_input:
            calculated = evaluate_math(expense_amount_input)
            if calculated is not None and calculated > 0:
                st.caption(f"💰 Calculated: ${calculated:,.2f}")
            elif calculated is not None and calculated <= 0:
                st.warning("Amount must be greater than 0")
            else:
                st.error("Invalid expression. Use only +, -, *, /, (), and numbers")
        
        if st.button("Add Expense", use_container_width=True):
            calculated_amount = evaluate_math(expense_amount_input) if expense_amount_input else None
            if expense_name and calculated_amount and calculated_amount > 0:
                st.session_state.expense_items.append({
                    'category': expense_category,
                    'name': expense_name,
                    'amount': calculated_amount
                })
                st.success(f"Added {expense_name}: ${calculated_amount:.2f}")
                st.rerun()
            else:
                st.error("Please enter valid name and amount")
    
    st.markdown("---")
    
    # Manage categories
    with st.expander("📋 Manage Categories"):
        st.write("**Current Categories:**")
        for category in sorted(st.session_state.custom_categories):
            col_cat1, col_cat2 = st.columns([3, 1])
            with col_cat1:
                st.write(f"• {category}")
            with col_cat2:
                # Prevent deletion if category is in use
                category_in_use = any(
                    item['category'] == category 
                    for item in st.session_state.expense_items
                )
                if st.button("🗑️", key=f"del_cat_{category}", 
                           disabled=category_in_use,
                           help="Cannot delete category with existing expenses"):
                    st.session_state.custom_categories.remove(category)
                    st.rerun()
    
    st.markdown("---")
    
    # Clear buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear All", use_container_width=True):
            st.session_state.income_items = []
            st.session_state.expense_items = []
            st.rerun()
    
    with col2:
        # Export button
        if st.button("Export Data", use_container_width=True):
            export_data = {
                'income': st.session_state.income_items,
                'expenses': st.session_state.expense_items,
                'categories': st.session_state.custom_categories
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"budget_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

# Main content area
col1, col2, col3 = st.columns(3)

# Calculate totals
total_income = sum(item['amount'] for item in st.session_state.income_items)
total_expenses = sum(item['amount'] for item in st.session_state.expense_items)
net_balance = total_income - total_expenses

# Display summary metrics
with col1:
    st.metric("Total Income", f"${total_income:,.2f}", delta=None)

with col2:
    st.metric("Total Expenses", f"${total_expenses:,.2f}", delta=None)

with col3:
    delta_color = "normal" if net_balance >= 0 else "inverse"
    st.metric("Net Balance", f"${net_balance:,.2f}", 
              delta=f"${abs(net_balance):,.2f} {'surplus' if net_balance >= 0 else 'deficit'}")

st.markdown("---")

# Create two columns for income and expenses
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Income Breakdown")
    if st.session_state.income_items:
        income_df = pd.DataFrame(st.session_state.income_items)
        
        # Display table
        st.dataframe(
            income_df.style.format({'amount': '${:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )
        
        # Delete buttons
        st.write("Remove items:")
        for idx, item in enumerate(st.session_state.income_items):
            if st.button(f"❌ {item['source']}", key=f"del_income_{idx}"):
                st.session_state.income_items.pop(idx)
                st.rerun()
    else:
        st.info("No income items added yet. Use the sidebar to add income sources.")

with col2:
    st.subheader("📉 Expense Breakdown")
    if st.session_state.expense_items:
        expense_df = pd.DataFrame(st.session_state.expense_items)
        
        # Display table
        st.dataframe(
            expense_df.style.format({'amount': '${:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )
        
        # Delete buttons
        st.write("Remove items:")
        for idx, item in enumerate(st.session_state.expense_items):
            if st.button(f"❌ {item['name']}", key=f"del_expense_{idx}"):
                st.session_state.expense_items.pop(idx)
                st.rerun()
    else:
        st.info("No expense items added yet. Use the sidebar to add expenses.")

st.markdown("---")

# Visualizations
if st.session_state.expense_items or st.session_state.income_items:
    st.subheader("📊 Visual Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Expense pie chart by category
        if st.session_state.expense_items:
            expense_df = pd.DataFrame(st.session_state.expense_items)
            expense_by_category = expense_df.groupby('category')['amount'].sum().reset_index()
            
            fig_pie = px.pie(
                expense_by_category,
                values='amount',
                names='category',
                title='Expenses by Category',
                hole=0.3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with viz_col2:
        # Income vs Expenses bar chart
        summary_data = pd.DataFrame({
            'Type': ['Income', 'Expenses', 'Net Balance'],
            'Amount': [total_income, total_expenses, net_balance],
            'Color': ['green', 'red', 'blue' if net_balance >= 0 else 'orange']
        })
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=summary_data['Type'],
            y=summary_data['Amount'],
            marker_color=summary_data['Color'],
            text=[f'${val:,.2f}' for val in summary_data['Amount']],
            textposition='auto',
        ))
        fig_bar.update_layout(
            title='Budget Summary',
            yaxis_title='Amount ($)',
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed expense breakdown
    if st.session_state.expense_items:
        st.subheader("💳 Detailed Expense Analysis")
        expense_df = pd.DataFrame(st.session_state.expense_items)
        
        fig_detailed = px.bar(
            expense_df.sort_values('amount', ascending=True),
            y='name',
            x='amount',
            color='category',
            orientation='h',
            title='All Expenses (Sorted by Amount)',
            labels={'amount': 'Amount ($)', 'name': 'Expense'},
            text='amount'
        )
        fig_detailed.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
        fig_detailed.update_layout(height=max(400, len(expense_df) * 30))
        st.plotly_chart(fig_detailed, use_container_width=True)

# Footer with tips
st.markdown("---")
st.markdown("""
### 💡 Budget Tips:
- **50/30/20 Rule**: Allocate 50% to needs, 30% to wants, and 20% to savings
- **Track regularly**: Update your budget weekly to stay on track
- **Emergency fund**: Aim for 3-6 months of expenses in savings
- **Review monthly**: Analyze spending patterns and adjust as needed
""")
