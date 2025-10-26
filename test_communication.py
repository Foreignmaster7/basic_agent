from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


class QueryMessage(Model):
    question: str


class ResponseMessage(Model):
    answer: str


test_agent = Agent(name="TestClient", seed="test_seed",
                   port=8002, endpoint=["http://127.0.0.1:8002/submit"])

fund_agent_if_low(test_agent.wallet.address())


async def on_interval(ctx: Context):
    tutor_address = "agent1qt69vgkuuzt6zw5t4xv34jd2pznd405ty2tkfcdesf39uaqcge73kp0qrnv"
    query = QueryMessage(question="What is algebra?")
    await ctx.send(tutor_address, query)


@test_agent.on_message(model=ResponseMessage)
async def handle_response(ctx: Context, sender: str, msg: ResponseMessage):
    ctx.logger.info(f"Received from {sender}: {msg.answer}")

test_agent.on_interval(period=5.0)(on_interval)
if __name__ == "__main__":
    test_agent.run()
