from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import asyncio


class QueryMessage(Model):
    question: str


class ResponseMessage(Model):
    answer: str


test_agent = Agent(name="TestClient", seed="test_seed",
                   port=8002, endpoint=["http://127.0.0.1:8002/submit"])
fund_agent_if_low(test_agent.wallet.address())
proto = Protocol(name="TestQuery")
chat_address = "agent1qt9yu6nhpkl7zdasza5e2a4p0scjwt76xv39krdznnh0gdwvq4nrk8f9uzv"


async def on_startup(ctx: Context):
    ctx.logger.info("TestClient starting, waiting for registration...")
    await asyncio.sleep(10)
    ctx.logger.info(f"Sending query to ChatAgent {chat_address}")
    query = QueryMessage(question="What is geometry?")
    await ctx.send(chat_address, query)


@proto.on_message(model=ResponseMessage)
async def handle_response(ctx: Context, sender: str, msg: ResponseMessage):
    ctx.logger.info(f"Received response from {sender}: {msg.answer}")

test_agent.on_event("startup")(on_startup)
test_agent.include(proto, publish_manifest=True)

if __name__ == "__main__":
    test_agent.run()
