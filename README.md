
Explain why you chose star schema over snowflake.
I chose the Star Schema because it is easy to understand and faster to use. The questions, most, are answered by joining the main Fact table to the dimension tables, compared to the Snowflake Schema that needs more joins, which make it slower.
In this case, it is done by joining the Sales table to the dimension tables.
![Star Schema Diagram](Data_Warehousing/schema/sales.drawio.png)
