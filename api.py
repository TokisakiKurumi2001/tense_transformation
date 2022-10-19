from pipeline import GeneralTenseTransformation
from TeXid import PostProcess
from standard_tense import StandardTense
import torch

class RecommendTense:
    def __init__(self):
        # predict user tense
        ckpt = "TeXid_model/model_v4"
        self.model = PostProcess(ckpt)
        
        # read csv for input question
        self.standard_tense = StandardTense()

        # tense transformation
        self.general_tense_transformation = GeneralTenseTransformation()

    def __call__(self, standard_answer: str, sent: str) -> str:
        tense = self.model(sent)
        __standard_tense = self.standard_tense(standard_answer)
        if tense == __standard_tense:
            return f'Your tense is matched'
        else:
            return self.general_tense_transformation(sent, tense, __standard_tense)


if __name__ == "__main__":
    recommend_tense = RecommendTense()
    standard_answer = "My greatest weakness is lack of confidence."
    sent = "My weakness was here."
    print(recommend_tense(standard_answer, sent))