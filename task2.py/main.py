import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users(url: str, timeout: int = 10) -> list[dict]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def find_users_by_city(users: list[dict], city_name: str) -> list[dict]:
    normalized_city = city_name.strip().lower()
    return [
        user for user in users
        if user.get("address", {}).get("city", "").strip().lower() == normalized_city
    ]


def print_users(users: list[dict]) -> None:
    if not users:
        print("No users found in that city.")
        return

    print("\nMatching Users:\n")
    for user in users:
        print(f"Name     : {user.get('name', 'N/A')}")
        print(f"Username : {user.get('username', 'N/A')}")
        print(f"Email    : {user.get('email', 'N/A')}")
        print(f"City     : {user.get('address', {}).get('city', 'N/A')}")
        print("-" * 40)


def main() -> None:
    try:
        users = fetch_users(API_URL)
        search_city = input("Enter city name to search: ").strip()
        matching_users = find_users_by_city(users, search_city)
        print_users(matching_users)

    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
    except requests.exceptions.ConnectionError:
        print("Connection Error: Unable to connect to the API.")
    except requests.exceptions.Timeout:
        print("Request Timed Out.")
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
    except ValueError:
        print("Error: Invalid JSON response.")


if __name__ == "__main__":
    main()
