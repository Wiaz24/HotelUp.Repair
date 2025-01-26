# HotelUp - Repair service
![dockerhub_badge](https://github.com/Wiaz24/HotelUp.Repair/actions/workflows/dockerhub.yml/badge.svg)

This service should expose endpoints on port `5001` starting with:
```http
/api/repair/
```

```http
/api/repair/repair_list
```

Nasłuchiwanie na event od janitora

## Healthchecks
Health status of the service should be available at:
```http
/api/repair/_health
```
and should return 200 OK if the service is running, otherwise 503 Service Unavailable.
