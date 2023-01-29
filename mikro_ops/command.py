from enum import Enum

class commandmikro(Enum):
    set_route = "ip route set numbers=0 gateway="
    dhcp_print= "ip dhcp-server lease print detail"

class regexmikro(Enum):
    details='D address=*.+\n*.+\n*.+\n*.+\n*.+\n*.+'
    ipadd_1='active-address=*.+'
    ipadd_2='active-address=(\d.+) active-mac-address'
    mac_add='active-mac-address=(.+) '
    hostname='host-name=(.+) '

class main_remote:
    def __init__(self):
        pass
    def main_remote_command(self,ip_pub,start_tun_range,end_tun_range,command):
        commands=[
            f"certificate add name=ca common-name={ip_pub} days-valid=3650 key-size=2048 key-usage=crl-sign,key-cert-sign",
            f"certificate add name=server common-name={ip_pub} days-valid=3650 key-size=2048 key-usage=digital-signature,key-encipherment,tls-server",
            "certificate sign ca name=ca-certificate",
            "certificate sign server name=server-certificate ca=ca-certificate",
            f"ip firewall nat add chain=srcnat src-address={start_tun_range}-{end_tun_range} out-interface=ether1 action=masquerade",
            "certificate export-certificate ca-certificate export-passphrase=””",
            f"ip pool add comment=vpn-pool ranges={start_tun_range}-{end_tun_range} name=vpn-pool",
            f"ppp profile add name=VPN local-address={start_tun_range} remote-address=vpn-pool use-encryption=yes dns-server=8.8.8.8",

            command,
        ]
        return commands

    def ovpn_mikro(self):
        commands=["interface ovpn-server server set enabled=yes default-profile=VPN port=1717 mode=ip netmask=24 certificate=server require-client-certificate=yes auth=sha1,md5 cipher=blowfish128,aes128",]
        return commands

    def sstp_mikro(self):
        commands=["interface sstp-server server set enabled=yes default-profile=VPN port=443 certificate=server  verify-client-certificate=yes authentication=mschap1,mschap2,chap,pap force-aes=yes pfs=yes",]
        return commands

    def pptp_mikro(self):
        commands=["interface pptp-server server set enabled=yes default-profile=VPN authentication=mschap1,mschap2",]
        return commands

    def l2tp_mikro(self):
        commands=[f"interface l2tp-server server set enabled=yes default-profile=VPN authentication=mschap1,mschap2,chap,pap use-ipsec=yes ipsec-secret=P@ssw0rd caller-id-type=ip-address one-session-per-host=yes",]
        return commands

    def socks_mikro(self,sock_port,max_conn,passwd):
        commands=[
            f"ip socks set enabled=yes port={sock_port} max-connections={max_conn} connection-idle-timeout=00:02:00 version=5 auth-method=password",
            "ip socks access add src-address=0.0.0.0/0 dst-address=0.0.0.0/0 action=allow",
            f"ip socks users add name=user1 password={passwd}",
        ]
        return commands
        
    def reverse_route(self,lan_range,remote_ip):
        commands=[f"ip route add dst-address={lan_range} gateway={remote_ip}",]
        return commands

    def add_secret(self,name,passwd,service,profile):
        command = [f"ppp secret add name={name} password={passwd} service={service} profile={profile}",]
        return command
