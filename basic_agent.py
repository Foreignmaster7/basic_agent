from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from datetime import datetime
from uuid import uuid4
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Create the agent
agent = Agent(name="ChatAgent", seed="chat_seed")

# Fund the agent (testnet funds)
fund_agent_if_low(agent.wallet.address())

# Initialize the chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# Utility function to create a chat message


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

# Handle incoming chat messages


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    # Send acknowledgement
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))

    # Process message content
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            # Respond with a simple message
            response = create_text_chat(
                f"Hello from {agent.name}! I got: {item.text}")
            await ctx.send(sender, response)
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
        else:
            ctx.logger.info(f"Unexpected content from {sender}")

# Handle acknowledgements


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

# Include the protocol and publish manifest
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
