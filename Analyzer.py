from Score import Score

class Analyzer:
    def score_authors(authors):
        scores = []
        for author in authors:
            score = Score()
            # Account age (Logarithmic)
            # 5 years = 10/10
            # 1 year = 3/10
            account_age_field = score.set_field('account_age', 10)

            # Activity
            # 200 posts/comments in last year = 10/10
            # 20 posts/comments in last year = 1/10
            activity_field = score.set_field('activity', 9)

            # Empathy
            emapthy_field = score.set_field('empathy', 6.5)

            scores.append(score)

        return scores

    def interpret_scores(scores):
        return []

