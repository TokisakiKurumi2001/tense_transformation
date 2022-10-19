import pandas as pd
class StandardTense:
    def __init__(self):
        df = pd.read_csv('result.csv', index_col='Sentence')
        self.query_tense = df[['Tense']]

    def __call__(self, standard_answer: str) -> str:
        return self.query_tense.at[standard_answer, 'Tense']

if __name__ == "__main__":
    standard_tense = StandardTense()
    sent = "My greatest weakness is lack of confidence."
    print(standard_tense(sent))