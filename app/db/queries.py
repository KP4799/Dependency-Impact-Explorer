from app.db.connection import get_driver

driver = get_driver()

def get_all_packages():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Package)
            RETURN p.name AS package
            ORDER BY p.name
            """
        )
        return [record["package"] for record in result]

def get_node_counts():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (n)

            RETURN labels(n)[0] AS label,
                   count(n) AS count
            """
        )

        return {
            record["label"]: record["count"]
            for record in result
        }

def get_relationship_count():
    with driver.session() as session:
        result = session.run(
            """
            MATCH ()-[r]->()

            RETURN count(r) AS count
            """
        )
        return result.single()["count"]

def get_repository_impacts(package_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH path=
                (r:Repository)-[:DEPENDS_ON*1..5]->
                (p:Package {name:$package})

            OPTIONAL MATCH
                (d:Developer)-[:MAINTAINS]->
                (r)

            RETURN
                r.name AS repository,
                collect(DISTINCT d.name) AS developers,
                path

            ORDER BY repository
            """,
            package=package_name,
        )

        impacts = []

        for record in result:
            impacts.append(
                {
                    "repository": record["repository"],
                    "developers": record["developers"],
                    "path": [node["name"] for node in record["path"].nodes],
                }
            )
        return impacts

def get_repositories_by_vulnerability(vulnerability_name):
    with driver.session() as session:
            result = session.run(
                """
                MATCH
                    (r:Repository)-[:DEPENDS_ON*1..5]->
                    (p:Package)-[:HAS_VULNERABILITY]->
                    (v:Vulnerability {name: $vulnerability})

                RETURN DISTINCT
                    r.name AS repository
                
                ORDER BY repository
                """,
                vulnerability=vulnerability_name
            )

            return [record["repository"] for record in result]
