from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_template = PromptTemplate.from_template("单词:{word},反义词：{antonym}")

examples_date = [
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt = example_template,
    examples = examples_date,
    prefix = "告诉我单词的反义词，我提供如下案例",
    suffix = "基于前面的实例告诉我，{input_word}的反义词是什么",
    input_variables = ['input_word']
)

prompt_text = few_shot_template.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)

model = Tongyi(model ="qwen-max")
print(model.invoke(input=prompt_text))