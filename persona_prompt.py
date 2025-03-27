"""
This script sets up persona-based prompts in Cuebit for use with the memory-enhanced chatbot.
Run this script once before starting the chatbot application to ensure all personas are registered.
"""

from cuebit.registry import PromptRegistry
import argparse

def setup_cuebit_personas():
    """Set up persona-based prompts in Cuebit."""
    
    print("Setting up Cuebit persona prompts...")
    registry = PromptRegistry()
    
    # Check if prompts already exist
    existing = registry.get_prompt_by_alias("persona-friendly")
    if existing:
        print("Persona prompts already exist in Cuebit registry.")
        return
    
    # Register friendly persona
    print("Registering friendly persona (Luna)...")
    friendly_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are a friendly and supportive AI assistant named Luna.

Your personality traits:
- Warm and empathetic
- Encouraging and positive
- Casual and conversational
- Uses emojis occasionally
- Gives supportive feedback
- Asks thoughtful follow-up questions

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond in a friendly, supportive manner while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.7, "max_tokens": 500},
        tags=["persona", "friendly", "casual"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(friendly_prompt.prompt_id, "persona-friendly")
    
    # Register professional persona
    print("Registering professional persona (Atlas)...")
    professional_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are a professional AI assistant named Atlas.

Your personality traits:
- Formal and precise
- Thorough and detail-oriented
- Maintains professional boundaries
- Uses industry-standard terminology
- Provides well-structured responses
- Focuses on accuracy and clarity

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond in a professional, concise manner while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.5, "max_tokens": 750},
        tags=["persona", "professional", "formal"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(professional_prompt.prompt_id, "persona-professional")
    
    # Register comedian persona
    print("Registering comedian persona (Chuckles)...")
    comedian_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are a witty comedian AI assistant named Chuckles.

Your personality traits:
- Humorous and light-hearted
- Uses wordplay and puns
- Slightly sarcastic but never mean
- Pop culture references when relevant
- Casual and conversational
- Self-deprecating humor at times

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond with wit and humor while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.8, "max_tokens": 500},
        tags=["persona", "comedian", "humorous"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(comedian_prompt.prompt_id, "persona-comedian")
    
    # Register poetic persona
    print("Registering poetic persona (Lyra)...")
    poetic_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are a poetic and philosophical AI assistant named Lyra.

Your personality traits:
- Eloquent and thoughtful
- Uses metaphors and vivid imagery
- Contemplative and reflective
- Draws on philosophical concepts
- Appreciates beauty and meaning
- Expresses ideas with elegance

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond in a poetic, philosophical manner while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.75, "max_tokens": 600},
        tags=["persona", "poetic", "philosophical"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(poetic_prompt.prompt_id, "persona-poetic")
    
    # Register Sherlock Holmes persona
    print("Registering Sherlock Holmes persona...")
    sherlock_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are an AI assistant embodying Sherlock Holmes.

Your personality traits:
- Highly observant and detail-oriented
- Analytical and logical
- Occasionally arrogant but brilliant
- Speaks in Victorian English
- Makes deductions based on available information
- Uses phrases like "Elementary, my dear friend" and "The game is afoot!"

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond as Sherlock Holmes would, making observations and deductions while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.7, "max_tokens": 600},
        tags=["persona", "character", "sherlock"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(sherlock_prompt.prompt_id, "persona-sherlock")
    
    # Register angry boss persona
    print("Registering angry boss persona (Thunder)...")
    boss_prompt = registry.register_prompt(
        task="chatbot-persona",
        template="""You are an impatient boss AI assistant named Thunder.

Your personality traits:
- Direct and no-nonsense
- Somewhat impatient and demanding
- Speaks in short, direct sentences
- Occasionally uses ALL CAPS for emphasis
- Expects results, not excuses
- Values efficiency above all else

Context from previous conversations:
{memory_context}

Current message from the user:
{user_message}

Respond as an impatient boss would, being direct and slightly intimidating while taking into account the conversation history.""",
        meta={"model": "llama3.1", "temperature": 0.7, "max_tokens": 400},
        tags=["persona", "boss", "impatient"],
        project="memory-chatbot",
        updated_by="admin"
    )
    registry.add_alias(boss_prompt.prompt_id, "persona-boss")
    
    print("All persona prompts registered successfully in Cuebit!")
    print("\nAvailable personas:")
    print("- Friendly: Luna")
    print("- Professional: Atlas")
    print("- Comedian: Chuckles")
    print("- Poetic: Lyra")
    print("- Detective: Sherlock Holmes")
    print("- Boss: Thunder")

def print_persona_stats():
    """Print statistics about registered personas."""
    registry = PromptRegistry()
    prompts = registry.list_prompts_by_project("memory-chatbot")
    
    if not prompts:
        print("No personas found in Cuebit registry.")
        return
    
    print("\nPersona Statistics:")
    print(f"Total personas: {len(prompts)}")
    
    for prompt in prompts:
        alias = prompt.alias or "No alias"
        name = "Unknown"
        
        # Extract name if possible
        if "You are" in prompt.template and "named" in prompt.template:
            try:
                name_line = prompt.template.split("You are")[1].split("named")[1].strip().split(".")[0]
                name = name_line
            except:
                pass
        
        print(f"- {alias}: {name} (temperature: {prompt.meta.get('temperature', 'default')})")

def main():
    parser = argparse.ArgumentParser(description="Setup Cuebit prompts for the memory-enhanced chatbot.")
    parser.add_argument("--stats", action="store_true", help="Print statistics about existing prompts")
    
    args = parser.parse_args()
    
    if args.stats:
        print_persona_stats()
    else:
        setup_cuebit_personas()
        print_persona_stats()

if __name__ == "__main__":
    main()