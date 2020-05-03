from scraper import get_player_stats


def fantasy_recommendations():
    players = get_player_stats()
    player_scores = []
    for player in players:
        p_t = (player.name, player.get_fantasy_score())
        player_scores.append(p_t)
    player_scores.sort(key=lambda x:x[1], reverse=True)
    return player_scores