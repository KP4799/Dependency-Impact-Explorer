from app.db.connection import get_driver

developers = [
    "Aman",
    "Shyam",
    "Mohan",
    "Ramesh",
    "Sneha",
    "Sophie",
    "Jiya",
    "Mukesh",
    "Diya",
    "Neha",
]

repositories = [
    "payments-api",
    "checkout-service",
    "customer-api",
    "notification-service",
    "analytics-worker",
    "inventory-api",
    "search-service",
    "auth-service",
    "reporting-api",
    "user-service",
]

packages = [
    "auth-lib",
    "jwt-lib",
    "crypto-lib",
    "payment-sdk",
    "email-sdk",
    "cache-lib",
    "logging-lib",
    "metrics-lib",
    "search-sdk",
    "storage-lib",
    "fastapi",
    "sqlalchemy",
    "redis-client",
    "http-client",
    "validation-lib",
    "scheduler-lib",
    "analytics-sdk",
    "reporting-lib",
    "notification-sdk",
    "orm-lib",
]

technologies = [
    "Python",
    "FastAPI",
    "Redis",
    "PostgreSQL",
    "Docker",
]

vulnerabilities = [
    ("Weak encryption", "High"),
    ("Outdated dependency", "Medium"),
    ("Memory leak", "Medium"),
    ("Authentication bypass", "Critical"),
    ("SQL injection", "Critical"),
]

developer_repository_map = {
    "Aman": "payments-api",
    "Shyam": "checkout-service",
    "Mohan": "customer-api",
    "Ramesh": "notification-service",
    "Sneha": "analytics-worker",
    "Sophie": "inventory-api",
    "Jiya": "search-service",
    "Mukesh": "auth-service",
    "Diya": "reporting-api",
    "Neha": "user-service",
}

repo_dependencies = {
    "payments-api": ["auth-lib", "jwt-lib", "crypto-lib"],
    "checkout-service": ["payment-sdk", "crypto-lib"],
    "customer-api": ["auth-lib", "jwt-lib"],
    "notification-service": ["notification-sdk", "email-sdk"],
    "analytics-worker": ["analytics-sdk", "metrics-lib", "logging-lib"],
    "inventory-api": ["storage-lib", "cache-lib", "redis-client"],
    "search-service": ["search-sdk", "http-client"],
    "auth-service": ["auth-lib", "crypto-lib"],
    "reporting-api": ["reporting-lib", "orm-lib", "sqlalchemy"],
    "user-service": ["validation-lib", "fastapi"],
}

package_dependencies = [
    ("auth-lib", "jwt-lib"),
    ("jwt-lib", "crypto-lib"),
    ("payment-sdk", "crypto-lib"),
    ("notification-sdk", "email-sdk"),
    ("analytics-sdk", "metrics-lib"),
    ("metrics-lib", "logging-lib"),
    ("storage-lib", "cache-lib"),
    ("cache-lib", "redis-client"),
    ("search-sdk", "http-client"),
    ("reporting-lib", "orm-lib"),
    ("orm-lib", "sqlalchemy"),
    ("validation-lib", "fastapi"),
]

package_technologies = [
    ("auth-lib", "Python"),
    ("jwt-lib", "Python"),
    ("fastapi", "FastAPI"),
    ("redis-client", "Redis"),
    ("sqlalchemy", "PostgreSQL"),
    ("storage-lib", "Docker"),
]

package_vulnerabilities = [
    ("crypto-lib", "Weak encryption"),
    ("jwt-lib", "Authentication bypass"),
    ("sqlalchemy", "SQL injection"),
    ("cache-lib", "Memory leak"),
    ("payment-sdk", "Outdated dependency"),
]

driver = get_driver()

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

    for developer in developers:
        session.run(
            "CREATE (:Developer {name:$name})",
            name=developer,
        )

    for repo in repositories:
        session.run(
            """
            CREATE (:Repository {
                name:$name,
                language:'Python'
            })
            """,
            name=repo,
        )

    for package in packages:
        session.run(
            """
            CREATE (:Package {
                name:$name,
                version:'1.0.0'
            })
            """,
            name=package,
        )

    for technology in technologies:
        session.run(
            "CREATE (:Technology {name:$name})",
            name=technology,
        )

    for vulnerability, severity in vulnerabilities:
        session.run(
            """
            CREATE (:Vulnerability {
                name:$name,
                severity:$severity
            })
            """,
            name=vulnerability,
            severity=severity,
        )

    for developer, repository in developer_repository_map.items():
        session.run(
            """
            MATCH (d:Developer {name: $developer})
            MATCH (r:Repository {name: $repository})

            CREATE (d)-[:MAINTAINS]->(r)
            """,
            developer=developer,
            repository=repository,
        )

    for repo, packages_list in repo_dependencies.items():
        first_package = packages_list[0]

        session.run(
            """
            MATCH (r:Repository {name:$repo})
            MATCH (p:Package {name:$package})

            CREATE (r)-[:DEPENDS_ON]->(p)
            """,
            repo=repo,
            package=first_package,
        )

    for parent, child in package_dependencies:
        session.run(
            """
            MATCH (p1:Package {name:$parent})
            MATCH (p2:Package {name:$child})

            CREATE (p1)-[:DEPENDS_ON]->(p2)
            """,
            parent=parent,
            child=child,
        )

    for package, technology in package_technologies:
        session.run(
            """
            MATCH (p:Package {name:$package})
            MATCH (t:Technology {name:$technology})

            CREATE (p)-[:USES]->(t)
            """,
            package=package,
            technology=technology,
        )

    for package, vulnerability in package_vulnerabilities:
        session.run(
            """
            MATCH (p:Package {name:$package})
            MATCH (v:Vulnerability {name:$vulnerability})

            CREATE (p)-[:HAS_VULNERABILITY]->(v)
            """,
            package=package,
            vulnerability=vulnerability,
        )

print("Database seeded successfully!")
driver.close()