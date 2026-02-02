#!/usr/bin/env python3
"""
Tip Calculator - Streamlit App
A simple app to calculate tips and split bills among people
"""
import streamlit as st

def calculate_tip(bill_amount, tip_percentage, num_people=1):
    """
    Calculate tip and total amount per person
    
    Args:
        bill_amount: The total bill before tip
        tip_percentage: Tip percentage (e.g., 15, 18, 20)
        num_people: Number of people splitting the bill (default: 1)
    
    Returns:
        Dictionary with tip amount, total, and per person amounts
    """
    tip_amount = bill_amount * (tip_percentage / 100)
    total_amount = bill_amount + tip_amount
    amount_per_person = total_amount / num_people
    tip_per_person = tip_amount / num_people
    
    return {
        'bill': bill_amount,
        'tip_amount': tip_amount,
        'total': total_amount,
        'num_people': num_people,
        'per_person': amount_per_person,
        'tip_per_person': tip_per_person
    }

def main():
    """Main function to run the Streamlit tip calculator"""
    
    # Page configuration
    st.set_page_config(
        page_title="Tip Calculator",
        page_icon="💰",
        layout="centered"
    )
    
    # Title and description
    st.title("💰 Tip Calculator")
    st.markdown("Calculate tips and split bills easily!")
    
    st.divider()
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        bill_amount = st.number_input(
            "Bill Amount ($)",
            min_value=0.0,
            value=50.0,
            step=0.01,
            format="%.2f"
        )
    
    with col2:
        num_people = st.number_input(
            "Number of People",
            min_value=1,
            value=1,
            step=1
        )
    
    # Tip percentage selection
    st.subheader("Select Tip Percentage")
    
    # Quick tip buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("15%", use_container_width=True):
            st.session_state.tip_percentage = 15.0
    with col2:
        if st.button("18%", use_container_width=True):
            st.session_state.tip_percentage = 18.0
    with col3:
        if st.button("20%", use_container_width=True):
            st.session_state.tip_percentage = 20.0
    with col4:
        if st.button("25%", use_container_width=True):
            st.session_state.tip_percentage = 25.0
    
    # Custom tip percentage slider
    if 'tip_percentage' not in st.session_state:
        st.session_state.tip_percentage = 18.0
    
    tip_percentage = st.slider(
        "Or choose custom tip percentage",
        min_value=0.0,
        max_value=50.0,
        value=st.session_state.tip_percentage,
        step=0.5,
        format="%.1f%%"
    )
    
    st.session_state.tip_percentage = tip_percentage
    
    st.divider()
    
    # Calculate results
    if bill_amount > 0:
        result = calculate_tip(bill_amount, tip_percentage, num_people)
        
        # Display results
        st.subheader("📊 Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Bill Amount", f"${result['bill']:.2f}")
        with col2:
            st.metric("Tip Amount", f"${result['tip_amount']:.2f}")
        with col3:
            st.metric("Total Amount", f"${result['total']:.2f}")
        
        st.divider()
        
        # Per person breakdown
        if num_people > 1:
            st.subheader("👥 Per Person Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Per Person", f"${result['per_person']:.2f}")
            with col2:
                st.metric("Tip Per Person", f"${result['tip_per_person']:.2f}")
        
        # Detailed breakdown
        with st.expander("📋 Detailed Breakdown"):
            st.write(f"**Bill Amount:** ${result['bill']:.2f}")
            st.write(f"**Tip Percentage:** {tip_percentage}%")
            st.write(f"**Tip Amount:** ${result['tip_amount']:.2f}")
            st.write(f"**Total Amount:** ${result['total']:.2f}")
            st.write(f"**Number of People:** {result['num_people']}")
            if num_people > 1:
                st.write(f"**Total Per Person:** ${result['per_person']:.2f}")
                st.write(f"**Tip Per Person:** ${result['tip_per_person']:.2f}")
    else:
        st.info("👆 Enter a bill amount to calculate the tip!")
    
    # Footer
    st.divider()
    st.caption("💡 Tip: Use the quick buttons or slider to adjust the tip percentage")

if __name__ == "__main__":
    main()
