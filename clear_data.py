import re
import os


def clear_data(text):
    text = text.replace("WEBVTT", "")
    # remove timestamp
    text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}", "", text)
    # strip blankline
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)


def clean_webvtt_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".vtt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".vtt", ".txt"))

            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            cleaned_text = clear_data(raw_text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Processed: {filename}")


# Example usage
clean_webvtt_directory(
    "/home/nampc/code/personal/tiktok/search_results/", "cleaned_text"
)
