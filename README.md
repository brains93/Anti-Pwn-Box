# Hacking_demokit
Demonstation kit to show off real world attacks 


#

## Hardware

- Watchguard XTM 3 series Firewall (any firewall will work)
- D-link DGS-1100-05v2 Managed switch (any managed switch with port security and Port mirroring)
- Raspberry pi (client machine/end user)
- Zima board (servers)
  - 2.5inch Hard drive 
  - 2 x usb drives (one will always be plugged into the Zima so low form factor is good)
- 60w LED driver powersupply
- 12-5v converter
- enclosure



#

## Setup

install virtulisation software of choice on the zima board. NOTE: it uses realtec NICs so Esxi will need those drivers added to the ISO. 
I used Proxmox for my setup. 

the standard install found [Here](https://www.proxmox.com/en/proxmox-ve/get-started) works fine out of the box, burn the ISO onto one of the USB sticks using etcher. You will be installing on the other USB so insure both are plugged into the board (you may need a usb hub for this to have a keyboard and mouse plugged in at the same time)

#


# VM setup 

Install as many or as little VMS on the 'server' as you like my setup I have one web server and one Snort IDS setup. to get the ISOs into proxmox 





```
auto vmbr0
iface vmbr0 inet static
        address 192.168.3.102/24
        gateway 192.168.3.1
        bridge-ports enp2s0
        bridge-stp off
        bridge-fd 0

auto vmbr1
iface vmbr1 inet static
        address 192.168.3.105/24
        bridge-ports enp3s0
        bridge-stp off
        bridge-fd 0
        bridge_ageing 0

```

