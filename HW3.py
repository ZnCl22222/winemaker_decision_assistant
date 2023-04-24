import streamlit as st
import numpy as np

def e_value(cb, hs, ts, ns):
    e_storm = cb*3300000 + (1-cb)*420000
    e_no_storm = hs*1500000 + ts*1410000 + ns*960000

    Specificity = 0.68
    Sensitivity = 0.63
    P_storm = 0.5

    P_DNS = Specificity*(1-P_storm) + (1-Sensitivity)*P_storm
    P_DS = Sensitivity*P_storm + (1-Specificity)*(1-P_storm)
    
    P_NS_DNS = round((Specificity*(1-P_storm)) / P_DNS, 2)
    P_S_DS = round((Sensitivity*P_storm) / P_DS, 2)

    if P_S_DS*e_storm + (1-P_S_DS)*e_no_storm > 960000:
        e_detect_storm = P_S_DS*e_storm + (1-P_S_DS)*e_no_storm
        action_storm = 'not harvest'
    else:
        e_detect_storm = 960000
        action_storm = 'harvest'

    if (1-P_NS_DNS)*e_storm + P_NS_DNS*e_no_storm > 960000:
        e_detect_no_storm = (1-P_NS_DNS)*e_storm + P_NS_DNS*e_no_storm
        action_no_storm = 'not harvest'
    else:
        e_detect_no_storm = 960000
        action_no_storm = 'harvest'

    return (round(P_DS*e_detect_storm + P_DNS*e_detect_no_storm, 2), action_storm, action_no_storm)


def MVP_ui():
    # Header
    st.header("Winemaker Descision Making Assistant")
    # Subheader
    st.subheader("We help you predict the storm and make decision!!")
    # Enter likelihoods
    cb = st.number_input("Enter the chance of botrytis: ", value = 0.1, min_value=0.0, max_value=1.0)
    hs = st.number_input("Enter the chance of high sugar value: ", value = 0.1, min_value=0.0, max_value=1.0)
    ts = st.number_input("Enter the chance of typical sugar value: ", value = 0.3, min_value=0.0, max_value=1.0)
    ns = st.number_input("Enter the chance of no sugar value: ", value = 0.6, min_value=0.0, max_value=1.0)

    if(st.button('What Should I Do')):
        if hs+ts+ns != 1:
            st.error("Invalid likelihood of sugar value (Should add up to 1)")
        else:
            e, a_s, a_ns = e_value(cb, hs, ts, ns)
            st.text("E-Value is {}.".format(e))
            value = e - 960000
            if value > 0:
                st.text("You should buy clairvoyance if its cost smaller than its value {}.".format(value))

            st.text("If detecting storm, you should " + a_s + '!')
            st.text("If detecting no storm, you should " + a_ns + '!')

if __name__ == '__main__':
	MVP_ui()