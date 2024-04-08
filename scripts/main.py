import sys

if len(sys.argv) < 3:
    print("Please provide a valid option (fetch, migrate) and a file path.")
    sys.exit(1)

option = sys.argv[1].lower()
path = sys.argv[2]

if option == "fetch":
    count = -1
    if len(sys.argv) >= 4:
        count = int(sys.argv[3])
    import fetch
    fetch.fetch(path, count)
elif option == "migrate":
    import migrate
    migrate.migrate(path)
