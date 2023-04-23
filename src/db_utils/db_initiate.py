from scheme import SystemContext
from system_prompts.prompts import SYSTEM_PROMPTS

if __name__ == '__main__':
    for prompt in SYSTEM_PROMPTS:
        SystemContext(
            context_id=prompt['id'],
            context_alias=prompt['context_alias'],
            context=prompt['context']
        ).save()