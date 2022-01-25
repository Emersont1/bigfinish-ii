import big_finish

def main():
    print("Fetching products...")
    ps = big_finish.get_products()

    print("Processing products...")
    for p in ps:
        id, path = big_finish.process_product(p)
        with open(id, "w") as f:
            f.write(path)

if __name__ == "__main__":
    main()