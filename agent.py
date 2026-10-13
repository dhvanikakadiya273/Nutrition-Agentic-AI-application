"""
agent.py — IBM Bob / WatsonX Nutrition Agent Core
Registers tools, loads the system prompt, and runs the agentic loop.
"""

import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.prompts import PromptTemplate
from langchain_classic.tools import Tool

from tools.nutrition_lookup import lookup_nutrition
from tools.meal_planner import generate_meal_plan
from tools.calorie_calculator import calculate_calories

load_dotenv()

# ── WatsonX LLM ────────────────────────────────────────────────────────────────
def get_llm() -> WatsonxLLM:
    return WatsonxLLM(
        model_id=os.getenv("WATSONX_MODEL_ID", "ibm/granite-13b-chat-v2"),
        url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        apikey=os.getenv("WATSONX_API_KEY"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 1024,
            "min_new_tokens": 1,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1,
        },
    )


# ── Tool registry ───────────────────────────────────────────────────────────────
TOOLS = [
    Tool(
        name="NutritionLookup",
        func=lookup_nutrition,
        description=(
            "Look up nutritional information for a food item. "
            "Input: food item name (e.g. 'chicken breast 100g'). "
            "Returns calories, protein, carbs, fat, fibre, and key vitamins."
        ),
    ),
    Tool(
        name="MealPlanner",
        func=generate_meal_plan,
        description=(
            "Generate a personalised meal plan. "
            "Input: JSON string with keys 'calories' (int), 'diet_type' (str), 'days' (int). "
            "Example: '{\"calories\": 1800, \"diet_type\": \"vegetarian\", \"days\": 7}'"
        ),
    ),
    Tool(
        name="CalorieCalculator",
        func=calculate_calories,
        description=(
            "Calculate daily caloric needs (BMR / TDEE). "
            "Input: JSON string with keys 'weight_kg', 'height_cm', 'age', 'gender', 'activity_level'. "
            "Activity levels: sedentary | lightly_active | moderately_active | very_active | extra_active"
        ),
    ),
]


# ── System prompt ───────────────────────────────────────────────────────────────
def _load_system_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


# ── Agent factory ────────────────────────────────────────────────────────────────
def build_agent() -> AgentExecutor:
    llm = get_llm()
    system_prompt = _load_system_prompt()

    react_template = system_prompt + """

Tools available:
{tools}

Use the following format:
Question: the input question you must answer
Thought: think step by step about what to do
Action: the tool to use — must be one of [{tool_names}]
Action Input: the input to the tool
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    prompt = PromptTemplate(
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        template=react_template,
    )

    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, handle_parsing_errors=True)


# ── CLI entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    agent_executor = build_agent()
    print("\n🥗 Nutrition AI Agent — type 'quit' to exit\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! Stay healthy 🌿")
            break
        if not user_input:
            continue
        response = agent_executor.invoke({"input": user_input})
        print(f"\nAgent: {response['output']}\n")
