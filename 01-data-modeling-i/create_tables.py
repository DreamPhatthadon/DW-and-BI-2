from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_repositories = "DROP TABLE IF EXISTS repositories"
table_drop_actors = "DROP TABLE IF EXISTS actors"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        actor_id int,
        actor_login text,
        PRIMARY KEY(actor_id)
    )
"""
table_create_repositories = """
    CREATE TABLE IF NOT EXISTS repositories (
        repo_id int,
        repo_name text,
        actor_id int,
        PRIMARY KEY(repo_id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(actor_id)
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        event_id text,
        event_type text,
        event_created_at text,
        repo_id int,
        PRIMARY KEY(event_id),
        CONSTRAINT fk_repository FOREIGN KEY(repo_id) REFERENCES repositories(repo_id)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repositories,
    table_create_events,
]
drop_table_queries = [
    table_drop_events,
    table_drop_repositories,
    table_drop_actors,
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
