import yaml, os, threading
import redis

class CommandCenter:
    def __init__(self):
        # with open('config/config.yml', 'r') as file:
        #     self.command_config = yaml.safe_load(file)
        self.current_intent = None
        self.current_command = None
        self.redis_instance = redis.Redis(
            host='127.0.0.1',
            port=6379,
            decode_responses=True
        )
        listener = self.redis_instance.pubsub()
        listener.subscribe('intent-output')
        for message in listener.listen():
            self.main(str(message))

    def check_intent(self, intent):
        for values in self.command_config['supported_intents']:
            if values.lower() == intent.lower():
                return True
        return False
    
    def main(self, message):
        if "intent" in message:
            is_valid_intent = self.check_intent(message)
            if is_valid_intent:
                self.current_intent = message
        elif "command" in message:
            self.current_command = message
        
        print(message)

    def match_intent_to_command(self, intent):
        pass

    def execute_command(self):
        pass

cc = CommandCenter()