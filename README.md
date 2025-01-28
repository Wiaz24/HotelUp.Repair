# HotelUp - Repair service
![dockerhub_badge](https://github.com/Wiaz24/HotelUp.Repair/actions/workflows/dockerhub.yml/badge.svg)

This service should expose endpoints on port `5001` starting with:
```http
/api/repair/
```

## Healthchecks
Health status of the service should be available at:
```http
/api/repair/health
```
and should return 200 OK if the service is running, otherwise 503 Service Unavailable.

## Message broker
This service uses `Pika` library to communicate with the message broker.

### AMQP Exchanges
This service creates the following exchanges:
- `HotelUp.Repair:DamageReportedEvent` - to notify about damage in a room while repair task. Published messages have
    payload structure that contains the following section:
    ```json
    {
        "message": {
            "taskId": "fc20b2b3-77c1-4cbc-bce1-1d854ebdc224",
            "reservationId": "00ce21d3-1b14-4d95-9a68-aa3a883e6e09",
            "repairType": "damage",
            "cost": 0.0
        }
    }
    ```