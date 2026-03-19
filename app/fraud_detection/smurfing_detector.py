import pandas as pd


def detect_fan_in(df, threshold=10):
    """
    Detect accounts receiving money from many different senders
    """

    counts = df.groupby("receiver_id")["sender_id"].nunique()

    suspicious = counts[counts >= threshold].index

    return set(suspicious)


def detect_fan_out(df, threshold=10):
    """
    Detect accounts sending money to many different receivers
    """

    counts = df.groupby("sender_id")["receiver_id"].nunique()

    suspicious = counts[counts >= threshold].index

    return set(suspicious)