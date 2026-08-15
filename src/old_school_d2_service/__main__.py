"""Command-line entry point for the initial UDP discovery service."""

from __future__ import annotations

import argparse
import os

from .migrations import apply_migrations
from .server import DiscoveryUDPServer
from .storage import PostgresEventStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Old-School-D2 UDP discovery service.")
    parser.add_argument("--host", default="127.0.0.1", help="IPv4 address to bind")
    parser.add_argument("--port", type=int, default=3074, help="UDP port to bind")
    parser.add_argument("--database-url", default=os.environ.get("OLD_SCHOOL_D2_DATABASE_URL"), help="PostgreSQL connection URL (or OLD_SCHOOL_D2_DATABASE_URL)")
    parser.add_argument("--label", default="manual-run", help="Sanitized experiment label")
    parser.add_argument("--migrate", action="store_true", help="Apply pending db/migrations SQL files and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.database_url:
        raise SystemExit("Set --database-url or OLD_SCHOOL_D2_DATABASE_URL.")
    if args.migrate:
        for filename in apply_migrations(args.database_url):
            print(f"applied {filename}")
        return
    store = PostgresEventStore(args.database_url)
    experiment_id = store.start_experiment(label=args.label)
    server = DiscoveryUDPServer((args.host, args.port), store, experiment_id)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
