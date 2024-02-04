"""Defines routings connecting client requests to internal services"""

endpoint_routing: dict[str, str] = {
    "postgresql/query/v1": "http://service-endpoints-postgresql-interface.default.svc.cluster.local:8081/query",
    "is_it_prime/v1": "TODO",
}
