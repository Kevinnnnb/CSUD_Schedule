from bs4 import BeautifulSoup

# Load the HTML content
file_path = '/Users/kevin/Desktop/test.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Define the data labels to extract
data_labels = [
    'data:date',
    'data:periode',
    'data:room',
    'data:matiere',
    'data:enseignant'
]

# Find the relevant <element> tags and extract their contents
elements = soup.find_all('element')

# Dictionary to store the extracted data
extracted_data = {}

for element in elements:
    label = element.find('x_label')
    if label and label.text in data_labels:
        # Store the contents of the <element> tag
        extracted_data[label.text] = str(element)

# Print the extracted data
for label, content in extracted_data.items():
    print(f"Label: {label}")
    print(content)
    print()

# You can also save this data to a file if needed
output_file_path = 'CSUD_Schedule/ISA/extracted_data.html'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for label, content in extracted_data.items():
        output_file.write(f"Label: {label}\n")
        output_file.write(content)
        output_file.write('\n\n')

print(f"Extracted data saved to {output_file_path}")