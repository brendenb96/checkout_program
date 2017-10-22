# Instrument Automated Checkout
## Overview
Program reads from checkout configuration file to decide which test to run for the system. Use "-h" option for all options. Most common command for diagnosing a system is as follows:
    ```
    ./local_checkout -av
    ```
    
For a full checkout including test image:
    ```
    ./local_checkout -iaV
    ```
    
Individual modules to be tested on the system can be chosen within the options.
Program after installation is located in /usr/local/imager/automated-checkout
Most recent checkout will be located at /usr/local/imager/automated-checkout/RECENT_CHECKOUT.txt
All system checkouts will be located in /usr/local/iamger/automated-checkout/checkouts

## Installation
```
[login as imager]  
cd ~  
wget http://aurora.phys.ucalgary.ca/public/automated-checkouts.zip  
unzip automated-checkouts.zip  
cd automated-checkouts  
su -enter root password-  
make (themis or rego)
```
