# NetCobra
a Network Swiss army knife written in Python

###Summary
NetCobra is a tool **similar** to netcat but smaller and more portable.
it can create and recieve connections, download files and upload them to connected hosts and it can spawn bind and reverse shells.  
    
###How to use  
#####values in square brackets [] are optional.  
  
**view help message:**  
`nc.py`  

**listener mode:**    
`nc.py -l -a [127.0.0.1] -p 1337`  
Note: When no value is provided for the address argument in listen mode the default address is used which is 0.0.0.0 (All interfaces)  

**Client mode:**  
`nc.py -c -a 127.0.0.1 -p 1337`    

**Creating a bind shell:**  
`nc.py -l -a [127.0.0.1] -p 1337 -s`  
  
**Creating a reverse shell:**  
`nc.py -c -a 127.0.0.1 -p 1337 -s`  
  
**Connect and upload a file:**  
`nc.py -c -a 127.0.0.1 -p 1337 -u file-path-here`  
  
**listen and download a file:**  
`nc.py -l -a [127.0.0.1] -p 1337 -d  
will download to the same file nc.py exists in
  
###This tool was made for educational purposes only, the author is **NOT** reposonsible for anything you do with this tool
