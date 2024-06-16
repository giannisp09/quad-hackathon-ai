import openai
import pandas as pd
import dotenv

dotenv.load_dotenv()

data_dir = "../real_data/"

# Load the CSV file
companies_info = pd.read_csv(data_dir + 'companies_info.csv')

# # OpenAI API key (make sure to set your API key here)
openai.api_key = 'insert-here'

# Function to extract SDGs from business summary
def extract_sdgs(business_summary):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant knowledgeable about Environmental, Social, and Governance (ESG) contributions."},
            {"role": "user", "content": f"Based on the following business summary, identify the company's contributions to Environmental, Social, and Governance (ESG) categories and return a 3-d vector with 1 being the identified category (if any): {business_summary} "}
        ]

    )
    sdgs = response['choices'][0]['message']['content']
    return sdgs

# Create a new DataFrame to store the results
results = []

# Loop through each company in the CSV
for index, row in companies_info.iterrows():
    ticker = row['stock']
    business_summary = row['longBusinessSummary']
    sdgs = extract_sdgs(business_summary)
    results.append({
        'stock': ticker,
        "ESG": sdgs
    })


def parse_sdgs(sdgs_text):
    # Extract the SDG numbers from the text
    sdg_numbers = [int(s) for s in sdgs_text.split() if s.isdigit()]
    
    # Prepare the ESG columns
    esg_columns = [0, 0, 0]
    for i in range(min(len(sdg_numbers), 3)):
        esg_columns[i] = sdg_numbers[i]
    return esg_columns

df_sdgs_extracted = companies_info

# Apply the parsing function to create ESG columns
df_sdgs_extracted[['ESG_1', 'ESG_2', 'ESG_3']] = pd.DataFrame(df_sdgs_extracted['ESG'].apply(parse_sdgs).tolist(), index=df_sdgs_extracted.index)

# Convert results to DataFrame
df_results = pd.DataFrame(results)

# Save the results to a new CSV file
df_results.to_csv('../real_data/companies_sdgs_extracted.csv', index=False)

print("SDGs have been extracted and saved to /mnt/data/companies_sdgs_extracted.csv")
