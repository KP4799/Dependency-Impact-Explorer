from app.db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run(
        """
        MATCH (n)
        RETURN labels(n)[0] AS label, count(*) AS count
        """
    )

    for row in result:
        print(f"{row['label']}: {row['count']}")

driver.close()