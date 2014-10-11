simple-dns
===========
Just a simple DNS Server

## Usage
hosts 文件里指定要劫持的域名，格式为：  

    #IP            Domain
    127.0.0.1     www.alipay.com

非劫持域名会向上级 DNS Server 递归查询，返回正确的 IP 地址。  

## Sample

Attacker(127.0.0.1):

    sudo python dns.py


Target(127.0.0.1):

    ➜  ~ nslookup 
    > server 127.0.0.1
    Default server: 127.0.0.1
    Address: 127.0.0.1#53
    > test.website
    Server:		127.0.0.1
    Address:	127.0.0.1#53
       
    Non-authoritative answer:
    Name:	test.website
    Address: 1.1.1.1
    > 


