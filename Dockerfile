FROM odoo:14.0

COPY ./registration_form /mnt/extra-addons/registration_form

COPY ./config /etc/odoo/