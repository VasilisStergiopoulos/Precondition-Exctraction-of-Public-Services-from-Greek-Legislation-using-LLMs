import argparse
from .pipeline import PreconditionsPipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3, help="How many services to process")
    args = parser.parse_args()

    pipeline = PreconditionsPipeline()
    pipeline.run(limit=args.limit)


if __name__ == "__main__":
    main()