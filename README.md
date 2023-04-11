# APB  (WIP)
Demonstation kit to show off what attacks look like in the real world.
Showing how defence in depth can protect even the most vulnrable systems.

The end goal of this kit is to have a CTF style system with very vulnrable systems, protected with standard security tools and practices.

<details>
  <summary>Network Diagram</summary>
  
 ![hacking network diagram ](https://user-images.githubusercontent.com/60553334/216385244-c5af2751-6c19-4675-a241-33885f7d8316.jpg)
  
</details>

![APB](https://user-images.githubusercontent.com/60553334/231083442-56c5b7c9-a6a0-4197-9d1b-23550c63f5dc.jpeg)




## Hardware

- Watchguard XTM 3 series Firewall (any firewall will work)
- D-link DGS-1100-05v2 Managed switch (any managed switch with port security and Port mirroring)
- Raspberry pi (client machine/end user)
- Raspberry Pi (generic misc server, currently running LED code)
- Zima board (servers)
  - 2.5inch Hard drive 
  - 2 x usb drives (one will always be plugged into the Zima so low form factor is good)
- 60w LED driver powersupply
- 12-5v converter
- 3d printed case for Powersupply
- enclosure/ server rack

<details>
 <summary> custom PSU images </summary>
 I wanted to keep the PSU as small as I could so I chose a 60w LED driver with a 12-5v converter for the Raspberry Pi power
</details>

#

## Setup

install virtulisation software of choice on the zima board. NOTE: it uses realtec NICs so Esxi will need those drivers added to the ISO. 
I used Proxmox for my setup. 

the standard install found [Here](https://www.proxmox.com/en/proxmox-ve/get-started) works fine out of the box, burn the ISO onto one of the USB sticks using etcher. You will be installing on the other USB so insure both are plugged into the board (you may need a usb hub for this to have a keyboard and mouse plugged in at the same time)

#


## VM setup 

Install as many or as little VMS on the 'server' as you like my setup I have one web server and one Snort IDS setup. to get the ISOs into proxmox 


![image](https://user-images.githubusercontent.com/60553334/211364950-ecf786ad-eb07-4bfa-be70-400814f63ade.png)

![image](https://user-images.githubusercontent.com/60553334/211365097-6cee5574-2416-4eb6-bfb7-d85b64563941.png)

![image](https://user-images.githubusercontent.com/60553334/211365259-f5e40b50-8a12-42f4-9d57-468dab35b5e8.png)




#

## Snort setup 



The linux bridge that is being mirrored needs to have bridge aging set to 0 in order for it to replicate port mirror traffic to the Snort VM
edit the /etc/network/interfaces file so it looks like vmbr1 
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


## Current work 

I have now got 3 more zima boards, one of the lowest spec and 2 of the middle spec (lower RAM is the main change)
the lowest spec is now running PFsense and will replace the watchguard, I am not super happy about this as I want the firewall to look like a firewall but any old kit I can get my hands on for cheap/free is to old to be a good referance of whaat modern firewalls can do. 

The other two Zimas will be added to the Proxmox nodes for additional virtualisation. 

I will need to modify the PSU with aditional 12v output to account for the extra Zimaboard

Once the hardware is in I will then work on getting OWASP juice shop installed and put behind a WAF (I am not experianced with WAFs so I am not sure if this could protect Juice shop but we are going to find out)

I also need to get Elastic configured now I have the Hardware to support it (still not 100% sure this should be in the V1 of this will decided later)

I also need to tie in some form of blocking for the Snort detections. I may just move snort to the PFsense firewall for blocking and leave the detection snort in place to feed into Elastic 

