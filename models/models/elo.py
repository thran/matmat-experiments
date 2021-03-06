from collections import defaultdict
from model import Model, sigmoid


class EloModel(Model):

    def __init__(self, alpha=1.0, beta=0.1, decay_function=None):
        Model.__init__(self)

        self.alpha = alpha
        self.beta = beta
        self.decay_function = decay_function if decay_function is not None else lambda x: alpha / (1 + beta * x)

        self.global_skill = defaultdict(lambda: 0)
        self.difficulty = defaultdict(lambda: 0)
        self.student_attempts = defaultdict(lambda: 0)
        self.item_attempts = defaultdict(lambda: 0)

    def __str__(self):
        return "Elo; decay - alpha: {}, beta: {}".format(self.alpha, self.beta)

    def predict(self, student, item, extra=None):
        random_factor = 0 if extra is None or extra.get("choices", 0) == 0 else 1. / extra["choices"]
        prediction = sigmoid(self.global_skill[student] - self.difficulty[item], random_factor)
        return prediction

    def update(self, student, item, prediction, correct, extra=None):
        dif = (correct - prediction)

        self.global_skill[student] += self.decay_function(self.student_attempts[student]) * dif
        self.difficulty[item] -= self.decay_function(self.item_attempts[item]) * dif
        self.student_attempts[student] += 1
        self.item_attempts[item] += 1