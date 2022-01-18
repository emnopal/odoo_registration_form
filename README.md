# Odoo Registration Form
This is simple odoo module for Registration Form

# How to run?

## Run docker compose <br>
1. Run DB <br>
`$ docker-compose up -d postgres`
2. Create Role<br>
`$ docker exec -ti -u root registration_form_db_1 psql -U postgres`<br>
`CREATE ROLE odoo WITH CREATEDB LOGIN ENCRYPTED PASSWORD '1234';`<br>
`\q` to quit<br>
3. Run Odoo<br>
`$ docker-compose run --rm odoo`

## Start PostgreSQL
`$ docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=odoo --name db postgres`

## Run odoo
`$ docker run -v /path/to/config:/etc/odoo -p 8069:8069 --name odoo --link db:db -t odoo`

## Mount custom addons or module
`$ docker run -v /path/to/addons:/mnt/extra-addons -p 8069:8069 --name odoo --link db:db -t odoo`
