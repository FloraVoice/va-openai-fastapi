from agents.realtime import RealtimeAgent, RealtimeRunner

agent = RealtimeAgent(
    name="FloraVoice Assistant",
    instructions="You are a helpful voice assistant for FloraVoice, a flower shop. Keep responses short and conversational.",
)

_runner_config = {
    "model_settings": {
        "model_name": "gpt-realtime",
        "audio": {
            "input": {
                "format": "pcm16",
                "transcription": {"model": "gpt-4o-mini-transcribe"},
                "turn_detection": {
                    "type": "semantic_vad",
                    "interrupt_response": True,
                },
            },
            "output": {
                "format": "pcm16",
                "voice": "ash",
            },
        },
    }
}


def make_runner() -> RealtimeRunner:
    return RealtimeRunner(starting_agent=agent, config=_runner_config)
