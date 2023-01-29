import streamlit as st
import public_ip as ip
from PIL import Image
from mongod import mikro_mongo
import mikro_ops
from panel import ui_panel

panel=ui_panel()
obj=mikro_ops.mikro()
mongo=mikro_mongo()
image = Image.open('address-your-wallpaper.jpg')
st.image(image)

mode = st.radio("Select Mode : ", ('Connect local Network to exists VPN ',
                                    'Configure New Site/Site VPN Location',
                                    'Configure Remote Access VPN',
                                    'Active/Deactive location',
                                    'Configure Socks5',
                                    'Add User VPN'))
panel.mode_vpn(mode)
'------------------------------'
col1, col2, col3 ,col4,col5= st.columns(5)
if col3.button('Show Users'):
    panel.dhcp_details()
    
