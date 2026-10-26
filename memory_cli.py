import argparse
from memory_store import MemoryStore, VALID_TYPES

def main():
    parser = argparse.ArgumentParser(description="Manage project context memory")
    parser.add_argument("--db", default="data/memory.db")
    subs = parser.add_subparsers(dest="command", required=True)
    ls = subs.add_parser("list")
    ls.add_argument("--project")
    ls.add_argument("--type", choices=sorted(VALID_TYPES))
    ls.add_argument("--limit", type=int, default=100)
    search = subs.add_parser("search")
    search.add_argument("query")
    search.add_argument("--project")
    search.add_argument("--type", choices=sorted(VALID_TYPES))
    search.add_argument("--limit", type=int, default=10)
    add = subs.add_parser("add")
    add.add_argument("--project", required=True)
    add.add_argument("--type", choices=sorted(VALID_TYPES), required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--content", required=True)
    add.add_argument("--tags", default="")
    add.add_argument("--source", default="")
    export = subs.add_parser("export")
    export.add_argument("--project", required=True)
    export.add_argument("--output", default="PROJECT_MEMORY.md")
    args = parser.parse_args()
    store = MemoryStore(args.db)
    if args.command == "add":
        print(f"Saved memory #{store.add(args.project,args.type,args.title,args.content,args.tags,args.source)}")
    elif args.command == "list":
        for x in store.list(args.project, args.type, limit=args.limit):
            print(f"#{x['id']} [{x['kind']}] {x['project']} — {x['title']} ({x['status']})\n  {x['content']}")
    elif args.command == "search":
        for x in store.search(args.query, args.project, args.type, args.limit):
            print(f"#{x['id']} [{x['kind']}] score={x['score']} — {x['title']}\n  {x['content']}")
    elif args.command == "export":
        store.export_markdown(args.project, args.output)
        print(f"Exported to {args.output}")

if __name__ == "__main__":
    main()
