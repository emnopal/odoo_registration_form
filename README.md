# Odoo Registration Form
This is simple odoo module for Registration Form

# How to run?

## Run docker compose
`$ docker-compose up -d`

## Start PostgreSQL
`$ docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=odoo --name db postgres`

## Run odoo
`$ docker run -v /path/to/config:/etc/odoo -p 8069:8069 --name odoo --link db:db -t odoo`

## Mount custom addons or module
`$ docker run -v /path/to/addons:/mnt/extra-addons -p 8069:8069 --name odoo --link db:db -t odoo`
