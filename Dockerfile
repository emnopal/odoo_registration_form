FROM odoo:14.0

USER root

RUN apt-get update
RUN apt-get install -y nano git build-essential libssl-dev libffi-dev cargo
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir apispec>=4.0.0 cerberus extendable graphene \
    graphql_server jsondiff marshmallow marshmallow-objects>=2.0.0 parse-accept-language \
    pyquerystring promise pyjwt pyjwt[cryptography] cryptography email_validator lxml \
    pysaml2 python-jose python-ldap zxcvbn