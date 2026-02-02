import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

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
        income_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, key="income_amount")
        
        if st.button("Add Income", use_container_width=True):
            if income_source and income_amount > 0:
                st.session_state.income_items.append({
                    'source': income_source,
                    'amount': income_amount
                })
                st.success(f"Added {income_source}: ${income_amount:.2f}")
                st.rerun()
            else:
                st.error("Please enter both source and amount")
    
    with tab2:
        st.subheader("Add Expense")
        expense_category = st.selectbox(
            "Category",
            ["Housing", "Transportation", "Food & Dining", "Utilities", 
             "Healthcare", "Entertainment", "Shopping", "Savings", "Other"],
            key="expense_category"
        )
        expense_name = st.text_input("Expense Name", key="expense_name")
        expense_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, key="expense_amount")
        
        if st.button("Add Expense", use_container_width=True):
            if expense_name and expense_amount > 0:
                st.session_state.expense_items.append({
                    'category': expense_category,
                    'name': expense_name,
                    'amount': expense_amount
                })
                st.success(f"Added {expense_name}: ${expense_amount:.2f}")
                st.rerun()
            else:
                st.error("Please enter both name and amount")
    
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
                'expenses': st.session_state.expense_items
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
