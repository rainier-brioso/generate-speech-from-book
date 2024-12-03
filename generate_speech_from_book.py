import requests
import subprocess
import re
import sys

# Function to convert Roman numerals to integers
def roman_to_int(roman):
    roman_numerals = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8,
        'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
        'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20
    }
    return roman_numerals.get(roman.upper(), None)

# Function to find and extract the chapter content
def get_chapter_content(book_content, chapter_number):
    # Special handling for the first chapter labeled 'Capítulo primero.'
    if chapter_number == 1:
        chapter_pattern = re.compile(r'Capítulo primero\.(.*?)(?=Capítulo\s+[IVXLCDM]|$)', re.S)
    else:
        # Convert chapter_number to Roman numeral
        roman_numeral = next((k for k, v in {
            'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 
            'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13, 
            'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 
            'XIX': 19, 'XX': 20
        }.items() if v == chapter_number), None)

        if not roman_numeral:
            raise ValueError(f"Chapter {chapter_number} not found.")
        
        chapter_pattern = re.compile(
            rf'Capítulo\s+{roman_numeral}\.(.*?)(?=Capítulo\s+[IVXLCDM]|$)', re.S
        )
    
    # Search for the chapter content
    match = chapter_pattern.search(book_content)
    if not match:
        raise ValueError(f"Chapter {chapter_number} not found.")
    
    return match.group(1).strip()

# Function to download the book from the provided URL
def download_book(url):
    response = requests.get(url)
    response.raise_for_status()  # Will raise an exception if there's an error
    return response.text

# Function to call f5-tts_infer-cli and generate speech from text
def generate_speech(text, model="F5-TTS", ref_audio="Recording.m4a"):
    try:
        # Construct the f5-tts_infer-cli command
        command = [
            "f5-tts_infer-cli",
            "--model", model,
            "--ref_audio", ref_audio,
            "--gen_text", text
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print("Speech generation completed.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error generating speech: {e}")
        sys.exit(1)

# Main function
def main(chapter_number):
    # URL of the book (Gutenberg Project, Don Quixote)
    book_url = "https://www.gutenberg.org/files/2000/2000-0.txt"
    
    print("Downloading the book...")
    try:
        # Step 1: Download the book content
        book_content = download_book(book_url)
        
        # Step 2: Extract the chapter content
        print(f"Searching for Chapter {chapter_number}...")
        chapter_content = get_chapter_content(book_content, chapter_number)
        
        # Step 3: Generate speech using the extracted chapter content
        print(f"Generating speech for Chapter {chapter_number}...")
        generate_speech(chapter_content)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Get the chapter number as input from the user
    if len(sys.argv) != 2:
        print("Usage: python script.py <chapter_number>")
        sys.exit(1)

    chapter_number = int(sys.argv[1])
    main(chapter_number)
