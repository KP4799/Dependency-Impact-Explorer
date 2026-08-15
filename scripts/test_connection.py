from app.db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run(
        """
        RETURN "Connected successfully!" AS message
        """
    )

    print(result.single()["message"])

driver.close()