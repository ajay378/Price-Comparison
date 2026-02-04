import json
import webbrowser

def show_cheapest_product(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # If file has a "cheapest" key (like your example)
        if "cheapest" in data:
            cheapest = data["cheapest"]
        # Otherwise, calculate it from results
        elif "results" in data and data["results"]:
            cheapest = min(data["results"], key=lambda x: x.get("price", float("inf")))
        else:
            print("❌ No valid data found in JSON.")
            return

        title = cheapest.get("title", "Unknown Product")
        store = cheapest.get("store", "Unknown Store")
        price = cheapest.get("price", "N/A")

        print("\n✅ Cheapest Product Found:")
        print(f"📦 Product: {title}")
        print(f"🏬 Store: {store}")
        print(f"💰 Price: ₹{price}\n")

        # If there’s a link, open it (optional)
        if "link" in cheapest:
            open_it = input("🌐 Open the store page in browser? (y/n): ").strip().lower()
            if open_it == "y":
                webbrowser.open(cheapest["link"])

    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format in '{filename}'.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    show_cheapest_product("products.json")
