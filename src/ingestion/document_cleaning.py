import re


def clean_document(content: str) -> str:
    """
    Cleans English and Vietnamese text by removing special characters, converting to lowercase, and normalizing spaces.

    Args:
        content (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Remove special characters, keeping only letters and spaces
    cleaned_text = re.sub(r"[^a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêếìíòóôõùúăđĩũơƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỂỄẾỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪưạảấầẩẫậắằẳẵặẹẻẽềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹÝỲỴỶỸ\ss0-9]", "", content)


    # Convert to lowercase
    cleaned_text = cleaned_text.lower()

    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


if __name__ == "__main__":
    # Example usage
    text_en = "Hello, World! Let's clean it: 100% clean!"
    text_vn = "Xin chào, thế giới! Hãy làm sạch nó: 100% sạch sẽ!"

    print("Original English text:   ", text_en)
    print("Cleaned English text:    ", clean_document(text_en))
    print("Original Vietnamese text:", text_vn)
    print("Cleaned Vietnamese text: ", clean_document(text_vn))
