import csv
import json

TEST_DATA_DIR = "tests/data"

# Sample data for User model
users = [
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "hashed_password": "hashed_password_1",
        "is_active": True,
    },
    {
        "id": 2,
        "username": "jane_doe",
        "email": "jane@example.com",
        "hashed_password": "hashed_password_2",
        "is_active": True,
    },
    {
        "id": 3,
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "hashed_password_3",
        "is_active": True,
    },
]

# Sample data for Listing model
listings = [
    {
        "id": 1,
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "beds": 2,
        "bedrooms": 1,
        "mean_rating": 4.5,
        "count_ratings": 10,
        "nightly_price": 100.0,
        "owner_id": 1,
    },
    {
        "id": 2,
        "name": "Modern Apartment",
        "description": "A modern apartment in the city center.",
        "beds": 1,
        "bedrooms": 1,
        "mean_rating": 4.8,
        "count_ratings": 20,
        "nightly_price": 150.0,
        "owner_id": 2,
    },
    {
        "id": 3,
        "name": "Beach House",
        "description": "A beautiful beach house with ocean views.",
        "beds": 3,
        "bedrooms": 2,
        "mean_rating": 4.7,
        "count_ratings": 15,
        "nightly_price": 200.0,
        "owner_id": 3,
    },
]


def write_dict_to_csv(file_path: str, columns: list[str], data: list[dict]):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)


def write_dict_to_json(file_path: str, data: dict):
    with open(file_path, mode="w") as file:
        json.dump(data, file, indent=4)


def write_csv_to_json(csv_file_path: str, json_file_path: str):
    with open(csv_file_path) as file:
        reader = csv.DictReader(file)
        data = list(reader)

    with open(json_file_path, mode="w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    # Write sample data to CSV files
    write_dict_to_csv(f"{TEST_DATA_DIR}/users.csv", users[0].keys(), users)
    write_dict_to_csv(f"{TEST_DATA_DIR}/listings.csv", listings[0].keys(), listings)

    # Write sample data to JSON files
    write_dict_to_json(f"{TEST_DATA_DIR}/users.json", users)
    write_dict_to_json(f"{TEST_DATA_DIR}/listings.json", listings)
