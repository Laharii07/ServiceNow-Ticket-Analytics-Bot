import pandas as pd
from datetime import datetime

SLA_HOURS = {"High": 4, "Medium": 8, "Low": 24}

def compute_sla_status(df: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now()
    df = df.copy()
    df['created_at']   = pd.to_datetime(df['created_at'])
    df['sla_deadline'] = pd.to_datetime(df['sla_deadline'])
    df['hours_left']   = (df['sla_deadline'] - now).dt.total_seconds() / 3600
    
    def status(h):
        if h < 0:    return 'Breached'
        if h < 2:    return 'At Risk'
        return 'On Track'
    
    df['sla_status'] = df['hours_left'].apply(status)
    return df[df['status'].isin(['Open', 'In Progress'])]

def get_summary(df: pd.DataFrame) -> dict:
    return {
        'total':    len(df),
        'breached': (df['sla_status'] == 'Breached').sum(),
        'at_risk':  (df['sla_status'] == 'At Risk').sum(),
        'on_track': (df['sla_status'] == 'On Track').sum(),
    }
