import os


def load_high_scores():
    if not os.path.exists("assets/high_scores.txt"):
        return []

    with open("assets/high_scores.txt", "r") as file:
        scores = [int(line.strip()) for line in file]
    return sorted(scores, reverse=True)


def save_high_scores(scores):
    with open("assets/high_scores.txt", "w") as file:
        for score in scores:
            file.write(f"{score}\n")


def update_high_scores(new_score):
    scores = load_high_scores()

    if len(scores) < 5 or new_score > min(scores):
        scores.append(new_score)
        scores = sorted(scores, reverse=True)[:5]  # Keep only top 5
        save_high_scores(scores)

    # return scores
