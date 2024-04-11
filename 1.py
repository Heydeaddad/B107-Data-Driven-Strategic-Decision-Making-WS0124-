import pandas as pd

# Ensure openpyxl is installed: pip install openpyxl
# Ensure pyarrow is installed for future compatibility: pip install pyarrow

try:
    # Load the dataset
    file_path = "C:\\Users\\Oleg\\Downloads\\dataset_free-tiktok-scraper_2022-07-27_21-44-20-266.xlsx"
    df = pd.read_excel(file_path)

    # Specify the columns to keep
    columns_to_keep = [
        "authorMeta/digg",
        "authorMeta/fans",
        "authorMeta/following",
        "authorMeta/heart",
        "authorMeta/id",
        "authorMeta/nickName",
        "authorMeta/verified",
        # "authorMeta/video",  # Assuming this was removed due to the previous advice
        "commentCount",
        "createTime",
        "createTimeISO",
        "diggCount",
        "downloaded",
        "hashtags/0/id",
        "hashtags/0/name",
        "hashtags/1/id",
        "hashtags/1/name",
        "id",
        "videoMeta/duration",
        "videoMeta/height",
        "videoMeta/width"
    ]

    # Trim the dataset
    trimmed_df = df[columns_to_keep]

    # Define the full path including the filename and extension for the trimmed dataset
    trimmed_file_path = "C:\\Users\\Oleg\\OneDrive\\Рабочий стол\\Новая папка\\trimmed_dataset.xlsx"

    # Save the trimmed dataset to the new Excel file
    trimmed_df.to_excel(trimmed_file_path, index=False)

    print(f"Trimmed dataset saved to {trimmed_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")