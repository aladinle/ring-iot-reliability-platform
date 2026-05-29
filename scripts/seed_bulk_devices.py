import argparse

from backend.testing.device_fleet_generator import seed_fleet


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed generated IoT test devices into the backend.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()

    seed_fleet(args.base_url, args.count)
    print(f"Seeded {args.count} generated test devices into {args.base_url}")


if __name__ == "__main__":
    main()

