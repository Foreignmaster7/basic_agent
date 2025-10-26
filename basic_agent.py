from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
from datetime import datetime
from uuid import uuid4

# Define a message model


class TextMessage(Model):
    text: str


# Create an agent
agent = Agent(name="TestAgent", seed="test_seed")

# Fund the agent (testnet funds for Agentverse)
fund_agent_if_low(agent.wallet.address())

# Create a protocol
proto = Protocol(name="SimpleChat")

# Handle incoming messages


@proto.on_message(model=TextMessage)
async def handle_message(ctx: Context, sender: str, msg: TextMessage):
    ctx.logger.info(f"Received message from {sender}: {msg.text}")
    # Send a response
    response = TextMessage(
        text=f"Hello from {agent.name}! I got your message: {msg.text}")
    await ctx.send(sender, response)

# Include the protocol and publish manifest
agent.include(proto, publish_manifest=True)

# Run the agent
if __name__ == "__main__":
    agent.run()
