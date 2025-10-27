from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
import re


class QueryMessage(Model):
    question: str


class ResponseMessage(Model):
    answer: str


agent = Agent(name="TutorAgent", seed="tutor_seed", port=8001,
              endpoint=["http://127.0.0.1:8001/submit"])
fund_agent_if_low(agent.wallet.address())
proto = Protocol(name="TutorProtocol")

knowledge_graph = {
    "algebra": "branch of mathematics dealing with symbols and their operations. Start with linear equations: ax + b = c",
    "geometry": "study of shapes and sizes. Key concepts: points, lines, angles, and theorems like Pythagoras.",
    "calculus": "deals with rates of change and accumulation. Includes derivatives and integrals."
}


@proto.on_message(model=QueryMessage, replies=ResponseMessage)
async def handle_query(ctx: Context, sender: str, msg: QueryMessage):
    ctx.logger.info(f"Received query from {sender}: {msg.question}")
    topic = re.sub(r'[^\w\s]', '', msg.question.lower()).split()[-1]
    answer = knowledge_graph.get(
        topic, f"No info on {msg.question}. Try 'algebra' or 'geometry'.")
    response = ResponseMessage(answer=f"TutorAgent says: {answer}")
    ctx.logger.info(f"Sending response to {sender}: {response}")
    await ctx.send(sender, response)

agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
