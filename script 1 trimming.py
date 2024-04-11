import pandas as pd



try:
   
    file_path = "path to the raw dataset" # loading dataset
    df = pd.read_excel(file_path)

   
    columns_to_keep = [   # trimming
        "authorMeta/digg",
        "authorMeta/fans",
        "authorMeta/following",
        "authorMeta/heart",
        "authorMeta/id",
        "authorMeta/nickName",
        "authorMeta/verified",
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

 
    trimmed_df = df[columns_to_keep]

    
    trimmed_file_path = "path to trimmed datased"

   
    trimmed_df.to_excel(trimmed_file_path, index=False)

    print(f"Trimmed dataset saved to {trimmed_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
