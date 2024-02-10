"""Defines routings connecting client requests to internal services"""

endpoint_routing: dict[str, str] = {
    "is_it_prime/v1": "http://ksvc-endpoint-is-it-prime.default.svc.cluster.local",
    "postgresql/query/v1": "http://service-endpoints-postgresql-interface.default.svc.cluster.local:8080/query",
}
