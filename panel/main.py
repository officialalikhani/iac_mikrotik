import streamlit as st
import public_ip as ip
from mongod import mikro_mongo
import mikro_ops

class ui_panel:
    def __init__(self):
        self.obj=mikro_ops.mikro()
        self.mongo=mikro_mongo()
        self.host='ip address'
        self.port='port'
        self.username='username'
        self.password='passwrd'

    def dhcp_details(self):
        dets = self.obj.dhcp_details_reg(self.host, self.port, self.username, self.password)
        device=0
        for det in dets:
            device +=1
            ipadd=det['ipaddress']
            mac=det['mac-address']
            hostname=det['hostname']
            st.text_input(f'Device = {device}', f'Hostname= {hostname}     IP-address= {ipadd}     Mac-address= {mac}')
            
    def deactive_loc_router(self,loc):
        self.mongo.deactive_loc(loc)

    def active_loc_router(self,loc):
        self.mongo.active_loc(loc)

    def configure_new_site(self):
        with st.form(key='my_form'):
                cl1, cl2 = st.columns(2)
                with cl1:
                    host = st.text_input(label='Enter ip address : ')
                    port = st.text_input(label='Enter port : ')
                    username = st.text_input(label='Enter username : ')
                    password = st.text_input(label='Enter password : ')
                    
                with cl2:
                    country_usr = st.text_input(label='Enter country : ')
                    password_vpn = st.text_input(label='Enter password of your vpn : ')
                    local_ip = st.text_input(label='Enter local ip : ')
                    remote_ip = st.text_input(label='Enter remote ip : ')
                submit_button = st.form_submit_button(label='Submit')
                if submit_button == True: 
                    self.obj.local_site_sstp(host,port,username,password,country_usr,password_vpn,local_ip,remote_ip)

    def configure_remote_access(self):
        with st.form(key='my_form'):
                    cl1, cl2 = st.columns(2)
                    with cl1:
                        ip_pub = st.text_input(label='Enter ip address server : ')
                        port = st.text_input(label='Enter port server: ') 
                        username = st.text_input(label='Enter username : ')
                        password = st.text_input(label='Enter password : ') 
                    with cl2:
                        type_ = st.text_input('Protocol : ','ovpn/sstp/l2tp/pptp')
                        start_tun_range = st.text_input(label='Enter start ip range : ')
                        end_tun_range = st.text_input(label='Enter end ip range : ')
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button == True: 
                        self.obj.main_vpn_access(self,type_,ip_pub,port,username,password,start_tun_range,end_tun_range)

    def active_deactive(self,loc_act,loc_deact):
        col1,col2=st.columns(2)
        with col1:
            'Deactived Loaction'
            loc = st.radio("Select a Location: ", loc_act)
            if st.button('Deactived'):
                self.deactive_loc_router(loc)
                st.write(f'{loc} Deactived!')
        with col2:
            'Active Loaction'
            loc = st.radio("Select a Location: ", loc_deact)
            if st.button('Active'):
                self.active_loc_router(loc)
                st.write(f'{loc} Actived!')

    def socks_ui(self):
        with st.form(key='my_form'):
                    cl1, cl2 = st.columns(2)
                    with cl1:
                        ip_pub = st.text_input(label='Enter ip address : ')
                        port = st.text_input(label='Enter port : ')
                        username = st.text_input(label='Enter username : ')
                        password = st.text_input(label='Enter password : ')
                    with cl2:
                        sock_port = st.text_input(label='Enter socks5 port : ')
                        passwd = st.text_input(label='Enter password of your socks : ')
                        max_conn = st.text_input(label='Enter max connection : ')
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button == True: 
                        self.obj.socks(sock_port,max_conn,passwd,ip_pub,port,username,password)
    def add_ppp_sec(self):
        with st.form(key='my_form'):
                    cl1, cl2 = st.columns(2)
                    with cl1:
                        ip_pub = st.text_input(label='Enter ip address : ')
                        port = st.text_input(label='Enter port : ')
                        password = st.text_input(label='Enter password : ')
                        username = st.text_input(label='Enter username : ')
                    with cl2:
                        name = st.text_input(label='Enter name vpn : ')
                        passwd = st.text_input(label='Enter password vpn : ')
                        service = st.text_input(label='Enter service : ')
                        profile = st.text_input(label='Enter profile : ')
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button == True: 
                        self.obj.add_ppp_secret(ip_pub,port,name,username,password,passwd,service,profile)

    def mode_vpn(self,mode):
        loc_act=self.mongo.select_loc_active()
        loc_deact=self.mongo.select_loc_deactive()
        if mode == 'Connect local Network to exists VPN ':
            '------------------------------'
            status = st.radio("Select VPN location: ", loc_act)
            if st.button('Apply'):
                try:
                    self.obj.cm_mikro(self.obj.setgw(status),self.host, self.port, self.username, self.password)
                except Exception as e:
                    print(e)
                st.write('Connected') 
                st.text_input('Your current ip', ip.get())

        elif mode == 'Configure New Site/Site VPN Location':
            '------------------------------'
            self.configure_new_site()

        elif mode == 'Configure Remote Access VPN':
            '------------------------------'
            self.configure_remote_access()

        elif mode == 'Active/Deactive location':
            '------------------------------'
            self.active_deactive(loc_act,loc_deact)

        elif mode == 'Configure Socks5':
            self.socks_ui()

        elif mode == 'Add User VPN':
            self.add_ppp_sec()
