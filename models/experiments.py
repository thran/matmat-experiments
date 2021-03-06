from data.data import Data
from models.model import AvgModel, AvgItemModel
import pylab as plt
import seaborn as sbn
from models.elo import EloModel
from models.eloTree import EloTreeModel
from models.eloTreeDecay import EloTreeDecayModel
from models.eloCurrent import EloPriorCurrentModel
from models.eloTime import EloTimeModel
from skills import load_skills, load_questions, get_question_parents, get_skill_parents, split_multiplication_skills
from utils import elo_grid_search, compare_models, compare_brier_curve, get_skills, elo_pfa_search
import pandas as pd

data = Data("data/matmat-all-2015-09-16.pd", train=0)
qp, sp = get_question_parents(load_questions()), get_skill_parents(load_skills())
split_skills, split_questions = split_multiplication_skills()
qps, sps = get_question_parents(split_questions), get_skill_parents(split_skills)

compare_models(data, [
    # AvgModel(),
    # AvgItemModel(),
    # EloModel(),
    EloModel(alpha=0.8, beta=0),
    # EloTreeModel(qp, sp, alpha=1.2, beta=0.1, KC=3.5, KI=2.5),
    EloTreeModel(qp, sp, alpha=0.6, beta=0.02, KC=3.5, KI=2.5),
    # EloTreeModel(qp, sp, alpha=1.2, beta=0.1, KC=3.5, KI=2.5, level_decay=2.5),
    EloTreeDecayModel(qp, sp, alpha=0.25, beta=0.02),
    # EloTreeDecayModel(qps, sps, alpha=0.25, beta=0.02),
    # EloTreeDecayModel(qp, sp, alpha=0.25, beta=0),
    # EloTreeDecayModel(qp, sp, alpha=1.2, beta=0.1, without_decay=True, KC=3.5, KI=2.5),
    # EloPriorCurrentModel(alpha=0.8, beta=0, KC=1, KI=1),
    EloTimeModel(alpha=0.8, beta=0, time_penalty_slope=0.9),
    # EloTimeModel(alpha=0.8, beta=0, time_penalty_slope=0.95),
    # EloTimeModel(alpha=0.8, beta=0, time_penalty_slope=1),
    EloPriorCurrentModel(alpha=0.8, beta=0, KC=2.5, KI=1),
], dont=0, evaluate=0)

# compare_brier_curve(data, AvgItemModel(), EloModel(alpha=0.8, beta=0))
# compare_brier_curve(data, EloTreeDecayModel(qp, sp, alpha=0.25, beta=0.02), EloModel(alpha=0.8, beta=0))
# compare_brier_curve(data, EloTreeDecayModel(qp, sp, alpha=0.25, beta=0.02), EloTreeDecayModel(qp, sp, alpha=0.25, beta=0))
# compare_brier_curve(data, EloTreeModel(qp, sp, alpha=0.6, beta=0.02, KC=3.5, KI=2.5), EloTreeDecayModel(qp, sp, alpha=0.25, beta=0))
# elo_grid_search(data, beta_range=(0, 0.1, 0.02), model_class=EloModel)
# elo_grid_search(data, beta_range=(0, 0.1, 0.02), model_class=EloPriorCurrentModel)
# elo_grid_search(data, beta_range=(0, 0.2, 0.02), model_class=EloTreeModel)
# elo_grid_search(data, alpha_range=(0.05, 0.4, 0.05), beta_range=(0, 0.1, 0.02), model_class=EloTreeDecayModel)

# elo_pfa_search(data, model_class=EloPriorCurrentModel)
# elo_pfa_search(data, model_class=EloTreeModel)

# pd.Series(get_skills(data, EloModel(alpha=0.8, beta=0)), name="skill").to_pickle("../data/skills-Elo.pd")

plt.show()