from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

schema = [
    ResponseSchema(name = 'fact1', description = 'fact1 about topic'),
    ResponseSchema(name = 'fact2', description = 'fact2 about topic'),
    ResponseSchema(name = 'fact3', description = 'fact3 about topic'),
    ResponseSchema(name = 'fact4', description = 'fact4 about topic'),
]

parser = StructuredOutputParser.from_response_schemas(schema)    

template = PromptTemplate(
    template = "give me 4 facts about a {topic} \n {format_instruction}",
    input_variables = ['topic'],
    partial_variables = {'format_instruction' : parser.get_format_instructions()}

)
prompt = template.invoke({'topic':'blackhole'}) 

result = model.invoke(prompt)

final_result = parser.parse(result.content) 
print(final_result)