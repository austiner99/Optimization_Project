import matplotlib.pyplot as plt
from collections import Counter
from string_paragraph import string

# Calculate and print the total word count
total_word_count = len(string.split())
print(f"Total word count: {total_word_count}")

# Count occurrences of each character
string = string.replace("’", "'")
char_counts = Counter(string)

# Filter for specific characters (a-z, ., ,, ', ?)
allowed_chars = "abcdefghijklmnopqrstuvwxyz.,'?"
filtered_counts = {char: char_counts[char] for char in allowed_chars if char in char_counts}

# Sort by frequency (highest to lowest)
sorted_counts = dict(sorted(filtered_counts.items(), key=lambda item: item[1], reverse=True))

# Plot the histogram
plt.figure(figsize=(8, 5))  # Adjust figure size
plt.bar(sorted_counts.keys(), sorted_counts.values(), color='skyblue')
plt.xlabel('Characters')
plt.ylabel('Frequency')
plt.title(f'Character Frequency Histogram from ChatGPT-Generated Text ({total_word_count} Words)')
plt.tight_layout()  # Adjust spacing
plt.savefig('Optimization_Project/pics/character_frequency_histogram.png')
plt.show()
plt.close()

# List of common words to count
common_words = ['the', 'of', 'and', 'to', 'in', 'is', 'for', 'that', 'was']

# Split the string into words and count occurrences of each word
word_counts = Counter(string.lower().split())

# Filter for the common words
filtered_word_counts = {word: word_counts[word] for word in common_words if word in word_counts}

# Sort by frequency (highest to lowest)
sorted_word_counts = dict(sorted(filtered_word_counts.items(), key=lambda item: item[1], reverse=True))

# Plot the histogram for common words
plt.figure(figsize=(8, 5))  # Adjust figure size
plt.bar(sorted_word_counts.keys(), sorted_word_counts.values(), color='lightgreen')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title(f'Common Word Frequency Histogram from ChatGPT-Generated Text ({total_word_count} Words)')
plt.tight_layout()  # Adjust spacing
plt.savefig('Optimization_Project/pics/common_word_frequency_histogram.png')
plt.show()
plt.close()

# List of common bigrams to count
common_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'es', 'on', 'st', 'nt', 'en', 'ed', 'nd', 'or', 'ar', 'ng']

# Count occurrences of each bigram
bigrams = [string[i:i+2] for i in range(len(string) - 1)]
bigram_counts = Counter(bigrams)

# Filter for the common bigrams
filtered_bigram_counts = {bigram: bigram_counts[bigram] for bigram in common_bigrams if bigram in bigram_counts}

# Sort by frequency (highest to lowest)
sorted_bigram_counts = dict(sorted(filtered_bigram_counts.items(), key=lambda item: item[1], reverse=True))

# Plot the histogram for common bigrams
plt.figure(figsize=(8, 5))  # Adjust figure size
plt.bar(sorted_bigram_counts.keys(), sorted_bigram_counts.values(), color='orange')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.title(f'Bigram Frequency Histogram from ChatGPT-Generated Text ({total_word_count} Words)')
plt.tight_layout()  # Adjust spacing
plt.savefig('Optimization_Project/pics/common_bigram_frequency_histogram.png')
plt.show()
plt.close()