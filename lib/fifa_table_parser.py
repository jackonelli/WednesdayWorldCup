from xml.etree import ElementTree
from attrdict import AttrDict
from util.io import write_dict_to_json


def data_from_team(team):
    """
    Args:
        team (Element):
    """
    for tag in team:
        if tag.attrib['class'] == 'tbl-teamcode':
            team_code = get_code(tag)

        if tag.attrib['class'] == 'tbl-matches-num':
            games_played = int(get_games_played(tag))

        if tag.attrib['class'] == 'tbl-goalfor':
            goals_scored = int(get_goals_scored(tag))

        if tag.attrib['class'] == 'tbl-goalagainst':
            goals_conceded = int(get_goals_conceded(tag))

    return team_code, {'games_played': games_played,
                       'goals_scored': goals_scored,
                       'goals_conceded': goals_conceded}


def get_code(tag):
    """ Get team FIFA code

    Args:
        tag (element tree tag): With attrib {'class': 'tbl-teamcode'}
    """

    code = None
    div_tag = tag.find('a/div')
    for sub_div in div_tag:
        if sub_div.attrib['class'] == 't-n':
            code = sub_div.find('span').text
    return code


def get_games_played(tag):
    """ Get games played

    Args:
        tag (element tree tag): With attrib {'class': 'tbl-matches-num'}
    """

    return tag.find('span').text


def get_games_played(tag):
    """ Get games played

    Args:
        tag (element tree tag): With attrib {'class': 'tbl-matches-num'}
    """

    return tag.find('span').text


def get_goals_scored(tag):
    """ Get games played

    Args:
        tag (element tree tag): With attrib {'class': 'tbl-matches-num'}
    """

    return tag.find('span').text


def get_goals_conceded(tag):
    """ Get games played

    Args:
        tag (element tree tag): With attrib {'class': 'tbl-matches-num'}
    """

    return tag.find('span').text


def get_totals(stats):

    totals = dict()
    for team in stats.values():
        for key, value in team.items():
            if isinstance(value, int):
                if key in totals.keys():
                    totals[key] += value
                else:
                    totals[key] = value
    return AttrDict(totals)


def print_team(team):

    team_data = data_from_team(team)
    print('Team: {team_code}, Games played: {games_played}, Goals scored: {goals_scored},'
          ' Goals conceded: {goals_conceded}'.format(**team_data))


def get_stats():
    stats_dict = dict()
    for team in table_body:
        team_code, team_data = data_from_team(team)
        stats_dict[team_code] = AttrDict(team_data)
    return stats_dict


def main():
    html_tree = ElementTree.parse('data/fifa.html')
    table_body = html_tree.find('body/table/tbody')
    team_stats = get_stats()


if __name__ == '__main__':
    main()
