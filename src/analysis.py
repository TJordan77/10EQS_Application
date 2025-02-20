import sys
import csv
import os
import requests
from dotenv import load_dotenv
import utils
print(dir(utils))

from utils import clean_price, clean_stock, clean_category, clean_date

def main():
    # Load environment variables
    load_dotenv()

    # Check for command-line argument (CSV file path)
    if len(sys.argv) < 2:
        print("Usage: python src/analysis.py <path_to_csv>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]

    # Read the CSV data
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data_rows = list(reader)
    except FileNotFoundError:
        print(f"Error: File not found - {csv_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # Clean and transform data
    cleaned_data = []
    data_quality_issues = []

    for row in data_rows:
        original_price = row['our_price']
        original_stock = row['current_stock']
        original_category = row['category']
        original_date = row['restock_date']

        price = clean_price(original_price)
        if price is None and original_price not in (None, ''):
            data_quality_issues.append(f"Invalid price: '{original_price}'")

        stock = clean_stock(original_stock)
        if stock is None and original_stock not in (None, '') and original_stock.lower() != 'out of stock':
            data_quality_issues.append(f"Invalid stock value: '{original_stock}'")

        category = clean_category(original_category)
        if category is None:
            data_quality_issues.append(f"Missing category: '{original_category}'")

        restock_date = clean_date(original_date)
        if restock_date is None and original_date not in (None, ''):
            data_quality_issues.append(f"Invalid date format: '{original_date}'")

        cleaned_data.append({
            'product_name': row['product_name'].strip() if row['product_name'] else None,
            'our_price': price,
            'category': category,
            'current_stock': stock,
            'restock_threshold': row['restock_threshold'] if row['restock_threshold'] else None,
            'restock_date': restock_date,
            'supplier': row['supplier'].strip() if row['supplier'] else None
        })

    # Integrate external data
    # We will use https://api.sampleapis.com/coffee/hot as an example
    base_url = os.getenv("API_BASE_URL", "https://api.sampleapis.com")
    coffee_endpoint = f"{base_url}/coffee/hot"

    external_data = []
    try:
        response = requests.get(coffee_endpoint, timeout=30)
        if response.status_code == 200:
            external_data = response.json()
        else:
            print(f"Warning: Unable to fetch external data from {coffee_endpoint}. "
                  f"Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching external data: {e}")

    # We'll do a mock average coffee price calculation
    external_coffee_price_sum = 0.0
    external_coffee_count = 0

    for cdata in external_data:
        if 'coffee' in cdata.get('title', '').lower():
            external_coffee_price_sum += 12.99
            external_coffee_count += 1
        else:
            external_coffee_price_sum += 9.99
            external_coffee_count += 1

    if external_coffee_count > 0:
        external_avg_coffee_price = round(external_coffee_price_sum / external_coffee_count, 2)
    else:
        external_avg_coffee_price = None

    # Compare our coffee products' average price
    coffee_items = [item for item in cleaned_data 
                    if (item['category'] and 'coffee' in item['category'].lower()) 
                    or ('coffee' in item['product_name'].lower())]

    our_coffee_prices = [item['our_price'] for item in coffee_items if item['our_price'] is not None]
    if our_coffee_prices:
        our_avg_coffee_price = round(sum(our_coffee_prices) / len(our_coffee_prices), 2)
    else:
        our_avg_coffee_price = 0

    # Write out the report to "report.md"
    try:
        with open("report.md", "w", encoding='utf-8') as rep:
            rep.write("# Data Integration Report\n\n")

            # 1. Data quality issues
            rep.write("## 1. Data Quality Issues Found\n")
            if data_quality_issues:
                for issue in data_quality_issues:
                    rep.write(f"- {issue}\n")
            else:
                rep.write("- No significant data quality issues found.\n")

            # 2. Cleaned data summary
            rep.write("\n## 2. Cleaned Data Summary\n")
            rep.write(f"Total records processed: {len(cleaned_data)}\n\n")
            rep.write("Sample of cleaned data:\n\n")
            sample_count = 5 if len(cleaned_data) > 5 else len(cleaned_data)
            for i in range(sample_count):
                rep.write(f"- {cleaned_data[i]}\n")

            # 3. External data integration results
            rep.write("\n## 3. External Data Integration Results\n")
            rep.write(f"Fetched {len(external_data)} external coffee records from {coffee_endpoint}.\n")
            if external_avg_coffee_price is not None:
                rep.write(f"Calculated mock average coffee price from external data: ${external_avg_coffee_price}\n")
            else:
                rep.write("Could not calculate external average coffee price.\n")

            # 4. Business Insight
            rep.write("\n## 4. Business Insight\n")
            if external_avg_coffee_price is not None:
                rep.write(f"Our average coffee price: ${our_avg_coffee_price}\n")
                if our_avg_coffee_price > external_avg_coffee_price:
                    rep.write(
                        "- **Insight**: Our coffee products are priced higher than the external average. "
                        "Consider a small price reduction to stay competitive.\n"
                    )
                else:
                    rep.write(
                        "- **Insight**: Our coffee products are priced below or around the external average. "
                        "We may have room to increase margins or emphasize our value.\n"
                    )
            else:
                rep.write("- **Insight**: External average coffee price not available. No comparison possible.\n")

            # 5. Future Recommendations
            rep.write("\n## 5. Future Recommendations\n")
            rep.write("- Expand external data sources for tea-specific insights.\n")
            rep.write("- Implement real-time updates for more accurate pricing recommendations.\n")
            rep.write("- Include more robust error handling for missing or malformed data.\n")

        print("Analysis complete. 'report.md' generated successfully.")
    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    main()
