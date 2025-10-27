from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from datetime import datetime
from uuid import uuid4


class QueryMessage(Model):
    question: str


class ResponseMessage(Model):
    answer: str


agent = Agent(name="ChatAgent", seed="chat_seed", port=8000, endpoint=[
              "https://unshattered-filomena-sottedly.ngrok-free.dev/submit"])
fund_agent_if_low(agent.wallet.address())
query_proto = Protocol(name="QueryHandler")
tutor_address = "agent1qt69vgkuuzt6zw5t4xv34jd2pznd405ty2tkfcdesf39uaqcge73kp0qrnv"


@query_proto.on_message(model=QueryMessage, replies=ResponseMessage)
async def handle_query(ctx: Context, sender: str, msg: QueryMessage):
    ctx.logger.info(f"Received query from {sender}: {msg.question}")
    ctx.storage.set("client_endpoint", sender)
    ctx.logger.info(f"Forwarding query to TutorAgent {tutor_address}: {msg}")
    await ctx.send(tutor_address, msg)


@query_proto.on_message(model=ResponseMessage)
async def handle_tutor_response(ctx: Context, sender: str, msg: ResponseMessage):
    ctx.logger.info(f"Received response from TutorAgent: {msg.answer}")
    client_endpoint = ctx.storage.get("client_endpoint")
    if client_endpoint:
        ctx.logger.info(f"Sending response to {client_endpoint}: {msg.answer}")
        await ctx.send(client_endpoint, ResponseMessage(answer=msg.answer))
    else:
        ctx.logger.error("No client endpoint found for response")

agent.include(query_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
