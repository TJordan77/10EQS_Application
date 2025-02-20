# 10EQS's 60 Minute Data Integration Challenge Submission

This project is a tool that helps a small business owner track their product pricing against market conditions.

## Project Overview & Features

1. **CSV Parsing & Cleaning**: Reads `data/products.csv` and cleans data (price, stock, date, category).
2. **External Data Integration**: Fetches coffee-related data from a sample API ([https://api.sampleapis.com/coffee](Coffee API)).
3. **Actionable Insight**: Compares our average coffee price against a mock calculated average from the external data.
4. **Report Generation**: Outputs a `report.md` with data quality findings, summary, and insights.


## Repos Structure

Repo Structure
├── README.md          # How to set up and use the files
├── data/
│   └── products.csv   # Original data file
├── src/
│   ├── analysis.py    # Main script
│   └── utils.py       # Helper functions
├── requirements.txt   # Dependecies
└── report.md          # Generated insights report


## Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/TJordan77/10EQS_Application.git
   ```
2. **Create and activate virtual environment (if you want)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux
   .\venv\Scripts\activate   # On Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Set the `API_BASE_URL` variable if needed. Defaults to `https://api.sampleapis.com` if not set.
   Example:
   ```bash
   API_BASE_URL=https://api.sampleapis.com
   ```
5. **Run the script**
   ```bash
   python src/analysis.py data/products.csv
   ```
6. **View the report**
   - Open the newly created `report.md` file in the repository root.

## Approach

- **Data Cleaning**: I standardized prices, converted out-of-stock strings to numeric 0, and normalized date formats.
- **External Data**: I chose [SampleAPIs](https://sampleapis.com) because it provides open coffee data. The data includes coffee names and attributes, allowing a basic comparison.
- **Insights**: I generated a simple recommendation on whether our coffee prices are higher or lower than an external average.

## Time (Well) Spent

- **Planning & Setup**: 15 minutes 
- **CSV Reading & Cleaning**: 20 minutes
- **External API Integration & Mocked Price Logic**: 15 minutes
- **Reporting & Documentation**: 10 minutes

## Known Issues / Limitations

- Sample API data doesn't include real pricing, so I used a mock approach.
- Some CSV fields were incomplete or malformed in the original ask



