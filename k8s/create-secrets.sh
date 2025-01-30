#!/bin/bash

NAMESPACE=$1
if [ -z "$1" ]; then
    NAMESPACE="hotelup"
fi
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

cat << EOF | kubectl apply -f -
    apiVersion: v1
    kind: Secret
    metadata:
        name: repair-secret
        namespace: ${NAMESPACE}
    type: Opaque
    data:
        OAUTH2_CLIENT_ID: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/Oidc/ClientId --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
        OAUTH2_CLIENT_SECRET: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/Oidc/ClientSecret --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
        OAUTH2_METADATA_URL: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/Oidc/MetadataAddress --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
        POSTGRES_DB: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/Postgres/ConnectionString --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
        RABBITMQ_USER: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/MessageBroker/RabbitMQ/UserName --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
        RABBITMQ_PASSWORD: $(echo -n "`aws ssm get-parameter --name /HotelUp.Repair/Production/MessageBroker/RabbitMQ/Password --with-decrypt --output text --profile wiaz --region us-east-1 --query Parameter.Value`" | base64 -w0)
EOF