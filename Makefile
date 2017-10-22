rego:
	mkdir /usr/local/imager/automated-checkout
	mkdir /usr/local/imager/automated-checkout/checkouts
	cp -r modules /usr/local/imager/automated-checkout/
	cp -r configs /usr/local/imager/automated-checkout/
	cp local_checkout.py /usr/local/imager/automated-checkout/
	cp README.md /usr/local/imager/automated-checkout/
	chmod +x /usr/local/imager/automated-checkout/local_checkout.py
	ln -sf /usr/local/imager/automated-checkout/configs/regocheckout_config.cfg /usr/local/imager/automated-checkout/checkout_config.cfg
	echo 'imager ALL=(ALL) NOPASSWD: /usr/local/imager/automated-checkout/local_checkout.py' | sudo EDITOR='tee -a' visudo
	@echo ***CONFIRM CHECKOUT_CONFIG IS CONFIGURED PROPERLY FOR THIS SYSTEM***

themis:
	mkdir /usr/local/imager/automated-checkout
	mkdir /usr/local/imager/automated-checkout/checkouts
	cp -r modules /usr/local/imager/automated-checkout/
	cp -r configs /usr/local/imager/automated-checkout/
	cp local_checkout.py /usr/local/imager/automated-checkout/
	cp README.md /usr/local/imager/automated-checkout/
	chmod +x /usr/local/imager/automated-checkout/local_checkout.py
	ln -sf /usr/local/imager/automated-checkout/configs/themischeckout_config.cfg /usr/local/imager/automated-checkout/checkout_config.cfg
	echo 'imager ALL=(ALL) NOPASSWD: /usr/local/imager/automated-checkout/local_checkout.py' | sudo EDITOR='tee -a' visudo
	@echo ***CONFIRM CHECKOUT_CONFIG IS CONFIGURED PROPERLY FOR THIS SYSTEM***