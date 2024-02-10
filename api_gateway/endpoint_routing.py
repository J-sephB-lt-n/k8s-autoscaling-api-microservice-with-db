"""Defines routings connecting client requests to internal services"""

import os

endpoint_routing: dict[str, str] = {
    "is_it_prime/v1": os.environ["IS_IT_PRIME__V1"],
    "postgresql/query/v1": "http://service-endpoints-postgresql-interface.default.svc.cluster.local:8080/query",
}
