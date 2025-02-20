def calculate_pvs(row):
    """
    Calculate the Player Value Score (PVS) for a given match statistics row.
    """
    # Weight factors
    alpha = 10    # Rating weight
    beta = 1.5    # Offensive contribution weight
    gamma = 1.2   # Defensive contribution weight
    delta = 1     # Possession & Passing weight

    # Offensive contributions
    A = (
        row['goals'] * 6 + row['assists'] * 4 + row['shots'] * 1 +
        row['key_passes'] * 2 + row['dribble_won'] * 1.5
    )

    # Defensive contributions
    B = (
        row['tackles'] * 1.5 + row['interceptions'] * 1.5 +
        row['clearances'] * 1.5 + row['blocks'] * 1.5 + row['aerials_won'] * 1.5
    )

    # Possession & Passing
    C = (
        row['total_passes'] * 0.1 + row['pass_success'] * 1.5 +
        row['pass_cross_accurate'] * 1 + row['pass_long_ball_accurate'] * 1
    )

    # Penalties for negative actions
    penalties = (
        row['yellow_cards'] * 2 + row['red_cards'] * 5 +
        row['dispossessed'] * 0.5 + row['turnovers'] * 0.5 + row['own_goals'] * 6
    )

    # Final PVS calculation
    PVS = (alpha * row['rating']) + (beta * A) + (gamma * B) + (delta * C) - penalties
    return PVS
