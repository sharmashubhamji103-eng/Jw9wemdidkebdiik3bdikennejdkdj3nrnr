import re
import os
import glob
import sys

def rotate_cards_file():
    """Rename existing cards.txt to the next available historyN.txt"""
    if not os.path.exists('cards.txt'):
        return
    # Find all history files and get the highest index
    history_files = glob.glob('history*.txt')
    indices = []
    for f in history_files:
        match = re.search(r'history(\d+)\.txt$', f)
        if match:
            indices.append(int(match.group(1)))
    next_index = max(indices) + 1 if indices else 1
    os.rename('cards.txt', f'history{next_index}.txt')

def extract_cards(text):
    """
    Extract unique card entries from raw text.
    Expected pattern: 15-16 digit card | MM | YY | CVV (3-4 digits)
    Returns sorted list of strings in format: card|MM|YYYY|CVV
    """
    pattern = r'(\d{15,16})\|(\d{2})\|(\d{2})\|(\d{3,4})'
    matches = re.findall(pattern, text)
    cards = set()
    for card, month, year, cvv in matches:
        # Convert 2-digit year to 4-digit (assuming 2000s)
        if len(year) == 2:
            year_full = '20' + year
        else:
            year_full = year
        # Ensure month is two digits
        month = month.zfill(2)
        cards.add(f"{card}|{month}|{year_full}|{cvv}")
    return sorted(cards)  # sort for consistent order

def main(input_file='text.txt'):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    cards = extract_cards(content)
    if not cards:
        print("No valid card data found.")
        return

    rotate_cards_file()
    with open('cards.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(cards))
    print(f"Saved {len(cards)} unique cards to cards.txt")

if __name__ == '__main__':
    # Use first command-line argument as input file, otherwise default to 'text.txt'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'text.txt'
    main(input_file)