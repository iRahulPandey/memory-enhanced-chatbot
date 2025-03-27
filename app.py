import subprocess
import pandas as pd
import streamlit as st
from cuebit.registry import PromptRegistry
from litellm import completion
import uuid

def get_ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:]]
        return models
    except Exception as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        return ["mixtral", "llama3.1"]  # Fallback models

def main():
    st.set_page_config(page_title="Persona Chatbot with Cuebit", layout="wide")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = str(uuid.uuid4())
    
    st.title("Memory-Enhanced Chatbot with Dynamic Personas 🤖")
    st.caption("Powered by Cuebit Prompt Management")
    
    # Sidebar for settings
    with st.sidebar:
        st.title("Settings")
        
        # New Chat button
        if st.button("New Chat", type="primary"):
            st.session_state.messages = []
            st.session_state.chat_id = str(uuid.uuid4())
            st.rerun()
        
        # Get available Ollama models
        available_models = get_ollama_models()
        selected_model = st.selectbox("Select Model", available_models)
        
        # Allow temperature adjustment
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        
        # Initialize Cuebit and load persona prompts
        registry = PromptRegistry()
        prompts = registry.list_prompts_by_project("memory-chatbot")
        
        # Get persona options
        persona_options = []
        for p in prompts:
            if p.alias and p.alias.startswith("persona-"):
                display_name = p.alias.replace("persona-", "").title()
                persona_options.append((p.alias, display_name))
        
        # If no personas found, provide default options
        if not persona_options:
            st.warning("No persona prompts found in Cuebit. Please set up persona prompts first.")
            persona_options = [
                ("persona-friendly", "Friendly"),
                ("persona-professional", "Professional")
            ]
        
        # Default to friendly if available
        default_index = 0
        for i, (alias, _) in enumerate(persona_options):
            if alias == "persona-friendly":
                default_index = i
                break
        
        # Persona selection dropdown
        selected_persona = st.selectbox(
            "Choose a Persona",
            options=[p[0] for p in persona_options],
            format_func=lambda x: next((p[1] for p in persona_options if p[0] == x), x),
            index=default_index
        )
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("What would you like to discuss?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get the selected persona prompt from Cuebit
        registry = PromptRegistry()
        persona_prompt = registry.get_prompt_by_alias(selected_persona)
        
        if not persona_prompt:
            st.error(f"Persona '{selected_persona}' not found in Cuebit registry.")
            # Create a fallback system prompt
            system_prompt = f"You are a helpful assistant with a {selected_persona.replace('persona-', '')} personality."
        else:
            # Build memory context from chat history
            memory_context = "Previous conversations:\n" + "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" 
                for msg in st.session_state.messages[-5:-1]  # Last few messages, excluding current
            ])
            
            # Generate the system prompt from the template
            try:
                system_prompt = persona_prompt.template.format(
                    memory_context=memory_context,
                    user_message=prompt
                )
            except KeyError as e:
                st.warning(f"Template format error: {str(e)}. Using default prompt.")
                system_prompt = f"You are a helpful assistant with a {selected_persona.replace('persona-', '')} personality. Previous context: {memory_context}"
        
        # Generate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            try:
                # Get user-selected parameters
                response = completion(
                    model=f"ollama/{selected_model}",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    api_base="http://localhost:11434",
                    temperature=temperature,
                    max_tokens=500,
                    stream=True
                )
                
                # Process streaming response
                for chunk in response:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.get('content', '')
                        if content:
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                
                # Final update
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                full_response = "I apologize, but I encountered an error generating the response."
                message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()