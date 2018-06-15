"""Prediction module"""
from scipy.stats import poisson, gamma
from lib.fifa_table_parser import get_totals
from util.io import read_json_to_attrdict


class PoissonGammaModel(object):
    """Poisson Gamma Model for simulating game scores"""

    def __init__(self, data_path):
        """Init"""
        self.alpha_attack = int()
        self.alpha_defence = int()
        self.beta = int()

        self.stats = read_json_to_attrdict(data_path)
        if self.stats:
            self.totals = get_totals(self.stats)

    def __str__(self):
        string = 'Poisson Gamma model: alpha_attack: {}, beta: {},' \
                 ' alpha_defence: {}'.format(self.alpha_attack,
                                             self.beta,
                                             self.alpha_defence)
        return string

    def set_prior_params(self):
        self.alpha_attack = self.totals.goals_conceded / self.totals.games_played
        self.alpha_defence = self.totals.goals_conceded / self.totals.games_played
        self.beta = 1

    def get_posterior_params(self, team):
        """https://www.quora.com/What-is-an-intuitive-explanation-for-why-Gamma-is-the-conjugate-prior-for-a-Poisson#"""
        team_stats = self.stats.get(team.fifa_code)
        if team_stats:
            alpha_attack = self.alpha_attack + team_stats.get('goals_scored')
            alpha_defence = self.alpha_defence + team_stats.get('goals_conceded')
            beta = self.beta + self.stats[team.fifa_code]['games_played']
        else:
            alpha_attack = self.alpha_attack
            alpha_defence = self.alpha_defence
            beta = self.beta

        return alpha_attack, alpha_defence, beta

    def sample_game_score(self, game):
        home_alpha_att, home_alpha_defence, home_beta = self.get_posterior_params(game.home_team)
        away_alpha_att, away_alpha_defence, away_beta = self.get_posterior_params(game.away_team)

        home_lambda = self.get_lambda_sample(home_alpha_att, home_beta, away_alpha_defence, away_beta)
        away_lambda = self.get_lambda_sample(away_alpha_att, away_beta, home_alpha_defence, home_beta)

        game.home_result = poisson.rvs(home_lambda)
        game.away_result = poisson.rvs(away_lambda)

    @staticmethod
    def get_lambda_sample(alpha_att, beta_att, alpha_def, beta_def):
        lambda_att = gamma.rvs(alpha_att, scale=1 / beta_att)
        lambda_def = gamma.rvs(alpha_def, scale=1 / beta_def)

        return (lambda_att + lambda_def) / 2


def main():
    paul = PoissonGammaModel('../data/team_stats.json')


if __name__ == '__main__':
    main()
