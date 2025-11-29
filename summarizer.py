from concurrent.futures import ThreadPoolExecutor
from prompts import section_retrieval_prompts, section_summary_prompts

def summarize_section_with_llm(section_name, retriever, llm_model):
    retrieval_prompt = section_retrieval_prompts.get(section_name)
    summary_instruction = section_summary_prompts.get(section_name)

    if not retrieval_prompt or not summary_instruction:
        return f"Prompts for '{section_name}' not found."

    retrieved_docs = retriever.invoke(retrieval_prompt)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    response = llm_model.generate_content(
        f"Context from an Annual Report:\n{context_text}\n\nInstruction: {summary_instruction}."
    )
    return response.text

def summarize_all_sections(multi_query_retriever, llm_model):
    summaries = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(summarize_section_with_llm, section, multi_query_retriever, llm_model): section
            for section in section_retrieval_prompts.keys()
        }
        for future in futures:
            section = futures[future]
            try:
                summaries[section] = future.result()
            except Exception as e:
                summaries[section] = f"Error summarizing {section}: {e}"
    return summaries
