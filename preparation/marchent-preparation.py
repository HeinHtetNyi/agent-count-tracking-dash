import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

warehouse_1 = create_engine(os.environ["WAREHOUSE_1"])
warehouse_x = create_engine(os.environ["WAREHOUSE_X"])

township_df = pd.read_sql(
    """
        SELECT *
        FROM LTspFile
    """, warehouse_x
)[["To chk", "Township_Name_Eng"]]

merchant_df = pd.read_sql(
    """
    SELECT CONCAT(township, ", ", province) AS location, code AS merchant_id
    FROM merchant
    GROUP BY code, township, province;
    """, warehouse_1
)

in_target_df = pd.read_sql(
    """
        SELECT * FROM in_target
    """, warehouse_x
)

in_merchant_df = pd.read_sql(
    """
        SELECT * FROM in_merchant
    """, warehouse_x
)

marchent_with_ts_df = in_merchant_df.merge(merchant_df, how="left", left_on="Merchant ID", right_on="merchant_id")
marchent_with_ts_df = marchent_with_ts_df.merge(township_df, how="left", left_on="location", right_on="To chk")

current_count_df = marchent_with_ts_df.groupby("Township_Name_Eng").agg(current_merchant_count =("Merchant ID", "count")).reset_index()

bind_with_target_count_df = current_count_df.merge(in_target_df, how="inner", left_on="Township_Name_Eng", right_on="Township")

final_df = bind_with_target_count_df[["Township_Name_Eng", "current_merchant_count", "Merchant"]]
final_df.rename(columns={"Township_Name_Eng": "township", "Merchant": "target_merchant_count"})
print(final_df.head)

final_df.to_csv("./preparation/merchant_analysis.csv", index=False)