import paramiko
import json
import re
from .command import commandmikro,regexmikro ,main_remote
import mongod

class mikro:
    def __init__(self):
        self.mongo=mongod.mikro_mongo()
        self.remote=main_remote()

    def cm_mikro(self,command,host, port, username, password):
        try:
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port, username, password,allow_agent=False,look_for_keys=False)
                for commands in command:
                    print(commands,end='\r')
                    stdin, stdout, stderr = ssh.exec_command(commands)
                    lines = stdout.read()
                    out=lines.decode()
                    return out
        except:
            False

    def main_vpn_access(self,type,ip_pub,port,username,password,start_tun_range,end_tun_range):
        try:
            dict = {
                "ovpn": self.remote.main_remote_command,
                "sstp": self.remote.main_remote_command,
                "l2tp": self.remote.main_remote_command,
                "pptp": self.remote.main_remote_command,
            }
            remote_vpn = dict.get(type)(ip_pub,start_tun_range,end_tun_range,self.remote.ovpn_mikro())
            self.cm_mikro(remote_vpn,ip_pub, port, username, password)
        except:
            False

    def local_site_sstp(self,ip_pub,port,username,password,country_usr,password_vpn,start_tun_range,end_tun_range):
        try:                                            
            commands = self.remote.main_remote_command(ip_pub,start_tun_range,end_tun_range,self.remote.sstp_mikro())
            self.cm_mikro(commands,ip_pub, port, username, password)
            set_int=f'interface sstp-client add connect-to={ip_pub} user={country_usr} password={password_vpn} comment={country_usr} disabled=no'
            self.cm_mikro(set_int,ip_pub, port, username, password)
            self.mongo.insert_loc(country_usr,start_tun_range,ip_pub)
        except:
            False

    def setgw(self,loc):
        try:
            vpn_loc=self.mongo.select_loc_ip(loc)
            commands =[commandmikro.set_route.value+vpn_loc]
            return commands
        except:
            False
                
    def dhcp_details_reg(self,host, port, username, password):
        command=[commandmikro.dhcp_print.value]
        income_details=self.cm_mikro(command,host, port, username, password)
        details=re.findall(regexmikro.details.value,income_details)
        list=[]
        for spec in details:
            ipadd=re.findall(regexmikro.ipadd_1.value,spec)[0]
            ipadd=re.findall(regexmikro.ipadd_2.value,ipadd)[0]
            mac=re.findall(regexmikro.mac_add.value,spec)[0]
            try:
                hostname=re.findall(regexmikro.hostname.value,spec)[0]
            except:
                hostname=None
            appjson={
                'ipaddress':ipadd,
                'mac-address':mac,
                'hostname':hostname 
                }
            list.append(appjson)
        return list

    def socks(self,sock_port,max_conn,passwd,ip_pub,port,username,password):
        try:
            commands = self.remote.socks_mikro(sock_port,max_conn,passwd)
            self.cm_mikro(commands,ip_pub, port, username, password)
            return True
        except:
            False

    def add_ppp_secret(self,ip_pub,port,name,username,password,passwd,service,profile):
        try:
            command= self.remote.add_secret(name,passwd,service,profile)
            self.cm_mikro(command,ip_pub, port, username, password)
        except:
            False


