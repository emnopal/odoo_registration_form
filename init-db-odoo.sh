#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username odoo --dbname odoo <<-EOSQL
    CREATE ROLE odoo WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'rahasia'
EOSQL