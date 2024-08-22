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

agent_df = pd.read_sql(
    """
    SELECT CONCAT(township, ", ", province) AS location, code AS agent_id
    FROM agent
    GROUP BY code, township, province;
    """, warehouse_1
)

in_target_df = pd.read_sql(
    """
        SELECT * FROM in_target
    """, warehouse_x
)

in_agent_df = pd.read_sql(
    """
        SELECT * FROM in_agent
    """, warehouse_x
)

agent_with_ts_df = in_agent_df.merge(agent_df, how="left", left_on="Agent ID", right_on="agent_id")
agent_with_ts_df = agent_with_ts_df.merge(township_df, how="left", left_on="location", right_on="To chk")

current_count_df = agent_with_ts_df.groupby("Township_Name_Eng").agg(current_agent_count =("Agent ID", "count")).reset_index()

bind_with_target_count_df = current_count_df.merge(in_target_df, how="inner", left_on="Township_Name_Eng", right_on="Township")

final_df = bind_with_target_count_df[["Township_Name_Eng", "current_agent_count", "Agent"]]
final_df.rename(columns={"Township_Name_Eng": "township", "Agent": "target_agent_count"})
print(final_df.head)

final_df.to_csv("./agent_count_tracking.csv", index=False)